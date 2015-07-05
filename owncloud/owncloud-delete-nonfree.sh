#!/bin/bash -e

SUFFIX=".tar.bz2"
ORIG_SOURCE=$1
REPACK_SOURCE="$(basename $ORIG_SOURCE $SUFFIX)-repack${SUFFIX}"

[ -d owncloud ] && rm -rf owncloud

tar -xf $1

# delete jslint
pushd owncloud/apps/files_texteditor/js/vendor/ace/src-noconflict/
sed -i '/^ \* JSHint, by JSHint Community\.$/,/^})()$/d' worker-javascript.js
popd

# delete minify entirely as it's a mess that contains at least one instance
# of JSMin, which is under the same problematic license as jslint
rm -rf owncloud/3rdparty/mrclay/minify

tar -cjf $REPACK_SOURCE owncloud
rm -rf owncloud
