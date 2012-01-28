#include <stdio.h>
#include <gpgme.h>

int main (int argc, char *argv[]) {

	gpgme_ctx_t   ctx;
	gpgme_error_t err;
	const char    *ver;
	gpgme_engine_info_t info;

	ver = gpgme_check_version(NULL);
	printf("gpgme version: %s\n", ver);

	err = gpgme_new(&ctx);
	if (err != GPG_ERR_NO_ERROR) {
		printf("** gpgme_new return %d\n", err);
	}
	
	info = gpgme_ctx_get_engine_info(ctx);
	while(info) {
		printf("protocol:%d, file_name:%s\n", info->protocol, info->file_name);
		info = info->next;
	}

	err = gpgme_ctx_set_engine_info(ctx, GPGME_PROTOCOL_OpenPGP, "/usr/bin/gpg", NULL);
	if (err != GPG_ERR_NO_ERROR) {
		printf("** gpgme_ctx_set_engine_info return %d\n", err);
	}

	info = gpgme_ctx_get_engine_info(ctx);
	while(info) {
		printf("protocol:%d, file_name:%s\n", info->protocol, info->file_name);
		info = info->next;
	}
	return 0;
}
