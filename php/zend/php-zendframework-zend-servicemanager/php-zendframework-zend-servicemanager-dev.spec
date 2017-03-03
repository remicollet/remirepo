# remirepo/Fedora spec file for php-zendframework-zend-servicemanager
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    2ae3b6e4978ec2e9ff52352e661946714ed989f9
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-servicemanager
%global php_home     %{_datadir}/php
%global library      ServiceManager
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.7.8
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
BuildRequires:  php-composer(container-interop/container-interop) >= 1.0
BuildRequires:  php-spl
# From composer, "require-dev": {
#        "zendframework/zend-di": "~2.5",
#        "zendframework/zend-mvc": "~2.5",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.0",
#        "athletic/athletic": "dev-master"
BuildRequires:  php-composer(%{gh_owner}/zend-di)               >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-mvc)              >= 2.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
# Because of bootstrap
BuildRequires:  php-composer(%{gh_owner}/zend-code)             >= 2.5
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0"
#        "container-interop/container-interop": "~1.0"
Requires:       php(language) >= 5.5
Requires:       php-composer(container-interop/container-interop) >= 1.0
Requires:       php-composer(container-interop/container-interop) <  2
# From phpcompatinfo report for version 2.7.4
Requires:       php-spl
%if ! %{bootstrap}
# From composer, "suggest": {
#        "ocramius/proxy-manager": "ProxyManager 0.5.* to handle lazy initialization of services",
#        "zendframework/zend-di": "Zend\\Di component"
%if 0%{?fedora} >= 21
Suggests:       php-composer(ocramius/proxy-manager)
Suggests:       php-composer(%{gh_owner}/zend-di)
%endif
# Autoloader
Requires:       php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
The Service Locator design pattern is implemented by the Zend\ServiceManager
component. The Service Locator is a service/object locator, tasked with
retrieving other objects.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

# NOTICE container-interop/container-interop is PSR-0
# so will be managed by the fallback_autoloader option


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
* Fri Mar  3 2017 Remi Collet <remi@remirepo.net> - 2.7.8-1
- Update to 2.7.8

* Thu Apr 28 2016 Remi Collet <remi@fedoraproject.org> - 2.7.6-1
- update to 2.7.6

* Tue Feb  2 2016 Remi Collet <remi@fedoraproject.org> - 2.7.5-1
- update to 2.7.5

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 2.7.4-2
- update to 2.7.4
- raise minimal php version to 5.5
- add dependency on container-interop/container-interop ~1.0

* Thu Aug  6 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-2
- fix description

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
