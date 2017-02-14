# remirepo/Fedora spec file for php-zendframework-zend-expressive
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    891507003240cec0404ca3b157a88a311c1f9c26
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-expressive
%global php_home     %{_datadir}/php
%global library      Expressive
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.1.1
Release:        1%{?dist}
Summary:        PSR-7 Middleware Microframework based on Stratigility

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
BuildRequires:  php-composer(container-interop/container-interop)    >= 1.1
BuildRequires:  php-composer(psr/http-message)                       >= 1.0
BuildRequires:  php-composer(%{gh_owner}/zend-diactoros)             >= 1.1
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-router)     >= 1.1
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-template)   >= 1.0.1
BuildRequires:  php-composer(%{gh_owner}/zend-stratigility)          >= 1.3.3
BuildRequires:  php-reflection
BuildRequires:  php-spl
# From composer, "require-dev": {
#        "filp/whoops": "^1.1 || ^2.0",
#        "phpunit/phpunit": "^4.7",
#        "zendframework/zend-coding-standard": "~1.0.0",
#        "zendframework/zend-expressive-aurarouter": "^1.0 || ^2.0",
#        "zendframework/zend-expressive-fastroute": "^1.0 || ^2.0",
#        "zendframework/zend-expressive-zendrouter": "^1.0 || ^2.0",
#        "zendframework/zend-servicemanager": "^2.6",
#        "malukenho/docheader": "^0.1.5",
#        "mockery/mockery": "^0.9.5"
BuildRequires:  php-composer(phpunit/phpunit)                        >= 4.7
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)                >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-aurarouter) >= 1.0
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-fastroute)  >= 1.0
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-zendrouter) >= 1.0
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)        >= 2.6
BuildRequires:  php-composer(mockery/mockery)                        >= 0.9.5
# For dependencies autoloader
BuildRequires:  php-zendframework-zend-loader                        >= 2.5.1-4
%endif

# From composer, "require": {
#        "php": "^5.6 || ^7.0",
#        "container-interop/container-interop": "^1.1",
#        "psr/http-message": "^1.0",
#        "zendframework/zend-diactoros": "^1.1",
#        "zendframework/zend-expressive-router": "^1.1 || ^2.0",
#        "zendframework/zend-expressive-template": "^1.0.1",
#        "zendframework/zend-stratigility": "^1.3.3"
Requires:       php(language) >= 5.6
Requires:       php-composer(container-interop/container-interop)    >= 1.1
Requires:       php-composer(container-interop/container-interop)    <  2
Requires:       php-composer(psr/http-message)                       >= 1.0
Requires:       php-composer(psr/http-message)                       <  2
Requires:       php-composer(%{gh_owner}/zend-diactoros)             >= 1.1
Requires:       php-composer(%{gh_owner}/zend-diactoros)             <  2
Requires:       php-composer(%{gh_owner}/zend-expressive-router)     >= 1.1
Requires:       php-composer(%{gh_owner}/zend-expressive-router)     <  3
Requires:       php-composer(%{gh_owner}/zend-expressive-template)   >= 1.0.1
Requires:       php-composer(%{gh_owner}/zend-expressive-template)   <  2
Requires:       php-composer(%{gh_owner}/zend-stratigility)          >= 1.3.3
Requires:       php-composer(%{gh_owner}/zend-stratigility)          <  2
# From phpcompatinfo report for version 1.2.0
Requires:       php-reflection
Requires:       php-spl
%if ! %{bootstrap}
# From composer, "suggest": {
#        "filp/whoops": "^2.0 to use the Whoops error handler",
#        "zendframework/zend-expressive-helpers": "^1.0 for its UrlHelper, ServerUrlHelper, and BodyParseMiddleware",
#        "aura/di": "3.0.*@beta to make use of Aura.Di dependency injection container",
#        "xtreamwayz/pimple-container-interop": "^1.0 to use Pimple for dependency injection",
#        "zendframework/zend-servicemanager": "^2.5 to use zend-servicemanager for dependency injection"
%if 0%{?fedora} >= 21
#Suggests:       php-composer(filp/whoops)
Suggests:       php-composer(%{gh_owner}/zend-expressive-helpers)
Suggests:       php-composer(aura/di)
#Suggests:       php-composer(xtreamwayz/pimple-container-interop)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
%endif
# Autoloader
Requires:       php-composer(%{gh_owner}/zend-loader)           >= 2.5
Requires:       php-zendframework-zend-loader                   >= 2.5.1-4
%endif

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
zend-expressive builds on zend-stratigility to provide a minimalist PSR-7
middleware framework for PHP, with the following features:
* Routing. Choose your own router; we support:
  - Aura.Router
  - FastRoute
  - ZF2's MVC router
* DI Containers, via container-interop. Middleware matched via routing is
  retrieved from the composed container.
* Optionally, templating. We support:
  -  Plates
  -  Twig
  -  ZF2's PhpRenderer

Documentation: http://zend-expressive.readthedocs.io/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv LICENSE.md LICENSE

: Create dependency autoloader
cat << 'EOF' | tee autoload.php
<?php
if (file_exists('%{php_home}/Aura/Di/autoload.php')) {
   require_once '%{php_home}/Aura/Di/autoload.php';
}
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
: drop tests using optional filp/whoops
rm test/Whoops*
rm test/Container/Whoops*

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
require_once '%{php_home}/Mockery/autoload.php';
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
%{php_home}/Zend/%{library}/*
%{php_home}/Zend/%{library}-autoload.php


%changelog
* Tue Feb 14 2017 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1

* Tue Feb 14 2017 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0
- allow zend-expressive-router 2.0
- raise dependency on zend-stratigility 1.3.3

* Tue Jan 10 2017 Remi Collet <remi@fedoraproject.org> - 1.0.6-1
- update to 1.0.6

* Fri Dec  9 2016 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- update to 1.0.5

* Thu Dec  8 2016 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- update to 1.0.4

* Sat Nov 12 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- update to 1.0.3

* Fri Nov 11 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2
- raise dependency on PHP 5.6

* Sat Jul  2 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- clean autoloader, rely on zend-loader >= 2.5.1-4

* Sat Jul  2 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package

