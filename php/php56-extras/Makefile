SRCDIR := $(shell pwd)
NAME   := php-extras
INCL1  := $(shell php-config --includes)
INCL2  := -I $(shell php-config --include-dir)/sapi/embed
LIBS   := -lphp5 $(shell php-config --libs)

include ../../common/Makefile

tembed: tembed.c
	gcc -Wall $(INCL1) $(INCL2) tembed.c $(LIBS) -o tembed

debug:
	time rpmbuild $(RPMDEFINES) --with debug -bb $(NAME).spec

srpm:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) --define "scl rh-php56" --define "scl_prefix rh-php56-" -bs $(NAME).spec
