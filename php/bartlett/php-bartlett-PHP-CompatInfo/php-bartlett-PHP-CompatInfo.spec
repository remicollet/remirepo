# spec file for php-bartlett-PHP-CompatInfo
#
# Copyright (c) 2011-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    4f9def9b616c3af1bb577c188b66f3039e8dd333
#global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     llaville
%global gh_project   php-compat-info

Name:           php-bartlett-PHP-CompatInfo
Version:        3.4.0
%global specrel 1
Release:        %{?gh_short:0.%{specrel}.git%{gh_short}}%{!?gh_short:%{specrel}}%{?dist}
Summary:        Find out version and the extensions required for a piece of code to run

Group:          Development/Libraries
License:        BSD
URL:            http://php5.laurent-laville.org/compatinfo/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?gh_short:-%{gh_short}}.tar.gz

# Autoloader for RPM - die composer !
Patch0:         %{name}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
# to run test suite
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-composer(bartlett/php-reflect) >= 2.4

# From composer.json, "require"
#        "php": ">=5.3.0",
#        "ext-libxml": "*",
#        "ext-pcre": "*",
#        "ext-spl": "*",
#        "ext-json": "*",
#        "symfony/console": "~2.5",
#         "bartlett/php-reflect": "~2.4",
#         "seld/jsonlint": "~1.1"
Requires:       php(language) >= 5.3.0
Requires:       php-json
Requires:       php-libxml
Requires:       php-pcre
Requires:       php-spl
Requires:       php-composer(bartlett/php-reflect) >= 2.4
Requires:       php-composer(bartlett/php-reflect) <  3
Requires:       php-composer(symfony/console)      >= 2.5
Requires:       php-composer(symfony/console)      <  3
Requires:       php-composer(seld/jsonlint)        >= 1.1
Requires:       php-composer(seld/jsonlint)        <  2
# From composer.json, "suggest"
#        "doctrine/cache": "Allow caching results, since bartlett/php-reflect 2.2"
Requires:       php-composer(doctrine/cache)
# Required by autoloader
Requires:       php-composer(phpunit/php-timer)
Requires:       php-composer(nikic/php-parser)
Requires:       php-composer(symfony/class-loader)
Requires:       php-composer(symfony/event-dispatcher)
Requires:       php-composer(symfony/finder)

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

%patch0 -p1 -b .rpm

sed -e 's/@package_version@/%{version}/' \
    -i $(find src -name \*.php)


%build
# Nothing


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/php
cp -pr src/Bartlett %{buildroot}%{_datadir}/php/Bartlett

install -D -p -m 755 bin/phpcompatinfo           %{buildroot}%{_bindir}/phpcompatinfo
install -D -p -m 644 bin/phpcompatinfo.json.dist %{buildroot}%{_sysconfdir}/phpcompatinfo.json
install -D -p -m 644 bin/phpcompatinfo.1         %{buildroot}%{_mandir}/man1/phpcompatinfo.1


%check
# Not ready (local build with php 5.6 and xcache 4.0-dev)
rm tests/Reference/Extension/XcacheExtensionTest.php

%{_bindir}/phpunit \
    -d date.timezone=UTC \
    -d memory_limit=-1 \
%if 0%{?rhel} < 6 && 0%{?fedora} < 8
    || exit 0
%endif


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      bartlett.laurent-laville.org/PHP_CompatInfo >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json README.*
%config(noreplace) %{_sysconfdir}/phpcompatinfo.json
%{_bindir}/phpcompatinfo
%{_datadir}/php/Bartlett/CompatInfo
%{_datadir}/php/Bartlett/CompatInfo.php
%{_mandir}/man1/phpcompatinfo.1*


%changelog
* Thu Sep 25 2014 Remi Collet <remi@fedoraproject.org> - 3.4.0-1
- Update to 3.4.0

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

