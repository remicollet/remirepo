# remirepo/Fedora spec file for php-zendframework-zend-serializer
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    ff74ea020f5f90866eb28365327e9bc765a61a6e
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-serializer
%global php_home     %{_datadir}/php
%global library      Serializer
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.8.0
Release:        1%{?dist}
Summary:        Zend Framework %{library} component

Group:          Development/Libraries
License:        BSD
URL:            http://framework.zend.com/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-dom
BuildRequires:  php-libxml
BuildRequires:  php-pcre
BuildRequires:  php-simplexml
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
BuildRequires:  php-composer(%{gh_owner}/zend-json)             >= 2.5
# From composer, "require-dev": {
#        "zendframework/zend-math": "^2.6",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3",
#        "squizlabs/php_codesniffer": "^2.3.1",
#        "phpunit/PHPUnit": "^4.5"
BuildRequires:  php-composer(%{gh_owner}/zend-math)             >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.7.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.5
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.6 || ^7.0",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0",
#        "zendframework/zend-json": "^2.5 || ^3.0"
Requires:       php(language) >= 5.6
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  4
Requires:       php-composer(%{gh_owner}/zend-json)             >= 2.5
Requires:       php-composer(%{gh_owner}/zend-json)             <  4
# From composer, "suggest": {
#        "zendframework/zend-math": "(^2.6 || ^3.0) To support Python Pickle serialization",
#        "zendframework/zend-servicemanager": "(^2.7.5 || ^3.0.3) To support plugin manager support"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-math)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
Suggests:       php-pecl(igbinary)
Suggests:       php-pecl(msgpack)
%endif
%endif
# From phpcompatinfo report for version 2.5.1
Requires:       php-dom
Requires:       php-libxml
Requires:       php-pcre
Requires:       php-simplexml
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
The Zend\Serializer component provides an adapter based interface
to simply generate storable representation of PHP types by different
facilities, and recover.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


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

%{_bindir}/phpunit --include-path=%{buildroot}%{php_home}

if which php70; then
   php70 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home} || :
fi
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


%changelog
* Tue Jun 21 2016 Remi Collet <remi@fedoraproject.org> - 2.8.0-1
- update to 2.8.0
- raise dependency on PHP 5.6

* Wed May 11 2016 Remi Collet <remi@fedoraproject.org> - 2.7.2-1
- update to 2.7.2
- dependency to zend-math is now optional

* Tue Apr 19 2016 Remi Collet <remi@fedoraproject.org> - 2.7.1-1
- update to 2.7.1

* Thu Apr  7 2016 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- update to 2.7.0

* Thu Feb  4 2016 Remi Collet <remi@fedoraproject.org> - 2.6.1-1
- update to 2.6.1

* Wed Feb  3 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0
- raise dependency on PHP >= 5.5
- raise dependency on zend-stdlib ~2.7
- raise dependency on zend-math ~2.6
- raise dependency on zend-servicemanager ~2.7.5

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
