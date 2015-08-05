# remirepo spec/Fedora file for php-zendframework-zend-i18n
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    1
%global gh_commit    509271eb7947e4aabebfc376104179cffea42696
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-i18n
%global php_home     %{_datadir}/php
%global library      I18n
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.5.1
Release:        0%{?dist}
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
BuildRequires:  php(language) >= 5.3.23
BuildRequires:  php-ctype
BuildRequires:  php-date
BuildRequires:  php-intl
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
# From composer, "require-dev": {
#        "zendframework/zend-cache": "~2.5",
#        "zendframework/zend-config": "~2.5",
#        "zendframework/zend-eventmanager": "~2.5",
#        "zendframework/zend-filter": "~2.5",
#        "zendframework/zend-servicemanager": "~2.5",
#        "zendframework/zend-validator": "~2.5",
#        "zendframework/zend-view": "~2.5",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.0"
BuildRequires:  php-composer(%{gh_owner}/zend-cache)            >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-config)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-eventmanager)     >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-filter)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-validator)        >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-view)             >= 2.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": ">=5.3.23",
#        "zendframework/zend-stdlib": "~2.5"
Requires:       php(language) >= 5.3.23
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  3
# From composer, "suggest": {
#        "ext-intl": "Required for most features of Zend\\I18n; included in default builds of PHP",
#        "zendframework/zend-cache": "Zend\\Cache component",
#        "zendframework/zend-config": "Zend\\Config component",
#        "zendframework/zend-eventmanager": "You should install this package to use the events in the translator",
#        "zendframework/zend-filter": "You should install this package to use the provided filters",
#        "zendframework/zend-servicemanager": "Zend\\ServiceManager component",
#        "zendframework/zend-validator": "You should install this package to use the provided validators",
#        "zendframework/zend-view": "You should install this package to use the provided view helpers",
#        "zendframework/zend-resources": "Translation resources"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-cache)
Suggests:       php-composer(%{gh_owner}/zend-config)
Suggests:       php-composer(%{gh_owner}/zend-eventmanager)
Suggests:       php-composer(%{gh_owner}/zend-filter)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
Suggests:       php-composer(%{gh_owner}/zend-validator)
Suggests:       php-composer(%{gh_owner}/zend-view)
Suggests:       php-composer(%{gh_owner}/zend-i18n-resources)
%endif
%endif
Requires:       php-intl
# From phpcompatinfo report for version 2.5.1
Requires:       php-ctype
Requires:       php-date
Requires:       php-pcre
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\I18n comes with a complete translation suite which supports all major
formats and includes popular features like plural translations and text
domains. The Translator component is mostly dependency free, except for
the fallback to a default locale, where it relies on the Intl PHP extension.

The translator itself is initialized without any parameters, as any
configuration to it is optional. A translator without any translations
will actually do nothing but just return the given message IDs.


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
cat << EOF | tee vendor/autoload.php
<?php
require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\\Loader\\AutoloaderFactory::factory(array(
    'Zend\\Loader\\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendTest\\\\%{library}' => dirname(__DIR__).'/test/',
           'Zend\\\\%{library}'     => '%{buildroot}%{php_home}/Zend/%{library}'
))));
require_once '%{php_home}/Zend/autoload.php';
EOF
%{_bindir}/phpunit --include-path=%{buildroot}%{php_home}
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
* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package