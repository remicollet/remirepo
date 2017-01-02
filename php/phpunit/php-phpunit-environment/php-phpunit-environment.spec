# remirepo/fedora spec file for php-phpunit-environment
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    5795ffe5dc5b02460c3e34222fee8cbe245d8fac
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   environment
%global php_home     %{_datadir}/php
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-phpunit-environment
Version:        2.0.0
Release:        1%{?dist}
Summary:        Handle HHVM/PHP environments

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-fedora-autoloader-devel
%if %{with_tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "^5.0"
BuildRequires:  php-composer(phpunit/phpunit) >= 5.0
%endif

# from composer.json, "require": {
#        "php": "^5.6 || ^7.0"
Requires:       php(language) >= 5.6
# From phpcompatinfo report for 2.0.0
Requires:       php-pcre
Requires:       php-posix
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(sebastian/environment) = %{version}


%description
This component provides functionality that helps writing PHP code that
has runtime-specific (PHP / HHVM) execution paths.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

# Restore PSR-0 tree
mkdir  SebastianBergmann
mv src SebastianBergmann/Environment


%build
# Generate the Autoloader
%{_bindir}/phpab \
   --template fedora \
   --output SebastianBergmann/Environment/autoload.php \
   SebastianBergmann/Environment


%install
rm -rf   %{buildroot}
mkdir -p %{buildroot}%{php_home}/SebastianBergmann
cp -pr                           SebastianBergmann/Environment \
         %{buildroot}%{php_home}/SebastianBergmann/Environment


%if %{with_tests}
%check
: Run tests - set include_path to ensure PHPUnit autoloader use it
# remirepo:13
run=0
ret=0
if which php56; then
   php56 -d include_path=.:%{buildroot}%{php_home}:%{php_home} \
   %{_bindir}/phpunit --bootstrap %{buildroot}%{php_home}/SebastianBergmann/Environment/autoload.php
   run=1
fi
if which php71; then
   php71 -d include_path=.:%{buildroot}%{php_home}:%{php_home} \
   %{_bindir}/phpunit --bootstrap %{buildroot}%{php_home}/SebastianBergmann/Environment/autoload.php
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/php -d include_path=.:%{buildroot}%{php_home}:%{php_home} \
%{_bindir}/phpunit --bootstrap %{buildroot}%{php_home}/SebastianBergmann/Environment/autoload.php
# remirepo:2
fi
exit $ret
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md composer.json
%dir %{php_home}/SebastianBergmann
     %{php_home}/SebastianBergmann/Environment


%changelog
* Sat Nov 26 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0
- raise dependency on PHP 5.6
- switch to fedora/autoloader

* Wed Aug 31 2016 Remi Collet <remi@fedoraproject.org> - 1.3.8-1
- update to 1.3.8

* Tue May 17 2016 Remi Collet <remi@fedoraproject.org> - 1.3.7-1
- update to 1.3.7
- add explicit dependencies on pcre and posix

* Wed May  4 2016 Remi Collet <remi@fedoraproject.org> - 1.3.6-1
- update to 1.3.6

* Sun Feb 28 2016 Remi Collet <remi@fedoraproject.org> - 1.3.5-1
- update to 1.3.5

* Wed Dec  2 2015 Remi Collet <remi@fedoraproject.org> - 1.3.3-1
- update to 1.3.3 (no change on linux)
- run test suite with both php 5 and 7 when available

* Mon Aug  3 2015 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- update to 1.3.2

* Sun Aug  2 2015 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- update to 1.3.1

* Sun Jul 26 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- update to 1.3.0

* Fri Apr  3 2015 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- update to 1.2.2
- fix license handling

* Tue Dec  2 2014 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- update to 1.2.1

* Sat Oct 25 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0

* Wed Oct  8 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0

* Sun Oct  5 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- enable test suite

* Wed Jun 25 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-4
- composer dependencies

* Wed Apr 23 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- add generated autoload.php

* Tue Apr  1 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
