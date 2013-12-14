#!/bin/sh

if [ "$1" = "" ]
then
	echo usage $0 version
	exit 1
fi

tmp=$(mktemp --dir)
pushd $tmp

echo -e "\n+ channel"
pear channel-discover pear.symfony.com

echo -e "\n+ packages"
pear list-all -c symfony2 | while read name version descr
do
	if [ "$name" = "ALL" -o "$name" = "PACKAGE" -o "$version" = "" ]
	then
		continue
	fi
	pear download $name-$1
	tar xf $(basename $name)-$1.tgz --strip-components=1
done
lst=$(find Symfony -name autoloader.php)

popd
echo -e "\n+ archive: autoloader-$1.tgz"
tar cvzf autoloader-$1.tgz -C $tmp $lst

echo -e "\n+ cleanups"
rm -rf $tmp
