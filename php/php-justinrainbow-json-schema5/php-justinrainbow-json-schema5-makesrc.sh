#!/bin/bash

NAME=$(basename $PWD)
OWNER=$(sed   -n '/^%global gh_owner/{s/.* //;p}'   $NAME.spec)
PROJECT=$(sed -n '/^%global gh_project/{s/.* //;p}' $NAME.spec)
MAJOR=$(sed   -n '/^%global major/{s/.* //;p}'      $NAME.spec)
MINOR=$(sed   -n '/^%global minor/{s/.* //;p}'      $NAME.spec)
VERSION=$MAJOR.$MINOR
COMMIT=$(sed  -n '/^%global gh_commit/{s/.* //;p}'  $NAME.spec)
SHORT=${COMMIT:0:7}

echo -e "\nCreate git snapshot\nName=$NAME, Owner=$OWNER, Project=$PROJECT, Version=$VERSION\n"

echo "Cloning..."
git clone https://github.com/$OWNER/$PROJECT.git $PROJECT-$COMMIT

echo "Getting commit..."
pushd $PROJECT-$COMMIT
git checkout $COMMIT
cp composer.json ../composer.json
popd

echo "Archiving..."
tar czf $NAME-$VERSION-$SHORT.tgz --exclude .git $PROJECT-$COMMIT

echo "Cleaning..."
rm -rf $PROJECT-$COMMIT

echo "Done."
