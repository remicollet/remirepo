# remirepo spec file for php-aws-php-sns-message-validator, from:
#
# Fedora spec file for php-aws-php-sns-message-validator
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     aws
%global github_name      aws-php-sns-message-validator
%global github_version   1.1.0
%global github_commit    c9fce7635417bcc75383ec5f6fa3790a4d9729b8

%global composer_vendor  aws
%global composer_project aws-php-sns-message-validator

# "php": ">=5.4"
%global php_min_ver 5.4

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Amazon SNS message validation

Group:         Development/Libraries
License:       ASL 2.0
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-openssl
## phpcompatinfo (computed from version 1.1.0)
BuildRequires: php-date
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-openssl
# phpcompatinfo (computed from version 1.1.0)
Requires:      php-json
Requires:      php-pcre
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming
Provides:      php-%{composer_vendor}-%{composer_project} = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
The Amazon SNS Message Validator for PHP library allows you to validate that
incoming HTTP(S) POST messages are valid Amazon SNS notifications. This library
is standalone and does not depend on the AWS SDK for PHP or Guzzle.

Autoloader: %{phpdir}/Aws/Sns/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Aws\\Sns\\', dirname(dirname(__DIR__)));

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}/Aws/Sns
cp -rp src/* %{buildroot}%{phpdir}/Aws/Sns/


%check
%if %{with_tests}
: Make PSR-0 tests
mkdir -p tests-psr0/Aws
ln -s ../../tests tests-psr0/Aws/Sns

: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require_once '%{buildroot}%{phpdir}/Aws/Sns/autoload.php';
$fedoraClassLoader->addPrefix('Aws\\Sns\\', __DIR__.'/tests-psr0');
BOOTSTRAP

%{_bindir}/phpunit --verbose --bootstrap bootstrap.php

if which php70; then
   php70 %{_bindir}/phpunit --verbose --bootstrap bootstrap.php
fi
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc composer.json
%doc README.md
%dir %{phpdir}/Aws
     %{phpdir}/Aws/Sns


%changelog
* Sat Apr 16 2016 Remi Collet <remi@remirepo.net> - 1.1.0-1
- backport for remi repository

* Mon Apr 11 2016 Shawn Iwinski <shawn@iwin.ski> - 1.1.0-1
- Initial package
