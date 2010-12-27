#!/bin/sh
exec /usr/bin/php -C -d include_path=/usr/share/pear \
    -d output_buffering=1 /usr/share/pear/pearcmd.php "$@"
