# remirepo/fedora spec file for php-herrera-io-version
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    d39d9642b92a04d8b8a28b871b797a35a2545e85
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     kherge-abandoned
%global gh_project   php-version
%global php_home     %{_datadir}/php
%global ns_vendor    Herrera
%global ns_project   Version
%global c_vendor     herrera-io
%global c_project    version
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{c_vendor}-%{c_project}
Version:        1.1.1
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        A library for creating, editing, and comparing semantic versioning numbers

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

Source1:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-pcre
# From composer.json, "require-dev": {
#        "herrera-io/phpunit-test-case": "1.*",
#        "phpunit/phpunit": "3.7.*"
BuildRequires:  php-composer(%{c_vendor}/phpunit-test-case) >= 1
BuildRequires:  php-composer(phpunit/phpunit) >= 3.7
# Autoloader
BuildRequires:  php-composer(symfony/class-loader)
%endif

# from composer.json, "require": {
#        "php": ">=5.3.3",
Requires:       php(language) >= 5.3.3
# Autoloader
Requires:       php-composer(symfony/class-loader)
# from phpcompatinfo report for version 1.1.1
Requires:       php-pcre

Provides:       php-composer(%{c_vendor}/%{c_project}) = %{version}


%description
%{summary}.

Currently, v2.0.0 of the Semantic Versioning specification is supported.

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
mkdir src/vendors
cat << 'EOF' | tee src/vendors/autoload.php
<?php
// This library
require_once '%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';
// Dependencies
require_once '%{php_home}/%{ns_vendor}/PHPUnit/autoload.php';
EOF

%{_bindir}/phpunit --verbose
%else
: test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%doc composer.json
%dir %{php_home}/%{ns_vendor}
     %{php_home}/%{ns_vendor}/%{ns_project}


%changelog
* Wed Oct 21 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- initial package