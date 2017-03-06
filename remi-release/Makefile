SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
include ../common/Makefile

el5:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME)-el.spec --define 'dist .el5.remi' --define 'rhel 5'

el6:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME)-el.spec --define 'dist .el6.remi' --define 'rhel 6'

el7:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME)-el.spec --define 'dist .el7.remi' --define 'rhel 7'

f26:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME).spec --define 'dist .f26.remi' --define 'fedora 26'

f25:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME).spec --define 'dist .f25.remi' --define 'fedora 25'

f24:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME).spec --define 'dist .f24.remi' --define 'fedora 24'

f23:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME).spec --define 'dist .f23.remi' --define 'fedora 23'

f22:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME).spec --define 'dist .f22.remi' --define 'fedora 22'


