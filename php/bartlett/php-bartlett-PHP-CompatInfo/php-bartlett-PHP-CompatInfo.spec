# remirepo/fedora spec file for php-bartlett-PHP-CompatInfo
#
# Copyright (c) 2011-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?php_version:  %global php_version  %(php -r 'echo PHP_VERSION;' 2>/dev/null)}
%global gh_commit    cbd03899c8a48eb2f9274035c0770d83821905ab
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
#global gh_date      20151005
%global gh_owner     llaville
%global gh_project   php-compat-info
#global prever       RC2
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-bartlett-PHP-CompatInfo
Version:        5.0.5
%global specrel 1
Release:        %{?gh_date:1%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Find out version and the extensions required for a piece of code to run

Group:          Development/Libraries
License:        BSD
URL:            http://php5.laurent-laville.org/compatinfo/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?prever}-%{gh_short}.tar.gz

# Script for fedora-review
Source1:        fedora-review-check

# Autoloader for RPM - die composer !
Source2:        %{name}-5.0.0-autoload.php

# Autoload and sqlite database path
Patch0:         %{name}-5.0.0-rpm.patch

BuildArch:      noarch
BuildRequires:  php(language) >= 5.4.0
%if %{with_tests}
# to run test suite
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-pdo_sqlite
BuildRequires:  php-composer(bartlett/php-reflect) >= 4.0
BuildRequires:  php-composer(bartlett/php-compatinfo-db) >= 1.15
# For our patch / autoloader
BuildRequires:  php-composer(fedora/autoloader)
%endif

# From composer.json, "require"
#        "php": ">=5.4.0",
#        "ext-libxml": "*",
#        "ext-pcre": "*",
#        "ext-spl": "*",
#        "ext-json": "*",
#        "ext-pdo_sqlite": "*",
#        "symfony/console": "~2.5",
#        "bartlett/php-reflect": "~4.0",
#        "bartlett/php-compatinfo-db": "~1.0"
Requires:       php(language) >= 5.4.0
Requires:       php-cli
Requires:       php-json
Requires:       php-libxml
Requires:       php-pcre
Requires:       php-pdo_sqlite
Requires:       php-spl
Requires:       php-composer(bartlett/php-reflect) >= 4.0
Requires:       php-composer(bartlett/php-reflect) <  5
Requires:       php-composer(bartlett/php-compatinfo-db) >= 1.15
Requires:       php-composer(bartlett/php-compatinfo-db) <  2
Requires:       php-composer(symfony/console)      >= 2.5
Requires:       php-composer(symfony/console)      <  3
# From composer.json, "require-dev": {
#        "doctrine/cache": "~1.3",
#        "psr/log": "~1.0",
#        "monolog/monolog": "~1.10",
#        "bartlett/monolog-callbackfilterhandler": "~1.0",
#        "bartlett/monolog-growlhandler": "~1.0",
#        "bartlett/phpunit-loggertestlistener": "~1.5",
#        "bartlett/umlwriter": "~1.0"
# From composer.json, "suggest"
#        "doctrine/cache": "Allow caching results, since bartlett/php-reflect 2.2",
#        "psr/log": "Allow logging events with the LogPlugin",
#        "monolog/monolog": "Allow logging events with the LogPlugin",
#        "bartlett/monolog-callbackfilterhandler": "Advanced filtering strategies for Monolog",
#        "bartlett/monolog-growlhandler": "Sends notifications to Growl for Monolog",
#        "bartlett/phpunit-loggertestlistener": "Allow logging unit tests to your favorite PSR-3 logger interface",
#        "bartlett/umlwriter": "Allow writing UML class diagrams (Graphviz or PlantUML)"
#        "doctrine/cache": "Allow caching results, since bartlett/php-reflect 2.2"
#        "bartlett/umlwriter": "Allow writing UML class diagrams (Graphviz or PlantUML)"
# Required by autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       phpcompatinfo = %{version}
Provides:       php-composer(bartlett/php-compatinfo) = %{version}


%description
PHP_CompatInfo will parse a file/folder/array to find out the minimum
version and extensions required for it to run. CLI version has many reports
(extension, interface, class, function, constant) to display and ability to
show content of dictionary references.

Documentation: http://php5.laurent-laville.org/compatinfo/manual/current/en/


%prep
%setup -q -n %{gh_project}-%{gh_commit}
#setup -q -n %{gh_project}-%{version}

%patch0 -p1 -b .rpm
cp %{SOURCE2} src/Bartlett/CompatInfo/autoload.php

# Cleanup patched files
find src -name \*rpm -delete -print

# Set package version
sed -e 's/@package_version@/%{version}%{?prever}/' \
    -i $(find src -name \*.php) bin/phpcompatinfo


%build
# Nothing


%install
mkdir -p %{buildroot}%{_datadir}/php
cp -pr src/Bartlett %{buildroot}%{_datadir}/php/Bartlett

install -D -p -m 755 bin/phpcompatinfo           %{buildroot}%{_bindir}/phpcompatinfo
install -D -p -m 644 bin/phpcompatinfo.json.dist %{buildroot}%{_sysconfdir}/phpcompatinfo.json
install -D -p -m 644 bin/phpcompatinfo.1         %{buildroot}%{_mandir}/man1/phpcompatinfo.1

install -D -p -m 755 %{SOURCE1}                  %{buildroot}%{_datadir}/%{name}/fedora-review-check


%if %{with_tests}
%check
mkdir vendor
ln -s %{buildroot}%{_datadir}/php/Bartlett/CompatInfo/autoload.php vendor/


ret=0
for cmd in php php56 php70 php71; do
  if which $cmd; then
    $cmd %{_bindir}/phpunit --include-path %{buildroot}%{_datadir}/php --verbose || ret=1
  fi
done
exit $ret
%endif


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      bartlett.laurent-laville.org/PHP_CompatInfo >/dev/null || :
fi


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json README.*
%config(noreplace) %{_sysconfdir}/phpcompatinfo.json
%{_bindir}/phpcompatinfo
%{_datadir}/php/Bartlett/CompatInfo
%{_mandir}/man1/phpcompatinfo.1*
%{_datadir}/%{name}


%changelog
* Fri Mar 17 2017 Remi Collet <remi@remirepo.net> - 5.0.5-1
- Update to 5.0.5

* Tue Jan 17 2017 Remi Collet <remi@fedoraproject.org> - 5.0.4-1
- update to 5.0.4

* Wed Jan 11 2017 Remi Collet <remi@fedoraproject.org> - 5.0.3-1
- update to 5.0.3

* Fri Dec 16 2016 Remi Collet <remi@fedoraproject.org> - 5.0.2-1
- update to 5.0.2

* Mon Oct 31 2016 Remi Collet <remi@fedoraproject.org> - 5.0.1-2
- switch to fedora/autoloader

* Wed Jul  6 2016 Remi Collet <remi@fedoraproject.org> - 5.0.1-1
- update to 5.0.1

* Wed Mar  9 2016 Remi Collet <remi@fedoraproject.org> - 5.0.0-2
- display DB version instead of build date

* Thu Dec 10 2015 Remi Collet <remi@fedoraproject.org> - 5.0.0-1
- update to 5.0.0
- raise dependency on bartlett/php-reflect ~4.0
- raise minimal php version to 5.4
- add dependency on bartlett/php-compatinfo-db

* Wed Nov 25 2015 Remi Collet <remi@fedoraproject.org> - 4.5.2-1
- update to 4.5.2

* Sun Oct 11 2015 Remi Collet <remi@fedoraproject.org> - 4.5.1-1
- update to 4.5.1

* Thu Oct  8 2015 Remi Collet <remi@fedoraproject.org> - 4.5.0-2
- add upstream patch for missing extensions
  https://github.com/llaville/php-compat-info/issues/210

* Tue Oct  6 2015 Remi Collet <remi@fedoraproject.org> - 4.5.0-1
- update to 4.5.0

* Sat Oct  3 2015 Remi Collet <remi@fedoraproject.org> - 4.4.0-3
- test build of master

* Sat Jul 18 2015 Remi Collet <remi@fedoraproject.org> - 4.4.0-2
- test build of master

* Mon Jul 13 2015 Remi Collet <remi@fedoraproject.org> - 4.4.0-1
- update to 4.4.0

* Fri Jun 26 2015 Remi Collet <remi@fedoraproject.org> - 4.3.0-3
- rewrite autoloader

* Sun Jun 21 2015 Remi Collet <remi@fedoraproject.org> - 4.3.0-2
- fix autoloader

* Tue Jun 16 2015 Remi Collet <remi@fedoraproject.org> - 4.3.0-1
- update to 4.3.0

* Tue May 19 2015 Remi Collet <remi@fedoraproject.org> - 4.2.0-1
- update to 4.2.0
- raise dependency on bartlett/php-reflect 3.1

* Fri Apr 24 2015 Remi Collet <remi@fedoraproject.org> - 4.1.0-2
- test build from generictest branch

* Fri Apr 17 2015 Remi Collet <remi@fedoraproject.org> - 4.1.0-1
- update to 4.1.0
- keep upstream shebang with /usr/bin/env (for SCL)

* Sat Apr  4 2015 Remi Collet <remi@fedoraproject.org> - 4.0.0-2
- add cache plugin in default configuration

* Sat Apr  4 2015 Remi Collet <remi@fedoraproject.org> - 4.0.0-1
- update to 4.0.0

* Thu Mar 26 2015 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.9.RC2
- update to 4.0.0 RC2
- add dependency on bartlett/umlwriter

* Thu Mar 12 2015 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.8.RC1
- update to 4.0.0 RC1

* Fri Feb 27 2015 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.7.20150227git4966955
- don't display xdebug message when not on a tty
- add fedora-review-check script
- handle --without tests option to skip test suite during build

* Fri Feb 27 2015 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.6.20150227git4966955
- update to 4.0.0beta3

* Sun Feb 22 2015 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.5.20150220git442d25d
- fix reported version

* Sun Feb 22 2015 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.4.20150220git442d25d
- update to 4.0.0beta2

* Wed Feb  4 2015 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.3.20150204git6cd2777
- update to 4.0.0beta1

* Mon Feb  2 2015 Remi Collet <remi@fedoraproject.org> - 3.7.3-1
- Update to 3.7.3

* Tue Jan 20 2015 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.2.20150116gitd900ea4
- add patch for DB path (pr #163)
- take care of test suite results only in f21 for now

* Mon Jan 19 2015 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.1.20150116gitd900ea4
- 4.0.0 snapshot

* Mon Jan  5 2015 Remi Collet <remi@fedoraproject.org> - 3.7.2-1
- Update to 3.7.2
- open https://github.com/llaville/php-compat-info/pull/157

* Fri Dec 19 2014 Remi Collet <remi@fedoraproject.org> - 3.7.1-1
- Update to 3.7.1

* Fri Dec 12 2014 Remi Collet <remi@fedoraproject.org> - 3.7.0-1
- Update to 3.7.0

* Thu Nov 20 2014 Remi Collet <remi@fedoraproject.org> - 3.6.1-1
- Update to 3.6.1

* Thu Nov 13 2014 Remi Collet <remi@fedoraproject.org> - 3.6.0-1
- Update to 3.6.0
- add dependency on justinrainbow/json-schema
- raise dependency on bartlett/php-reflect 2.6

* Thu Oct 16 2014 Remi Collet <remi@fedoraproject.org> - 3.5.0-1
- Update to 3.5.0
- add dependency on sebastian/version
- raise dependency on bartlett/php-reflect 2.5

* Thu Sep 25 2014 Remi Collet <remi@fedoraproject.org> - 3.4.0-1
- Update to 3.4.0
- raise dependency on bartlett/php-reflect 2.4

* Wed Sep 24 2014 Remi Collet <remi@fedoraproject.org> - 3.4.0-0.1.ded22dc
- Test build of upcoming 3.4.0

* Fri Aug 22 2014 Remi Collet <remi@fedoraproject.org> - 3.3.0-1
- Update to 3.2.0
- add dependency on seld/jsonlint
- raise dependency on bartlett/php-reflect 2.3
- enable the cache plugin in default configuration

* Fri Jul 25 2014 Remi Collet <remi@fedoraproject.org> - 3.2.0-3
- cleanup pear registration

* Thu Jul 24 2014 Remi Collet <remi@fedoraproject.org> - 3.2.0-2
- add upstream patch for SNMP extension

* Thu Jul 24 2014 Remi Collet <remi@fedoraproject.org> - 3.2.0-1
- Update to 3.2.0

* Wed Jul 23 2014 Remi Collet <remi@fedoraproject.org> - 3.2.0-0.1.970d967
- Test build of upcoming 3.2.0
- add manpage

* Mon May 26 2014 Remi Collet <remi@fedoraproject.org> - 3.1.0-2
- fix dependencies

* Mon May 12 2014 Remi Collet <remi@fedoraproject.org> - 3.1.0-1
- update to 3.1.0
- sources from github
- patch autoloader to not rely on composer
- drop documentation (link to online doc in description)

* Fri Dec 13 2013 Remi Collet <remi@fedoraproject.org> - 2.26.0-1
- Update to 2.26.0 (stable)

* Thu Nov 14 2013 Remi Collet <remi@fedoraproject.org> - 2.25.0-1
- Update to 2.25.0
- remove phpci temporary compat command

* Fri Oct 18 2013 Remi Collet <remi@fedoraproject.org> - 2.24.0-1
- update to 2.24.0
- raise dependency, PHP_Reflect 1.9.0

* Sat Oct 12 2013 Remi Collet <remi@fedoraproject.org> - 2.24.0-0.1
- 2.24.0 test (not released)

* Mon Sep 23 2013 Remi Collet <remi@fedoraproject.org> - 2.23.1-1
- Update to 2.23.1

* Fri Sep 20 2013 Remi Collet <remi@fedoraproject.org> - 2.23.0-1
- Update to 2.23.0
- raise dependencies: PHP 5.3.0, PHP_Reflect 1.8.0 (and < 2)
- add patch for new constants in jsonc 1.3.2

* Fri Aug 23 2013 Remi Collet <remi@fedoraproject.org> - 2.22.0-1
- Update to 2.22.0

* Tue Aug 20 2013 Remi Collet <remi@fedoraproject.org> - 2.21.0-1
- Update to 2.21.0
- patch for https://github.com/llaville/php-compat-info/issues/99

* Thu Jul 25 2013 Remi Collet <remi@fedoraproject.org> - 2.20.0-1
- Update to 2.20.0
- patch from https://github.com/llaville/php-compat-info/pull/98

* Fri Jul 12 2013 Remi Collet <remi@fedoraproject.org> - 2.19.0-1
- Update to 2.19.0
- add module and install to fileExtensions in default configuration
  for drupal packages, #979830
- patch from https://github.com/llaville/php-compat-info/pull/95

* Wed Jun 26 2013 Remi Collet <remi@fedoraproject.org> - 2.18.0-1
- Update to 2.18.0
- raise dependencies, PHP_Reflect 1.7.0
- drop PHP 5.5 patches, applied upstream
- add patch for windows only constants

* Fri Jun 07 2013 Remi Collet <remi@fedoraproject.org> - 2.17.0-2
- keep phpci command for now

* Fri Jun 07 2013 Remi Collet <remi@fedoraproject.org> - 2.17.0-1
- Update to 2.17.0
- phpci command renamed to phpcompatinfo

* Fri May 10 2013 Remi Collet <remi@fedoraproject.org> - 2.16.0-1
- Update to 2.16.0

* Fri Apr 12 2013 Remi Collet <remi@fedoraproject.org> - 2.15.0-2
- add upstream man page (from github)

* Fri Apr 12 2013 Remi Collet <remi@fedoraproject.org> - 2.15.0-1
- Update to 2.15.0
- raise dependencies, PHP_Reflect 1.6.2
- add more patches for PHP 5.5 reference

* Tue Apr 02 2013 Remi Collet <remi@fedoraproject.org> - 2.14.1-1
- Update to 2.14.1
- make cache path user dependent

* Mon Mar 18 2013 Remi Collet <remi@fedoraproject.org> - 2.14.0-3
- add patch for broken extension report
  https://github.com/llaville/php-compat-info/issues/76

* Mon Mar 18 2013 Remi Collet <remi@fedoraproject.org> - 2.14.0-2
- provides phpci
- cleanups

* Mon Mar 18 2013 Remi Collet <remi@fedoraproject.org> - 2.14.0-1
- Update to 2.14.0

* Tue Feb 26 2013 Remi Collet <remi@fedoraproject.org> - 2.13.2-1
- Update to 2.13.2

* Tue Feb 26 2013 Remi Collet <remi@fedoraproject.org> - 2.13.1-1
- Update to 2.13.1
- raise dependencies, PHP_Reflect 1.6.1

* Fri Feb 22 2013 Remi Collet <remi@fedoraproject.org> - 2.13.0-1
- Update to 2.13.0
- raise dependencies, PHP_Reflect 1.6.0

* Fri Jan 18 2013 Remi Collet <remi@fedoraproject.org> - 2.12.1-1
- update to Version 2.12.1
- fix path to documentation in description

* Thu Jan 17 2013 Remi Collet <remi@fedoraproject.org> - 2.12.0-1
- update to Version 2.12.0
- drop dependency on eZ components
- raise PHPUnit dependency to 3.6.0
- update References for PHP 5.5 (non yet merged by upstream)

* Fri Dec 21 2012 Remi Collet <remi@fedoraproject.org> - 2.11.0-1
- update to Version 2.11.0
- html documentation is now provided by upstream

* Mon Nov 26 2012 Remi Collet <remi@fedoraproject.org> - 2.10.0-2
- generate documentation using asciidoc, without phing

* Mon Nov 26 2012 Remi Collet <remi@fedoraproject.org> - 2.10.0-1
- Version 2.10.0 (stable) - API 2.10.0 (stable)
- raise dependencies, PHP_Reflect 1.5.0
- drop documentation build

* Tue Oct 30 2012 Remi Collet <remi@fedoraproject.org> - 2.9.0-1
- Version 2.9.0 (stable) - API 2.9.0 (stable)
- raise dependencies, PHP_Reflect 1.4.3, Console_CommandLine 1.2.0

* Sat Sep 29 2012 Remi Collet <remi@fedoraproject.org> - 2.8.1-1
- Version 2.8.1 (stable) - API 2.8.0 (stable)

* Mon Sep 17 2012 Remi Collet <remi@fedoraproject.org> - 2.8.0-1
- Version 2.8.0 (stable) - API 2.8.0 (stable)
- new extensions : amqp, geoip, inclued, xcache

* Mon Sep  3 2012 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- Version 2.7.0 (stable) - API 2.7.0 (stable)

* Sun Aug 19 2012 Remi Collet <remi@fedoraproject.org> - 2.6.0-3
- rebuilt for new pear_datadir

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 2.6.0-2
- rebuildt for new pear_testdir

* Wed Aug 01 2012 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- Version 2.6.0 (stable) - API 2.6.0 (stable)
- raise dependencies: PHPUnit 3.6.0, PHP_Reflect 1.4.2

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul  8 2012 Remi Collet <remi@fedoraproject.org> - 2.5.0-1.1
- drop XslTest in EL-6

* Fri Jun 22 2012 Remi Collet <remi@fedoraproject.org> - 2.5.0-1
- Version 2.5.0 (stable) - API 2.5.0 (stable)
- use reference="ALL" in provided config

* Fri May 11 2012 Remi Collet <remi@fedoraproject.org> - 2.4.0-1.1
- add patch for old libxml

* Fri May 11 2012 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- Version 2.4.0 (stable) - API 2.3.0 (stable)

* Mon Mar 05 2012 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- Version 2.3.0 (stable) - API 2.3.0 (stable)

* Sat Feb 25 2012 Remi Collet <remi@fedoraproject.org> - 2.2.5-1
- Version 2.2.5 (stable) - API 2.2.0 (stable)

* Fri Feb 17 2012 Remi Collet <remi@fedoraproject.org> - 2.2.4-1
- Version 2.2.4 (stable) - API 2.2.0 (stable)

* Tue Feb 14 2012 Remi Collet <remi@fedoraproject.org> - 2.2.3-1
- Version 2.2.3 (stable) - API 2.2.0 (stable)

* Thu Feb 09 2012 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- Version 2.2.2 (stable) - API 2.2.0 (stable)

* Sun Feb 05 2012 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- Version 2.2.1 (stable) - API 2.2.0 (stable)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Sep 24 2011 Remi Collet <remi@fedoraproject.org> - 2.1.0-3.1
- no html doc on EL6

* Wed Sep 21 2011 Remi Collet <remi@fedoraproject.org> - 2.1.0-3
- remove all files with licensing issue
  don't use it during test, don't install it
  can keep it in sources are this files are still under free license

* Tue Sep 20 2011 Remi Collet <remi@fedoraproject.org> - 2.1.0-2
- comments from review #693204
- remove ascii*js (not used)
- add MIT to license for bundled jquery

* Thu Aug 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.1.0-1
- Version 2.1.0 (stable) - API 2.1.0 (stable)
- fix documentation for asciidoc 8.4

* Sat Jun 04 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.0-1
- Version 2.0.0 (stable) - API 2.0.0 (stable)
- add HTML documentation

* Tue Apr 26 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.0-0.3.RC4
- Version 2.0.0RC4 (beta) - API 2.0.0 (beta)

* Fri Mar 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.0-0.2.RC3
- Version 2.0.0RC3

* Wed Feb 23 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.0-0.1.RC2
- Version 2.0.0RC2
- Initial Release

