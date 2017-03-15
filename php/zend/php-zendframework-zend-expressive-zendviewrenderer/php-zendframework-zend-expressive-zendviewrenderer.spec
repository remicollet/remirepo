# remirepo/Fedora spec file for php-zendframework-zend-expressive-zendviewrenderer
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    0757034f2f97e4b966afcfb2937e9884204a062c
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-expressive-zendviewrenderer
%global php_home     %{_datadir}/php
%global library      Expressive
%global sublib       ZendView
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.4.0
Release:        1%{?dist}
Summary:        zend-view PhpRenderer integration for Expressive

Group:          Development/Libraries
License:        BSD
URL:            https://zendframework.github.io/zend-expressive/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-composer(psr/http-message)                       >= 1.0
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(container-interop/container-interop)    >= 1.2
BuildRequires:  php-composer(psr/http-message)                       >= 1.0.1
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-helpers)    >= 1.4
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-router)     >= 1.3.2
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-template)   >= 1.0.1
BuildRequires:  php-composer(%{gh_owner}/zend-filter)                >= 2.6.1
BuildRequires:  php-composer(%{gh_owner}/zend-i18n)                  >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)        >= 2.7.8
BuildRequires:  php-composer(%{gh_owner}/zend-view)                  >= 2.8.1
# not in composer.json (dev dep of zend-expressive-helpers)
BuildRequires:  php-composer(%{gh_owner}/zend-diactoros)
# From composer, "require-dev": {
#        "malukenho/docheader": "^0.1.5",
#        "phpunit/phpunit": "^6.0.8 || ^5.7.15",
#        "zendframework/zend-coding-standard": "~1.0.0"
%if 0%{?fedora} >= 26
%global phpunit %{_bindir}/phpunit6
%else
%global phpunit %{_bindir}/phpunit
%endif
BuildRequires:  %{phpunit}
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)                >= 2.5
# For dependencies autoloader
BuildRequires:  php-zendframework-zend-loader                        >= 2.5.1-4
%endif

# From composer, "require": {
#        "php": "^5.6 || ^7.0",
#        "container-interop/container-interop": "^1.2",
#        "psr/http-message": "^1.0.1",
#        "zendframework/zend-expressive-helpers": "^1.4 || ^2.2 || ^3.0.1 || ^4.0",
#        "zendframework/zend-expressive-router": "^1.3.2 || ^2.1",
#        "zendframework/zend-expressive-template": "^1.0.4",
#        "zendframework/zend-servicemanager": "^2.7.8 || ^3.3",
#        "zendframework/zend-view": "^2.8.1"
Requires:       php(language) >= 5.6
Requires:       php-composer(container-interop/container-interop)    >= 1.2
Requires:       php-composer(container-interop/container-interop)    <  2
Requires:       php-composer(psr/http-message)                       >= 1.0.1
Requires:       php-composer(psr/http-message)                       <  2
Requires:       php-composer(%{gh_owner}/zend-expressive-helpers)    >= 1.4
Requires:       php-composer(%{gh_owner}/zend-expressive-helpers)    <  5
Requires:       php-composer(%{gh_owner}/zend-expressive-router)     >= 1.3.2
Requires:       php-composer(%{gh_owner}/zend-expressive-router)     <  3
Requires:       php-composer(%{gh_owner}/zend-expressive-template)   >= 1.0.4
Requires:       php-composer(%{gh_owner}/zend-expressive-template)   <  2
Requires:       php-composer(%{gh_owner}/zend-filter)                >= 2.6.1
Requires:       php-composer(%{gh_owner}/zend-filter)                <  3
Requires:       php-composer(%{gh_owner}/zend-i18n)                  >= 2.6
Requires:       php-composer(%{gh_owner}/zend-i18n)                  <  3
Requires:       php-composer(%{gh_owner}/zend-servicemanager)        >= 2.7.8
Requires:       php-composer(%{gh_owner}/zend-servicemanager)        <  4
Requires:       php-composer(%{gh_owner}/zend-view)                  >= 2.8.1
Requires:       php-composer(%{gh_owner}/zend-view)                  <  3
# From phpcompatinfo report for version 1.1.0
Requires:       php-pcre
Requires:       php-spl
%if ! %{bootstrap}
# Autoloader
Requires:       php-composer(%{gh_owner}/zend-loader)                >= 2.5
Requires:       php-zendframework-zend-loader                        >= 2.5.1-4
%endif

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
zend-view PhpRenderer integration for Expressive.


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
EOF

# remirepo:7
ret=0
if which php56; then
   php56 %{_bindir}/phpunit || ret=1
fi
if which php71; then
   php71 %{_bindir}/phpunit6 || ret=1
fi
%{phpunit} --verbose
# remirepo:1
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
* Wed Mar 15 2017 Remi Collet <remi@remirepo.net> - 1.4.0-1
- Update to 1.4.0
- use phpunit6 on F26+

* Fri Mar  3 2017 Remi Collet <remi@remirepo.net> - 1.3.0-1
- Update to 1.3.0
- raise dependency on container-interop/container-interop 1.2
- raise dependency on psr/http-message 1.0.1
- raise dependency on zend-expressive-helpers 1.4
- raise dependency on zend-servicemanager 2.7.8

* Fri Jan 13 2017 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- update to 1.2.1

* Wed Jan 11 2017 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0
- raise dependency on PHP version 5.6
- allow zend-expressive-helpers version 3.0
- add dependency on zend-expressive-router
- raise dependency on zend-expressive-template version 1.0.4
- drop dependency on zend-filter and zend-i18n
- raise dependency on zend-view version 2.8.1

* Sat Jul  2 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- initial package

