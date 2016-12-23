# remirepo/fedora spec file for php-zendframework-zend-modulemanager
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    2a59ab9a0dd7699a55050dff659ab0f28272b46e
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-modulemanager
%global php_home     %{_datadir}/php
%global library      ModuleManager
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.7.2
Release:        1%{?dist}
Summary:        Zend Framework %{library} component

Group:          Development/Libraries
License:        BSD
URL:            https://zendframework.github.io/%{gh_project}/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-config)           >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-eventmanager)     >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
# From composer, "require-dev": {
#        "zendframework/zend-console": "^2.6",
#        "zendframework/zend-di": "^2.6",
#        "zendframework/zend-loader": "^2.5",
#        "zendframework/zend-mvc": "^2.7",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.0"
BuildRequires:  php-composer(%{gh_owner}/zend-console)          >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-di)               >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-mvc)              >= 2.7
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.7.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
# Because of bootstrap
BuildRequires:  php-composer(%{gh_owner}/zend-code)             >= 2.5
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "zendframework/zend-config": "^2.6",
#        "zendframework/zend-eventmanager": "^2.6.2 || ^3.0",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0"
Requires:       php(language) >= 5.5
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-config)           >= 2.6
Requires:       php-composer(%{gh_owner}/zend-config)           <  3
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     >= 2.6.2
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     <  4
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  4
# From composer, "suggest": {
#        "zendframework/zend-config": "Zend\\Config component",
#        "zendframework/zend-console": "Zend\\Console component",
#        "zendframework/zend-loader": "Zend\\Loader component",
#        "zendframework/zend-mvc": "Zend\\Mvc component",
#        "zendframework/zend-servicemanager": "Zend\\ServiceManager component"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-console)
Suggests:       php-composer(%{gh_owner}/zend-loader)
Suggests:       php-composer(%{gh_owner}/zend-mvc)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
%endif
%endif
# From phpcompatinfo report for version 2.6.1
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend Framework 2.0 introduces a new and powerful approach to modules.
This new module system is designed with flexibility, simplicity, and
re-usability in mind. A module may contain just about anything:
PHP code, including MVC functionality; library code; view scripts;
and/or public assets such as images, CSS, and JavaScript.
The possibilities are endless.

Zend\ModuleManager is the component that enables the design of a module architecture for PHP applcations.

Documentation: https://zendframework.github.io/%{gh_project}/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv LICENSE.md LICENSE


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
%license LICENSE
%doc *.md
%doc composer.json
%{php_home}/Zend/%{library}


%changelog
* Tue May 17 2016 Remi Collet <remi@fedoraproject.org> - 2.7.2-1
- update to 2.7.2
- zend-config is now required

* Sun Feb 28 2016 Remi Collet <remi@fedoraproject.org> - 2.7.1-1
- update to 2.7.1
- https://github.com/zendframework/zend-modulemanager/pull/33

* Fri Feb 26 2016 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- update to 2.7.0
- raise dependency on zend-eventmanager >= 2.6.2

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 2.6.1-1
- update to 2.6.1
- raise dependency on zend-stdlib ~2.7

* Thu Sep 10 2015 Remi Collet <remi@fedoraproject.org> - 2.5.3-1
- update to 2.5.3
- raise minimum php version to 5.5

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
