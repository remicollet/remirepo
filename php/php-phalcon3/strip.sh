#!/bin/sh

NAME=$(sed    -n '/^Name:/{s/.* //;s/%{.*}//;p}'    *.spec)
OWNER=$(sed   -n '/^%global gh_owner/{s/.* //;p}'   $NAME.spec)
PROJECT=$(sed -n '/^%global gh_project/{s/.* //;p}' $NAME.spec)
VERSION=$(sed -n '/^Version:/{s/.* //;p}'           $NAME.spec)
COMMIT=$(sed  -n '/^%global gh_commit/{s/.* //;p}'  $NAME.spec)
SHORT=${COMMIT:0:7}

upstream=$PROJECT-$VERSION.tar.gz
downstream=$PROJECT-$VERSION-strip.tar.xz
list1=$(mktemp)
list2=$(mktemp)

echo -e "\nCreate git snapshot\nName=$NAME, Owner=$OWNER, Project=$PROJECT, Version=$VERSION, Short=$SHORT\n"

if [ ! -f $upstream ]; then
	wget https://github.com/$OWNER/$PROJECT/archive/$COMMIT/$upstream
fi
if [ ! -f $upstream ]; then
	echo missgin upstream archive
else
	echo Unpacking...
	tar tf $upstream >$list1
	tar xf $upstream
	echo Cleaning non-free stuff...
	rm $PROJECT-$COMMIT/ext/phalcon/assets/filters/jsminifier.? \
	   $PROJECT-$COMMIT/ext/phalcon/assets/filters/cssminifier.? \
	   $PROJECT-$COMMIT/build/php?/*/phalcon.zep.?
	echo Packing...
	tar cJf $downstream $PROJECT-$COMMIT
	tar tf  $downstream >$list2
	echo "Diffing..."
	diff $list1 $list2
fi

rm -f $list1 $list2
