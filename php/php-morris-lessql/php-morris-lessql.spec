# remirepo/fedora spec file for php-morris-lessql
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    ff6c631e3abf1d3ee618f5262be4cc6ed09f6957
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     morris
#global gh_date      20150820
%global gh_project   lessql
%global with_tests   0%{!?_without_tests:1}
%global psr0         LessQL

Name:           php-%{gh_owner}-%{gh_project}
Version:        0.3.4
Release:        1%{?gh_date?%{gh_date}git%{gh_short}}%{?dist}
Summary:        The agile PHP ORM alternative

Group:          Development/Libraries
License:        MIT
URL:            http://lessql.net/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{?gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.4
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-spl
# For tests, from composer.json 	"require-dev": {
#		"phpunit/phpunit": "~4.6",
#		"codeclimate/php-test-reporter": "dev-master"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.6
BuildRequires:  php-pdo
BuildRequires:  php-date
%endif
# For autoloader
BuildRequires:  php-composer(theseer/autoload)

# From composer.json, 	"require": {
#		"php": ">=5.3.4"
Requires:       php(language) >= 5.3.4
# From phpcompatinfo report for 0.3.4
Requires:       php-json
Requires:       php-pcre
Requires:       php-spl

# Composer
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
LessQL is a lightweight and performant alternative to Object-Relational
Mapping for PHP.

Autoloader: %{_datadir}/php/%{psr0}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: generate an simple autoloader
%{_bindir}/phpab --output src/%{psr0}/autoload.php src/%{psr0}


%install
rm -rf     %{buildroot}

: Library
mkdir -p           %{buildroot}%{_datadir}/php
cp -pr src/%{psr0} %{buildroot}%{_datadir}/php/%{psr0}


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require '%{buildroot}%{_datadir}/php/%{psr0}/autoload.php';
EOF

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --no-coverage tests || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --no-coverage tests || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose tests
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
%license LICENSE.md
%doc composer.json
%doc CHANGELOG.md
%doc README.md
%{_datadir}/php/%{psr0}


%changelog
* Tue Sep 27 2016 Remi Collet <remi@fedoraproject.org> - 0.3.4-1
- initial package

