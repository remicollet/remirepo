RPMDEFINES := --define "_sourcedir $(SRCDIR)" \
              --define "_specdir $(SRCDIR)" \
              --define "_srcrpmdir $(SRCDIR)" \
              --define "_rpmdir $(SRCDIR)"

SRCDEFINES := --define "dist .remi" \
              --define "_source_filedigest_algorithm 1" \
              --define "_binary_filedigest_algorithm 1"

clean:
	echo Clean $(NAME) in $(SRCDIR)
	@rm -fv *~

srpm:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME).spec

devsrpm:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME)-dev.spec

build:
	rpmbuild $(RPMDEFINES) -bb $(NAME).spec

devbuild:
	rpmbuild $(RPMDEFINES) -bb $(NAME)-dev.spec


