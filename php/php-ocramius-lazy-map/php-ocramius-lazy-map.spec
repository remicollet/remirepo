# spec file for php-ocramius-lazy-map
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    7fe3d347f5e618bcea7d39345ff83f3651d8b752
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     Ocramius
%global gh_project   LazyMap
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-ocramius-lazy-map
Version:        1.0.0
Release:        1%{?dist}
Summary:        Lazy instantiation logic for a map of objects

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-phpunit-PHPUnit >= 3.7
BuildRequires:  php-theseer-autoload

# From composer.json
#      "php": ">=5.3.3"
Requires:       php(language) >= 5.3.3

Provides:       php-composer(ocramius/lazy-map) = %{version}


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