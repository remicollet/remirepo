#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <string.h>
#include <unistd.h>
#include <gpgme.h>

char *fingerprint = "64DF06E42FCF2094590CDEEE2E96F141B3DD2B2E";
char *passphrase = "blabla";
char *clear = "foo bar";
char *testkey =
"-----BEGIN PGP PRIVATE KEY BLOCK-----\n"
"Version: GnuPG v1.4.3 (GNU/Linux)\n\n"

"lQHhBENQAKwRBADpy828KU+0SuoetJTrJ5dR86PiO3CsH8K6QRP7wY82Eh/9NTJ3\n"
"afRj0FNPaVSP0NciPeM4G4uFoQ3lsIf+FBEPXH1D97/XigWObU8K6ha2/s8wU98z\n"
"/samjTHLR+VKZ031B5/8p5Y49yvkkEyBkF1G85yeIXK0WZorKBPncRKuUwCgxOi/\n"
"IEa+ZuqHlmlDF2LTRIBOfrkEAK+WLRMWUD0bqj1TYwnxwPWiuns32/ZXLWuPfb5o\n"
"crNt7x5LSe7wJhjyIiFhiU0qR33X/FrT2umzOxlRYfINXT9DUHDocxxbED6fxAHw\n"
"X2IDd5tWXgCkSBHn2yAneNY6ycPdS3RvqJGlYFg7cOc0kz4urjqRt9fIagzpZQtL\n"
"fXHfBACl3EWgvLhVBo5ExZbrtlOA2q0x9UGhhNaSkeBWBr2qDeZErQjMTO0+viaN\n"
"/SX0zxeWtM3z06rkUHd1DKORDRM5R7shBTv9/Quojn0gbYbOem+e1mlCe27TRxcP\n"
"yeIKk00PqbVuff9QlK9GqKEWGzsEXCmxZ160Dul3CGlf/vQZHf4DAwJAwtVOoL7t\n"
"cGBlDCPs4m+HNqT+hD5LGtrx8IC/dnPGNrjFsVybcptYgdn4i6nkSnu+g6a7rcjN\n"
"qTUyYrQkdGVzdGtleSAodGVzdGtleSkgPHRlc3RAZXhhbXBsZS5uZXQ+iF4EExEC\n"
"AB4FAkNQAKwCGwMGCwkIBwMCAxUCAwMWAgECHgECF4AACgkQLpbxQbPdKy58pwCc\n"
"Dz9qEBEVt1gcKCwNay0fm4vLqCkAn1P0KV1giECUVXBuZ5YUndDB1QqtnQFXBENQ\n"
"AK0QBACNXzJQG4NHUJqLPImezbl+ii+93MjMo8LpSlv9Np5ruWIKtxuqmVEe4k+r\n"
"1DDmSl8hppifpRtx2hefbDTl8Tdf5MNGvf5JE3AHYUehZ+ldjgYCOZ53fJDgKV65\n"
"ZidQSGGXsRcyE7SHgMQ6rTL92PA2IQmkcf9xkg6xM2h55UusMwADBQP9EGQ0BAdW\n"
"RUtA21/cR6F+t97KZnVSet225UYv8azv8p8cK4R1lrZXChFadK9Kt+/My4HAx7J7\n"
"zd1IPuKQ0QniuvuLT3Mwz19B7FGXaJenwTw0P1ihtmSPq9GAOkOA4ZPhHLl9OFwI\n"
"eAZzjfshRfvm0haO3vwlxdjhwxyJ/a/JEF3+AwMCQMLVTqC+7XBgepY5Qw0vGNYN\n"
"K5jkMtn1Pjj/tzYKJIvneoEXb9lEzV4fpju1q8p+FmKHokwjq6FrEF2edKtuYygj\n"
"qNKIrYhJBBgRAgAJBQJDUACtAhsMAAoJEC6W8UGz3SsusGQAn21Jynp2uGE9AnDU\n"
"BjoYSlJsrQm0AJ4m57ArwLXA7WXk5iQbMWlvhWCq4g==\n"
"=awlp\n"
"-----END PGP PRIVATE KEY BLOCK-----\n";

gpgme_error_t passphrase_decrypt_cb (
		void * pass,
		const char *uid_hint, const char *passphrase_info,
		int last_was_bad, int fd) {
	if (last_was_bad) {
		printf("Incorrent passphrase\n");
		return 1;
	}
	if (write(fd, passphrase, strlen(passphrase)) == strlen(passphrase) && write(fd, "\n", 1) == 1) {
		printf("Passphrase sent\n");
		return 0;
	}
	printf("write failed\n");
	return 1;
}

