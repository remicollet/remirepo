# remirepo/Fedora spec file for php-zendframework-zend-router
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    03763610632a9022aff22a0e8f340852e68392a1
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-router
%global php_home     %{_datadir}/php
%global library      Router
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        3.0.2
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
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(container-interop/container-interop) >= 1.1
BuildRequires:  php-composer(%{gh_owner}/zend-http)               >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)     >= 2.7.5
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)             >= 2.7.5
# From composer, "require-dev": {
#        "zendframework/zend-i18n": "^2.6",
#        "squizlabs/php_codesniffer": "^2.3",
#        "phpunit/phpunit": "^4.5",
#        "sebastian/version": "^1.0.4"
BuildRequires:  php-composer(%{gh_owner}/zend-i18n)               >= 2.6
BuildRequires:  php-composer(phpunit/phpunit)                     >= 4.0
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)             >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "container-interop/container-interop": "^1.1",
#        "zendframework/zend-http": "^2.5",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3",
#        "zendframework/zend-stdlib": "^2.7.5 || ^3.0"
Requires:       php(language) >= 5.5
%if ! %{bootstrap}
Requires:       php-composer(container-interop/container-interop) >= 1.1
Requires:       php-composer(container-interop/container-interop) <  2
Requires:       php-composer(%{gh_owner}/zend-http)               >= 2.5
Requires:       php-composer(%{gh_owner}/zend-http)               <  3
Requires:       php-composer(%{gh_owner}/zend-servicemanager)     >= 2.7.5
Requires:       php-composer(%{gh_owner}/zend-servicemanager)     <  4
Requires:       php-composer(%{gh_owner}/zend-stdlib)             >= 2.7.5
Requires:       php-composer(%{gh_owner}/zend-stdlib)             <  4
# From composer, "suggest": {
#        "zendframework/zend-i18n": "^2.6, if defining translatable HTTP path segments"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-i18n)
%endif
# From composer, "conflict": {
#        "zendframework/zend-mvc": "<3.0.0"
Conflicts:      php-composer(%{gh_owner}/zend-mvc)                <  3
%endif
# From phpcompatinfo report for version 2.5.1
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
zend-router provides flexible HTTP routing.

Routing currently works against the zend-http request and responses,
and provides capabilities around:

* Literal path matches
* Path segment matches (at path boundaries, and optionally validated
  using regex)
* Regular expression path matches
* HTTP request scheme
* HTTP request method
* Hostname

Additionally, it supports combinations of different route types in tree
structures, allowing for fast, b-tree lookups.

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
cat << 'EOF' | tee vendor/autoload.php
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
%license LICENSE
%doc *.md
%doc composer.json
%{php_home}/Zend/%{library}


%changelog
* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 3.0.2-1
- update to 3.0.2

* Tue Apr 19 2016 Remi Collet <remi@fedoraproject.org> - 3.0.1-1
- initial package

