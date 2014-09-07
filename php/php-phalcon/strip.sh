#!/bin/sh

if [ $# -lt 2 ]; then
	echo usage $0 version commit
	exit 1
fi

owner=phalcon
project=cphalcon
version=$1
commit=$2
upstream=$project-$version.tar.gz
downstream=$project-$version-strip.tar.bz2
list1=$(mktemp)
list2=$(mktemp)

if [ ! -f $upstream ]; then
	wget https://github.com/$owner/$project/archive/$commit/$upstream
fi
if [ ! -f $upstream ]; then
	echo missgin upstream archive
else
	echo Unpacking...
	tar tf $upstream >$list1
	tar xf $upstream
	echo Cleaning non-free stuff...
	rm $project-$commit/ext/assets/filters/jsminifier.? \
	   $project-$commit/ext/assets/filters/cssminifier.? \
	   $project-$commit/build/*/phalcon.?
	echo Packing...
	tar cjf $downstream $project-$commit
	tar tf  $downstream >$list2
	echo "Diffing..."
	diff $list1 $list2
fi

rm -f $list1 $list2