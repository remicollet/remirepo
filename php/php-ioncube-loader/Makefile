SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
include ../../common/Makefile

refl:
	php -n -d zend_extension=ioncube_loader.so --re "ionCube loader"  > REFLECTION
