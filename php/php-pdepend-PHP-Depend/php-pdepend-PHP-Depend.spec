# remirepo spec file for php-pdepend-PHP-Depend, from:
#
# Fedora spec file for php-pdepend-PHP-Depend
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%global gh_commit    3f7deab87836dd83d7a7b6a2098f75d8f38566aa
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     pdepend
%global gh_project   pdepend
%{!?__pear: %global __pear %{_bindir}/pear}
%global pear_name    PHP_Depend
%global pear_channel pear.pdepend.org
%global php_home     %{_datadir}/php/PDepend
%global with_tests   0%{!?_without_tests:1}

Name:           php-pdepend-PHP-Depend
Version:        2.3.0
Release:        1%{?dist}
Summary:        PHP_Depend design quality metrics for PHP package

Group:          Development/Libraries
License:        BSD
URL:            http://pdepend.org/
# git snashop to get upstream test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh
# Autoloader
Source2:        %{name}-autoload.php
Patch0:         %{name}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# From composer/json, "require-dev": {
#        "phpunit/phpunit": "^4.4.0,<4.8",
#        "squizlabs/php_codesniffer": "^2.0.0"
# Test suite pass with PHPUnit 4.8.12 and PHPUnit 5.0.5
BuildRequires:  php-composer(phpunit/phpunit) >= 4.0.0
BuildRequires:  php(language) >= 5.3.7
BuildRequires:  php-composer(symfony/dependency-injection) >= 2.3.0
BuildRequires:  php-composer(symfony/filesystem) >= 2.3.0
BuildRequires:  php-composer(symfony/config) >= 2.3.0
BuildRequires:  php-bcmath
BuildRequires:  php-date
BuildRequires:  php-dom
BuildRequires:  php-iconv
BuildRequires:  php-libxml
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
BuildRequires:  php-reflection
BuildRequires:  php-simplexml
BuildRequires:  php-spl
BuildRequires:  php-tokenizer
BuildRequires:  php-xml
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)
%endif

# From composer.json, "require": {
#        "php": ">=5.3.7"
#        "symfony/dependency-injection": "^2.3.0|^3",
#        "symfony/filesystem": "^2.3.0|^3",
#        "symfony/config": "^2.3.0|^3"
Requires:       php(language) >= 5.3.7
Requires:       php-composer(symfony/dependency-injection) >= 2.3.0
Requires:       php-composer(symfony/dependency-injection) <  4
Requires:       php-composer(symfony/filesystem) >= 2.3.0
Requires:       php-composer(symfony/filesystem) <  4
Requires:       php-composer(symfony/config) >= 2.3.0
Requires:       php-composer(symfony/config) <  4
# From phpcompatinfo report for version 2.3.0
Requires:       php-bcmath
Requires:       php-date
Requires:       php-dom
Requires:       php-iconv
Requires:       php-libxml
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-simplexml
Requires:       php-spl
Requires:       php-tokenizer
Requires:       php-xml
# Autoloader
Requires:       php-composer(fedora/autoloader)

# Single package in this channel
Obsoletes:      php-channel-pdepend <= 1.3

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
PHP_Depend is an adaption of the established Java development tool JDepend.
This tool shows you the quality of your design in the terms of extensibility,
reusability and maintainability.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p0
cp %{SOURCE2} src/main/php/PDepend/autoload.php

find src/main/php -name \*php -exec sed -e 's:@package_version@:%{version}:' -i {} \;
find src/test/php -name \*xml -exec sed -e 's:@package_version@:%{version}:' -i {} \;


%build
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

: Library
mkdir -p $(dirname %{buildroot}%{php_home})
cp -pr src/main/php/PDepend %{buildroot}%{php_home}

: Resources
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -pr src/main/resources %{buildroot}%{_datadir}/%{name}/resources

: Command
install -Dpm 0755 src/bin/pdepend %{buildroot}%{_bindir}/pdepend


%check
%if %{with_tests}
%if 0%{?fedora} >= 22
# Temporary ignore this test, BC break in libxml, see
# https://bugzilla.redhat.com/1199396  incorrect identification of duplicate ID
rm src/test/php/PDepend/Report/Jdepend/ChartTest.php
%endif

cat << 'EOF' | tee src/test/php/PDepend/bootstrap.php
<?php
require '%{buildroot}%{php_home}/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('PDepend\\', __DIR__);
EOF

# remirepo:11
ret=0
run=0
if which php71; then
    php71 %{_bindir}/phpunit -d memory_limit=1G || ret=1
    run=1
fi
if which php56; then
    php56 %{_bindir}/phpunit -d memory_limit=1G || ret=1
    run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit -d memory_limit=1G --verbose
# remirepo:2
fi
exit $ret
%else
: Test suite disabled
%endif


%pre
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json
%doc CHANGELOG
%{php_home}
%{_datadir}/%{name}
%{_bindir}/pdepend


%changelog
* Wed Nov 23 2016 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- update to 2.3.0
- add dependency on iconv, mbstring and xml

* Tue Nov 22 2016 Remi Collet <remi@fedoraproject.org> - 2.2.6-1
- update to 2.2.6
- switch to fedora/autoloader

