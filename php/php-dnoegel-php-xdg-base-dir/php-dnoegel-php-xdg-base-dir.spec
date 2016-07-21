#
# Fedora spec file for php-dnoegel-php-xdg-base-dir
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     dnoegel
%global github_name      php-xdg-base-dir
%global github_version   0.1
%global github_commit    265b8593498b997dc2d31e75b89f053b5cc9621a

%global composer_vendor  dnoegel
%global composer_project php-xdg-base-dir

# "php": ">=5.3.2"
%global php_min_ver 5.3.2

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Implementation of the XDG Base Directory Specification for PHP

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
## phpcompatinfo (computed from version 0.1)
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 0.1)
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.

Autoloader: %{phpdir}/XdgBaseDir/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}


%build
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

$fedoraClassLoader->addPrefix('XdgBaseDir\\', dirname(__DIR__));

return $fedoraClassLoader;
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}/XdgBaseDir
cp -rp src/* %{buildroot}%{phpdir}/XdgBaseDir/


%check
%if %{with_tests}
sed 's#rmdir\($runtimeDir\);#rmdir($runtimeDir); echo PHP_EOL,">>>>> runtimeDir=$runtimeDir",PHP_EOL;#' \
    -i tests/XdgTest.php

: Skip test known to fail in rpmbuild env
sed 's/function testGetRuntimeShouldDeleteDirsWithWrongPermission/function SKIP_testGetRuntimeShouldDeleteDirsWithWrongPermission/' \
    -i tests/XdgTest.php

%{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}%{phpdir}/XdgBaseDir/autoload.php
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{phpdir}/XdgBaseDir


%changelog
* Fri Jul 15 2016 Shawn Iwinski <shawn@iwin.ski> - 0.1-1
- Initial package
