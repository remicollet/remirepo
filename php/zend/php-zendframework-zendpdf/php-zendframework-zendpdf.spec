# remirepo/Fedora spec file for php-zendframework-zendpdf
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    041f90c339cff63a3c4d03a28ef1ea5188059793
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zendpdf
%global php_home     %{_datadir}/php
%global library      ZendPdf
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.0.2
Release:        1%{?dist}
Summary:        Zend Framework %{library} component

Group:          Development/Libraries
License:        BSD
URL:            https://framework.zend.com/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh
Source2:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-ctype
BuildRequires:  php-date
BuildRequires:  php-gd
BuildRequires:  php-iconv
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-zlib
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  php-composer(%{gh_owner}/zend-memory)           >= 2.0.0
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.0.0
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)
%endif

# From composer, "require": {
#        "php": ">=5.3.3",
#        "zendframework/zend-memory": ">=2.0.0",
#        "zendframework/zend-stdlib": ">=2.0.0"
Requires:       php(language) >= 5.3.3
Requires:       php-composer(%{gh_owner}/zend-memory)           >= 2.0.0
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.0.0
# From phpcompatinfo report for version 1.0.1
Requires:       php-ctype
Requires:       php-date
Requires:       php-gd
Requires:       php-iconv
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-spl
Requires:       php-zlib

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
%{summary}.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}
cp -pr library/%{library} %{buildroot}%{php_home}/%{library}

install -pm 644 %{SOURCE2} %{buildroot}%{php_home}/%{library}/autoload.php


%check
%if %{with_tests}
mkdir vendor
cat << EOF | tee vendor/autoload.php
<?php
require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\\Loader\\AutoloaderFactory::factory(array(
    'Zend\\Loader\\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendTest\\\\%{library}' => dirname(__DIR__).'/tests/ZendXmlTest'
))));
require_once '%{buildroot}%{php_home}/%{library}/autoload.php';
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
%license LICENSE.txt
%doc README.md
%doc composer.json
%{php_home}/%{library}


%changelog
* Thu Aug  6 2015 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- initial package