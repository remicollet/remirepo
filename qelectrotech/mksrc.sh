#!/bin/sh

if [ "$1" = "" ]; then
   echo usage $0 REVISION  [ VER ]
   exit 1
fi
REV=$1
VER=${2-0.4}
RPM=$(php -r "printf('%.2f', $VER);")

svn export -r $REV svn://svn.tuxfamily.org/svnroot/qet/qet/trunk qelectrotech-${VER}-svn${REV}

sed -e "/displayedVersion/s/${VER}-dev/${VER}-dev (Revision ${REV})/" \
    -i qelectrotech-${VER}-svn${REV}/sources/qet.h

tar czf qelectrotech-${VER}-svn${REV}.tgz qelectrotech-${VER}-svn${REV}
rm -rf qelectrotech-${VER}-svn${REV}

vendor="Remi Collet <remi@fedoraproject.org>"
rpmdate=$(LC_ALL="C" date +"%a %b %d %Y")

sed -e "s/%changelog/%changelog\n* $rpmdate $vendor - ${RPM}-0.1.svn${REV}\n- Update to ${VER} snapshot revision ${REV}\n/" \
    -e "/global svnrel/s/svnrel.*/svnrel $1/" \
    -i *spec
