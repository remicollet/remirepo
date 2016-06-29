# remirepo/Fedora spec file for php-zendframework-zend-hydrator
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    0ac0d3e569781f1895670b0c8d0dc7f25b8a3182
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-hydrator
%global php_home     %{_datadir}/php
%global library      Hydrator
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.2.1
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
BuildRequires:  php-reflection
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 3.0
# From composer, "require-dev": {
#        "zendframework/zend-eventmanager": "^3.0",
#        "zendframework/zend-inputfilter": "^2.6",
#        "zendframework/zend-serializer": "^2.6.1",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3",
#        "zendframework/zend-filter": "^2.6",
#        "phpunit/phpunit": "^4.5",
#        "squizlabs/php_codesniffer": "^2.3.1"
BuildRequires:  php-composer(%{gh_owner}/zend-eventmanager)     >= 2.6.2
BuildRequires:  php-composer(%{gh_owner}/zend-inputfilter)      >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-serializer)       >= 2.6.1
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.7.5
BuildRequires:  php-composer(%{gh_owner}/zend-filter)           >= 2.6
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.5
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "zendframework/zend-stdlib": "^3.0"
Requires:       php(language) >= 5.5
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 3.0
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  4
# From composer, "suggest": {
#        "zendframework/zend-eventmanager": "^2.6.2 || ^3.0, to support aggregate hydrator usage",
#        "zendframework/zend-serializer": "^2.6.1, to use the SerializableStrategy",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3, to support hydrator plugin manager usage",
#        "zendframework/zend-filter": "^2.6, to support naming strategy hydrator usage"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-eventmanager)     >= 2.6.2
Suggests:       php-composer(%{gh_owner}/zend-serializer)       >= 2.6.1
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)   >= 2.7.5
Suggests:       php-composer(%{gh_owner}/zend-filter)           >= 2.6
%endif
# From phpcompatinfo report for version 1.1.0
Requires:       php-date
Requires:       php-reflection
Requires:       php-spl
# Autoloader
Requires:       php-composer(%{gh_owner}/zend-loader)           >= 2.5

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Hydrator provides utilities for mapping arrays to objects,
and vice versa, including facilities for filtering which data
is mapped as well as providing mechanisms for mapping nested
structures.

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

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home} || ret=1
   run=1
fi
if which php71; then
   php70 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home} || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --include-path=%{buildroot}%{php_home} --verbose
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
%doc CONTRIBUTING.md README.md
%doc composer.json
%{php_home}/Zend/%{library}


%changelog
* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- update to 2.2.1 for ZendFramework 3
- raise dependency on zend-stdlib >= 3.0

* Fri Feb 19 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0
- raise dependency on zend-stdlib >= 2.7

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- initial package
