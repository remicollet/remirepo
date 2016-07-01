# remirepo/Fedora spec file for php-zendframework-zend-paginator
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    42211f3e1e8230953c641e91fec5aa9fe964eb95
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-paginator
%global php_home     %{_datadir}/php
%global library      Paginator
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.7.0
Release:        1%{?dist}
Summary:        Zend Framework %{library} component

Group:          Development/Libraries
License:        BSD
URL:            https://framework.zend.com/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
# From composer, "require-dev": {
#        "zendframework/zend-cache": "^2.6.1",
#        "zendframework/zend-config": "^2.6.0",
#        "zendframework/zend-db": "^2.7",
#        "zendframework/zend-filter": "^2.6.1",
#        "zendframework/zend-json": "^2.6.1",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3",
#        "zendframework/zend-view": "^2.6.3",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.0"
BuildRequires:  php-composer(%{gh_owner}/zend-cache)            >= 2.6.1
BuildRequires:  php-composer(%{gh_owner}/zend-config)           >= 2.6.0
BuildRequires:  php-composer(%{gh_owner}/zend-db)               >= 2.7
BuildRequires:  php-composer(%{gh_owner}/zend-filter)           >= 2.6.1
BuildRequires:  php-composer(%{gh_owner}/zend-json)             >= 2.6.1
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.7.5
BuildRequires:  php-composer(%{gh_owner}/zend-view)             >= 2.6.3
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
#        "zendframework/zend-cache": "Zend\\Cache component to support cache features",
#        "zendframework/zend-db": "Zend\\Db component",
#        "zendframework/zend-filter": "Zend\\Filter component",
#        "zendframework/zend-json": "Zend\\Json component",
#        "zendframework/zend-servicemanager": "Zend\\ServiceManager component",
#        "zendframework/zend-view": "Zend\\View component"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-cache)
Suggests:       php-composer(%{gh_owner}/zend-db)
Suggests:       php-composer(%{gh_owner}/zend-filter)
Suggests:       php-composer(%{gh_owner}/zend-json)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
Suggests:       php-composer(%{gh_owner}/zend-view)
%endif
%endif
# From phpcompatinfo report for version 2.5.1
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Paginator is a flexible component for paginating
collections of data and presenting that data to users.

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
* Tue Apr 12 2016 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- update to 2.7.0

* Wed Feb 24 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0
- raise dependency on PHP >= 5.5
- raise dependency on zend-stdlib >= 2.7

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
