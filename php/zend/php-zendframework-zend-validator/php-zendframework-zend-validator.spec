# remirepo/Fedora spec file for php-zendframework-zend-validator
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    063694d3c781f284ab8f846b8af64c45d94aaf51
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-validator
%global php_home     %{_datadir}/php
%global library      Validator
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.7.2
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
BuildRequires:  php-ctype
BuildRequires:  php-date
BuildRequires:  php-fileinfo
BuildRequires:  php-hash
BuildRequires:  php-intl
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)             >= 2.7
Requires:       php-composer(container-interop/container-interop) > 1.1
# From composer, "require-dev": {
#        "zendframework/zend-cache": "^2.6.1",
#        "zendframework/zend-config": "^2.6",
#        "zendframework/zend-db": "^2.7",
#        "zendframework/zend-filter": "^2.6",
#        "zendframework/zend-http": "^2.5.4",
#        "zendframework/zend-i18n": "^2.6",
#        "zendframework/zend-math": "^2.6",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3",
#        "zendframework/zend-session": "^2.6.2",
#        "zendframework/zend-uri": "^2.5",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "^4.0"
BuildRequires:  php-composer(%{gh_owner}/zend-cache)            >= 2.6.1
BuildRequires:  php-composer(%{gh_owner}/zend-config)           >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-db)               >= 2.7
BuildRequires:  php-composer(%{gh_owner}/zend-filter)           >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-http)             >= 2.5.4
BuildRequires:  php-composer(%{gh_owner}/zend-i18n)             >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-math)             >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.7.5
BuildRequires:  php-composer(%{gh_owner}/zend-session)          >= 2.6.2
BuildRequires:  php-composer(%{gh_owner}/zend-uri)              >= 2.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0",
#        "container-interop/container-interop": "^1.1"
Requires:       php(language) >= 5.5
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-stdlib)             >= 2.7
Requires:       php-composer(%{gh_owner}/zend-stdlib)             <  4
Requires:       php-composer(container-interop/container-interop) > 1.1
Requires:       php-composer(container-interop/container-interop) < 2
# From composer, "suggest": {
#        "zendframework/zend-db": "Zend\\Db component",
#        "zendframework/zend-filter": "Zend\\Filter component, required by the Digits validator",
#        "zendframework/zend-i18n": "Zend\\I18n component to allow translation of validation error messages as well as to use the various Date validators",
#        "zendframework/zend-math": "Zend\\Math component",
#        "zendframework/zend-i18n-resources": "Translations of validator messages",
#        "zendframework/zend-servicemanager": "Zend\\ServiceManager component to allow using the ValidatorPluginManager and validator chains",
#        "zendframework/zend-session": "Zend\\Session component",
#        "zendframework/zend-uri": "Zend\\Uri component, required by the Uri and Sitemap\\Loc validators"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-db)
Suggests:       php-composer(%{gh_owner}/zend-filter)
Suggests:       php-composer(%{gh_owner}/zend-i18n)
Suggests:       php-composer(%{gh_owner}/zend-math)
Suggests:       php-composer(%{gh_owner}/zend-i18n-resources)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
Suggests:       php-composer(%{gh_owner}/zend-session)
Suggests:       php-composer(%{gh_owner}/zend-uri)
%endif
%endif
# From phpcompatinfo report for version 2.5.3
Requires:       php-ctype
Requires:       php-date
Requires:       php-fileinfo
Requires:       php-hash
Requires:       php-intl
Requires:       php-pcre
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
The Zend\Validator component provides a set of commonly needed validators.
It also provides a simple validator chaining mechanism by which multiple
validators may be applied to a single datum in a user-defined order.


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
* Tue Apr 19 2016 Remi Collet <remi@fedoraproject.org> - 2.7.2-1
- Update to 2.7.2

* Wed Apr  6 2016 Remi Collet <remi@fedoraproject.org> - 2.7.1-1
- Update to 2.7.1

* Wed Apr  6 2016 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- Update to 2.7.0

* Thu Feb 18 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0
- raise dependency on zend-stdlib ^2.7
- add dependency on container-interop/container-interop

* Fri Sep  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.3-1
- Update to 2.5.3

* Thu Aug  6 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-2
- fix description

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- initial package
