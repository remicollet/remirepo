#include "php.h"
#include "lzf.h"

#define LZF_BLOCKSIZE	(1024 * 64 - 1)

typedef struct {
	char signature[3];
	char usize[2];
} lzf_header_uncompressed;

typedef struct {
	char signature[3];
	char csize[2];
	char usize[2];
} lzf_header_compressed;

typedef struct _php_lzf_compress_filter {
	int persistent;
	char *buffer;
	size_t buffer_pos;
} php_lzf_filter_state;

static void fill_header_compressed(lzf_header_compressed *header, size_t compressed, size_t uncompressed)
{
	/* Copied from liblzf/lzf.c */
	
	header->signature[0] = 'Z';
	header->signature[1] = 'V';
	header->signature[2] = 1;
	header->csize[0] = compressed >> 8;
	header->csize[1] = compressed & 0xff;
	header->usize[0] = uncompressed >> 8;
	header->usize[1] = uncompressed & 0xff;
}

static void fill_header_uncompressed(lzf_header_uncompressed *header, size_t uncompressed)
{
	/* Copied from liblzf/lzf.c */
	
	header->signature[0] = 'Z';
	header->signature[1] = 'V';
	header->signature[2] = 0;
	header->usize[0] = uncompressed >> 8;
	header->usize[1] = uncompressed & 0xff;
}

static int php_lzf_filter_state_ctor(php_lzf_filter_state *inst, int persistent)
{
	inst->persistent = persistent;
	inst->buffer = pemalloc(LZF_BLOCKSIZE, persistent);
	inst->buffer_pos = 0;

	return SUCCESS;
}

static void php_lzf_filter_state_dtor(php_lzf_filter_state *inst TSRMLS_DC)
{
	pefree(inst->buffer, inst->persistent);
}

static int lzf_compress_filter_append_bucket(
	php_stream *stream,
	php_stream_filter_status_t *exit_status,
	php_lzf_filter_state *inst,
	php_stream_bucket_brigade *buckets_out,
	int persistent TSRMLS_DC)
{
	int status;
	size_t buffer_size;
	php_stream_bucket *new_bucket;
	char *output_buffer;

	/* Allocate buffer with a size of data and (larger) header */
	output_buffer = pemalloc(inst->buffer_pos + sizeof(lzf_header_compressed), persistent);

	if (!output_buffer)
		goto fail;
		
	/* Try to compress data. */
	status = lzf_compress(inst->buffer, inst->buffer_pos, output_buffer + sizeof(lzf_header_compressed), inst->buffer_pos);

	/* 
	 * If we were able to compress data, write compressed block. Otherwise 
	 * use uncompressed block.
	 */
	if (status > 0) {
		output_buffer = perealloc(output_buffer, status + sizeof(lzf_header_compressed), persistent);
		fill_header_compressed((lzf_header_compressed *) output_buffer, status, inst->buffer_pos);
		buffer_size = status + sizeof(lzf_header_compressed);
	} else {
		/* Pessimistic case - we still need to memcpy() data */
		output_buffer = perealloc(output_buffer, inst->buffer_pos + sizeof(lzf_header_uncompressed), persistent);
		fill_header_uncompressed((lzf_header_uncompressed *) output_buffer, inst->buffer_pos);
		memcpy(output_buffer + sizeof(lzf_header_uncompressed), inst->buffer, inst->buffer_pos);
		buffer_size = inst->buffer_pos + sizeof(lzf_header_uncompressed);
	}

	/* Create new bucket and append it */
	new_bucket = php_stream_bucket_new(stream, output_buffer, buffer_size, 1, 0 TSRMLS_CC);
	if (!new_bucket)
		goto fail_free_buffer;

	php_stream_bucket_append(buckets_out, new_bucket TSRMLS_CC);

	/* Clear our buffer */
	inst->buffer_pos = 0; 
	
	/* Change exit status */
	*exit_status = PSFS_PASS_ON;
	
	return SUCCESS;

fail_free_buffer:
	pefree(output_buffer, persistent);
fail:
	return FAILURE;
}

