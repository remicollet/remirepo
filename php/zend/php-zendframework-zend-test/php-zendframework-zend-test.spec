# remirepo spec/Fedora file for php-zendframework-zend-test
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    da3b3b2a70385c11a382477b18d68cb3f16624ea
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-test
%global php_home     %{_datadir}/php
%global library      Test
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.5.1
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
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
BuildRequires:  php-pcre
BuildRequires:  php-composer(%{gh_owner}/zend-console)          >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-dom)              >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-eventmanager)     >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-http)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-mvc)              >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-uri)              >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-view)             >= 2.5
# From composer, "require-dev": {
#        "fabpot/php-cs-fixer": "1.7.*",
#        "mikey179/vfsStream": "~1.2",
#        "zendframework/zend-i18n": "~2.5",
#        "zendframework/zend-log": "~2.5",
#        "zendframework/zend-modulemanager": "~2.5",
#        "zendframework/zend-serializer": "~2.5",
#        "zendframework/zend-session": "~2.5"
BuildRequires:  php-composer(mikey179/vfsStream)                >= 1.2
BuildRequires:  php-composer(%{gh_owner}/zend-i18n)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-log)              >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-modulemanager)    >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-serializer)       >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-session)          >= 2.5
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": ">=5.3.23",
#        "phpunit/PHPUnit": "~4.0",
#        "zendframework/zend-console": "~2.5",
#        "zendframework/zend-dom": "~2.5",
#        "zendframework/zend-eventmanager": "~2.5",
#        "zendframework/zend-http": "~2.5",
#        "zendframework/zend-mvc": "~2.5",
#        "zendframework/zend-servicemanager": "~2.5",
#        "zendframework/zend-stdlib": "~2.5",
#        "zendframework/zend-uri": "~2.5",
#        "zendframework/zend-view": "~2.5"
Requires:       php(language) >= 5.3.23
Requires:       php-composer(phpunit/phpunit)                   >= 4.0
Requires:       php-composer(phpunit/phpunit)                   <  5
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-console)          >= 2.5
Requires:       php-composer(%{gh_owner}/zend-console)          <  3
Requires:       php-composer(%{gh_owner}/zend-dom)              >= 2.5
Requires:       php-composer(%{gh_owner}/zend-dom)              <  3
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     >= 2.5
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     <  3
Requires:       php-composer(%{gh_owner}/zend-http)             >= 2.5
Requires:       php-composer(%{gh_owner}/zend-http)             <  3
Requires:       php-composer(%{gh_owner}/zend-mvc)              >= 2.5
Requires:       php-composer(%{gh_owner}/zend-mvc)              <  3
Requires:       php-composer(%{gh_owner}/zend-servicemanager)   >= 2.5
Requires:       php-composer(%{gh_owner}/zend-servicemanager)   <  3
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  3
Requires:       php-composer(%{gh_owner}/zend-uri)              >= 2.5
Requires:       php-composer(%{gh_owner}/zend-uri)              <  3
Requires:       php-composer(%{gh_owner}/zend-view)             >= 2.5
Requires:       php-composer(%{gh_owner}/zend-view)             <  3
# From composer, "suggest": {
#        "zendframework/zend-console": "Zend\\Console component"
%if 0%{?fedora} >= 21
# https://github.com/zendframework/zend-test/pull/2
%endif
%endif
# From phpcompatinfo report for version 2.5.1
Requires:       php-pcre

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
The Zend\Test component provides tools to facilitate unit testing of your
Zend Framework applications. At this time, we offer facilities to enable
testing of your Zend Framework MVC applications.

PHPUnit is the only library supported currently.


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
%{_bindir}/phpunit --include-path=%{buildroot}%{php_home}
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
* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package