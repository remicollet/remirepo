#
# Fedora spec file for php-jakub-onderka-php-console-color
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     JakubOnderka
%global github_name      PHP-Console-Color
%global github_version   0.1
%global github_commit    e0b393dacf7703fc36a4efc3df1435485197e6c1

%global composer_vendor  jakub-onderka
%global composer_project php-console-color

# "php": ">=5.3.2"
%global php_min_ver 5.3.2

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Simple library for creating colored console ouput

Group:         Development/Libraries
License:       BSD
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

# Add LICENSE file
# https://github.com/JakubOnderka/PHP-Console-Color/pull/8
# https://patch-diff.githubusercontent.com/raw/JakubOnderka/PHP-Console-Color/pull/8.patch
Patch0:        %{name}-pr8-add-license.patch

BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
## phpcompatinfo (computed from version 0.1)
BuildRequires: php-pcre
BuildRequires: php-posix
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 0.1)
Requires:      php-pcre
Requires:      php-posix
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.

Autoloader: %{phpdir}/JakubOnderka/PhpConsoleColor/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Add LICENSE file
%patch0 -p1

: Modify example.php to use generated autoloader
sed "/require_once/s#.*#require_once '%{phpdir}/JakubOnderka/PhpConsoleColor/autoload.php';#" \
    -i example.php


%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/JakubOnderka/PhpConsoleColor/autoload.php
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

$fedoraClassLoader->addPrefix('JakubOnderka\\PhpConsoleColor\\', dirname(dirname(__DIR__)));

return $fedoraClassLoader;
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
%{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}%{phpdir}/JakubOnderka/PhpConsoleColor/autoload.php
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json
%doc example.php
%dir %{phpdir}/JakubOnderka
     %{phpdir}/JakubOnderka/PhpConsoleColor


%changelog
* Fri Jul 15 2016 Shawn Iwinski <shawn@iwin.ski> - 0.1-1
- Initial package
