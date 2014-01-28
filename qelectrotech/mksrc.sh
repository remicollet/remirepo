#!/bin/sh

if [ "$1" = "" ]; then
   echo usage $0 REVISION  [ VER ]
   exit 1
fi
REV=$1
VER=${2-0.3}

svn export -r $REV svn://svn.tuxfamily.org/svnroot/qet/qet/trunk qelectrotech-${VER}-svn${REV}
tar czf qelectrotech-${VER}-svn${REV}.tgz qelectrotech-${VER}-svn${REV}
rm -rf qelectrotech-${VER}-svn${REV}

vendor="Remi Collet <remi@fedoraproject.org>"
rpmdate=$(LC_ALL="C" date +"%a %b %d %Y")

sed -e "s/%changelog/%changelog\n* $rpmdate $vendor - ${VER}-2.svn${REV}\n- Update to ${VER} snapshot revision ${REV}\n/" \
    -e "/global svnrel/s/svnrel.*/svnrel $1/" \
    -i *spec
