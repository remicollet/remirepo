#!/bin/sh

name=Horde_Text_Filter
list=$(mktemp)

if [ -f $name-$1.tgz ]
then
	tar xif $name-$1.tgz
	tar tf $name-$1.tgz >$list.old

	rm $name-$1/lib/Horde/Text/Filter/JavascriptMinify/JsMin.php
	sed -e '/JsMin.php/d' -i package.xml

	tar czf $name-$1-strip.tgz package.xml $name-$1
	tar tf $name-$1-strip.tgz | grep -v '/$' >$list.new

	diff $list.old $list.new
	rm -rf $name-$1 package.xml
else
	echo "usage $0 <version>"
fi
rm -f  $list*
