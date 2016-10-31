# remirepo/fedora spec file for php-bartlett-PHP-Reflect
#
# Copyright (c) 2011-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    7aaf1f43760aff4b97c679c46dd8b6700c948ff5
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
#global gh_date      20150331
%global gh_owner     llaville
%global gh_project   php-reflect
#global prever       RC2
%if %{bootstrap}
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-bartlett-PHP-Reflect
Version:        4.0.2
%global specrel 2
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Adds the ability to reverse-engineer PHP

Group:          Development/Libraries
License:        BSD
URL:            http://php5.laurent-laville.org/reflect/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?prever}-%{gh_short}.tar.gz

# Autoloader for RPM - die composer !
Source1:        %{name}-autoload.php

# Enable cache plugin
Patch0:         %{name}-4.0.0-rpm.patch

BuildArch:      noarch
BuildRequires:  php(language) >= 5.4.0
%if %{with_tests}
# to run test suite
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-composer(sebastian/version)                 >= 1.0
BuildRequires:  php-composer(nikic/php-parser)                  >= 1.4
BuildRequires:  php-composer(nikic/php-parser)                  <  2
BuildRequires:  php-composer(doctrine/collections)              >= 1.2
BuildRequires:  php-composer(symfony/event-dispatcher)          >= 2.5
BuildRequires:  php-composer(symfony/finder)                    >= 2.5
BuildRequires:  php-composer(symfony/console)                   >= 2.5
BuildRequires:  php-composer(symfony/stopwatch)                 >= 2.5
BuildRequires:  php-composer(symfony/dependency-injection)      >= 2.5
BuildRequires:  php-composer(phpdocumentor/reflection-docblock) >= 2.0
BuildRequires:  php-composer(seld/jsonlint)                     >= 1.1
BuildRequires:  php-composer(justinrainbow/json-schema)         >= 1.3
BuildRequires:  php-composer(justinrainbow/json-schema)         <  2
BuildRequires:  php-composer(monolog/monolog)                   >= 1.10
# For our patch / autoloader
BuildRequires:  php-doctrine-collections                        >= 1.3.0-2
BuildRequires:  php-doctrine-cache                              >= 1.4.1
BuildRequires:  php-composer(fedora/autoloader)
%endif

