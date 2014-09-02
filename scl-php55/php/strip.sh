#!/bin/sh

if [ -z "$1" ]; then
	echo "usage $0 version"
	exit 1;
fi
if [ ! -f php-$1.tar.xz ]; then
	echo "missing php-$1.tar.xz archive"
	exit 2;
fi
old=$(mktemp)
new=$(mktemp)

echo "Untar..."
tar xf php-$1.tar.xz
rm -rf php-$1/ext/json
echo "Tar..."
tar cJf  php-$1-strip.tar.xz php-$1

echo "Diff..."
tar tf php-$1.tar.xz | sort >$old
tar tf php-$1-strip.tar.xz | sort >$new
diff $old $new

rm -f $old $new
