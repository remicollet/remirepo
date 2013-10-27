#!/bin/sh
OOO_ARCH=$(uname -m)
case $OOO_ARCH in
	x86_64 | s390x | ppc64 | sparc64 | aarch64)
		bits=64
		;;
	* )
		bits=32
		;;
esac
exec icu-config-$bits "$@"
