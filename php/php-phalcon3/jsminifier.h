/* Fake version to avoid non-free stuff */

#ifndef PHALCON_ASSETS_FILTERS_JSMINIFIER_H
#define PHALCON_ASSETS_FILTERS_JSMINIFIER_H

#include <Zend/zend.h>

int phalcon_jsmin(zval *return_value, zval *script TSRMLS_DC);

#endif /* PHALCON_ASSETS_FILTERS_JSMINIFIER_H */
