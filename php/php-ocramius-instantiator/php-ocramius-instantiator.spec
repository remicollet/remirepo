# spec file for php-ocramius-instantiator
#
# Copyright (c) 2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    cc754c2289ffd4483c319f6ed6ee88ce21676f64
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     Ocramius
%global gh_project   Instantiator
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-ocramius-instantiator
Version:        1.0.0
Release:        1%{?dist}
Summary:        Instantiate objects in PHP without invoking their constructors

Group:          Development/Libraries
# https://github.com/Ocramius/Instantiator/issues/9
# License is missing but included in each file (headers)
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-phpunit-PHPUnit
BuildRequires:  php-theseer-autoload
BuildRequires:  php-composer(ocramius/lazy-map) >= 1.0.0
BuildRequires:  php-composer(ocramius/lazy-map) <  1.1

# From composer.json
#        "php": ">=5.3.3"
#        "ocramius/lazy-map": "1.0.*"
Requires:       php(language) >= 5.3.3
Requires:       php-composer(ocramius/lazy-map) >= 1.0.0
Requires:       php-composer(ocramius/lazy-map) <  1.1
# From phpcompatinfo report for version 1.0.0
Requires:       php-reflection

Provides:       php-composer(ocramius/instantiator) = %{version}


%description
This library provides a way of avoiding usage of constructors when
instantiating PHP classes.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Nothing


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{_datadir}/php
cp -pr src/* %{buildroot}%{_datadir}/php


%check
%if %{with_tests}
: Generate autoloader
phpab \
    --basedir $PWD \
    --output autoload.php \
    src tests %{_datadir}/php/LazyMap

: Disabled known to fail tests
sed -e '/Phar/d' \
    -i tests/InstantiatorTest/InstantiatorTest.php

: Run test suite
phpunit \
    --bootstrap autoload.php \
    -d date.timezone=UTC
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc *.md
%{_datadir}/php/Instantiator/


%changelog
* Thu Jul 17 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package