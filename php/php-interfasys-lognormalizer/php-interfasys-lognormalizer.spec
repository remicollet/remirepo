# remirepo/fedora spec file for php-interfasys-lognormalizer
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    d5e4c95e0b0ecc886b78aafda3773b3bcf2ec116
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
#global gh_date      20150801
%global gh_owner     interfasys
%global gh_project   lognormalizer
%global with_tests   0%{!?_without_tests:1}
%global ns_vendor    InterfaSys
%global ns_project   LogNormalizer


Name:           php-%{gh_owner}-%{gh_project}
Version:        1.0
Release:        1%{?dist}
Summary:        Parses variables and converts them to string

Group:          Development/Libraries
License:        AGPLv3+
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-composer(theseer/autoload)
%if %{with_tests}
BuildRequires:  php(language) >= 5.4.0
BuildRequires:  php-date
BuildRequires:  php-intl
BuildRequires:  php-json
BuildRequires:  php-spl
# From composer.json, "require-dev": {
#    "phpunit/phpunit": "4.*",
#    "codeclimate/php-test-reporter": "dev-master",
#    "codacy/coverage": "dev-master"
BuildRequires:  php-composer(phpunit/phpunit) >= 4
%endif

# From composer.json, "require": {
#    "php": ">=5.4.0"
Requires:       php(language) >= 5.4.0
# From phpcompatinfo report for date 20150801
Requires:       php-json
Requires:       php-spl

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Parses variables and converts them to string so that they can be logged.

Based on the Monolog formatter/normalizer.

Autoloader: %{_datadir}/php/%{ns_vendor}/%{ns_project}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}



%build
%{_bindir}/phpab -o src/autoload.php src


%install
rm -rf     %{buildroot}

: Create a PSR-0 tree
mkdir -p   %{buildroot}%{_datadir}/php/%{ns_vendor}
cp -pr src %{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_project}


%check
%if %{with_tests}
: Run test suite with system PHP
%{_bindir}/phpunit \
    --bootstrap %{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_project}/autoload.php

if which php70; then
  : Run test suite with PHP 7.0 SCL
  php70 %{_bindir}/phpunit \
    --bootstrap %{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_project}/autoload.php
fi
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc *.md
%doc composer.json
%{_datadir}/php/%{ns_vendor}


%changelog
* Thu Jan 14 2016 Remi Collet <remi@fedoraproject.org> - 1.0-1
- version 1.0 (no change)

* Thu Jan 14 2016 Remi Collet <remi@fedoraproject.org> - 0-0.1.20150801gitd5e4c95
- initial package