# remirepo spec file for php-react-promise, from Fedora:
#
# Fedora spec file for php-react-promise
#
# Copyright (c) 2014-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     reactphp
%global github_name      promise
%global github_version   2.4.0
%global github_commit    f942da7b505d1a294284ab343d05df42d02ad6d9

%global composer_vendor  react
%global composer_project promise

# "php": ">=5.4.0"
%global php_min_ver 5.4.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       A lightweight implementation of CommonJS Promises/A for PHP

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: %{_bindir}/phpunit
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
## phpcompatinfo (computed from version 2.4.0)
BuildRequires: php-json
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 2.4.0)
Requires:      php-json
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
A lightweight implementation of CommonJS Promises/A [1] for PHP.

[1] http://wiki.commonjs.org/wiki/Promises/A


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

$fedoraClassLoader->addPrefix('React\\Promise\\', dirname(dirname(__DIR__)));

require_once __DIR__ . '/functions_include.php';

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}/React/Promise
cp -rp src/* %{buildroot}%{phpdir}/React/Promise/


%check
%if %{with_tests}
: Restore PSR-0 for tests
mkdir -p psr-0/React/
mv tests psr-0/React/Promise
mv psr-0 tests
mv tests/React/Promise/fixtures/* tests/React/Promise/

: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php

require_once '%{buildroot}%{phpdir}/React/Promise/autoload.php';

$fedoraClassLoader->addPrefix(null, __DIR__ . '/tests');
BOOTSTRAP

%{_bindir}/phpunit --verbose --bootstrap ./bootstrap.php

if which php70; then
   php70 %{_bindir}/phpunit --verbose --bootstrap ./bootstrap.php
fi
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
%doc composer.json
%dir %{phpdir}/React
     %{phpdir}/React/Promise


%changelog
* Mon Apr 04 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.4.0-1
- Updated to 2.4.0 (RHBZ #1319558)

* Wed Sep 23 2015 Remi Collet <remi@remirepo.net> - 2.2.1-2
- clean from Fedora

* Tue Sep 22 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.2.0-7
- Minor updates

* Mon Aug 10 2015 Remi Collet <remi@remirepo.net> - 2.2.1-1
- update to 2.2.1

* Sun Jun 28 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.2.0-6
- Autoloader updates

* Fri Jun 12 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.2.0-4
- Use new $fedoraClassLoader concept in autoloader

* Mon Jun 01 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.2.0-3
- Use include path in autoloader

* Mon Jun 01 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.2.0-2
- Added autoloader

* Sun Jan 04 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.2.0-1
- Updated to 2.2.0 (BZ #1178411)

* Fri Oct 31 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- backport 2.1.0 for remi repo.

* Mon Oct 27 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.1.0-1
- Updated to 2.1.0

* Wed Oct 15 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.0.0-1
- Initial package
