# remirepo/Fedora spec file for php-zendframework-zend-feed
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    0661345b82b51428619e05d3aadd3de65b57fa54
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-feed
%global php_home     %{_datadir}/php
%global library      Feed
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.5.2
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
BuildRequires:  php(language) >= 5.3.23
BuildRequires:  php-ctype
BuildRequires:  php-date
BuildRequires:  php-dom
BuildRequires:  php-hash
BuildRequires:  php-libxml
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-tidy
BuildRequires:  php-composer(%{gh_owner}/zend-escaper)          >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
# From composer, "require-dev": {
#        "zendframework/zend-db": "~2.5",
#        "zendframework/zend-cache": "~2.5",
#        "zendframework/zend-http": "~2.5",
#        "zendframework/zend-servicemanager": "~2.5",
#        "zendframework/zend-validator": "~2.5",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.0"
BuildRequires:  php-composer(%{gh_owner}/zend-db)               >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-cache)            >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-http)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-validator)        >= 2.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
# Because of boostraped Db
BuildRequires:  php-composer(%{gh_owner}/zend-eventmanager)   >= 2.5
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": ">=5.3.23",
#        "zendframework/zend-escaper": "~2.5",
#        "zendframework/zend-stdlib": "~2.5"
Requires:       php(language) >= 5.3.23
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-escaper)          >= 2.5
Requires:       php-composer(%{gh_owner}/zend-escaper)          <  3
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  3
# From composer, "suggest": {
#        "zendframework/zend-cache": "Zend\\Cache component",
#        "zendframework/zend-db": "Zend\\Db component",
#        "zendframework/zend-http": "Zend\\Http for PubSubHubbub, and optionally for use with Zend\\Feed\\Reader",
#        "zendframework/zend-servicemanager": "Zend\\ServiceManager component, for default/recommended ExtensionManager implementations",
#        "zendframework/zend-validator": "Zend\\Validator component"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-cache)
Suggests:       php-composer(%{gh_owner}/zend-db)
Suggests:       php-composer(%{gh_owner}/zend-http)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
Suggests:       php-composer(%{gh_owner}/zend-validator)
%endif
%endif
# From phpcompatinfo report for version 2.5.2
Requires:       php-ctype
Requires:       php-date
Requires:       php-dom
Requires:       php-hash
Requires:       php-libxml
Requires:       php-pcre
Requires:       php-spl
Requires:       php-tidy

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Feed provides functionality for consuming RSS and Atom feeds.
It provides a natural syntax for accessing elements of feeds, feed attributes,
and entry attributes. Zend\Feed also has extensive support for modifying feed
and entry structure with the same natural syntax, and turning the result back
into XML.


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
cat << EOF | tee vendor/autoload.php
<?php
require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\\Loader\\AutoloaderFactory::factory(array(
    'Zend\\Loader\\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendTest\\\\%{library}' => dirname(__DIR__).'/test/',
           'Zend\\\\%{library}'     => '%{buildroot}%{php_home}/Zend/%{library}'
))));
require_once '%{php_home}/Zend/autoload.php';
EOF
%if 0%{?rhel} == 5
# sqlite is too old
rm test/PubSubHubbub/Model/SubscriptionTest.php
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
* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- initial package