# From composer.json, "require": {
#        "php": ">=5.4.0",
#        "ext-tokenizer": "*",
#        "ext-pcre": "*",
#        "ext-spl": "*",
#        "ext-json": "*",
#        "ext-date": "*",
#        "ext-reflection": "*",
#        "sebastian/version": "~1.0|~2.0",
#        "nikic/php-parser": "~1.4",
#        "doctrine/collections": "~1.2",
#        "symfony/event-dispatcher": "~2.5",
#        "symfony/finder": "~2.5",
#        "symfony/console": "~2.5"
#        "symfony/stopwatch": "~2.5",
#        "symfony/dependency-injection": "~2.5",
#        "phpdocumentor/reflection-docblock": "~2.0",
#        "justinrainbow/json-schema": "~1.3",
#        "seld/jsonlint": "~1.1"
Requires:       php(language) >= 5.4.0
Requires:       php-cli
Requires:       php-date
Requires:       php-json
Requires:       php-pcre
Requires:       php-pdo_sqlite
Requires:       php-reflection
Requires:       php-spl
Requires:       php-tokenizer
Requires:       php-composer(sebastian/version)                 >= 1.0
Requires:       php-composer(sebastian/version)                 <  3
Requires:       php-composer(nikic/php-parser)                  >= 1.4
Requires:       php-composer(nikic/php-parser)                  <  2
Requires:       php-composer(doctrine/collections)              >= 1.2
Requires:       php-composer(doctrine/collections)              <  2
Requires:       php-composer(symfony/event-dispatcher)          >= 2.5
Requires:       php-composer(symfony/event-dispatcher)          <  3
Requires:       php-composer(symfony/finder)                    >= 2.5
Requires:       php-composer(symfony/finder)                    <  3
Requires:       php-composer(symfony/console)                   >= 2.5
Requires:       php-composer(symfony/console)                   <  3
Requires:       php-composer(symfony/stopwatch)                 >= 2.5
Requires:       php-composer(symfony/stopwatch)                 <  3
Requires:       php-composer(symfony/dependency-injection)      >= 2.5
Requires:       php-composer(symfony/dependency-injection)      <  3
Requires:       php-composer(phpdocumentor/reflection-docblock) >= 2.0
Requires:       php-composer(phpdocumentor/reflection-docblock) <  3
Requires:       php-composer(seld/jsonlint)                     >= 1.1
Requires:       php-composer(seld/jsonlint)                     <  2
Requires:       php-composer(justinrainbow/json-schema)         >= 1.3
Requires:       php-composer(justinrainbow/json-schema)         <  2
#    "require-dev": {
#        "doctrine/cache": "~1.3",
#        "psr/log": "~1.0",
#        "monolog/monolog": "~1.10",
#        "bartlett/phpunit-loggertestlistener": "~1.3",
#        "bartlett/umlwriter": "~1.0"
#    "suggest": {
#        "doctrine/cache": "Allow caching results"
#        "psr/log": "Allow logging events with the LogPlugin",
#        "monolog/monolog": "Allow logging events with the LogPlugin",
#        "bartlett/phpunit-loggertestlistener": "Allow logging unit tests to your favorite PSR-3 logger interface",
#        "bartlett/umlwriter": "Allow writing UML class diagrams (Graphviz or PlantUML)"
Requires:       php-composer(doctrine/cache)           >= 1.3
Requires:       php-composer(psr/log)                  >= 1.0
%if ! %{bootstrap}
Requires:       php-composer(bartlett/umlwriter)       >= 1.0
Requires:       php-composer(bartlett/umlwriter)       <  2
%if 0%{?fedora} >= 21
Suggests:       php-composer(psr/log)
Suggests:       php-composer(monolog/monolog)
%endif
%endif
# For our patch / autoloader
Requires:       php-composer(fedora/autoloader)
Requires:       php-doctrine-collections               >= 1.3.0-2
Requires:       php-doctrine-cache                     >= 1.4.1
Requires:       php-PsrLog                             >= 1.0.0-8

Obsoletes:      php-channel-bartlett <= 1.3

Provides:       php-composer(bartlett/php-reflect) = %{version}


%description
PHP_Reflect adds the ability to reverse-engineer classes, interfaces,
functions, constants and more, by connecting php callbacks to other tokens.

Documentation: http://php5.laurent-laville.org/reflect/manual/current/en/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1 -b .rpm
cp %{SOURCE1} src/Bartlett/Reflect/autoload.php

sed -e 's/@package_version@/%{version}%{?prever}/' \
    -i $(find src -name \*.php) bin/phpreflect


%build
# Nothing


%install
mkdir -p %{buildroot}%{_datadir}/php
cp -pr src/Bartlett %{buildroot}%{_datadir}/php/Bartlett

install -D -p -m 755 bin/phpreflect           %{buildroot}%{_bindir}/phpreflect
install -D -p -m 644 bin/phpreflect.json.dist %{buildroot}%{_sysconfdir}/phpreflect.json
install -D -p -m 644 bin/phpreflect.1         %{buildroot}%{_mandir}/man1/phpreflect.1


%check
%if %{with_tests}
# Version 4.0.2: OK, but incomplete, skipped, or risky tests!
# Tests: 122, Assertions: 123, Incomplete: 3.
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --include-path=%{buildroot}%{_datadir}/php || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --include-path=%{buildroot}%{_datadir}/php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit \
    --include-path=%{buildroot}%{_datadir}/php \
    --verbose
# remirepo:2
fi
exit $ret
%else
: Test suite disabled
%endif


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      bartlett.laurent-laville.org/PHP_Reflect >/dev/null || :
fi


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json README.*
%config(noreplace) %{_sysconfdir}/phpreflect.json
%{_bindir}/phpreflect
%{_datadir}/php/Bartlett/Reflect*
%{_mandir}/man1/phpreflect.1*


