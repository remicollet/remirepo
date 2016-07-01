#!/bin/bash

NAME=$(basename $PWD)
if [ "$1" = "dev" ]; then
SPEC=$NAME-dev.spec
COMP=composer-dev.json
else
SPEC=$NAME.spec
COMP=composer.json
fi
OWNER=$(sed   -n '/^%global gh_owner/{s/.* //;p}'   $SPEC)
PROJECT=$(sed -n '/^%global gh_project/{s/.* //;p}' $SPEC)
VERSION=$(sed -n '/^Version:/{s/.* //;p}'           $SPEC)
COMMIT=$(sed  -n '/^%global gh_commit/{s/.* //;p}'  $SPEC)
SHORT=${COMMIT:0:7}

echo -e "\nCreate git snapshot\nName=$NAME, Owner=$OWNER, Project=$PROJECT, Version=$VERSION\n"

echo "Cloning..."
rm -rf $PROJECT-$COMMIT
git clone https://github.com/$OWNER/$PROJECT.git $PROJECT-$COMMIT

echo "Getting commit..."
pushd $PROJECT-$COMMIT
git checkout $COMMIT
cp composer.json ../$COMP
popd

echo "Archiving..."
tar czf $NAME-$VERSION-$SHORT.tgz --exclude .git $PROJECT-$COMMIT

echo "Cleaning..."
rm -rf $PROJECT-$COMMIT

echo "Done."
