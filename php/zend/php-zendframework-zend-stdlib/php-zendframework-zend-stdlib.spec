# remirepo/Fedora spec file for php-zendframework-zend-stdlib
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    0e44eb46788f65e09e077eb7f44d2659143bcc1f
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-stdlib
%global php_home     %{_datadir}/php
%global library      Stdlib
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.7.7
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
BuildRequires:  php-composer(%{gh_owner}/zend-hydrator)         >= 1.1
BuildRequires:  php-date
BuildRequires:  php-iconv
BuildRequires:  php-intl
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
BuildRequires:  php-reflection
BuildRequires:  php-spl
# From composer, "require-dev": {
#        "zendframework/zend-config": "~2.5",
#        "zendframework/zend-eventmanager": "~2.5",
#        "zendframework/zend-inputfilter": "~2.5",
#        "zendframework/zend-serializer": "~2.5",
#        "zendframework/zend-servicemanager": "~2.5",
#        "zendframework/zend-filter": "~2.5",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.0",
#        "athletic/athletic": "~0.1"
BuildRequires:  php-composer(%{gh_owner}/zend-config)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-eventmanager)     >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-inputfilter)      >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-serializer)       >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-filter)           >= 2.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "zendframework/zend-hydrator": "~1.1"
Requires:       php(language) >= 5.5
Requires:       php-composer(%{gh_owner}/zend-hydrator)         >= 1.1
Requires:       php-composer(%{gh_owner}/zend-hydrator)         <  2
%if ! %{bootstrap}
# From composer, "suggest": {
#        "zendframework/zend-eventmanager": "To support aggregate hydrator usage",
#        "zendframework/zend-serializer": "Zend\\Serializer component",
#        "zendframework/zend-servicemanager": "To support hydrator plugin manager usage",
#        "zendframework/zend-filter": "To support naming strategy hydrator usage"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-eventmanager)
Suggests:       php-composer(%{gh_owner}/zend-serializer)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
Suggests:       php-composer(%{gh_owner}/zend-filter)
%endif
%endif
# From phpcompatinfo report for version 2.7.4
Requires:       php-date
Requires:       php-iconv
Requires:       php-intl
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl
# Autoloader
Requires:       php-composer(%{gh_owner}/zend-loader)           >= 2.5

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Stdlib is a set of components that implements general purpose utility
class for different scopes like:
* array utilities functions;
* hydrators;
* json serializable interfaces;
* general messaging systems;
* string wrappers;
* etc.

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
* Wed Apr 13 2016 Remi Collet <remi@fedoraproject.org> - 2.7.7-1
- update to 2.7.7

* Fri Feb 19 2016 Remi Collet <remi@fedoraproject.org> - 2.7.6-1
- update to 2.7.6
- raise dependency on zendframework/zend-hydrator >= 1.1

* Tue Feb 16 2016 Remi Collet <remi@fedoraproject.org> - 2.7.5-1
- update to 2.7.5

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 2.7.4-1
- update to 2.7.4
- add dependency on zendframework/zend-hydrator ^1.0.0

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- initial package
