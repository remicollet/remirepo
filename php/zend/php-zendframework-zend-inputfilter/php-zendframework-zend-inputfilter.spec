# remirepo/Fedora spec file for php-zendframework-zend-inputfilter
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    3208cddbb92df029230cde676a5c8e5a22b531c6
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-inputfilter
%global php_home     %{_datadir}/php
%global library      InputFilter
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.5.5
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
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-filter)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-validator)        >= 2.5.3
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
# From composer, "require-dev": {
#        "zendframework/zend-i18n": "~2.5",
#        "zendframework/zend-servicemanager": "~2.5",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "^4.5"
BuildRequires:  php-composer(%{gh_owner}/zend-i18n)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.5
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": ">=5.5"
#        "zendframework/zend-filter": "~2.5",
#        "zendframework/zend-validator": "^2.5.3",
#        "zendframework/zend-stdlib": "~2.5"
Requires:       php(language) >= 5.5
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-filter)           >= 2.5
Requires:       php-composer(%{gh_owner}/zend-filter)           <  3
Requires:       php-composer(%{gh_owner}/zend-validator)        >= 2.5.3
Requires:       php-composer(%{gh_owner}/zend-validator)        <  3
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  3
# From composer, "suggest": {
#        "zendframework/zend-servicemanager": "To support plugin manager support"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
%endif
%endif
# From phpcompatinfo report for version 2.5.5
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
The Zend\InputFilter component can be used to filter and validate generic sets
of input data. For instance, you could use it to filter $_GET or $_POST values,
CLI arguments, etc.


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
   php70 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home}
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
* Fri Sep  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.5-1
- update to 2.5.5
- raise dependency on zend-validator ^2.5.3
- raise build dependency on PHPUnit ^4.5

* Wed Aug 12 2015 Remi Collet <remi@fedoraproject.org> - 2.5.4-1
- update to 2.5.4

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.3-1
- initial package