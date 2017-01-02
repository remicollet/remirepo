# remirepo/Fedora spec file for php-zendframework-zend-xmlrpc
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    04f5c91e4d15ab8ca379877ec962589c5e9b66d7
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-xmlrpc
%global php_home     %{_datadir}/php
%global library      XmlRpc
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
URL:            https://zendframework.github.io/%{gh_project}/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-simplexml
BuildRequires:  php-date
BuildRequires:  php-dom
BuildRequires:  php-iconv
BuildRequires:  php-libxml
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-xmlwriter
BuildRequires:  php-composer(%{gh_owner}/zend-http)             >= 2.5.4
BuildRequires:  php-composer(%{gh_owner}/zend-math)             >= 2.7
BuildRequires:  php-composer(%{gh_owner}/zend-server)           >= 2.7
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
BuildRequires:  php-composer(%{gh_owner}/zendxml)               >= 1.0.2
# From composer, "require-dev": {
#        "phpunit/PHPUnit": "^4.8",
#        "squizlabs/php_codesniffer": "^2.3.1"
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.8
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.6 || ^7.0",
#        "zendframework/zend-http": "^2.5.4",
#        "zendframework/zend-math": "^2.7 || ^3.0",
#        "zendframework/zend-server": "^2.7",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0",
#        "zendframework/zendxml": "^1.0.2"
Requires:       php(language) >= 5.6
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-http)             >= 2.5.4
Requires:       php-composer(%{gh_owner}/zend-http)             <  3
Requires:       php-composer(%{gh_owner}/zend-math)             >= 2.7
Requires:       php-composer(%{gh_owner}/zend-math)             <  4
Requires:       php-composer(%{gh_owner}/zend-server)           >= 2.7
Requires:       php-composer(%{gh_owner}/zend-server)           <  3
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  4
Requires:       php-composer(%{gh_owner}/zendxml)               >= 1.0.2
Requires:       php-composer(%{gh_owner}/zendxml)               <  2
# From composer, "suggest": {
#        "zendframework/zend-cache": "To support Zend\\XmlRpc\\Server\\Cache usage"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-cache)
%endif
%endif
# From phpcompatinfo report for version 2.5.2
Requires:       php-simplexml
Requires:       php-date
Requires:       php-dom
Requires:       php-iconv
Requires:       php-libxml
Requires:       php-pcre
Requires:       php-spl
Requires:       php-xmlwriter

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
From its home page, XML-RPC is described as a ”...remote procedure calling
using HTTP as the transport and XML as the encoding. XML-RPC is designed
to be as simple as possible, while allowing complex data structures to be
transmitted, processed and returned.”

Zend\XmlRpc provides support for both consuming remote XML-RPC services and
building new XML-RPC servers.

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
require_once 'test/TestAsset/functions.php';
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
%license LICENSE
%doc *.md
%doc composer.json
%{php_home}/Zend/%{library}


%changelog
* Tue Jun 21 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0
- raise dependency on PHP 5.6
- raise dependency on zend-server 2.7

* Fri Apr 22 2016 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- update to 2.5.2
- raise dependency on PHP >= 5.5
- raise dependency on zend-http >= 2.5.4
- raise dependency on zend-math >= 2.7
- raise dependency on zend-server >= 2.6.1
- raise dependency on zend-stdlib >= 2.7

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
