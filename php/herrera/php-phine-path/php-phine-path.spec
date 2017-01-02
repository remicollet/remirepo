# remirepo/fedora spec file for php-phine-path
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    cbe1a5eb6cf22958394db2469af9b773508abddd
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     box-project
%global gh_project   box2-path
%global php_home     %{_datadir}/php
%global ns_vendor    Phine
%global ns_project   Path
%global c_vendor     phine
%global c_project    path
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{c_vendor}-%{c_project}
Version:        1.1.0
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        A PHP library for improving the use of file system paths

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

Source1:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-filter
BuildRequires:  php-pcre
BuildRequires:  php-composer(%{c_vendor}/exception) >= 1.0
# From composer.json, "require-dev": {
#        "league/phpunit-coverage-listener": "~1.0"
BuildRequires:  php-composer(phpunit/phpunit)
# Autoloader
BuildRequires:  php-composer(symfony/class-loader)
%endif

# from composer.json, "require": {
#        "php": ">=5.3.3",
#        "phine/exception": "~1.0"
Requires:       php(language) >= 5.3.3
Requires:       php-composer(%{c_vendor}/exception) >= 1.0
Requires:       php-composer(%{c_vendor}/exception) <  2
# Autoloader
Requires:       php-composer(symfony/class-loader)
# from phpcompatinfo report for version 1.1.0
Requires:       php-filter
Requires:       php-pcre

Provides:       php-composer(%{c_vendor}/%{c_project}) = %{version}


%description
This library provides a utility methods for file system paths.

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE1} src/lib/%{ns_vendor}/%{ns_project}/autoload.php


%build
# Empty


%install
rm -rf                      %{buildroot}
mkdir -p                    %{buildroot}%{php_home}
cp -pr src/lib/%{ns_vendor} %{buildroot}%{php_home}/%{ns_vendor}


%check
%if %{with_tests}
%{_bindir}/phpunit \
   --bootstrap %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php \
   --no-configuration \
   --verbose \
   src/tests
%else
: test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{php_home}/%{ns_vendor}/%{ns_project}


%changelog
* Tue Oct 27 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- initial package