%changelog
* Mon Oct 31 2016 Remi Collet <remi@fedoraproject.org> - 4.0.2-2
- switch to fedora/autoloader

* Fri Sep 23 2016 Remi Collet <remi@fedoraproject.org> - 4.0.2-1
- update to 4.0.2

* Wed Aug 10 2016 Remi Collet <remi@fedoraproject.org> - 4.0.1-2
- fix test suite to work with all Monolog versions
  from https://github.com/llaville/php-reflect/pull/22

* Wed Jul  6 2016 Remi Collet <remi@fedoraproject.org> - 4.0.1-1
- update to 4.0.1
- rewrite autoloader

* Mon Apr 18 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-3
- allow sebastian/version 2.0
- run test suite with both PHP 5 and 7 when available

* Sat Dec  5 2015 Remi Collet <remi@fedoraproject.org> - 4.0.0-1
- update to 4.0.0
- raise dependency on nikic/php-parser >= 1.4
- raise dependency on PHP >= 5.4

* Tue Sep 29 2015 Remi Collet <remi@fedoraproject.org> - 3.1.2-1
- update to 3.1.2

* Fri Jun 26 2015 Remi Collet <remi@fedoraproject.org> - 3.1.1-3
- rewrite autoloader

* Sun Jun 21 2015 Remi Collet <remi@fedoraproject.org> - 3.1.1-2
- fix autoloader

* Thu Jun 18 2015 Remi Collet <remi@fedoraproject.org> - 3.1.1-1
- update to 3.1.1

* Mon May 11 2015 Remi Collet <remi@fedoraproject.org> - 3.1.0-1
- update to 3.1.0

* Thu Apr 16 2015 Remi Collet <remi@fedoraproject.org> - 3.0.1-1
- update to 3.0.1
- raise dependency on nikic/php-parser >= 1.2.2

* Sat Apr  4 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-2
- add cache plugin in default configuration

* Fri Apr  3 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- update to 3.0.0
- cleanup EL-5 stuff

* Tue Mar 31 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.13.20150331git7efd1d0
- pull latest upstream changes

* Tue Mar 31 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.12.20150330git2c88d1a
- pull latest upstream changes

* Tue Mar 24 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.11.RC2
- update to 3.0.0 RC2
- add dependency on bartlett/umlwriter

* Thu Mar 12 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.10.RC1
- update to 3.0.0 RC1

* Thu Feb 26 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.9.20150226gitaab371c
- update to 3.0.0 beta3

* Mon Feb 23 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.8.20150219gite7f804e
- fix output

* Sun Feb 22 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.7.20150219gite7f804e
- fix reported version

* Sun Feb 22 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.6.20150219gite7f804e
- update to 3.0.0 beta2

* Wed Feb 04 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.5.20150203gitb4b807b
- update to 3.0.0 beta1

