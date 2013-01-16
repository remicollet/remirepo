#!/bin/sh

name=Image_Text
list=$(mktemp)

if [ -f $name-$1.tgz ]
then
	tar xif $name-$1.tgz
	tar tf $name-$1.tgz >$list.old

	rm -r $name-$1/tests
	sed -e '/tests/d' -i package.xml

	tar czf $name-$1-strip.tgz package.xml $name-$1
	tar tf $name-$1-strip.tgz | grep -v '/$' >$list.new

	diff $list.old $list.new
	rm -rf $name-$1 package.xml
else
	echo "usage $0 <version>"
fi
rm -f  $list*
