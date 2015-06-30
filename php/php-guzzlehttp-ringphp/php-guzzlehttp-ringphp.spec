# remirepo spec for php-guzzlehttp-ringphp, from Fedora:
#
# Fedora spec file for php-guzzlehttp-ringphp
#
# Copyright (c) 2014-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     guzzle
%global github_name      RingPHP
%global github_version   1.1.0
%global github_commit    dbbb91d7f6c191e5e405e900e3102ac7f261bc0b

%global composer_vendor  guzzlehttp
%global composer_project ringphp

# "php": ">=5.4.0"
%global php_min_ver      5.4.0
# "guzzlehttp/streams": "~3.0"
#     Note: Min version not "3.0" because autoloader required
%global streams_min_ver  3.0.0-3
%global streams_max_ver  4.0
# "react/promise": "~2.0"
#     Note: Min version not "2.0" because autoloader required
%global promise_min_ver  2.2.0-4
%global promise_max_ver  3.0

%if 0%{?rhel} == 5
# no nodejs available in RHEL-5
%global with_tests %{?_with_tests:1}%{!?_with_tests:0}
%else
# Build using "--without tests" to disable tests
%global with_tests %{?_without_tests:0}%{!?_without_tests:1}
%endif

%{!?phpdir:    %global phpdir    %{_datadir}/php}
%{!?testsdir:  %global testsdir  %{_datadir}/tests}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       5%{?github_release}%{?dist}
Summary:       Simple handler system used to power clients and servers in PHP

Group:         Development/Libraries
License:       MIT
URL:           http://ringphp.readthedocs.org
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: nodejs
BuildRequires: %{_bindir}/phpunit
## composer.json
BuildRequires: php(language)                    >= %{php_min_ver}
#BuildRequires: php-composer(guzzlehttp/streams) >= %%{streams_min_ver}
BuildRequires: php-guzzlehttp-streams           >= %{streams_min_ver}
#BuildRequires: php-composer(react/promise)      >= %%{promise_min_ver}
BuildRequires: php-react-promise                >= %{promise_min_ver}
BuildRequires: php-curl
## phpcompatinfo (computed from version 1.1.0)
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
BuildRequires: php-zlib
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                    >= %{php_min_ver}
#Requires:      php-composer(guzzlehttp/streams) >= %%{streams_min_ver}
Requires:      php-guzzlehttp-streams           >= %{streams_min_ver}
Requires:      php-composer(guzzlehttp/streams) <  %{streams_max_ver}
#Requires:      php-composer(react/promise)      >= %%{promise_min_ver}
Requires:      php-react-promise                >= %{promise_min_ver}
Requires:      php-composer(react/promise)      <  %{promise_max_ver}
# composer.json: optional
Requires:      php-curl
# phpcompatinfo (computed from version 1.1.0)
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Provides low level APIs used to power HTTP clients and servers through a simple,
PHP callable that accepts a request hash and returns a future response hash.
RingPHP supports both synchronous and asynchronous workflows by utilizing both
futures and promises [1].

RingPHP is inspired by Clojure's Ring [2], but has been modified to accommodate
clients and servers for both blocking and non-blocking requests.

[1] https://github.com/reactphp/promise
[2] https://github.com/ring-clojure/ring


# ------------------------------------------------------------------------------


%package tests

Summary:  Tests for %{name}
Group:    Development/Libraries

Requires: %{name} = %{version}-%{release}
Requires: nodejs
Requires: php-composer(phpunit/phpunit)
# phpcompatinfo (computed from version 1.1.0)
Requires: php-json
Requires: php-pcre
Requires: php-reflection
Requires: php-zlib

%description tests
%{summary}.


# ------------------------------------------------------------------------------


%prep
%setup -qn %{github_name}-%{github_commit}

: Create library autoloader
(cat <<'AUTOLOAD'
<?php
/**
 * Autoloader created by %{name}-%{version}-%{release}
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

require_once '%{phpdir}/GuzzleHttp/Stream/autoload.php';
require_once '%{phpdir}/React/Promise/autoload.php';

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('GuzzleHttp\\Ring\\', dirname(dirname(__DIR__)));

return $fedoraClassLoader;
AUTOLOAD
) | tee src/autoload.php

: Create tests autoloader
(cat <<'AUTOLOAD'
<?php
/**
 * Autoloader created by %{name}-tests-%{version}-%{release}
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

require_once 'GuzzleHttp/Ring/autoload.php';

$fedoraClassLoader->addPrefix('GuzzleHttp\\Tests\\Ring\\', __DIR__);
$fedoraClassLoader->setUseIncludePath(true);

return $fedoraClassLoader;
AUTOLOAD
) | tee tests/autoload.php

: Create custom tests PHPUnit config
rm -f phpunit.xml.dist
(cat <<'PHPUNIT'
<?xml version="1.0" encoding="UTF-8"?>
<phpunit bootstrap="./bootstrap.php" colors="true">
    <testsuites>
        <testsuite>
            <directory>.</directory>
        </testsuite>
    </testsuites>
</phpunit>
PHPUNIT
) | tee phpunit.xml.dist

: Modify tests bootstrap
sed -e "s#.*require.*autoload.*#require __DIR__ . '/autoload.php';#" \
    -e "s#Client/Server.php#GuzzleHttp/Tests/Ring/Client/Server.php#" \
    -i tests/bootstrap.php


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

: Library
mkdir -p %{buildroot}%{phpdir}/GuzzleHttp/Ring
cp -rp src/* %{buildroot}%{phpdir}/GuzzleHttp/Ring/

: Tests -- classes must be PSR-0
mkdir -p %{buildroot}%{testsdir}/%{name}/GuzzleHttp/Tests/Ring
cp -rp tests/* %{buildroot}%{testsdir}/%{name}/GuzzleHttp/Tests/Ring/
mv %{buildroot}%{testsdir}/%{name}/GuzzleHttp/Tests/Ring/{autoload,bootstrap}.php \
    %{buildroot}%{testsdir}/%{name}/
cp -p phpunit.xml.dist %{buildroot}%{testsdir}/%{name}/


%check
%if %{with_tests}
%{_bindir}/phpunit -v \
    --configuration %{buildroot}%{testsdir}/%{name} \
    --include-path %{buildroot}%{phpdir}
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc *.rst
%doc composer.json
%{phpdir}/GuzzleHttp/Ring

%files tests
%{testsdir}/%{name}


%changelog
* Sun Jun 28 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.0-5
- Autoloader updates

* Fri Jun 12 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.0-3
- Fix tests' autoload

* Fri Jun 12 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.0-2
- Use new $fedoraClassLoader concept in autoloader
- Remove secondary "tests" directory from tests sub-package

* Mon Jun 01 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.0-1
- Updated to 1.1.0
- Updated source URL
- Added autoloader
- Sub-packaged tests

* Fri Feb 13 2015 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- backport for remi repository

* Sun Dec 28 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.5-1
- Updated to 1.0.5

* Thu Nov 13 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.3-1
- Updated to 1.0.3
- Removed color turn off and default timezone for phpunit

* Mon Oct 27 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.1-1
- Initial package
