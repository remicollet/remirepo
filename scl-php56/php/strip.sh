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

ver=$1
shift

echo "Untar..."
tar xf php-$ver.tar.xz
pushd php-$ver
rm -rf ext/json
if [ -n "$2" ]
then
	for i in $*
	do
		patch -p1 --no-backup <../$i
	done
fi
popd
echo "Tar..."
tar cJf  php-$ver-strip.tar.xz php-$ver

echo "Diff..."
tar tf php-$ver.tar.xz | sort >$old
tar tf php-$ver-strip.tar.xz | sort >$new
diff $old $new

rm -f $old $new
