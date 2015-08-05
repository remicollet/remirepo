# remirepo spec/Fedora file for php-zendframework-zend-crypt
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    15537e8e438a98923f05c40c45c162342ea8235a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-crypt
%global php_home     %{_datadir}/php
%global library      Crypt
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.5.1
Release:        2%{?dist}
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
BuildRequires:  php-mcrypt
BuildRequires:  php-hash
BuildRequires:  php-openssl
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-math)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.5
# From composer, "require-dev": {
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.0",
#        "zendframework/zend-config": "~2.5"
BuildRequires:  php-composer(%{gh_owner}/zend-config)           >= 2.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": ">=5.3.23",
#        "zendframework/zend-math": "~2.5",
#        "zendframework/zend-stdlib": "~2.5",
#        "zendframework/zend-servicemanager": "~2.5"
Requires:       php(language) >= 5.3.23
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-math)             >= 2.5
Requires:       php-composer(%{gh_owner}/zend-math)             <  3
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  3
Requires:       php-composer(%{gh_owner}/zend-servicemanager)   >= 2.5
Requires:       php-composer(%{gh_owner}/zend-servicemanager)   <  3
# From composer, "suggest": {
#        "ext-mcrypt": "Required for most features of Zend\\Crypt"
# https://github.com/zendframework/zend-crypt/issues/3
Requires:       php-mcrypt
%endif
# From phpcompatinfo report for version 2.5.2
Requires:       php-hash
Requires:       php-openssl
Requires:       php-pcre
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Crypt provides support of some cryptographic tools.
The available features are:
* encrypt-then-authenticate using symmetric ciphers
  (the authentication step is provided using HMAC);
* encrypt/decrypt using symmetric and public key algorithm
  (e.g. RSA algorithm);
* generate digital sign using public key algorithm (e.g. RSA algorithm);
* key exchange using the Diffie-Hellman method;
* key derivation function (e.g. using PBKDF2 algorithm);
* secure password hash (e.g. using Bcrypt algorithm);
* generate Hash values;
* generate HMAC values;

The main scope of this component is to offer an easy and secure way
to protect and authenticate sensitive data in PHP.


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
* Wed Aug  5 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-2
- fix dependencies

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package