# remirepo/fedora spec file for php-phpunit-PHP-Timer
#
# Copyright (c) 2010-2015 Christof Damian, Remi Collet
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%global gh_commit    3dcf38ca72b158baf0bc245e9184d3fdffa9c46f
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   php-timer
%global php_home     %{_datadir}/php
%global pear_name    PHP_Timer
%global pear_channel pear.phpunit.de
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-phpunit-PHP-Timer
Version:        1.0.9
Release:        1%{?dist}
Summary:        PHP Utility class for timing

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-fedora-autoloader-devel
%if %{with_tests}
# From composer.json"require-dev": {
#        "phpunit/phpunit": "^4.8.35 || ^5.7 || ^6.0"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.8.35
%endif

# From composer.json
#        "php": "^5.3.3 || ^7.0"
Requires:       php(language) >= 5.3.3
# From phpcompatinfo report for version 1.0.5
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(phpunit/php-timer) = %{version}
# For compatibility with PEAR mode
Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
PHP Utility class for timing


%prep
%setup -q -n %{gh_project}-%{gh_commit}

# Restore PSR-0 tree
mv src PHP
mkdir PHP/Timer


%build
phpab \
   --template fedora \
   --output  PHP/Timer/Autoload.php \
   PHP


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr PHP %{buildroot}%{php_home}


%if %{with_tests}
%check
mkdir vendor
touch vendor/autoload.php

: Run tests - set include_path to ensure PHPUnit autoloader use it
# remirepo:13
run=0
ret=0
if which php56; then
  php56 -d include_path=.:%{buildroot}%{php_home}:%{php_home} \
  %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
  php71 -d include_path=.:%{buildroot}%{php_home}:%{php_home} \
  %{_bindir}/phpunit6 || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/php -d include_path=.:%{buildroot}%{php_home}:%{php_home} \
%{_bindir}/phpunit --verbose
# remirepo:2
fi
exit $ret
%endif


%clean
rm -rf %{buildroot}


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%doc composer.json
%{php_home}/PHP


%changelog
* Sun Feb 26 2017 Remi Collet <remi@fedoraproject.org> - 1.0.9-1
- update to 1.0.9
- switch to fedora/autoloader

* Fri May 13 2016 Remi Collet <remi@fedoraproject.org> - 1.0.8-1
- update to 1.0.8
- run test with both PHP 5 and 7 when available

* Sun Jul 26 2015 Remi Collet <remi@fedoraproject.org> - 1.0.7-1
- update to 1.0.7 (only CS)

* Mon Jun 15 2015 Remi Collet <remi@fedoraproject.org> - 1.0.6-1
- update to 1.0.6
- generate autoloader, no more provided by upstream
- enable test suite during build
- add explicit spec license header

* Fri Jul 18 2014 Remi Collet <remi@fedoraproject.org> - 1.0.5-5
- add composer dependencies

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.0.5-3
- cleanup pear registry

* Wed Apr 23 2014 Remi Collet <remi@fedoraproject.org> - 1.0.5-2
- get sources from github
- run test suite when build --with tests

* Fri Aug 02 2013 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5

* Sat Oct  6 2012 Remi Collet <rpms@famillecollet.com> 1.0.4-1
- update to 1.0.4

* Mon Sep 24 2012 Remi Collet <rpms@famillecollet.com> 1.0.3-1
- update to 1.0.3

* Sun Oct 23 2011 Remi Collet <rpms@famillecollet.com> 1.0.2-1
- update to 1.0.2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Sep 26 2010 Christof Damian <christof@damian.net> - 1.0.0-2
- fix timezone warnings

* Thu Jul 15 2010 Christof Damian <christof@damian.net> - 1.0.0-1
- initial package
