# remirepo/Fedora spec file for php-zendframework-zend-expressive-fastroute
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    7bbc70d1e5b5d8be1e2e786ef36230a5f26110d3
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-expressive-fastroute
%global php_home     %{_datadir}/php
%global library      Expressive
%global sublib       Router
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.2.1
Release:        1%{?dist}
Summary:        FastRoute integration for %{library}

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
BuildRequires:  php-composer(nikic/fast-route)                       >= 1.0.0
BuildRequires:  php-composer(psr/http-message)                       >= 1.0
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-router)     >= 1.0
BuildRequires:  php-pcre
# From composer, "require-dev": {
#        "phpunit/phpunit": "^4.7",
#        "zendframework/zend-coding-standard": "~1.0.0"
BuildRequires:  php-composer(phpunit/phpunit)                        >= 4.7
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)                >= 2.5
# For dependencies autoloader
BuildRequires:  php-zendframework-zend-loader                        >= 2.5.1-4
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "nikic/fast-route": "^1.0.0",
#        "psr/http-message": "^1.0",
#        "zendframework/zend-expressive-router": "^1.0"
Requires:       php(language) >= 5.5
Requires:       php-composer(nikic/fast-route)                       >= 1.0.0
Requires:       php-composer(nikic/fast-route)                       <  2
Requires:       php-composer(psr/http-message)                       >= 1.0
Requires:       php-composer(psr/http-message)                       <  2
Requires:       php-composer(%{gh_owner}/zend-expressive-router)     >= 1.0
Requires:       php-composer(%{gh_owner}/zend-expressive-router)     <  2
# From phpcompatinfo report for version 1.2.0
Requires:       php-pcre
%if ! %{bootstrap}
# Autoloader
Requires:       php-composer(%{gh_owner}/zend-loader)                >= 2.5
Requires:       php-zendframework-zend-loader                        >= 2.5.1-4
%endif

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Provides FastRoute integration for Expressive.

Documentation:
https://zendframework.github.io/zend-expressive/features/router/fast-route/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv LICENSE.md LICENSE

: Create dependency autoloader
cat << 'EOF' | tee autoload.php
<?php
require_once '%{php_home}/FastRoute/bootstrap.php';
EOF


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/Zend/%{library}
cp -pr src %{buildroot}%{php_home}/Zend/%{library}/%{sublib}

install -m644 autoload.php %{buildroot}%{php_home}/Zend/%{library}-%{sublib}-fast-autoload.php


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
   php56 %{_bindir}/phpunit --verbose || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --verbose || ret=1
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
%{php_home}/Zend/%{library}/%{sublib}/Fast*
%{php_home}/Zend/%{library}-%{sublib}-fast-autoload.php


%changelog
* Wed Dec 14 2016 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- update to 1.2.1

* Sat Jul  2 2016 Remi Collet <remi@fedoraproject.org> - 1.2.0-2
- clean autoloader, rely on zend-loader >= 2.5.1-4

* Fri Jul  1 2016 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- initial package

