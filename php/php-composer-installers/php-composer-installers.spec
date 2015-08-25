#
# Fedora spec file for php-composer-installers
#
# Copyright (c) 2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     composer
%global github_name      installers
%global github_version   1.0.21
%global github_commit    d64e23fce42a4063d63262b19b8e7c0f3b5e4c45

%global composer_vendor  composer
%global composer_project installers

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       A multi-framework Composer library installer

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

# Fix PHPUnit check in CakePHPInstallerTest
# https://github.com/composer/installers/pull/226
Patch0:        %{name}-pr226.patch

BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: %{_bindir}/phpunit
BuildRequires: php-composer(composer/composer)
## phpcompatinfo (computed from version 1.0.21)
BuildRequires: php(language) >= 5.3.0
BuildRequires: php-pcre
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

Requires:      php-composer(composer/composer)
# phpcompatinfo (computed from version 1.0.21)
Requires:      php(language) >= 5.3.0
Requires:      php-pcre
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
This is for PHP package authors to require in their composer.json. It will
install their package to the correct location based on the specified package
type.

The goal of installers is to be a simple package type to install path map.
Users can also customize the install path per package and package authors
can modify the package name upon installing.

installers isn't intended on replacing all custom installers. If your package
requires special installation handling then by all means, create a custom
installer to handle it.


%prep
%setup -qn %{github_name}-%{github_commit}

%patch0 -p1

: Create autoloader
cat <<'AUTOLOAD' | tee src/Composer/Installers/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 *
 * Created by %{name}-%{version}-%{release}
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

$fedoraClassLoader->addPrefix('Composer\\Installers\\', dirname(dirname(__DIR__)));

require_once '%{phpdir}/Composer/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing to build


%install
mkdir -p %{buildroot}%{phpdir}
cp -rp src/Composer %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require_once '%{buildroot}%{phpdir}/Composer/Installers/autoload.php';
$fedoraClassLoader->addPrefix('Composer\\Installers\\Test\\', __DIR__ . '/tests');
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
%{phpdir}/Composer/Installers


%changelog
* Thu Aug 20 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.21-1
- Initial package
