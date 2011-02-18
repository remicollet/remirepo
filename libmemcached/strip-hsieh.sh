#!/bin/bash -ex

ver=$1

tdir=`mktemp -d tmpXXXXXX`
pushd $tdir

tar -xzf ../libmemcached-$ver.tar.gz

pushd libmemcached-$ver
 rm libhashkit/hsieh.c
 grep -r 'azillionmonkeys' . && exit 1
popd

rm -f ../libmemcached-$ver-exhsieh.tar.gz
tar --no-xattrs -czf ../libmemcached-$ver-exhsieh.tar.gz libmemcached-$ver

tar -tzf ../libmemcached-$ver.tar.gz | sort > manifest-before
tar -tzf ../libmemcached-$ver-exhsieh.tar.gz | sort > manifest-after

diff -u manifest-before manifest-after || true

popd
rm -rf $tdir
