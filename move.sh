#!/bin/sh

if [ -z "$1" ]; then
	echo "Usage  $0  local_path  [ remote_path ]"
	exit 1
else
	LOC=${1%/}
fi
if [ -z "$2" ]; then
	GIT=$LOC
else
	GIT=${2%/}
fi


if [ ! -d $LOC ]; then
	echo "** $LOC not found"
	exit 1
fi
if [ -d $LOC/.git ]; then
	echo "** $LOC already moved"
	exit 1
fi

git status $LOC

echo -n "OK ?: "; read rien

pushd /tmp

rm -rf remirepo/
git clone /home/rpmbuild/SPECS/remirepo
cd remirepo/
git filter-branch --prune-empty --subdirectory-filter $LOC
ls -l

echo -n "OK ?: "; read rien

ssh git@git.remirepo.net mkdir -p site/rpms/${GIT}.git \; cd site/rpms/${GIT}.git \; git init --bare
ssh git@git.remirepo.net ./mkrepos.sh 
git remote set-url origin git@git.remirepo.net:site/rpms/${GIT}.git
git remote -v

echo -n "OK ?: "; read rien

git push
popd

echo "--- cleanup"
git rm -rf $LOC
rm -rf $LOC
echo $LOC >>.gitignore
git commit -m "$LOC moved to git.remirepo.net" $LOC

echo "--- clone"
cd $(dirname $LOC)
git clone git@git.remirepo.net:site/rpms/${GIT}.git

