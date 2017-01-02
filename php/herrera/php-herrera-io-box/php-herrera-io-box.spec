# remirepo/fedora spec file for php-herrera-io-box
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    b55dceb5c65cc831e94ec0786b0b9b15f1103e8e
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     box-project
%global gh_project   box2-lib
%global php_home     %{_datadir}/php
%global ns_vendor    Herrera
%global ns_project   Box
%global c_vendor     herrera-io
%global c_project    box
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{c_vendor}-%{c_project}
Version:        1.6.1
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        A library for simplifying the PHAR build process

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

Source1:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-phar
BuildRequires:  php-bz2
BuildRequires:  php-hash
BuildRequires:  php-json
BuildRequires:  php-openssl
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-tokenizer
BuildRequires:  php-composer(tedivm/jshrink) >= 1.0
BuildRequires:  php-composer(phine/path) >= 1.0
# From composer.json, "require-dev": {
#        "herrera-io/annotations": "~1.0",
#        "herrera-io/phpunit-test-case": "1.*",
#        "mikey179/vfsStream": "1.1.0",
#        "phpunit/phpunit": "3.7.*",
#        "phpseclib/phpseclib": "~0.3"
BuildRequires:  php-composer(%{c_vendor}/annotations) >= 1.0
BuildRequires:  php-composer(%{c_vendor}/phpunit-test-case) >= 1
BuildRequires:  php-composer(mikey179/vfsStream) >= 1.1.0
BuildRequires:  php-composer(phpunit/phpunit) >= 3.7
BuildRequires:  php-phpseclib-crypt-rsa
# Autoloader
BuildRequires:  php-composer(symfony/class-loader)
%endif

# from composer.json, "require": {
#        "php": ">=5.3.3",
#        "ext-phar": "*",
#        "tedivm/jshrink": "~1.0",
#        "phine/path": "~1.0"
Requires:       php(language) >= 5.3.3
Requires:       php-phar
Requires:       php-composer(tedivm/jshrink) >= 1.0
Requires:       php-composer(tedivm/jshrink) <  2
Requires:       php-composer(phine/path) >= 1.0
Requires:       php-composer(phine/path) <  2
# From composer.json, "suggest": {
#        "herrera-io/annotations": "For compacting annotated docblocks.",
#        "phpseclib/phpseclib": "For verifying OpenSSL signed phars without the phar extension."
Requires:       php-composer(%{c_vendor}/annotations)
Requires:       php-phpseclib-crypt-rsa

# Autoloader
Requires:       php-composer(symfony/class-loader)
# from phpcompatinfo report for version 1.6.1
Requires:       php-bz2
Requires:       php-hash
Requires:       php-json
Requires:       php-openssl
Requires:       php-pcre
Requires:       php-spl
Requires:       php-tokenizer

Provides:       php-composer(%{c_vendor}/%{c_project}) = %{version}


%description
%{summary}.

Box is a library built on the Phar class. It is designed to make it easier
to create new phars and modifying existing ones. Features include compacting
source files, better custom stub generation, and better OpenSSL signing
handling.

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE1} src/lib/%{ns_vendor}/%{ns_project}/autoload.php


%build
# Empty


%install
rm -rf                      %{buildroot}
mkdir -p                    %{buildroot}%{php_home}
cp -pr src/lib/%{ns_vendor} %{buildroot}%{php_home}/%{ns_vendor}


%check
%if %{with_tests}
cat << 'EOF' | tee src/tests/bootstrap.php
<?php
// Resources are only used in test suite
if (!defined('RES_DIR')) define('RES_DIR', __DIR__ . '/../../res');
// This library
require_once '%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';
// Dependencies
require_once '%{php_home}/%{ns_vendor}/PHPUnit/autoload.php';
require_once '%{php_home}/org/bovigo/vfs/autoload.php';
// From old bootstrap
org\bovigo\vfs\vfsStreamWrapper::register();
// Test classes
$fedoraClassLoader->addPrefix('Herrera\\Box\\Tests\\', __DIR__);
EOF

: Ignore test failing only in mock
sed -e 's/testVerifyErrorHandlingBug/skipVerifyErrorHandlingBug/' \
    -i src/tests/Herrera/Box/Tests/Signature/OpenSslTest.php
sed -e 's/testFindStubLengthOpenError/skipFindStubLengthOpenError/' \
    -i src/tests/Herrera/Box/Tests/ExtractTest.php
sed -e '/strict/d' phpunit.xml.dist >phpunit.xml

%{_bindir}/php -d phar.readonly=0 \
%{_bindir}/phpunit \
   --verbose
%else
: test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%doc composer.json
%{php_home}/%{ns_vendor}/%{ns_project}


%changelog
* Tue Oct 27 2015 Remi Collet <remi@fedoraproject.org> - 1.6.1-1
- initial package