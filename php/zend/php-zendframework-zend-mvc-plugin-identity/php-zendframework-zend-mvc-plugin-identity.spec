# remirepo/Fedora spec file for php-zendframework-zend-mvc-plugin-identity
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    7677ef175e4ce5e15dbe0c1cd520bbe381a31460
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-mvc-plugin-identity
%global php_home     %{_datadir}/php
%global library      Identity
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.0.0
Release:        1%{?dist}
Summary:        Zend Framework Mvc-Plugin-%{library} component

Group:          Development/Libraries
License:        BSD
URL:            https://zendframework.github.io/%{gh_project}/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-composer(container-interop/container-interop) >= 1.1
BuildRequires:  php-composer(%{gh_owner}/zend-mvc)                >= 3.0
BuildRequires:  php-composer(%{gh_owner}/zend-authentication)     >= 2.5.3
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)     >= 2.7.5
BuildRequires:  php-spl
# From composer, "require-dev": {
#        "phpunit/PHPUnit": "^4.5",
#        "squizlabs/php_codesniffer": "^2.3.1"
BuildRequires:  php-composer(phpunit/phpunit)                     >= 4.5
BuildRequires:  php-composer(%{gh_owner}/zend-filter)             >= 2.6.1
BuildRequires:  php-composer(%{gh_owner}/zend-form)               >= 2.7
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
# For dependencies autoloader
BuildRequires:  php-zendframework-zend-loader                   >= 2.5.1-3
%endif

# From composer, "require": {
#        "php": "^5.6 || ^7.0",
#        "container-interop/container-interop": "^1.1",
#        "zendframework/zend-mvc": "^3.0",
#        "zendframework/zend-authentication": "^2.5.3",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3"
Requires:       php(language) >= 5.6
Requires:       php-composer(container-interop/container-interop) >= 1.1
Requires:       php-composer(container-interop/container-interop) <  2
Requires:       php-composer(%{gh_owner}/zend-mvc)                >= 3.0
Requires:       php-composer(%{gh_owner}/zend-mvc)                <  4
Requires:       php-composer(%{gh_owner}/zend-authentication)     >= 2.5.3
Requires:       php-composer(%{gh_owner}/zend-authentication)     <  3
Requires:       php-composer(%{gh_owner}/zend-servicemanager)     >= 2.7.5
Requires:       php-composer(%{gh_owner}/zend-servicemanager)     <  4
# From phpcompatinfo report for version 1.0.0
Requires:       php-spl
%if ! %{bootstrap}
# Autoloader
Requires:       php-composer(%{gh_owner}/zend-loader)             >= 2.5
Requires:       php-zendframework-zend-loader                     >= 2.5.1-3
%endif

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Provides a zend-mvc plugin (for versions 3.0 and up) that allows retrieving
the current identity as provided by zend-authentication.

* Issues at https://github.com/zendframework/zend-mvc-plugin-identity/issues
* Documentation is at https://zendframework.github.io/zend-mvc-plugin-identity/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv LICENSE.md LICENSE

: Create dependency autoloader
cat << 'EOF' | tee autoload.php
<?php
require_once '%{php_home}/Interop/Container/autoload.php';
EOF


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/Zend/Mvc/Plugin
cp -pr src %{buildroot}%{php_home}/Zend/Mvc/Plugin/%{library}

install -m644 autoload.php %{buildroot}%{php_home}/Zend/Mvc-Plugin-%{library}-autoload.php


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\Loader\AutoloaderFactory::factory(array(
    'Zend\Loader\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendTest\\Mvc\\Plugin\\%{library}' => dirname(__DIR__).'/test/',
           'Zend\\Mvc\\Plugin\\%{library}'     => '%{buildroot}%{php_home}/Zend/Mvc/Plugin/%{library}'
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
%license LICENSE
%doc *.md
%doc composer.json
%{php_home}/Zend/Mvc/Plugin/%{library}
%{php_home}/Zend/Mvc-Plugin-%{library}-autoload.php


%changelog
* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package

