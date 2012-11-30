SRCDIR := $(shell pwd)
NAME   := $(shell basename $(SRCDIR))
INCL1  := $(shell php-config --includes)
INCL2  := -I $(shell php-config --include-dir)/sapi/embed
LIBS   := -lphp5 $(shell php-config --libs)

include ../../common/Makefile

tembed: tembed.c
	gcc -Wall $(INCL1) $(INCL2) tembed.c $(LIBS) -o tembed
