SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
include ../../../common/Makefile

diff:
	colordiff --ignore-blank-lines -I 'Group:' -I 'defattr'  -u /work/fedora/php-symfony/*spec *spec