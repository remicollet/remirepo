RPMDEFINES := --define "_sourcedir $(SRCDIR)" \
              --define "_specdir $(SRCDIR)" \
              --define "_srcrpmdir $(SRCDIR)" \
              --define "_rpmdir $(SRCDIR)"

SRCDEFINES := --define "dist .remi" \
              --define "fedora 1" \
              --define "nophptag 1" \
              --define "_source_filedigest_algorithm 1" \
              --define "_binary_filedigest_algorithm 1"

arch:
	mv *.src.rpm /data/rpms/SRPMS.remi/ && echo done || echo Nothing to do

clean:
	@echo Clean $(NAME) in $(SRCDIR)
	@rm -rfv *~ noarch x86_64 *.src.rpm

fedsrpm:
	rpmbuild $(RPMDEFINES) --define "dist .fedora" -bs $(NAME).spec

srpm:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME).spec

devsrpm:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME)-dev.spec

build53:
	time rpmbuild $(RPMDEFINES) --define "phpname php53" --define "runselftest 0" -bb $(NAME).spec

bi53:
	time rpmbuild $(RPMDEFINES) --define "phpname php53" --define "runselftest 0"  -bi --short-circuit  $(NAME).spec

srpm53:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) --define "phpname php53" -bs $(NAME).spec

devsrpm53:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) --define "phpname php53" -bs $(NAME)-dev.spec

build:
	time rpmbuild $(RPMDEFINES) -bb $(NAME).spec

buildtest:
	time rpmbuild $(RPMDEFINES) -bb --with tests $(NAME).spec

bitest:
	rpmbuild $(RPMDEFINES) --with tests -bi --short-circuit $(NAME).spec

buildmini:
	time rpmbuild $(RPMDEFINES) --define "runselftest 0" --without tests -bb $(NAME).spec

bp:
	rpmbuild $(RPMDEFINES) -bp $(NAME).spec

bc:
	rpmbuild $(RPMDEFINES) -bc --short-circuit $(NAME).spec

bi:
	rpmbuild $(RPMDEFINES) --define "runselftest 0" -bi --short-circuit $(NAME).spec

devbp:
	rpmbuild $(RPMDEFINES)  --define "runselftest 0" -bp $(NAME)-dev.spec

devbi:
	rpmbuild $(RPMDEFINES)  --define "runselftest 0" -bi --short-circuit $(NAME)-dev.spec

devbl:
	rpmbuild $(RPMDEFINES) -bl --short-circuit $(NAME)-dev.spec

bl:
	rpmbuild $(RPMDEFINES) -bl --short-circuit $(NAME).spec

devbuild:
	time rpmbuild $(RPMDEFINES) -bb $(NAME)-dev.spec

devbuildmini:
	time rpmbuild $(RPMDEFINES) --define "runselftest 0" --without tests -bb $(NAME)-dev.spec

devbuildtest:
	time rpmbuild $(RPMDEFINES) --with tests -bb $(NAME)-dev.spec

sign:
	rpmsign --addsign *.src.rpm

/tmp/$(NAME)-filtered.spec: $(NAME).spec
	sed -e "s/%{phpname}/php/g;s/%{phpconfdir}/%{_sysconfdir}/g;s/%{phpbindir}/%{_bindir}/g;s/%{phpincldir}/%{_includedir}/g;s/%{_origsysconfdir}/%{_sysconfdir}/g;s/%{_origincludedir}/%{_includedir}/g" $(NAME).spec >/tmp/$(NAME)-filtered.spec

diff: /tmp/$(NAME)-filtered.spec
	colordiff -u  /tmp/$(NAME)-filtered.spec /home/extras/GIT/$(NAME)/$(NAME).spec 2>/dev/null

devdiff: /tmp/$(NAME)-filtered.spec
	colordiff -u  /tmp/$(NAME)-filtered.spec $(NAME)-dev.spec

rpmdiff:
	rpmdiff -i T -i L $(NAME) */$(NAME)*rpm

devsrc:
	spectool -g -S $(NAME)-dev.spec

php7src:
	spectool -g -S $(NAME)-php7.spec

php5build:
	@if test -f $(NAME)-dev.spec ; then \
		time rpmbuild $(RPMDEFINES) --define "scl php56" --without zts -bb $(NAME)-dev.spec ; \
	else \
		time rpmbuild $(RPMDEFINES) --define "scl php56" --without zts -bb $(NAME).spec ; \
	fi

php7build:
	@if test -f $(NAME)-php7.spec ; then \
		time rpmbuild $(RPMDEFINES) -bb $(NAME)-php7.spec ; \
	elif test -f $(NAME)-dev.spec ; then \
		time rpmbuild $(RPMDEFINES) -bb $(NAME)-dev.spec ; \
	else \
		time rpmbuild $(RPMDEFINES) -bb $(NAME).spec ; \
	fi

php71build:
	@if test -f $(NAME)-php7.spec ; then \
		time rpmbuild $(RPMDEFINES) --define "scl php71" --without zts -bb $(NAME)-php7.spec ; \
	elif test -f $(NAME)-dev.spec ; then \
		time rpmbuild $(RPMDEFINES) --define "scl php71" --without zts -bb $(NAME)-dev.spec ; \
	else \
		time rpmbuild $(RPMDEFINES) --define "scl php71" --without zts -bb $(NAME).spec ; \
	fi

php7test:
	@if test -f $(NAME)-php7.spec ; then \
		time rpmbuild $(RPMDEFINES) --define "scl php70" --without zts -bb --with tests $(NAME)-php7.spec ; \
	elif test -f $(NAME)-dev.spec ; then \
		time rpmbuild $(RPMDEFINES) --define "scl php70" --without zts -bb --with tests $(NAME)-dev.spec ; \
	else \
		time rpmbuild $(RPMDEFINES) --define "scl php70" --without zts -bb --with tests $(NAME).spec ; \
	fi

php7srpm:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME)-php7.spec

src:
	spectool -g -S $(NAME).spec

REFLECTION: $(NAME).spec

	php --re $(shell pwd | sed -e 's/.*-//') >REFLECTION

composer: $(NAME).spec
	tar xf $(shell spectool -l $(NAME).spec | head -n 1 | sed -e 's:.* ::' | sed -e 's:.*/::') --strip-components=1 '*/composer.json'

devcomposer:
	if [ -f composeer.json ]; then mv composer.json old.json; fi && \
	tar xf $(shell spectool -l $(NAME)-dev.spec | head -n 1 | sed -e 's:.*/::') --strip-components=1 '*/composer.json' && \
	mv composer.json composer-dev.json && \
	if [ -f old.json ]; then mv old.json composer.json; fi
