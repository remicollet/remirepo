# remirepo/Fedora spec file for php-zendframework-zend-expressive-zendviewrenderer
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    163e684ba3772a729a5e71abc9db14fb2574971f
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
Version:        1.1.0
Release:        1%{?dist}
Summary:        zend-view PhpRenderer integration for Expressive

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
BuildRequires:  php-composer(psr/http-message)                       >= 1.0
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(container-interop/container-interop)    >= 1.0
BuildRequires:  php-composer(psr/http-message)                       >= 1.0
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-helpers)    >= 1.1
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-template)   >= 1.0.1
BuildRequires:  php-composer(%{gh_owner}/zend-filter)                >= 2.6.1
BuildRequires:  php-composer(%{gh_owner}/zend-i18n)                  >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)        >= 2.7.5
BuildRequires:  php-composer(%{gh_owner}/zend-view)                  >= 2.6.5
# not in composer.json (dev dep of zend-expressive-helpers)
BuildRequires:  php-composer(%{gh_owner}/zend-diactoros)
# From composer, "require-dev": {
#        "phpunit/phpunit": "^4.7",
#        "squizlabs/php_codesniffer": "^2.3",
BuildRequires:  php-composer(phpunit/phpunit)                        >= 4.7
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)                >= 2.5
# For dependencies autoloader
BuildRequires:  php-zendframework-zend-loader                        >= 2.5.1-4
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "container-interop/container-interop": "^1.1",
#        "psr/http-message": "^1.0",
#        "zendframework/zend-expressive-helpers": "^1.1 || ^2.0",
#        "zendframework/zend-expressive-template": "^1.0.1",
#        "zendframework/zend-filter": "^2.6.1",
#        "zendframework/zend-i18n": "^2.6",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3",
#        "zendframework/zend-view": "^2.6.5"
Requires:       php(language) >= 5.5
Requires:       php-composer(container-interop/container-interop)    >= 1.0
Requires:       php-composer(container-interop/container-interop)    <  2
Requires:       php-composer(psr/http-message)                       >= 1.0
Requires:       php-composer(psr/http-message)                       <  2
Requires:       php-composer(%{gh_owner}/zend-expressive-helpers)    >= 1.1
Requires:       php-composer(%{gh_owner}/zend-expressive-helpers)    <  3
Requires:       php-composer(%{gh_owner}/zend-expressive-template)   >= 1.0.1
Requires:       php-composer(%{gh_owner}/zend-expressive-template)   <  2
Requires:       php-composer(%{gh_owner}/zend-filter)                >= 2.6.1
Requires:       php-composer(%{gh_owner}/zend-filter)                <  3
Requires:       php-composer(%{gh_owner}/zend-i18n)                  >= 2.6
Requires:       php-composer(%{gh_owner}/zend-i18n)                  <  3
Requires:       php-composer(%{gh_owner}/zend-servicemanager)        >= 2.7.5
Requires:       php-composer(%{gh_owner}/zend-servicemanager)        <  4
Requires:       php-composer(%{gh_owner}/zend-view)                  >= 2.6.5
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
* Sat Jul  2 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- initial package

