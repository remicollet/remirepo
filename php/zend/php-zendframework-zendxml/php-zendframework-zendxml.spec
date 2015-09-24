# remirepo/Fedora spec file for php-zendframework-zendxml
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    54edb3875aba5b45f02824f65f311c9fb2743a38
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zendxml
%global php_home     %{_datadir}/php
%global library      ZendXml
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.0.1
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
BuildRequires:  php(language) >= 5.3.23
BuildRequires:  php-simplexml
BuildRequires:  php-dom
BuildRequires:  php-libxml
BuildRequires:  php-pcre
BuildRequires:  php-spl
# From composer, "require-dev": {
#        "phpunit/phpunit": "~3.7",
#        "squizlabs/php_codesniffer": "~1.5"
BuildRequires:  php-composer(phpunit/phpunit)                   >= 3.7
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": ">=5.3.3"
Requires:       php(language) >= 5.3.3
# From phpcompatinfo report for version 1.0.1
Requires:       php-simplexml
Requires:       php-dom
Requires:       php-libxml
Requires:       php-pcre
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = 1:%{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
An utility component for XML usage and best practices in PHP.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}
cp -pr library/%{library} %{buildroot}%{php_home}/%{library}


%check
%if %{with_tests}
mkdir vendor
cat << EOF | tee vendor/autoload.php
<?php
require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\\Loader\\AutoloaderFactory::factory(array(
    'Zend\\Loader\\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendTest\\\\Xml' => dirname(__DIR__).'/tests/ZendXmlTest',
           '%{library}'      => '%{buildroot}%{php_home}/%{library}'
))));
require_once '%{php_home}/Zend/autoload.php';
EOF
cd tests
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
%doc README.md
%doc composer.json
%{php_home}/%{library}


%changelog
* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- initial package