# remirepo/Fedora spec file for php-zendframework-zend-mvc
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    e25f04a71b70985620f5ff3e762475848d049025
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-mvc
%global php_home     %{_datadir}/php
%global library      Mvc
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        3.0.4
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
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-reflection
BuildRequires:  php-intl
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-eventmanager)     >= 3.0
BuildRequires:  php-composer(%{gh_owner}/zend-http)             >= 2.5.4
BuildRequires:  php-composer(%{gh_owner}/zend-modulemanager)    >= 2.7.1
BuildRequires:  php-composer(%{gh_owner}/zend-router)           >= 3.0.1
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 3.0.3
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 3.0
BuildRequires:  php-composer(%{gh_owner}/zend-view)             >= 2.6.7
BuildRequires:  php-composer(container-interop/container-interop) >= 1.1
# From composer, "require-dev": {
#        "zendframework/zend-json": "^2.6.1 || ^3.0",
#        "zendframework/zend-psr7bridge": "^0.2",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/phpunit": "^4.5"
BuildRequires:  php-composer(%{gh_owner}/zend-json)             >= 2.6.1
BuildRequires:  php-composer(%{gh_owner}/zend-psr7bridge)       >= 0.2
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.5
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
# For dependencies autoloader
BuildRequires:  php-zendframework-zend-loader                   >= 2.5.1-3
%endif

# From composer, "require": {
#        "php": "^5.6 || ^7.0",
#        "zendframework/zend-eventmanager": "^3.0",
#        "zendframework/zend-http": "^2.5.4",
#        "zendframework/zend-modulemanager": "^2.7.1",
#        "zendframework/zend-router": "^3.0.1",
#        "zendframework/zend-servicemanager": "^3.0.3",
#        "zendframework/zend-stdlib": "^3.0",
#        "zendframework/zend-view": "^2.6.7",
Requires:       php(language) >= 5.6
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     >= 3.0
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     <  4
Requires:       php-composer(%{gh_owner}/zend-http)             >= 2.5.4
Requires:       php-composer(%{gh_owner}/zend-http)             <  3
Requires:       php-composer(%{gh_owner}/zend-modulemanager)    >= 2.7.1
Requires:       php-composer(%{gh_owner}/zend-modulemanager)    <  3
Requires:       php-composer(%{gh_owner}/zend-router)           >= 3.0.1
Requires:       php-composer(%{gh_owner}/zend-router)           <  4
Requires:       php-composer(%{gh_owner}/zend-servicemanager)   >= 3.0.3
Requires:       php-composer(%{gh_owner}/zend-servicemanager)   <  4
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 3.0
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  4
Requires:       php-composer(%{gh_owner}/zend-view)             >= 2.6.7
Requires:       php-composer(%{gh_owner}/zend-http)             <  3
Requires:       php-composer(container-interop/container-interop) >= 1.1
Requires:       php-composer(container-interop/container-interop) <  2
# From composer, "suggest": {
#        "zendframework/zend-json": "(^2.6.1 || ^3.0) To auto-deserialize JSON body content in AbstractRestfulController extensions, when json_decode is unavailable",
#        "zendframework/zend-mvc-console": "zend-mvc-console provides the ability to expose zend-mvc as a console application",
#        "zendframework/zend-mvc-i18n": "zend-mvc-i18n provides integration with zend-i18n, including a translation bridge and translatable route segments",
#        "zendframework/zend-mvc-plugin-fileprg": "To provide Post/Redirect/Get functionality around forms that container file uploads",
#        "zendframework/zend-mvc-plugin-flashmessenger": "To provide flash messaging capabilities between requests",
#        "zendframework/zend-mvc-plugin-identity": "To access the authenticated identity (per zend-authentication) in controllers",
#        "zendframework/zend-mvc-plugin-prg": "To provide Post/Redirect/Get functionality within controllers",
#        "zendframework/zend-psr7bridge": "(^0.2) To consume PSR-7 middleware within the MVC workflow",
#        "zendframework/zend-servicemanager-di": "zend-servicemanager-di provides utilities for integrating zend-di and zend-servicemanager in your zend-mvc application"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-json)
Suggests:       php-composer(%{gh_owner}/zend-mvc-console)
Suggests:       php-composer(%{gh_owner}/zend-mvc-i18n)
Suggests:       php-composer(%{gh_owner}/zend-mvc-plugin-fileprg)
Suggests:       php-composer(%{gh_owner}/zend-mvc-plugin-flashmessenger)
Suggests:       php-composer(%{gh_owner}/zend-mvc-plugin-identity)
Suggests:       php-composer(%{gh_owner}/zend-mvc-plugin-prg)
Suggests:       php-composer(%{gh_owner}/zend-psr7bridge)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager-di)
%endif
# Autoloader
Requires:       php-composer(%{gh_owner}/zend-loader)           >= 2.5
Requires:       php-zendframework-zend-loader                   >= 2.5.1-3
%endif
# From phpcompatinfo report for version 2.7.0
Requires:       php-reflection
Requires:       php-intl
Requires:       php-pcre
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Mvc is a brand new MVC implementation designed from the ground up
for Zend Framework 2, focusing on performance and flexibility.

