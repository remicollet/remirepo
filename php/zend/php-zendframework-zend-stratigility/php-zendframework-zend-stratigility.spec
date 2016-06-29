# remirepo/Fedora spec file for php-zendframework-zend-stratigility
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    b78388f096f669f9a9f15dabe5fa73c4d9fd9a09
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-stratigility
%global php_home     %{_datadir}/php
%global library      Stratigility
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.2.1
Release:        1%{?dist}
Summary:        Middleware for PHP

Group:          Development/Libraries
License:        BSD
URL:            https://framework.zend.com/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.4.8
BuildRequires:  php-composer(psr/http-message)                    >= 1.0
BuildRequires:  php-composer(%{gh_owner}/zend-escaper)            >= 2.3
BuildRequires:  php-pcre
BuildRequires:  php-reflection
BuildRequires:  php-spl
# From composer, "require-dev": {
#    "zendframework/zend-diactoros": "~1.0",
#    "phpunit/phpunit": "~4.7",
#    "squizlabs/php_codesniffer": "^2.3.1"
BuildRequires:  php-composer(%{gh_owner}/zend-diactoros)          >= 1.0
BuildRequires:  php-composer(phpunit/phpunit)                     >= 4.7
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)             >= 2.5
# For dependencies autoloader
BuildRequires:  php-zendframework-zend-loader                     >= 2.5.1-3
%endif

# From composer, "require": {
#    "php": "^5.4.8 || ^7.0",
#    "psr/http-message": "~1.0.0",
#    "zendframework/zend-escaper": "~2.3"
Requires:       php(language) >= 5.4.8
Requires:       php-composer(psr/http-message)                    >= 1.0
Requires:       php-composer(psr/http-message)                    <  1.1
Requires:       php-composer(%{gh_owner}/zend-escaper)            >= 2.3
Requires:       php-composer(%{gh_owner}/zend-escaper)            <  3
# From composer, "suggest": {
#    "psr/http-message-implementation": "Please install a psr/http-message-implementation to consume Stratigility; e.g., zendframework/zend-diactoros"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-diactoros)
%endif
# From phpcompatinfo report for version 2.7.4
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl
# Autoloader
Requires:       php-composer(%{gh_owner}/zend-loader)             >= 2.5
Requires:       php-zendframework-zend-loader                     >= 2.5.1-3

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
From "Strata", Latin for "layer", and "agility".

This package supercedes and replaces phly/conduit.

Stratigility is a port of Sencha Connect to PHP.
It allows you to create and dispatch middleware pipelines.

* File issues at https://github.com/zendframework/zend-stratigility/issues
* Issue patches to https://github.com/zendframework/zend-stratigility/pulls
* Documentation is at https://zendframework.github.io/zend-stratigility/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

: Create dependency autoloader
cat << 'EOF' | tee autoload.php
<?php
require_once '%{php_home}/Psr/Http/Message/autoload.php';
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
   php70 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home} || ret=1
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
%license LICENSE.md
%doc CONTRIBUTING.md README.md
%doc composer.json
%{php_home}/Zend/%{library}
%{php_home}/Zend/%{library}-autoload.php


%changelog
* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- initial package
