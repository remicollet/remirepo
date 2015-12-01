#
# Fedora spec file for php-behat-mink
#
# Copyright (c) 2015 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     minkphp
%global github_name      Mink
%global github_version   1.7.0
%global github_commit    6c129030ec2cc029905cf969a56ca8f087b2dfdf

%global composer_vendor  behat
%global composer_project mink

# "php": ">=5.3.1"
%global php_min_ver 5.3.1
# "symfony/css-selector": "~2.1"
#     NOTE: Min version not 2.1 because autoloader required
%global symfony_min_ver %{?el6:2.3.31}%{!?el6:2.7.1}
%global symfony_max_ver 3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%global phpdir   %{_datadir}/php
%global testsdir %{_datadir}/tests

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       Browser controller/emulator abstraction for PHP

Group:         Development/Libraries
License:       MIT
URL:           http://mink.behat.org/
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

# Modify driver testsuite bootstrap
Patch0:        %{name}-driver-testsuite-bootstrap.patch

BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language)                      >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(symfony/css-selector) >= %{symfony_min_ver}
## phpcompatinfo (computed from version 1.7.0)
BuildRequires: php-dom
BuildRequires: php-gd
BuildRequires: php-json
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-session
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                      >= %{php_min_ver}
Requires:      php-composer(symfony/css-selector) >= %{symfony_min_ver}
Requires:      php-composer(symfony/css-selector) <  %{symfony_max_ver}
# phpcompatinfo (computed from version 1.7.0)
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
One of the most important parts in the web is a browser. Browser is the window
through which web users interact with web applications and other users. Users
are always talking with web applications through browsers.

So, in order to test that our web application behaves correctly, we need a way
to simulate this interaction between the browser and the web application in our
tests. We need a Mink.

Mink is an open source browser controller/emulator for web applications,
written in PHP.

Read Mink at a Glance [1] to learn more about Mink and why you need it.

Autoloader: %{phpdir}/Behat/Mink/autoload.php

[1] http://mink.behat.org/en/latest/at-a-glance.html

# ------------------------------------------------------------------------------

%package driver-testsuite

Summary:   Mink driver testsuite

Requires:  %{name} = %{version}-%{release}
# phpcompatinfo (computed from version 1.7.0)
Requires:  php-gd
Requires:  php-json
Requires:  php-pcre
Requires:  php-reflection
Requires:  php-session
Requires:  php-spl

# Bundled
## driver-testsuite/web-fixtures/js/jquery-1.6.2-min.js
Provides:  bundled(js-jquery1) = 1.6.2
## driver-testsuite/web-fixtures/js/jquery-ui-1.8.14.custom.min.js
Provides:  bundled(js-jquery-ui) = 1.8.14

%description driver-testsuite
%{summary}.

Autoloader: %{testsdir}/%{name}-driver-testsuite/autoload.php
Bootstrap: %{testsdir}/%{name}-driver-testsuite/boostrap.php

# ------------------------------------------------------------------------------

%prep
%setup -qn %{github_name}-%{github_commit}

: Create library autoloader
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

$fedoraClassLoader->addPrefix('Behat\\Mink\\', dirname(dirname(__DIR__)));

require_once '%{phpdir}/Symfony/Component/CssSelector/autoload.php';

return $fedoraClassLoader;
AUTOLOAD

: Make PSR-0 driver testsuite tests
# Separate "tests-psr0" and "tests" directories so driver testsuite users (other
#     packages) do not need to update their code
mkdir -p driver-testsuite/tests-psr0/Behat/Mink/Tests/
ln -s ../../../../tests driver-testsuite/tests-psr0/Behat/Mink/Tests/Driver

: Create driver testsuite autoloader
cat <<'AUTOLOAD' | tee driver-testsuite/autoload.php
<?php
/**
 * Autoloader for %{name}-driver-testsuite and its' dependencies
 * (created by %{name}-driver-testsuite-%{version}-%{release}).
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

$fedoraClassLoader = require '%{phpdir}/Behat/Mink/autoload.php';
$fedoraClassLoader->addPrefix('Behat\\Mink\\Tests\\Driver\\', __DIR__ . '/tests-psr0');

return $fedoraClassLoader;
AUTOLOAD

: Patch driver testsuite bootstrap
%patch0 -p1


%build
# Empty build section, nothing to build


%install
: Library
mkdir -p  %{buildroot}%{phpdir}/Behat/Mink
cp -pr src/* %{buildroot}%{phpdir}/Behat/Mink/

: Driver testsuite
mkdir -p %{buildroot}%{testsdir}
cp -pr driver-testsuite %{buildroot}%{testsdir}/%{name}-driver-testsuite


%check
%if %{with_tests}
: Make PSR-0 tests
mkdir -p tests-psr0/Behat/Mink/
ln -s ../../../tests tests-psr0/Behat/Mink/Tests

: Create tests autoloader
cat <<'AUTOLOAD' | tee tests-psr0/autoload.php
<?php
$fedoraClassLoader = require_once '%{buildroot}%{phpdir}/Behat/Mink/autoload.php';
$fedoraClassLoader->addPrefix('Behat\\Mink\\Tests\\', __DIR__);
AUTOLOAD

%if 0%{?el6}
: Skip tests requiring PHPUnit with the "willReturn" function
sed 's/function testCreateNodeElements/function SKIP_testCreateNodeElements/' \
    -i tests/Driver/CoreDriverTest.php
sed 's/function testGetResponseHeader/function SKIP_testGetResponseHeader/' \
    -i tests/SessionTest.php
sed 's/function testAddressEqualsEmptyPath/function SKIP_testAddressEqualsEmptyPath/' \
    -i tests/WebAssertTest.php
%endif

: Run tests
%{_bindir}/phpunit --verbose --bootstrap tests-psr0/autoload.php
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%dir %{phpdir}/Behat
     %{phpdir}/Behat/Mink

%files driver-testsuite
%dir %{testsdir}
     %{testsdir}/%{name}-driver-testsuite


%changelog
* Wed Nov 25 2015 Shawn Iwinski <shawn@iwin.ski> - 1.7.0-1
- Initial package