The MVC layer is built on top of the following components:
* Zend\ServiceManager - Zend Framework provides a set of default service
  definitions set up at Zend\Mvc\Service. The ServiceManager creates and
  configures your application instance and workflow.
* Zend\EventManager - The MVC is event driven. This component is used
  everywhere from initial bootstrapping of the application, through returning
  response and request calls, to setting and retrieving routes and matched
  routes, as well as render views.
* Zend\Http - specifically the request and response objects, used within:
  Zend\Stdlib\DispatchableInterface. All “controllers” are simply dispatchable
  objects.

Documentation: https://zendframework.github.io/%{gh_project}/


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

mkdir -p   %{buildroot}%{php_home}/Zend/
cp -pr src %{buildroot}%{php_home}/Zend/%{library}

install -m644 autoload.php %{buildroot}%{php_home}/Zend/%{library}-autoload.php


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
define('RPM_BUILDROOT', '%{buildroot}%{php_home}/Zend');

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
   php71 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home} || ret=1
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
%{php_home}/Zend/%{library}
%{php_home}/Zend/%{library}-autoload.php


%changelog
* Wed Dec 21 2016 Remi Collet <remi@fedoraproject.org> - 3.0.4-1
- update to 3.0.4

* Fri Sep  2 2016 Remi Collet <remi@fedoraproject.org> - 3.0.3-1
- update to 3.0.3

* Fri Jul  1 2016 Remi Collet <remi@fedoraproject.org> - 3.0.2-1
- update to 3.0.2

* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 3.0.1-1
- update to 3.0.1 for ZendFramework 3
- raise dependency on PHP 5.6
- raise dependency on zend-eventmanager 3.0
- raise dependency on zend-stdlib 3.0
- raise dependency on zend-servicemanager 3.0.3
- add dependencies on zend-http, zend-modulemanager, zend-router, zend-view
- drop dependencies on zend-hydrator, zend-form, zend-psr7bridge
- add dependencies autoloader

* Tue Jun 14 2016 Remi Collet <remi@fedoraproject.org> - 2.7.10-1
- update to 2.7.10

* Wed Jun  1 2016 Remi Collet <remi@fedoraproject.org> - 2.7.8-1
- update to 2.7.8

* Wed Apr 13 2016 Remi Collet <remi@fedoraproject.org> - 2.7.7-1
- update to 2.7.7

* Thu Apr  7 2016 Remi Collet <remi@fedoraproject.org> - 2.7.6-1
- update to 2.7.6

* Wed Apr  6 2016 Remi Collet <remi@fedoraproject.org> - 2.7.5-1
- update to 2.7.5

* Mon Apr  4 2016 Remi Collet <remi@fedoraproject.org> - 2.7.4-1
- update to 2.7.4

* Wed Mar  9 2016 Remi Collet <remi@fedoraproject.org> - 2.7.3-1
- update to 2.7.3

* Thu Mar  3 2016 Remi Collet <remi@fedoraproject.org> - 2.7.1-1
- update to 2.7.1

* Wed Mar  2 2016 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- update to 2.7.0
- add dependency on zend-psr7bridge
- add dependency on container-interop
- raise dependency on zend-eventmanager >= 2.6.2
- raise dependency on zend-servicemanager >= 2.7.5
- raise dependency on zend-hydrator >= 1.1
- raise dependency on zend-form >= 2.7
- raise dependency on zend-stdlib >= 2.7.5

* Tue Feb 23 2016 Remi Collet <remi@fedoraproject.org> - 2.6.3-1
- update to 2.6.3

* Tue Feb 23 2016 Remi Collet <remi@fedoraproject.org> - 2.6.2-1
- update to 2.6.2

* Tue Feb 16 2016 Remi Collet <remi@fedoraproject.org> - 2.6.1-1
- update to 2.6.1
- raise dependency on zend-stdlib ^2.7.5

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0
- raise dependencies on zend-form ^2.6 and zend-stdlib ^2.7
- add dependency on zend-hydrator ^1.0

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-0
- update to 2.6.0, bootstrap build

* Thu Sep 24 2015 Remi Collet <remi@fedoraproject.org> - 2.5.3-1
- version 2.5.3

* Tue Sep 15 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- version 2.5.2

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
