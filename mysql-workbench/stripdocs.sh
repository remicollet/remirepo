#!/bin/bash

if [ "$1" = "" ]; then
	echo usage $0  version
	exit 1
fi

if [ ! -f mysql-workbench-gpl-$1-src.tar.gz ]; then
	echo please download mysql-workbench-gpl-$1-src.tar.gz
	echo from http://www.mysql.com/downloads/workbench/
	exit 1
fi

tdir=`mktemp -d tmpXXXXXX`
pushd $tdir

echo -n "unpacking..."
tar xzf ../mysql-workbench-gpl-$1-src.tar.gz && echo " done"
rm -rf mysql-workbench-gpl-$1-src/plugins/wb.doclib/res/DocLibrary
echo -n "packing..."
tar cJf ../mysql-workbench-nodocs-$1.tar.xz mysql-workbench-gpl-$1-src && echo " done"

echo -n "diffing..."
tar tzf ../mysql-workbench-gpl-$1-src.tar.gz | sort >before
echo -n "..."
tar tJf ../mysql-workbench-nodocs-$1.tar.xz  | sort >after

diff before after

popd
echo "cleaning..."
rm -rf $tdir