static int lzf_compress_append_data(
	php_stream *stream,
	php_stream_filter_status_t *exit_status,
	php_stream_bucket_brigade *buckets_out,
	php_lzf_filter_state *inst,
	const char *input_buffer,
	size_t input_buffer_len,
	size_t *consumed,
	int persistent TSRMLS_DC)
{
	size_t free_buffer;
	size_t bytes_to_copy;
	
	/* As long as there are data in the input buffer... */
	while (input_buffer_len) {
		free_buffer = LZF_BLOCKSIZE - inst->buffer_pos;		/* Free space in buffer */
		bytes_to_copy = MIN(free_buffer, input_buffer_len);	/* Bytes to copy into buffer */

		/* ... copy as many bytes into buffer as possible */
		memcpy(inst->buffer + inst->buffer_pos, input_buffer, bytes_to_copy);
		inst->buffer_pos += bytes_to_copy;
		input_buffer += bytes_to_copy;
		input_buffer_len -= bytes_to_copy;
		(*consumed) += bytes_to_copy;

		/* If the buffer is full, we need to flush it */
		if (inst->buffer_pos == LZF_BLOCKSIZE) {
			if (lzf_compress_filter_append_bucket(stream, exit_status, inst, buckets_out, persistent TSRMLS_CC) != SUCCESS)
				return FAILURE;
		}
	}
	
	return SUCCESS;
}

static php_stream_filter_status_t lzf_compress_filter(
	php_stream *stream,
	php_stream_filter *thisfilter,
	php_stream_bucket_brigade *buckets_in,
	php_stream_bucket_brigade *buckets_out,
	size_t *bytes_consumed,
	int flags TSRMLS_DC)
{
	size_t consumed = 0;
	php_lzf_filter_state *inst = (php_lzf_filter_state *) thisfilter->abstract;
	php_stream_filter_status_t exit_status = PSFS_FEED_ME;
	php_stream_bucket *bucket = NULL;

	while (buckets_in->head) {
		bucket = buckets_in->head;

		php_stream_bucket_unlink(bucket TSRMLS_CC);

		if (lzf_compress_append_data(stream, &exit_status, buckets_out, inst, bucket->buf, bucket->buflen, &consumed, 
				php_stream_is_persistent(stream) TSRMLS_CC) != SUCCESS)
			goto fail_free_bucket;

		php_stream_bucket_delref(bucket TSRMLS_CC);
	}

	if (bytes_consumed)
		*bytes_consumed = consumed;

	if (flags & PSFS_FLAG_FLUSH_CLOSE) {
		if (lzf_compress_filter_append_bucket(stream, &exit_status, inst, buckets_out, php_stream_is_persistent(stream) TSRMLS_CC) != SUCCESS)
			goto fail;
	}

	return exit_status;

fail_free_bucket:
	if (bucket != NULL)
		php_stream_bucket_delref(bucket TSRMLS_CC);
fail:
	return PSFS_ERR_FATAL;
}

static php_stream_filter_status_t lzf_decompress_filter(
	php_stream *stream,
	php_stream_filter *thisfilter,
	php_stream_bucket_brigade *buckets_in,
	php_stream_bucket_brigade *buckets_out,
	size_t *bytes_consumed,
	int flags TSRMLS_DC)
{
	return PSFS_PASS_ON;
}

static void lzf_filter_state_dtor(php_stream_filter *thisfilter TSRMLS_DC)
{
	assert(thisfilter->abstract != NULL);

	php_lzf_filter_state_dtor((php_lzf_filter_state *) thisfilter->abstract TSRMLS_CC);
	pefree(thisfilter->abstract, ((php_lzf_filter_state *) thisfilter->abstract)->persistent);
}

static php_stream_filter_ops lzf_compress_ops = {
	lzf_compress_filter,
	lzf_filter_state_dtor,
	"lzf.compress"
};

static php_stream_filter_ops lzf_decompress_ops = {
	lzf_decompress_filter,
	lzf_filter_state_dtor,
	"lzf.decompress"
};

static php_stream_filter *lzf_compress_filter_create(const char *filtername, zval *filterparams, int persistent TSRMLS_DC)
{
	php_lzf_filter_state *inst;

	inst = pemalloc(sizeof(php_lzf_filter_state), persistent);
	if (inst == NULL)
		return NULL;

	if (php_lzf_filter_state_ctor(inst, persistent) != SUCCESS) {
		pefree(inst, persistent);
		return NULL;
	}

	return php_stream_filter_alloc(&lzf_compress_ops, inst, persistent);
}

static php_stream_filter *lzf_decompress_filter_create(const char *filtername, zval *filterparams, int persistent TSRMLS_DC)
{
	php_lzf_filter_state *inst;

	inst = pemalloc(sizeof(php_lzf_filter_state), persistent);
	if (inst == NULL)
		return NULL;

	if (php_lzf_filter_state_ctor(inst, persistent) != SUCCESS) {
		pefree(inst, persistent);
		return NULL;
	}

	return php_stream_filter_alloc(&lzf_decompress_ops, inst, persistent);
}

php_stream_filter_factory php_lzf_compress_filter_factory = {
	lzf_compress_filter_create
};

php_stream_filter_factory php_lzf_decompress_filter_factory = {
	lzf_decompress_filter_create
};
