/*
    +--------------------------------------------------------------------+
    | PECL :: http                                                       |
    +--------------------------------------------------------------------+
    | Redistribution and use in source and binary forms, with or without |
    | modification, are permitted provided that the conditions mentioned |
    | in the accompanying LICENSE file are met.                          |
    +--------------------------------------------------------------------+
    | Copyright (c) 2004-2011, Michael Wallner <mike@php.net>            |
    +--------------------------------------------------------------------+
*/

#ifndef PHP_HTTP_SERF_H
#define PHP_HTTP_SERF_H

#if PHP_HTTP_HAVE_SERF

php_http_request_ops_t *php_http_serf_get_request_ops(void);

PHP_MINIT_FUNCTION(http_serf);
PHP_MSHUTDOWN_FUNCTION(http_serf);

extern zend_class_entry *php_http_serf_class_entry;
extern zend_function_entry php_http_serf_method_entry[];

#define php_http_serf_new php_http_object_new

PHP_METHOD(HttpSERF, __construct);

#endif /* PHP_HTTP_HAVE_SERF */
#endif /* PHP_HTTP_SERF_H */

/*
 * Local variables:
 * tab-width: 4
 * c-basic-offset: 4
 * End:
 * vim600: noet sw=4 ts=4 fdm=marker
 * vim<600: noet sw=4 ts=4
 */

