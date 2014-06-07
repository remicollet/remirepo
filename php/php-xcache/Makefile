SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
include ../../common/Makefile

refl:
	php --re "XCache"             > REFLECTION
	php --re "XCache Cacher"     >> REFLECTION
	php --re "XCache Coverager"  >> REFLECTION
	php --re "XCache Optimizer"  >> REFLECTION
