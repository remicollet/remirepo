# remirepo/Fedora spec file for php-zendframework-zend-expressive-platesrenderer
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    ee7f5f878650b8bcdb3aa04fdbb92420c9db33a4
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-expressive-platesrenderer
%global php_home     %{_datadir}/php
%global library      Expressive
%global sublib       Plates
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.2.0
Release:        1%{?dist}
Summary:        Plates integration for %{library}

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
BuildRequires:  php-composer(container-interop/container-interop)    >= 1.1
BuildRequires:  php-composer(league/plates)                          >= 3.1
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-template)   >= 1.0
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-helpers)    >= 2.2
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-router)     >= 1.3.2
BuildRequires:  php-reflection
BuildRequires:  php-spl
# From composer, "require-dev": {
#        "phpunit/phpunit": "^5.7",
#        "zendframework/zend-coding-standard": "~1.0.0"
BuildRequires:  php-composer(phpunit/phpunit)                        >= 5.7
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)                >= 2.5
# For dependencies autoloader
BuildRequires:  php-zendframework-zend-loader                        >= 2.5.1-4
%endif

# From composer, "require": {
#        "php": "^5.6 || ^7.0",
#        "container-interop/container-interop": "^1.1",
#        "league/plates": "^3.1",
#        "zendframework/zend-expressive-template": "^1.0",
#        "zendframework/zend-expressive-helpers": "^2.2 || ^3.0",
#        "zendframework/zend-expressive-router": "^1.3.2 || ^2.0"
Requires:       php(language) >= 5.6
Requires:       php-composer(container-interop/container-interop)    >= 1.1
Requires:       php-composer(container-interop/container-interop)    <  2
Requires:       php-composer(league/plates)                          >= 3.1
Requires:       php-composer(league/plates)                          <  4
Requires:       php-composer(%{gh_owner}/zend-expressive-template)   >= 1.0
Requires:       php-composer(%{gh_owner}/zend-expressive-template)   <  2
Requires:       php-composer(%{gh_owner}/zend-expressive-helpers)    >= 2.2
Requires:       php-composer(%{gh_owner}/zend-expressive-helpers)    <  4
Requires:       php-composer(%{gh_owner}/zend-expressive-router)     >= 1.3.2
Requires:       php-composer(%{gh_owner}/zend-expressive-router)     <  3
# From phpcompatinfo report for version 1.2.0
Requires:       php-reflection
Requires:       php-spl
%if ! %{bootstrap}
# From composer, "suggest": {
#        "mouf/pimple-interop": "^1.0 to use Pimple for dependency injection",
#        "aura/di": "3.0.*@beta to make use of Aura.Di dependency injection container",
#        "zendframework/zend-servicemanager": "^2.5 to use zend-servicemanager for dependency injection"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/aura/di)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
%endif
# Autoloader
Requires:       php-composer(%{gh_owner}/zend-loader)                >= 2.5
Requires:       php-zendframework-zend-loader                        >= 2.5.1-4
%endif

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Provides integration with Plates for Expressive.

Documentation: http://zend-expressive.readthedocs.io/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv LICENSE.md LICENSE

: Create dependency autoloader
cat << 'EOF' | tee autoload.php
<?php
require_once '%{php_home}/League/Plates/autoload.php';
if (file_exists('%{php_home}/Aura/Di/autoload.php')) {
   require_once '%{php_home}/Aura/Di/autoload.php';
}
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
%{php_home}/Zend/%{library}/%{sublib}/
%{php_home}/Zend/%{library}-%{sublib}-autoload.php


%changelog
* Wed Jan 11 2017 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0
- raise dependency on PHP version 5.6
- raise dependency on zend-expressive-helpers version 2.2, allow 3.0
- add dependency on zend-expressive-router

* Sat Jul  2 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- initial package