int main (int argc, char *argv[]) {

	gpgme_ctx_t   ctx;
	gpgme_error_t err;
	const char    *ver;
	gpgme_engine_info_t info;
	const char    *dir;
	char          buf[1024];
	gpgme_data_t  in, out;
	gpgme_key_t   keys[2] = {NULL, NULL};
	char         *crypted = NULL, *decrypted = NULL;
	size_t        ret_size;
	gpgme_import_result_t  impresult;
	gpgme_encrypt_result_t encresult;
	gpgme_decrypt_result_t decresult;

	printf("Starting\n");
	// TMP directory
	dir = tmpnam(NULL);
	sprintf(buf, "GNUPGHOME=%s", dir);
	printf("Using %s directory (%d,%d)\n", dir, mkdir(dir, 0755), putenv(buf));

	printf("Checking version\n");
	if (gpgme_engine_check_version(GPGME_PROTOCOL_OpenPGP) != GPG_ERR_NO_ERROR) {
		printf("gpgme_engine_check_version fails\n");
		exit(1);
	}

	ver = gpgme_check_version(NULL);
	printf("gpgme version: %s\n", ver);

	err = gpgme_new(&ctx);
	if (err != GPG_ERR_NO_ERROR) {
		printf("** gpgme_new return %d\n", err);
	}
	
/*
	info = gpgme_ctx_get_engine_info(ctx);
	while(info) {
		printf("protocol:%d, file_name:%s\n", info->protocol, info->file_name);
		info = info->next;
	}
*/
	err = gpgme_ctx_set_engine_info(ctx, GPGME_PROTOCOL_OpenPGP,
		(argc>1 ? argv[1] : "/usr/bin/gpg"),
		NULL);
	if (err != GPG_ERR_NO_ERROR) {
		printf("** gpgme_ctx_set_engine_info return %d\n", err);
	}

	info = gpgme_ctx_get_engine_info(ctx);
	while(info) {
		printf("protocol:%d, file_name:%s version:%s, req_version:%s, home_dir:%s\n",
			info->protocol, info->file_name,
			info->version, info->req_version, info->home_dir);
		info = info->next;
	}
	if (gpgme_data_new_from_mem(&in, testkey, strlen(testkey), 0) != GPG_ERR_NO_ERROR) {
		printf("Can't load the key\n");
		exit(1);
	}
	printf("Test key loaded\n");

	if (gpgme_op_import(ctx ,in) != GPG_ERR_NO_ERROR) {
		gpgme_data_release(in);
		printf("Can't import the key\n");
		exit(1);
	}
	printf("Test key imported\n");

	gpgme_data_release(in);
	impresult = gpgme_op_import_result(ctx);
	if (!impresult || !impresult->imports || impresult->imports->result != GPG_ERR_NO_ERROR) {
		printf("Can't get the result\n");
		exit(1);
	}
	printf("\timported: %d\n", impresult->imported);
	printf("\tunchanged: %d\n", impresult->unchanged);
	printf("\tnewuserids: %d\n", impresult->new_user_ids);
	printf("\tnewsubkeys: %d\n", impresult->new_sub_keys);
	printf("\tsecretimported: %d\n", impresult->secret_imported);
	printf("\tsecretunchanged: %d\n", impresult->secret_unchanged);
	printf("\tnewsignatures: %d\n", impresult->new_signatures);
	printf("\tskippedkeys: %d\n", impresult->skipped_new_keys);
	printf("\tfingerprint: %s\n", impresult->imports->fpr);

	if (gpgme_get_key(ctx, fingerprint, keys, 0) != GPG_ERR_NO_ERROR) {
		printf("Can't get the key\n");
		exit(1);
	}
	printf("Key found\n");

	if (gpgme_data_new_from_mem(&in, clear, strlen(clear), 0)!= GPG_ERR_NO_ERROR) {
		printf("could no create in-data buffer\n");
		exit(1);
	}
	if (gpgme_data_new(&out) != GPG_ERR_NO_ERROR) {
		printf("could not create out-data buffer\n");
		gpgme_data_release(in);
		exit(1);
	}
	if (gpgme_op_encrypt(ctx, keys, GPGME_ENCRYPT_ALWAYS_TRUST, in, out) != GPG_ERR_NO_ERROR) {
		printf("encrypt failed\n");
		gpgme_data_release(in);
		gpgme_data_release(out);
		exit(1);
	}
	encresult = gpgme_op_encrypt_result(ctx);
	if (encresult->invalid_recipients) {
		printf("Invalid recipient encountered\n");
		gpgme_data_release(in);
		gpgme_data_release(out);
		exit(1);
	}
	crypted = gpgme_data_release_and_get_mem(out, &ret_size);
	gpgme_data_release(in);
	printf("Encrypt('%s') = %d chars\n", clear, ret_size);

	gpgme_set_passphrase_cb(ctx, passphrase_decrypt_cb, passphrase);

	if (gpgme_data_new_from_mem(&in, crypted, ret_size, 0) != GPG_ERR_NO_ERROR) {
		printf("could not create in-data buffer\n");
	}
	if (gpgme_data_new(&out) != GPG_ERR_NO_ERROR) {
		printf("could not create out-data buffer\n");
		gpgme_data_release(in);
		exit(1);
	}
	if (gpgme_op_decrypt(ctx, in, out) != GPG_ERR_NO_ERROR) {
		printf("decrypt failed\n");
		gpgme_data_release(in);
		gpgme_data_release(out);
		exit(1);
	}
	decresult = gpgme_op_decrypt_result(ctx);
	if (decresult->unsupported_algorithm) {
		printf("unsupported algorithm\n");
		gpgme_data_release(in);
		gpgme_data_release(out);
		exit(1);
	}
	decrypted = gpgme_data_release_and_get_mem(out, &ret_size);
	gpgme_data_release(in);
	printf("Decrypt() = '%s'\n", decrypted);
	free(crypted);
	free(decrypted);

	return 0;
}
