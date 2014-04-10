#!/bin/sh
EXT="-d extension=posix.so"
DIR=$(/usr/bin/php -n -r 'echo ini_get("extension_dir");')
if [ -f $DIR/xml.so ] ; then
   EXT="$EXT -d extension=xml.so"
fi
exec /usr/bin/php -C \
    -n $EXT \
    -d include_path=/usr/share/pear \
    -d date.timezone=UTC \
    -d output_buffering=1 \
    -d variables_order=EGPCS \
    -d safe_mode=0 \
    -d register_argc_argv="On" \
    -d open_basedir="" \
    -d auto_prepend_file="" \
    -d auto_append_file=""  \
    /usr/share/pear/pearcmd.php "$@"
