#!/bin/sh
export PHP_PEAR_SYSCONF_DIR=@CONFDIR@
exec @BINDIR@/php -C -n -q -d include_path=@PEARDIR@ \
    -d output_buffering=1 @PEARDIR@/peclcmd.php "$@"
