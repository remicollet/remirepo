#!/bin/sh

if [ -z "$2" ]; then
	echo "usage  $0  local_path  remote_path"
	exit 1
fi

[ -d $1 ] || exit 1

git status $1

echo -n "OK ?: "; read rien

pushd /tmp

rm -rf remirepo/
git clone /home/rpmbuild/SPECS/remirepo
cd remirepo/
git filter-branch --prune-empty --subdirectory-filter $1
ls -l

echo -n "OK ?: "; read rien

ssh git@git.remirepo.net mkdir -p site/rpms/${2%/}.git \; cd site/rpms/${2%/}.git \; git init --bare
ssh git@git.remirepo.net ./mkrepos.sh 
git remote set-url origin git@git.remirepo.net:site/rpms/${2%/}.git
git remote -v

echo -n "OK ?: "; read rien

git push
popd

echo "--- cleanup"
git rm -rf $1
rm -rf $1
echo $1 >>.gitignore
git commit -m "$1 moved to git.remirepo.net" $1

echo "--- clone"
cd $(dirname $1)
git clone git@git.remirepo.net:site/rpms/${2%/}.git

