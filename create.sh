#!/bin/sh

if [ -z "$1" ]; then
	echo "Usage  $0  remote_path "
	exit 1
fi

GIT=${1%/}
LOC=$(basename $GIT)

if [ -d $LOC ]; then
	echo "** $LOC already exists"
	exit 1
fi

ssh git@git.remirepo.net mkdir -p site/rpms/${GIT}.git \; cd site/rpms/${GIT}.git \; git init --bare
ssh git@git.remirepo.net ./mkrepos.sh 

git clone git@git.remirepo.net:site/rpms/${GIT}.git

