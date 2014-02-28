#!/bin/sh

if [ -z "$1" ]; then
	echo "usage $0 version"
	exit 1;
fi

if [ -f php-$1.tar.xz ]; then
	told=php-$1.tar.xz
elif [ -f php-$1.tar.bz2 ]; then
	told=php-$1.tar.bz2
else
	echo "missing php-$1.tar.xz archive"
	exit 2;
fi
tnew=php-$1-strip.tar.xz

old=$(mktemp)
new=$(mktemp)

echo "Untar..."
tar xf $told
rm -rf php-$1/ext/json
echo "Tar..."
tar cJf  $tnew php-$1

echo "Diff..."
tar tf $told | sort >$old
tar tf $tnew | sort >$new
diff $old $new

rm -f $old $new
