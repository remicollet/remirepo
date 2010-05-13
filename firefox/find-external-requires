#!/bin/sh

# Finds requirements provided outside of the current file set

filelist=`sed "s/[]['\"*?{}]/\\\\\&/g"`

provides=`echo $filelist | /usr/lib/rpm/find-provides`

{
for f in $filelist ; do
	echo $f | /usr/lib/rpm/find-requires | while read req ; do
		found=0
		for p in $provides ; do
			if [ "$req" = "$p" ]; then
				found=1
			fi
		done
		if [ "$found" = "0" ]; then
			echo $req
		fi
	done
done
} | sort -u