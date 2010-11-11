SRCDIR := $(shell pwd)
NAME := oracle-instantclient-11.2

RPMDEFINES := --define "_sourcedir $(SRCDIR)" \
              --define "_specdir $(SRCDIR)" \
              --define "_srcrpmdir $(SRCDIR)" \
              --define "_rpmdir $(SRCDIR)"

SRCDEFINES := --define "dist .remi" \
              --define "_source_filedigest_algorithm 1" \
              --define "_binary_filedigest_algorithm 1"


arch:
	mv *.src.rpm /data/rpms/SRPMS.remi/ && echo done || echo Nothing to do

clean:
	@echo Clean $(NAME) in $(SRCDIR)
	@rm -rfv *~ noarch x86_64 *.src.rpm

srpm64:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME)-x86_64.spec

build64:
	rpmbuild $(RPMDEFINES) -bb $(NAME)-x86_64.spec

srpm32:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME)-i386.spec

build32:
	rpmbuild $(RPMDEFINES) -bb $(NAME)-i386.spec

bp:
	rpmbuild $(RPMDEFINES) -bp $(NAME).spec

