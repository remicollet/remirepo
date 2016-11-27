SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
include ../common/Makefile

refl:
	php -n -d extension=zephir_parser.so --re zephir_parser >REFLECTION

