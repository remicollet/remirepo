#
# Fedora spec file for php-di-symfony2-bridge
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     PHP-DI
%global github_name      Symfony2-Bridge
%global github_version   1.1.0
%global github_commit    e197ddc965e21c8b865a74d45dd73e334b674bd3

%global composer_vendor  php-di
%global composer_project symfony2-bridge

# "php-di/php-di": "~4.0 || ^5.0"
%global di_min_ver 4.0
%global di_max_ver 6.0
# "symfony/dependency-injection": "~2.0"
%global symfony_min_ver 2.0
%global symfony_max_ver 3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          %{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       PHP-DI integration with Symfony 2

Group:         Development/Libraries
License:       MIT
URL:           http://php-di.org/doc/frameworks/symfony2.html

# GitHub export does not include tests.
# Run php-di-symfony2-bridge-get-source.sh to create full source.
Source0:       %{name}-%{github_version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php-composer(php-di/php-di)                >= %{di_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(symfony/dependency-injection) >= %{symfony_min_ver}
## phpcompatinfo (computed from version 1.1.0)
BuildRequires: php(language)                              >= 5.3.0
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php-composer(php-di/php-di)                >= %{di_min_ver}
Requires:      php-composer(php-di/php-di)                <  %{di_max_ver}
Requires:      php-composer(symfony/dependency-injection) >= %{symfony_min_ver}
Requires:      php-composer(symfony/dependency-injection) <  %{symfony_max_ver}
# phpcompatinfo (computed from version 1.1.0)
Requires:      php(language)                              >= 5.3.0
# Autoloader
Requires:      php-composer(symfony/class-loader)

# php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}
Provides:      php-%{composer_vendor}-%{composer_project}           = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.

Autoloader: %{phpdir}/DI/Bridge/Symfony/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee src/DI/Bridge/Symfony/autoload.php
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

$fedoraClassLoader->addPrefix('DI\\Bridge\\Symfony\\', dirname(dirname(dirname(__DIR__))));

// Required dependencies
require_once '%{phpdir}/DI/autoload.php';
require_once '%{phpdir}/Symfony/Component/DependencyInjection/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing to build


%install
mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
$fedoraClassLoader = require '%{buildroot}%{phpdir}/DI/Bridge/Symfony/autoload.php';
$fedoraClassLoader->addPrefix('FunctionalTest\\DI\\Bridge\\Symfony\\', __DIR__.'/tests');
$fedoraClassLoader->addPrefix('UnitTest\\DI\\Bridge\\Symfony\\', __DIR__.'/tests');
BOOTSTRAP

: Run tests
%{_bindir}/phpunit --verbose --bootstrap bootstrap.php
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%dir %{phpdir}/DI/Bridge
     %{phpdir}/DI/Bridge/Symfony


%changelog
* Sun Jan 03 2016 Shawn Iwinski <shawn@iwin.ski> - 1.1.0-1
- Initial package
