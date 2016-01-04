# remirepo/Fedora spec file for php-zendframework-zend-view
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    b3d31e7ba6d0c13a76afe5c8d914a8ff08616b0d
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-view
%global php_home     %{_datadir}/php
%global library      View
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
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-date
BuildRequires:  php-dom
BuildRequires:  php-filter
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-eventmanager)     >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
# From composer, "require-dev": {
#        "zendframework/zend-authentication": "~2.5",
#        "zendframework/zend-cache": "~2.5",
#        "zendframework/zend-config": "~2.5",
#        "zendframework/zend-console": "~2.5",
#        "zendframework/zend-escaper": "~2.5",
#        "zendframework/zend-feed": "~2.5",
#        "zendframework/zend-filter": "~2.5",
#        "zendframework/zend-http": "~2.5",
#        "zendframework/zend-i18n": "~2.5",
#        "zendframework/zend-json": "~2.5",
#        "zendframework/zend-log": "~2.5",
#        "zendframework/zend-modulemanager": "~2.5",
#        "zendframework/zend-mvc": "~2.5",
#        "zendframework/zend-navigation": "~2.5",
#        "zendframework/zend-paginator": "~2.5",
#        "zendframework/zend-permissions-acl": "~2.5",
#        "zendframework/zend-serializer": "~2.5",
#        "zendframework/zend-servicemanager": "~2.5",
#        "zendframework/zend-session": "dev-master",
#        "zendframework/zend-uri": "~2.5",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.0"
BuildRequires:  php-composer(%{gh_owner}/zend-authentication)   >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-cache)            >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-config)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-console)          >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-escaper)          >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-feed)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-filter)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-http)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-i18n)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-json)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-log)              >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-modulemanager)    >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-mvc)              >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-navigation)       >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-paginator)        >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-permissions-acl)  >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-serializer)       >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-session)          >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-uri)              >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-eventmanager)     >= 2.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": ">=5.5",
#        "zendframework/zend-eventmanager": "~2.5",
#        "zendframework/zend-loader": "~2.5",
#        "zendframework/zend-stdlib": "~2.5"
Requires:       php(language) >= 5.5
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     >= 2.5
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     <  3
Requires:       php-composer(%{gh_owner}/zend-loader)           >= 2.5
Requires:       php-composer(%{gh_owner}/zend-loader)           <  3
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  3
# From composer, "suggest": {
#        "zendframework/zend-authentication": "Zend\\Authentication component",
#        "zendframework/zend-escaper": "Zend\\Escaper component",
#        "zendframework/zend-feed": "Zend\\Feed component",
#        "zendframework/zend-filter": "Zend\\Filter component",
#        "zendframework/zend-http": "Zend\\Http component",
#        "zendframework/zend-i18n": "Zend\\I18n component",
#        "zendframework/zend-json": "Zend\\Json component",
#        "zendframework/zend-mvc": "Zend\\Mvc component",
#        "zendframework/zend-navigation": "Zend\\Navigation component",
#        "zendframework/zend-paginator": "Zend\\Paginator component",
#        "zendframework/zend-permissions-acl": "Zend\\Permissions\\Acl component",
#        "zendframework/zend-servicemanager": "Zend\\ServiceManager component",
#        "zendframework/zend-uri": "Zend\\Uri component"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-authentication)
Suggests:       php-composer(%{gh_owner}/zend-escaper)
Suggests:       php-composer(%{gh_owner}/zend-feed)
Suggests:       php-composer(%{gh_owner}/zend-filter)
Suggests:       php-composer(%{gh_owner}/zend-http)
Suggests:       php-composer(%{gh_owner}/zend-i18n)
Suggests:       php-composer(%{gh_owner}/zend-json)
Suggests:       php-composer(%{gh_owner}/zend-mvc)
Suggests:       php-composer(%{gh_owner}/zend-navigation)
Suggests:       php-composer(%{gh_owner}/zend-paginator)
Suggests:       php-composer(%{gh_owner}/zend-permissions-acl)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
Suggests:       php-composer(%{gh_owner}/zend-uri)
%endif
%endif
# From phpcompatinfo report for version 2.5.2
Requires:       php-date
Requires:       php-dom
Requires:       php-filter
Requires:       php-pcre
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\View provides the “View” layer of Zend Framework 2’s MVC system.
It is a multi-tiered system allowing a variety of mechanisms for extension,
substitution, and more.


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
* Thu Aug  6 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- version 2.5.2

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package