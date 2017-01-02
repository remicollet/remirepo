# remirepo/Fedora spec file for php-zendframework-zend-psr7bridge
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    86c0b53b0c6381391c4add4a93a56e51d5c74605
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-psr7bridge
%global php_home     %{_datadir}/php
%global library      Psr7Bridge
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        0.2.2
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
BuildRequires:  php-reflection
BuildRequires:  php-intl
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-http)             >= 2.5
BuildRequires:  php-composer(psr/http-message)                  >= 1.0
BuildRequires:  php-composer(%{gh_owner}/zend-diactoros)        >= 1.1
# From composer, "require-dev": {
#        "phpunit/phpunit": "^4.7",
#        "squizlabs/php_codesniffer": "^2.3"
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.7
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": ">=5.5",
#        "zendframework/zend-http": "^2.5",
#        "psr/http-message": "^1.0",
#        "zendframework/zend-diactoros": "^1.1"
Requires:       php(language) >= 5.5
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-http)             >= 2.5
Requires:       php-composer(%{gh_owner}/zend-http)             <  3
Requires:       php-composer(psr/http-message)                  >= 1.0
Requires:       php-composer(psr/http-message)                  <  2
Requires:       php-composer(%{gh_owner}/zend-diactoros)        >= 1.1
Requires:       php-composer(%{gh_owner}/zend-diactoros)        <  2
%endif
# From phpcompatinfo report for version 0.2.1 => Nothing

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Code for converting PSR-7 messages to zend-http messages, and vice versa.

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
* Wed May 11 2016 Remi Collet <remi@fedoraproject.org> - 0.2.2-1
- update to 0.2.2

* Wed Mar  2 2016 Remi Collet <remi@fedoraproject.org> - 0.2.1-1
- initial package
