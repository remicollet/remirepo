# remirepo/Fedora spec file for php-zendframework-zend-session
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    79002c7b3e83477217121936c2577526f15555b1
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-session
%global php_home     %{_datadir}/php
%global library      Session
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.7.1
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
BuildRequires:  php-date
BuildRequires:  php-hash
BuildRequires:  php-pcre
BuildRequires:  php-session
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-eventmanager)     >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
# From composer, "require-dev": {
#        "zendframework/zend-cache": "^2.6.1",
#        "zendframework/zend-db": "^2.7",
#        "zendframework/zend-http": "^2.5.4",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3",
#        "zendframework/zend-validator": "^2.6",
#        "container-interop/container-interop": "^1.1",
#        "mongodb/mongodb": "^1.0.1",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.0"
BuildRequires:  php-composer(%{gh_owner}/zend-cache)            >= 2.6.1
BuildRequires:  php-composer(%{gh_owner}/zend-db)               >= 2.7
BuildRequires:  php-composer(%{gh_owner}/zend-http)             >= 2.5.4
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.7.5
BuildRequires:  php-composer(%{gh_owner}/zend-validator)        >= 2.6
BuildRequires:  php-composer(container-interop/container-interop) >= 1.1
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "zendframework/zend-eventmanager": "^2.6.2 || ^3.0",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0"
Requires:       php(language) >= 5.5
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     >= 2.6.2
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     <  4
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  4
# From composer, "suggest": {
#        "zendframework/zend-cache": "Zend\\Cache component",
#        "zendframework/zend-db": "Zend\\Db component",
#        "zendframework/zend-http": "Zend\\Http component",
#        "zendframework/zend-servicemanager": "Zend\\ServiceManager component",
#        "zendframework/zend-validator": "Zend\\Validator component"
#        "zendframework/zend-validator": "Zend\\Validator component",
#        "mongodb/mongodb": "If you want to use the MongoDB session save handler"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-cache)
Suggests:       php-composer(%{gh_owner}/zend-db)
Suggests:       php-composer(%{gh_owner}/zend-http)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
Suggests:       php-composer(%{gh_owner}/zend-validator)
Suggests:       php-composer(mongodb/mongodb)
%endif
%endif
# From phpcompatinfo report for version 2.5.2
Requires:       php-date
Requires:       php-hash
Requires:       php-pcre
Requires:       php-session
Requires:       php-spl
# Mongo is optional

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Session is a component to manage PHP session using an object
oriented interface.


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
# this test requires a running MongoDB server
rm test/SaveHandler/MongoDBTest.php

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
%if 0%{?rhel} == 5
# sqlite is too old
rm test/SaveHandler/DbTableGatewayTest.php
%endif

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
* Wed May 11 2016 Remi Collet <remi@fedoraproject.org> - 2.7.1-1
- update to 2.7.1

* Tue Apr 12 2016 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- update to 2.7.0
- add optional dependency on mongodb/mongodb

* Fri Feb 26 2016 Remi Collet <remi@fedoraproject.org> - 2.6.2-1
- update to 2.6.2

* Wed Feb 24 2016 Remi Collet <remi@fedoraproject.org> - 2.6.1-1
- update to 2.6.1

* Tue Feb 23 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0
- raise dependency on zend-eventmanager >= 2.6.2
- raise dependency on zend-stdlib >= 2.7

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- initial package
