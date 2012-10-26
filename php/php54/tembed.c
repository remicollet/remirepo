#include <stdio.h>
#include <php_embed.h>

int main (int argc, char*argv[]) {
    PHP_EMBED_START_BLOCK(argc, argv)
    zval    ver;
    zend_eval_string("phpversion();", &ver, "Get version" TSRMLS_CC);
    convert_to_string(&ver);
    php_printf("Build PHP Version: %s\n", PHP_VERSION);
    php_printf("Running PHP Version: %s\n", Z_STRVAL(ver));
    zval_dtor(&ver);
    PHP_EMBED_END_BLOCK()
    
    return 0;
}
