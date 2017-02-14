# remirepo/Fedora spec file for php-zendframework-zend-expressive-helpers
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    51f4248aa837b9e253579db341c1d454e3e34144
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-expressive-helpers
%global php_home     %{_datadir}/php
%global library      Expressive
%global sublib       Helper
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        3.0.1
Release:        1%{?dist}
Summary:        Helper/Utility classes for Expressive

Group:          Development/Libraries
License:        BSD
URL:            https://docs.zendframework.com/zend-expressive/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-composer(psr/http-message)                    >= 1.0
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(container-interop/container-interop) >= 1.1
BuildRequires:  php-composer(psr/http-message)                    >= 1.0
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-router)  >= 2.0
# From composer, "require-dev": {
#        "phpunit/phpunit": "^4.7",
#        "zendframework/zend-diactoros": "^1.2",
#        "mockery/mockery": "^0.9.5",
#        "zendframework/zend-coding-standard": "~1.0.0",
#        "malukenho/docheader": "^0.1.5"
BuildRequires:  php-composer(phpunit/phpunit)                     >= 4.7
BuildRequires:  php-composer(%{gh_owner}/zend-diactoros)          >= 1.2
BuildRequires:  php-composer(mockery/mockery)                     >= 0.9.5
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)             >= 2.5
# For dependencies autoloader
BuildRequires:  php-zendframework-zend-loader                     >= 2.5.1-4
%endif

# From composer, "require": {
#        "php": "^5.6 || ^7.0",
#        "container-interop/container-interop": "^1.1",
#        "psr/http-message": "^1.0",
#        "zendframework/zend-expressive-router": "^2.0"
Requires:       php(language) >= 5.5
Requires:       php-composer(container-interop/container-interop) >= 1.1
Requires:       php-composer(container-interop/container-interop) <  2
Requires:       php-composer(psr/http-message)                    >= 1.0
Requires:       php-composer(psr/http-message)                    <  2
Requires:       php-composer(%{gh_owner}/zend-expressive-router)  >= 2.0
Requires:       php-composer(%{gh_owner}/zend-expressive-router)  <  3
# From phpcompatinfo report for version 1.4.0
Requires:       php-json
Requires:       php-pcre
Requires:       php-spl
%if ! %{bootstrap}
# From composer, "suggest": {
#        "mouf/pimple-interop": "^1.0 to use Pimple for dependency injection",
#        "aura/di": "3.0.*@beta to make use of Aura.Di dependency injection container",
#        "zendframework/zend-servicemanager": "^2.5 to use zend-servicemanager for dependency injection"
%if 0%{?fedora} >= 21
Suggests:       php-composer(mouf/pimple-interop)
Suggests:       php-composer(aura/di)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
%endif
# Autoloader
Requires:       php-composer(%{gh_owner}/zend-loader)           >= 2.5
Requires:       php-zendframework-zend-loader                   >= 2.5.1-4
%endif

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Helper classes for Expressive.



%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv LICENSE.md LICENSE


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/Zend/%{library}
cp -pr src %{buildroot}%{php_home}/Zend/%{library}/%{sublib}


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
require_once '%{php_home}/Mockery/autoload.php';
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
%{php_home}/Zend/%{library}/%{sublib}/


%changelog
* Tue Feb 14 2017 Remi Collet <remi@fedoraproject.org> - 3.0.1-1
- update to 3.0.1
- raise dependency on PHP 5.6
- raise dependency on zend-expressive-router 2.0

* Sat Dec 24 2016 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- update to 2.2.0

* Mon Oct  3 2016 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- update to 2.1.0

* Fri Sep  2 2016 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- update to 2.0.3

* Sat Jul  2 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0

* Sat Jul  2 2016 Remi Collet <remi@fedoraproject.org> - 1.4.0-2
- drop autoloader, rely on zend-loader >= 2.5.1-4

* Sat Jul  2 2016 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- initial package

