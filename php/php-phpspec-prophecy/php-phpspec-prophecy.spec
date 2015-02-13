# spec file for php-phpspec-prophecy
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    9ca52329bcdd1500de24427542577ebf3fc2f1c9
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     phpspec
%global gh_project   prophecy
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-phpspec-prophecy
Version:        1.3.1
Release:        1%{?dist}
Summary:        Highly opinionated mocking framework for PHP 5.3+

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-theseer-autoload

# From composer.json
#        "phpdocumentor/reflection-docblock": "~2.0",
#        "doctrine/instantiator":             "~1.0,>=1.0.2"
Requires:       php(language) >= 5.3.3
Provides:       php-composer(phpdocumentor/reflection-docblock) >= 2.0
Provides:       php-composer(phpdocumentor/reflection-docblock) <  3
Provides:       php-composer(doctrine/instantiator) >= 1.0.2
Provides:       php-composer(doctrine/instantiator) <  2

Provides:       php-composer(phpspec/prophecy) = %{version}


%description
This small library aims at providing a very simple and efficient map
of lazy-instantiating objects.


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
    src tests

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
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%{_datadir}/php/LazyMap/


%changelog
* Thu Jul 17 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package