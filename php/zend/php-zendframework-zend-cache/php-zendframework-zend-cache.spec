# remirepo/Fedora spec file for php-zendframework-zend-cache
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    2c68def8f96ce842d2f2a9a69e2f3508c2f5312d
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-cache
%global php_home     %{_datadir}/php
%global library      Cache
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
URL:            https://framework.zend.com/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-reflection
BuildRequires:  php-date
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.7.5
BuildRequires:  php-composer(%{gh_owner}/zend-eventmanager)     >= 2.6.2
# From composer, "require-dev": {
#        "zendframework/zend-serializer": "^2.6",
#        "zendframework/zend-session": "^2.6.2",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/phpunit": "^4.5",
#        "phpbench/phpbench": "^0.10.0"
BuildRequires:  php-composer(%{gh_owner}/zend-serializer)       >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-session)          >= 2.6.2
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.5
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3",
#        "zendframework/zend-eventmanager": "^2.6.2 || ^3.0"
Requires:       php(language) >= 5.5
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  4
Requires:       php-composer(%{gh_owner}/zend-servicemanager)   >= 2.7.5
Requires:       php-composer(%{gh_owner}/zend-servicemanager)   <  4
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     >= 2.6.2
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     <  4
# From composer, "suggest": {
#        "zendframework/zend-serializer": "Zend\\Serializer component",
#        "zendframework/zend-session": "Zend\\Session component",
#        "ext-apcu": "APCU, to use the APC storage adapter",
#        "ext-apc": "APC or compatible extension, to use the APC storage adapter",
#        "ext-apcu": "APCU >= 5.1.0, to use the APCu storage adapter",
#        "ext-dba": "DBA, to use the DBA storage adapter",
#        "ext-memcache": "Memcache >= 2.0.0 to use the Memcache storage adapter",
#        "ext-memcached": "Memcached >= 1.0.0 to use the Memcached storage adapter",
#        "ext-mongo": "Mongo, to use MongoDb storage adapter",
#        "ext-redis": "Redis, to use Redis storage adapter",
#        "ext-wincache": "WinCache, to use the WinCache storage adapter",
#        "ext-xcache": "XCache, to use the XCache storage adapter",
#        "mongofill/mongofill": "Alternative to ext-mongo - a pure PHP implementation designed as a drop in replacement"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-serializer)
Suggests:       php-composer(%{gh_owner}/zend-session)
Suggests:       php-pecl(apcu)
Suggests:       php-dba
Suggests:       php-pecl(memcache)
Suggests:       php-pecl(memcached)
Suggests:       php-pecl(mongo)
Suggests:       php-pecl(redis)
Suggests:       php-xcache
%endif
%endif
# From phpcompatinfo report for version 2.5.2
Requires:       php-reflection
Requires:       php-date
Requires:       php-pcre
Requires:       php-pcre
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library}           < 2.5
Obsoletes:      php-ZendFramework2-%{library}-apc       < 2.5
Obsoletes:      php-ZendFramework2-%{library}-memcached < 2.5
Provides:       php-ZendFramework2-%{library}           = %{version}
Provides:       php-ZendFramework2-%{library}-apc       = %{version}
Provides:       php-ZendFramework2-%{library}-memcached = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Cache provides a general cache system for PHP.
The Zend\Cache component is able to cache different patterns
(class, object, output, etc) using different storage adapters
(DB, File, Memcache, etc).

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
cat << EOF | tee vendor/autoload.php
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
* Fri May 13 2016 Remi Collet <remi@fedoraproject.org> - 2.7.1-1
- update to 2.7.1

* Wed Apr 13 2016 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- update to 2.7.0

* Sat Feb 13 2016 Remi Collet <remi@fedoraproject.org> - 2.6.1-1
- update to 2.6.1

* Fri Feb 12 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0
- raise dependency on zend-stdlib >= 2.7
- raise dependency on zend-servicemanager >= 2.7.5
- raise dependency on zend-eventmanager >= 2.6.2

* Wed Sep 16 2015 Remi Collet <remi@fedoraproject.org> - 2.5.3-1
- update to 2.5.3
- zend-serializer is    optional

* Thu Aug  6 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-2
- add missing obsoletes

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- initial package
