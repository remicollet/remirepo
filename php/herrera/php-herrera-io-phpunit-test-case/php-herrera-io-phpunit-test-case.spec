# remirepo/fedora spec file for php-herrera-io-phpunit-test-case
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    a86781b70271b01eee792f4ab9864b0dfbab80ca
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     kherge-abandoned
%global gh_project   php-phpunit-testcase
%global php_home     %{_datadir}/php
%global ns_vendor    Herrera
%global ns_project   PHPUnit
%global c_vendor     herrera-io
%global c_project    phpunit-test-case
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{c_vendor}-%{c_project}
Version:        1.2.1
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        PHPUnit test case class with additional functionality

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

Source1:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
%if %{with_tests}
BuildRequires:  php-composer(phpunit/phpunit) >= 3.7
BuildRequires:  php-composer(symfony/process)
BuildRequires:  php-composer(symfony/class-loader)
%endif

# from composer.json, "require": {
#        "php": ">=5.3.3",
#        "phpunit/phpunit": "3.7.*"
Requires:       php(language) >= 5.3.3
Requires:       php-composer(phpunit/phpunit) >= 3.7
# from composer.json, "suggest": {
#        "symfony/process": "To run command line applications."
Requires:       php-composer(symfony/process)
# Autoloader
Requires:       php-composer(symfony/class-loader)
# from phpcompatinfo report for version 1.2.1
Requires:       php-reflection
Requires:       php-spl

Provides:       php-composer(%{c_vendor}/%{c_project}) = %{version}


%description
%{summary}.

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
   --verbose
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
* Wed Oct 21 2015 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- initial package