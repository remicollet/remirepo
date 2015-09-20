#!/bin/bash

NAME=php-PHPParser
OWNER=nikic
PROJECT=PHP-Parser
VERSION=$(sed -n '/^%global github_version/{s/.* //;p}' $NAME.spec)
COMMIT=$(sed -n '/^%global github_commit/{s/.* //;p}' $NAME.spec)
SHORT=${COMMIT:0:7}

echo "Cloning..."
git clone https://github.com/nikic/PHP-Parser.git $PROJECT-$SHORT

echo "Gettin commit..."
pushd $PROJECT-$SHORT
cp composer.json ../composer-$VERSION.json
git checkout $COMMIT
popd

echo "Archiving..."
tar czf $NAME-$VERSION-$SHORT.tgz --exclude .git $PROJECT-$SHORT

echo "Cleaning..."
rm -rf $PROJECT-$SHORT

echo "Done."
