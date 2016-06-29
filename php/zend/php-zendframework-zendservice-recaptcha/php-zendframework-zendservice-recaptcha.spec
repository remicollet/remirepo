# remirepo/Fedora spec file for php-zendframework-zendservice-recaptcha
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    4324cca8502d9f47b3b43a18acdd3fdbeb965536
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   ZendService_ReCaptcha
%global pk_project   zendservice-recaptcha
%global php_home     %{_datadir}/php
%global namespace    ZendService
%global library      ReCaptcha
%global with_tests   0%{!?_without_tests:1}

############# TODO seems dead / unmaintained - last commit in 2012 #########


Name:           php-%{gh_owner}-%{pk_project}
Version:        2.0.1
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
BuildRequires:  php-mcrypt
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  php-composer(%{gh_owner}/zend-http)             >= 2.0.0
BuildRequires:  php-composer(%{gh_owner}/zend-uri)              >= 2.0.0
BuildRequires:  php-composer(%{gh_owner}/zend-version)          >= 2.0.0
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)
%endif

# From composer, "require": {
#        "php": ">=5.3.3",
#        "zendframework/zend-http": ">=2.0.0",
#        "zendframework/zend-uri": ">=2.0.0",
#        "zendframework/zend-version": ">=2.0.0"
Requires:       php(language) >= 5.3.3
Requires:       php-composer(%{gh_owner}/zend-http)             >= 2.0.0
Requires:       php-composer(%{gh_owner}/zend-uri)              >= 2.0.0
Requires:       php-composer(%{gh_owner}/zend-version)          >= 2.0.0
# From phpcompatinfo report for version 2.0.1
Requires:       php-mcrypt

Provides:       php-composer(%{gh_owner}/%{pk_project}) = %{version}


%description
%{summary}.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}
cp -pr library/%{namespace} %{buildroot}%{php_home}/%{namespace}

install -pm 644 %{SOURCE2}  %{buildroot}%{php_home}/%{namespace}/%{library}/autoload.php


%check
%if %{with_tests}
mkdir vendor
cat << EOF | tee vendor/autoload.php
<?php
require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\\Loader\\AutoloaderFactory::factory(array(
    'Zend\\Loader\\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendServiceTest\\\\%{library}' => dirname(__DIR__).'/tests/ZendServiceTest/ReCaptcha'
))));
require_once '%{buildroot}%{php_home}/%{namespace}/%{library}/autoload.php';
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
* Thu Aug  6 2015 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- initial package