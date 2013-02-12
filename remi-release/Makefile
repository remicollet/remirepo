SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
include ../common/Makefile

el5:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME)-el5.spec --define 'dist .el5.remi' --define 'rhel 5'

el6:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME)-el5.spec --define 'dist .el6.remi' --define 'rhel 6'

