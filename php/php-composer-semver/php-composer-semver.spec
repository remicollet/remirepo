# remirepo/fedora spec file for php-composer-semver
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    c7cb9a2095a074d131b65a8a0cd294479d785573
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
#global gh_date      20150717
%global gh_owner     composer
%global gh_project   semver
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-composer-semver
Version:        1.4.2
Release:        1%{?gh_date:.%{gh_date}git%{gh_short}}%{?dist}
Summary:        Semver library that offers utilities, version constraint parsing and validation

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
# git snapshot to get upstream test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh
Source2:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# For tests
BuildRequires:  php(language) >= 5.3.2
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-spl
# From composer.json,     "require-dev": {
#        "phpunit/phpunit": "^4.5 || ^5.0.5",
#        "phpunit/phpunit-mock-objects": "2.3.0 || ^3.0"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.5
BuildRequires:  php-composer(phpunit/phpunit-mock-objects) >= 2.3
# Autoloader
BuildRequires:  php-composer(symfony/class-loader)
%endif

# From composer.json, "require": {
#        "php": "^5.3.2 || ^7.0",
Requires:       php(language) >= 5.3.2
# From phpcompatinfo report for version 1.0.0 (SpdxLicenses.php only)
Requires:       php-pcre
Requires:       php-spl
# Autoloader
Requires:       php-composer(symfony/class-loader)

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Semver library that offers utilities, version constraint parsing
and validation.

Originally written as part of composer/composer, now extracted and
made available as a stand-alone library.

To use this library, you just have to add, in your project:
  require_once '%{_datadir}/php/Composer/Semver/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE2} src/autoload.php


%build
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

: Library
mkdir -p   %{buildroot}%{php_home}/Composer/
cp -pr src %{buildroot}%{php_home}/Composer/Semver


%check
%if %{with_tests}
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap %{buildroot}%{php_home}/Composer/Semver/autoload.php
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap %{buildroot}%{php_home}/Composer/Semver/autoload.php
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit \
    --bootstrap %{buildroot}%{php_home}/Composer/Semver/autoload.php \
    --verbose
# remirepo:2
fi
exit $ret
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json
%doc *.md
%dir %{php_home}/Composer
     %{php_home}/Composer/Semver


%changelog
* Thu Sep  1 2016 Remi Collet <remi@fedoraproject.org> - 1.4.2-1
- update to 1.4.2

* Thu Jun  2 2016 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- update to 1.4.1

* Wed Mar 30 2016 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- update to 1.4.0

* Fri Feb 26 2016 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- update to 1.3.0
- run test suite with both PHP 5 and 7 when available

* Tue Nov 10 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0

* Wed Nov  4 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0

* Sun Oct  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package, version 1.0.0
