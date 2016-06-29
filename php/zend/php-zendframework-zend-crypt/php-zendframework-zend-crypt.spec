# remirepo/Fedora spec file for php-zendframework-zend-crypt
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    ed348e3e87c945759d11edae5316125c3582bc72
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
Version:        3.0.0
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
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-mbstring
BuildRequires:  php-hash
BuildRequires:  php-openssl
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-math)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
BuildRequires:  php-composer(container-interop/container-interop) >= 1.0
# From composer, "require-dev": {
#        "squizlabs/php_codesniffer": "^2.3.1",
#        "phpunit/PHPUnit": "~4.8"
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.8
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
# For dependencies autoloader
BuildRequires:  php-zendframework-zend-loader                   >= 2.5.1-3
%endif

# From composer, "require": {
#        "php": "^5.6 || ^7.0",
#        "ext-mbstring": "*",
#        "zendframework/zend-math": "^3.0",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0",
#        "container-interop/container-interop": "~1.0"
Requires:       php(language) >= 5.6
Requires:       php-mbstring
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-math)             >= 3.0
Requires:       php-composer(%{gh_owner}/zend-math)             <  4
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  4
Requires:       php-composer(container-interop/container-interop) >= 1.0
Requires:       php-composer(container-interop/container-interop) <  2
# From composer, "suggest": {
#        "ext-openssl": "Required for most features of Zend\\Crypt"
Requires:       php-openssl
# Autoloader
Requires:       php-composer(%{gh_owner}/zend-loader)           >= 2.5
Requires:       php-zendframework-zend-loader                   >= 2.5.1-3
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

Documentation: https://zendframework.github.io/%{gh_project}/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

: Create dependency autoloader
cat << 'EOF' | tee autoload.php
<?php
require_once '%{php_home}/Interop/Container/autoload.php';
EOF


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/Zend/
cp -pr src %{buildroot}%{php_home}/Zend/%{library}

install -m644 autoload.php %{buildroot}%{php_home}/Zend/%{library}-autoload.php


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
define('RPM_BUILDROOT', '%{buildroot}%{php_home}/Zend');

require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\Loader\AutoloaderFactory::factory(array(
    'Zend\Loader\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendTest\\%{library}' => dirname(__DIR__).'/test/',
           'Zend\\%{library}'     => '%{buildroot}%{php_home}/Zend/%{library}'
))));
require_once '%{php_home}/Zend/autoload.php';
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
%license LICENSE.md
%doc CONTRIBUTING.md README.md
%doc composer.json
%{php_home}/Zend/%{library}
%{php_home}/Zend/%{library}-autoload.php


%changelog
* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- update to 3.0.0 for ZendFramework 3
- add dependencies autoloader
- raise dependency on PHP 5.6
- raise dependency on zend-math 3.0

* Thu Feb  4 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0
- raise dependency on zend-math ~2.6
- raise dependency on zend-stdlib ~2.7
- drop dependency on zend-servicemanager
- add dependency on container-interop/container-interop

* Wed Nov 25 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- update to 2.5.2
- raise dependency on PHP 5.5

* Wed Aug  5 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-2
- fix dependencies

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
