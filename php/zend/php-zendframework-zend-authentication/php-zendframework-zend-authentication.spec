# remirepo/Fedora spec file for php-zendframework-zend-authentication
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    1422dec160eb769c719cad2229847fcbf20a1405
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-authentication
%global php_home     %{_datadir}/php
%global library      Authentication
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.5.3
Release:        1%{?dist}
Summary:        Zend Framework %{library} component

Group:          Development/Libraries
License:        BSD
URL:            http://framework.zend.com/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-ctype
BuildRequires:  php-date
BuildRequires:  php-hash
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
# From composer, "require-dev": {
#        "zendframework/zend-db": "^2.7",
#        "zendframework/zend-crypt": "^2.6",
#        "zendframework/zend-http": "^2.5.4",
#        "zendframework/zend-ldap": "^2.6",
#        "zendframework/zend-session": "^2.6.2",
#        "zendframework/zend-validator": "^2.6",
#        "zendframework/zend-uri": "^2.5",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.0"
BuildRequires:  php-composer(%{gh_owner}/zend-db)               >= 2.7
BuildRequires:  php-composer(%{gh_owner}/zend-crypt)            >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-http)             >= 2.5.4
BuildRequires:  php-composer(%{gh_owner}/zend-ldap)             >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-session)          >= 2.6.2
BuildRequires:  php-composer(%{gh_owner}/zend-validator)        >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-uri)              >= 2.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0"
Requires:       php(language) >= 5.5
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  4
# From composer, "suggest": {
#        "zendframework/zend-db": "Zend\\Db component",
#        "zendframework/zend-crypt": "Zend\\Crypt component",
#        "zendframework/zend-http": "Zend\\Http component",
#        "zendframework/zend-ldap": "Zend\\Ldap component",
#        "zendframework/zend-session": "Zend\\Session component",
#        "zendframework/zend-uri": "Zend\\Uri component",
#        "zendframework/zend-validator": "Zend\\Validator component"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-db)
Suggests:       php-composer(%{gh_owner}/zend-crypt)
Suggests:       php-composer(%{gh_owner}/zend-http)
Suggests:       php-composer(%{gh_owner}/zend-ldap)
Suggests:       php-composer(%{gh_owner}/zend-session)
Suggests:       php-composer(%{gh_owner}/zend-uri)
Suggests:       php-composer(%{gh_owner}/zend-validator)
%endif
%endif
# From phpcompatinfo report for version 2.5.2
Requires:       php-ctype
Requires:       php-date
Requires:       php-hash
Requires:       php-pcre
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
The Zend\Authentication component provides an API for authentication and
includes concrete authentication adapters for common use case scenarios.

Documentation: https://zendframework.github.io/%{gh_project}/


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/Zend/
cp -pr src %{buildroot}%{php_home}/Zend/%{library}


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\Loader\AutoloaderFactory::factory(array(
    'Zend\Loader\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendTest\\%{library}' => dirname(__DIR__).'/test/',
           'Zend\\%{library}'     => '%{buildroot}%{php_home}/Zend/%{library}'
))));
require_once '%{php_home}/Zend/autoload.php';
EOF

%{_bindir}/phpunit --include-path=%{buildroot}%{php_home}

if which php70; then
   php70 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home}
fi
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc CONTRIBUTING.md README.md
%doc composer.json
%{php_home}/Zend/%{library}


%changelog
* Sun Feb 28 2016 Remi Collet <remi@fedoraproject.org> - 2.5.3-1
- update to 2.5.3
- raise dependency on zend-stdlib ~2.7

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- initial package