* Tue Jan 20 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.4.20150118git398cdae
- fix composer only code (pr #17)

* Mon Jan 19 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.3.20150118git398cdae
- new 3.0 snapshot

* Fri Jan 16 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.2.20150115git0189a64
- update to 3.0.0 alpha3

* Tue Jan  6 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.1.20150105git51f7968
- update to 3.0.0 alpha2
- drop dependency on phpunit/php-timer
- add dependencies on php-pdo_sqlite, doctrine/collections,
  symfony/stopwatch, symfony/dependency-injection
  and phpdocumentor/reflection-docblock

* Mon Jan  5 2015 Remi Collet <remi@fedoraproject.org> - 2.6.2-1
- Update to 2.6.2
- open https://github.com/llaville/php-reflect/pull/16

* Thu Dec  4 2014 Remi Collet <remi@fedoraproject.org> - 2.6.1-1
- Update to 2.6.1

* Thu Nov 13 2014 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0
- add dependency on justinrainbow/json-schema

* Thu Oct 16 2014 Remi Collet <remi@fedoraproject.org> - 2.5.0-1
- Update to 2.5.0
- add dependency on sebastian/version

* Fri Sep 19 2014 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0

* Fri Aug 22 2014 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0
- add dependency on seld/jsonlint

* Fri Jul 25 2014 Remi Collet <remi@fedoraproject.org> - 2.2.0-2
- obsoletes php-channel-bartlett

* Thu Jul 24 2014 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0

* Wed Jul 23 2014 Remi Collet <remi@fedoraproject.org> - 2.2.0-0.1.fe9d18d
- Test build of upcoming 2.2.0
- add manpage

* Tue Jul  8 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0

* Mon May 26 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-2
- fix dependencies

* Mon May 12 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0
- sources from github
- patch autoloader to not rely on composer
- drop documentation (link to online doc in description)

* Sat Oct 12 2013 Remi Collet <remi@fedoraproject.org> - 1.9.0-1
- Update to 1.9.0
- raise dependency on PHP >= 5.3

* Mon Sep 23 2013 Remi Collet <remi@fedoraproject.org> - 1.8.1-1
- Update to 1.8.1

* Fri Sep 20 2013 Remi Collet <remi@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Jun 26 2013 Remi Collet <remi@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Sat Apr 06 2013 Remi Collet <remi@fedoraproject.org> - 1.6.2-1
- Update to 1.6.2

* Tue Feb 26 2013 Remi Collet <remi@fedoraproject.org> - 1.6.1-1
- Update to 1.6.1

* Fri Feb 22 2013 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- Version 1.6.0 (stable) - API 1.6.0 (stable)
- html documentation is now provided by upstream

* Mon Nov 26 2012 Remi Collet <remi@fedoraproject.org> - 1.5.0-2
- generate documentation using asciidoc, without phing

* Mon Nov 26 2012 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- Version 1.5.0 (stable) - API 1.5.0 (stable)
- drop documentation build

* Tue Oct 30 2012 Remi Collet <remi@fedoraproject.org> - 1.4.3-1
- Version 1.4.3 (stable) - API 1.4.0 (stable)

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.4.2-2
- rebuildt for new pear_testdir

* Wed Aug 01 2012 Remi Collet <remi@fedoraproject.org> - 1.4.2-1
- Version 1.4.2 (stable) - API 1.4.0 (stable)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 17 2012 Remi Collet <remi@fedoraproject.org> - 1.3.0-2
- bump release

* Fri Feb 17 2012 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Version 1.3.0 (stable) - API 1.3.0 (stable)

* Sun Feb 05 2012 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Version 1.2.0 (stable) - API 1.2.0 (stable)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 11 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.1.0-1
- Version 1.1.0 (stable) - API 1.1.0 (stable)

* Mon Sep 19 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.2-2
- remove unused .js and improve installation of generated doc
- use buildroot macro

* Mon Jul 18 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.2-1
- Version 1.0.2 (stable) - API 1.0.0 (stable)

* Thu Jun 16 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.1-1
- Version 1.0.1 (stable) - API 1.0.0 (stable)

* Thu Jun 02 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-1
- Version 1.0.0 (stable) - API 1.0.0 (stable)
- add HTML documentation

* Tue Apr 26 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-0.1.RC1
- Version 1.0.0RC1 (beta) - API 1.0.0 (beta)

* Sun Apr 17 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.7.0-1
- Version 0.7.0 (beta) - API 0.7.0 (beta)

* Mon Apr 11 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.6.0-1
- Version 0.6.0 (beta) - API 0.6.0 (beta)

* Wed Apr 06 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.5.1-1
- Version 0.5.1 (beta) - API 0.5.0 (beta)

* Fri Mar 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.5.0-1
- Version 0.5.0 (beta) - API 0.5.0 (beta)

* Fri Feb 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.4.0-1
- Version 0.4.0 (beta)
- Initial RPM package