* Thu Mar 10 2016 Remi Collet <remi@fedoraproject.org> - 2.2.4-1
- update to 2.2.4

* Tue Feb 23 2016 Remi Collet <remi@fedoraproject.org> - 2.2.3-1
- update to 2.2.3

* Fri Oct 16 2015 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- update to 2.2.2

* Fri Sep 25 2015 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- update to 2.2.1

* Mon Sep 21 2015 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- update to 2.2.0

* Thu Jul  2 2015 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- update to 2.1.0
- switch from pear channel to git snapshot sources
- run upstream test suite during build

* Sun May 04 2014 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4

* Fri Jul 26 2013 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1
- explicit dependencies
- cleanups

* Wed Sep 12 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.0-1
- upstream 1.0.7, backport for remi repo

* Wed Sep 12 2012 Christof Damian <christof@damian.net> - 1.1.0-1
- upstream 1.1.0

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
 - Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May  1 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.7-1
- upstream 1.0.7, backport for remi repo

* Tue May  1 2012 Christof Damian <christof@damian.net> - 1.0.7-1
- upstream 1.0.7

* Thu Apr 12 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.5-1
- upstream 1.0.5

* Wed Apr 11 2012 Christof Damian <christof@damian.net> - 1.0.5-1
- upstream 1.0.5

* Sat Mar 03 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.4-1
- upstream 1.0.4

* Tue Feb 28 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.3-1
- upstream 1.0.3

* Thu Feb 23 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.2-1
- upstream 1.0.2

* Sat Feb 11 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.1-1
- upstream 1.0.1, rebuild for remi repository

* Thu Feb  9 2012 Christof Damian <christof@damian.net> - 1.0.1-1
- upstream 1.0.1

* Tue Nov 01 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.10.6-1
- upstream 0.10.6, rebuild for remi repository

* Sun Oct 30 2011 Christof Damian <christof@damian.net> - 0.10.6-1
- upstream 0.10.6

* Fri May 27 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.10.5-1
- upstream 0.10.5
- rebuild for remi repository

* Fri May 20 2011 Christof Damian <christof@damian.net> - 0.10.5-1
- upstream 0.10.5

* Fri Mar  4 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.10.3-1
- upstream 0.10.3
- rebuild for remi repository

* Fri Mar  4 2011 Christof Damian <christof@damian.net> - 0.10.3-1
- upstream 0.10.3

* Mon Feb 28 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.10.2-1
- upstream 0.10.2
- rebuild for remi repository

* Mon Feb 28 2011 Christof Damian <cdamian@robin.gotham.krass.com> - 0.10.2-1
- upstream 0.10.2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.10.1-1
- upstream stable release 0.10.1 
- rebuild for remi repository

* Sun Feb  6 2011 Christof Damian <christof@damian.net> - 0.10.1-1
- upstream stable release 0.10.1 

* Sat Sep 18 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.19-1
- upstream 0.9.19
- rebuild for remi repository

* Fri Sep 17 2010 Christof Damian <christof@damian.net> - 0.9.19-1
- upstream 0.9.19

* Sat Sep 04 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.18-1
- rebuild for remi repository

* Fri Sep  3 2010 Christof Damian <christof@damian.net> - 0.9.18-1
- upstream 0.9.18

* Fri Jul 30 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.17-1
- rebuild for remi repository

* Fri Jul 30 2010 Christof Damian <christof@damian.net> - 0.9.17-1
- upstream 0.9.17

* Mon Jun 21 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.16-1
- rebuild for remi repository

* Sun Jun 20 2010 Christof Damian <christof@damian.net> - 0.9.16-1
- upstream 0.9.16: bugfixes

* Sun May 23 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.14-1
- rebuild for remi repository

* Sat May 22 2010 Christof Damian <christof@damian.net> - 0.9.14-1
- upstream 0.9.14

* Mon May 10 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.13-1
- rebuild for remi repository

* Mon May 10 2010 Christof Damian <christof@damian.net> - 0.9.13-1
- upstream 0.9.13 important bugfixes

* Thu Apr 29 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.12-1
- rebuild for remi repository

* Tue Apr 27 2010 Christof Damian <christof@damian.net> - 0.9.12-1
- upstream 0.9.12
- upstream removed all tests

* Thu Mar  4 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.11-1
- rebuild for remi repository

* Wed Mar  3 2010 Christof Damian <christof@damian.net> - 0.9.11-1
- upstream 0.9.11

* Thu Feb 25 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.10-1
- rebuild for remi repository

* Tue Feb 23 2010 Christof Damian <christof@damian.net> - 0.9.10-1
- upstream 0.9.10
- replaced define macro with global

* Mon Feb 01 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.9-2
- rebuild for remi repository

* Tue Jan 26 2010 Christof Damian <christof@damian.net> 0.9.9-2
- require pecl imagick, which is an optional requirement
- require php-xml for dom
- change postun to use channel macro for consistency
- own /usr/share/pear/PHP
- include test files (which currently don't work)

* Fri Jan  1 2010 Christof Damian <christof@damian.net> 0.9.9-1
- initial release
