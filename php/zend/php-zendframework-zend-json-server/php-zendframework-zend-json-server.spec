# remirepo/Fedora spec file for php-zendframework-zend-json-server
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    1dfcb6478952d7e271fbe07a241276b55dca91c5
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-json-server
%global php_home     %{_datadir}/php
%global library      Server
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        3.0.0
Release:        1%{?dist}
Summary:        Zend Json-Server is a JSON-RPC server implementation

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
BuildRequires:  php-reflection
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-json)               >= 2.6.1
BuildRequires:  php-composer(%{gh_owner}/zend-http)               >= 2.5.4
BuildRequires:  php-composer(%{gh_owner}/zend-server)             >= 2.6.1
# From composer, "require-dev": {
#        "squizlabs/php_codesniffer": "^2.3",
#        "phpunit/PHPUnit": "~4.0"
BuildRequires:  php-composer(phpunit/phpunit)                     >= 4.0
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)             >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "zendframework/zend-json": "^2.6.1 || ^3.0",
#        "zendframework/zend-http": "^2.5.4",
#        "zendframework/zend-server": "^2.6.1"
Requires:       php(language) >= 5.5
# Require zend-json 3.0.0 as conflicts with previous
Requires:       php-composer(%{gh_owner}/zend-json)               >= 3.0.0
Requires:       php-composer(%{gh_owner}/zend-json)               <  4
Requires:       php-composer(%{gh_owner}/zend-http)               >= 2.5.4
Requires:       php-composer(%{gh_owner}/zend-http)               <  3
Requires:       php-composer(%{gh_owner}/zend-server)             >= 2.6.1
Requires:       php-composer(%{gh_owner}/zend-server)             <  4
# From phpcompatinfo report for version 3.0.0
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Provides a JSON-RPC server implementation.

* File issues at https://github.com/zendframework/zend-json-server/issues
* Documentation is at http://framework.zend.com/manual/current/en/index.html#zend-json-server


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv LICENSE.md LICENSE


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/Zend/Json
cp -pr src %{buildroot}%{php_home}/Zend/Json/%{library}


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\Loader\AutoloaderFactory::factory(array(
    'Zend\Loader\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendTest\\Json\\%{library}' => dirname(__DIR__).'/test/',
           'Zend\\Json\\%{library}'     => '%{buildroot}%{php_home}/Zend/Json/%{library}'
))));
require_once '%{php_home}/Zend/autoload.php';
require_once __DIR__ . '/../test/TestAsset/FooFunc.php';
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
%{php_home}/Zend/Json/%{library}


%changelog
* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- initial package
