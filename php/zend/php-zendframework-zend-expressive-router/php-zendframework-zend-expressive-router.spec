# remirepo/Fedora spec file for php-zendframework-zend-expressive-router
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    50c9e4dff0cf65d9937c56b597c530e1bf5f8ef0
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-expressive-router
%global php_home     %{_datadir}/php
%global library      Expressive
%global sublib       Router
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.3.2
Release:        1%{?dist}
Summary:        %{sublib} subcomponent for %{library}

Group:          Development/Libraries
License:        BSD
URL:            https://framework.zend.com/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-composer(psr/http-message)                    >= 1.0
BuildRequires:  php-composer(fig/http-message-util)               >= 1.1
BuildRequires:  php-pcre
BuildRequires:  php-spl
# From composer, "require-dev": {
#        "phpunit/phpunit": "^4.7 || ^5.6",
#        "zendframework/zend-coding-standard": "~1.0.0",
#        "malukenho/docheader": "^0.1.5"
BuildRequires:  php-composer(phpunit/phpunit)                     >= 4.7
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)             >= 2.5
# For dependencies autoloader
BuildRequires:  php-zendframework-zend-loader                     >= 2.5.1-4
%endif

# From composer, "require": {
#        "php": "^5.6 || ^7.0",
#        "psr/http-message": "^1.0",
#        "fig/http-message-util": "^1.1"
Requires:       php(language) >= 5.6
Requires:       php-composer(psr/http-message)                    >= 1.0
Requires:       php-composer(psr/http-message)                    <  2
Requires:       php-composer(fig/http-message-util)               >= 1.1
Requires:       php-composer(fig/http-message-util)               <  2
# From phpcompatinfo report for version 1.2.0
Requires:       php-pcre
Requires:       php-spl
%if ! %{bootstrap}
# From composer, "suggest": {
#        "zendframework/zend-expressive-aurarouter": "^1.0 to use the Aura.Router routing adapter",
#        "zendframework/zend-expressive-fastroute": "^1.2 to use the FastRoute routing adapter",
#        "zendframework/zend-expressive-zendrouter": "^1.2 to use the zend-router routing adapter"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-expressive-aurarouter)
Suggests:       php-composer(%{gh_owner}/zend-expressive-fastroute)
Suggests:       php-composer(%{gh_owner}/zend-expressive-zendrouter)
%endif
# Autoloader
Requires:       php-composer(%{gh_owner}/zend-loader)           >= 2.5
Requires:       php-zendframework-zend-loader                   >= 2.5.1-4
%endif

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Router subcomponent for Expressive.

This package provides the following classes and interfaces:

* RouterInterface, a generic interface to implement for providing routing
  capabilities around PSR-7 ServerRequest messages.
* Route, a value object describing routed middleware.
* RouteResult, a value object describing the results of routing.

We currently support and provide the following routing integrations:

* Aura.Router: php-zendframework-zend-expressive-aurarouter
* FastRoute: php-zendframework-zend-expressive-fastroute
* ZF2 MVC Router: php-zendframework-zend-expressive-zendviewrouter

Documentation: http://zend-expressive.readthedocs.io/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv LICENSE.md LICENSE

: Create dependency autoloader
cat << 'EOF' | tee autoload.php
<?php
require_once '%{php_home}/Fig/Http/Message/autoload.php';
EOF


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/Zend/%{library}
cp -pr src %{buildroot}%{php_home}/Zend/%{library}/%{sublib}

install -m644 autoload.php %{buildroot}%{php_home}/Zend/%{library}-%{sublib}-autoload.php


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
           'ZendTest\\%{library}\\%{sublib}' => dirname(__DIR__).'/test/',
           'Zend\\%{library}\\%{sublib}'     => '%{buildroot}%{php_home}/Zend/%{library}/%{sublib}'
))));
require_once '%{php_home}/Zend/autoload.php';
EOF

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose
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
%dir %{php_home}/Zend/%{library}/
     %{php_home}/Zend/%{library}/%{sublib}/
     %{php_home}/Zend/%{library}-%{sublib}-autoload.php


%changelog
* Wed Dec 14 2016 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- update to 1.3.2

* Wed Dec 14 2016 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- update to 1.3.1
- raise dependency on PHP 5.6
- add dependency on fig/http-message-util

* Sat Jul  2 2016 Remi Collet <remi@fedoraproject.org> - 1.2.0-2
- drop autoloader, rely on zend-loader >= 2.5.1-4

* Fri Jul  1 2016 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- initial package

