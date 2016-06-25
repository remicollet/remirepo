# remirepo/Fedora spec file for php-zendframework-zend-soap
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    2d6012e7231cce550219eccfc80836a028d20bf1
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-soap
%global php_home     %{_datadir}/php
%global library      Soap
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.6.0
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
BuildRequires:  php-curl
BuildRequires:  php-dom
BuildRequires:  php-libxml
BuildRequires:  php-pcre
BuildRequires:  php-soap
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-server)           >= 2.6.1
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
BuildRequires:  php-composer(%{gh_owner}/zend-uri)              >= 2.5.2
# From composer, "require-dev": {
#        "zendframework/zend-config": "^2.6",
#        "zendframework/zend-http": "^2.5.4",
#        "phpunit/PHPUnit": "^4.8",
#        "squizlabs/php_codesniffer": "^2.3.1"
BuildRequires:  php-composer(%{gh_owner}/zend-config)           >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-http)             >= 2.5.4
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.8
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "zendframework/zend-server": "^2.6.1",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0",
#        "zendframework/zend-uri": "^2.5.2"
Requires:       php(language) >= 5.5
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-server)           >= 2.6.1
Requires:       php-composer(%{gh_owner}/zend-server)           <  3
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  4
Requires:       php-composer(%{gh_owner}/zend-uri)              >= 2.5.2
Requires:       php-composer(%{gh_owner}/zend-uri)              <  3
# From composer, "suggest": {
#        "zendframework/zend-http": "Zend\\Http component"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-http)
%endif
%endif
# From phpcompatinfo report for version 2.5.1
Requires:       php-curl
Requires:       php-dom
Requires:       php-libxml
Requires:       php-pcre
Requires:       php-soap
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Soap is a component to manage the SOAP protocol in order
to design client or server PHP application.

Documentation: https://zendframework.github.io/%{gh_project}/


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
require_once 'test/TestAsset/commontypes.php';
require_once 'test/TestAsset/call_user_func.php';
EOF

%{_bindir}/phpunit --include-path=%{buildroot}%{php_home}

if which php70; then
   php70 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home} || : ignore
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
* Fri Apr 22 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0
- raise dependency on PHP >= 5.5
- raise dependency on zend-server >= 2.6.1
- raise dependency on zend-stdlib >= 2.7
- raise dependency on zend-uri >= 2.5.2

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
