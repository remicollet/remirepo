# remirepo spec file for php-di, from:
#
# Fedora spec file for php-di
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     PHP-DI
%global github_name      PHP-DI
%global github_version   5.3.0
%global github_commit    854a6d8f54e2146f0a34f0a28f0adea688b634a3

%global composer_vendor  php-di
%global composer_project php-di

# "php": ">=5.5.0"
%global php_min_ver 5.5.0
# "container-interop/container-interop": "~1.0"
%global container_interop_min_ver 1.0
%global container_interop_max_ver 2.0
# "doctrine/annotations": "~1.2"
%global doctrine_annotations_min_ver 1.2
%global doctrine_annotations_max_ver 2.0
# "doctrine/cache": "~1.4"
%global doctrine_cache_min_ver 1.4
%global doctrine_cache_max_ver 2.0
# "mnapoli/phpunit-easymock": "~0.2.0"
%global phpunit_easymock_min_ver 0.2.0
%global phpunit_easymock_max_ver 1.0
# "php-di/invoker": "^1.1.1"
%global di_invoker_min_ver 1.1.1
%global di_invoker_max_ver 2.0
# "php-di/phpdoc-reader": "^2.0.1"
%global di_phpdoc_reader_min_ver 2.0.1
%global di_phpdoc_reader_max_ver 3.0
# "ocramius/proxy-manager": "~1.0|~2.0"
%global proxy_manager_min_ver 1.0
%global proxy_manager_max_ver 3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          %{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       The dependency injection container for humans

Group:         Development/Libraries
License:       MIT
URL:           http://php-di.org/

# GitHub export does not include tests.
# Run php-di-invoker-get-source.sh to create full source.
Source0:       %{name}-%{github_version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language)                                     >= %{php_min_ver}
BuildRequires: php-composer(container-interop/container-interop) >= %{container_interop_min_ver}
BuildRequires: php-composer(doctrine/annotations)                >= %{doctrine_annotations_min_ver}
BuildRequires: php-composer(doctrine/cache)                      >= %{doctrine_cache_min_ver}
BuildRequires: php-composer(mnapoli/phpunit-easymock)            >= %{phpunit_easymock_min_ver}
BuildRequires: php-composer(ocramius/proxy-manager)              >= %{proxy_manager_min_ver}
BuildRequires: php-composer(php-di/invoker)                      >= %{di_invoker_min_ver}
BuildRequires: php-composer(php-di/phpdoc-reader)                >= %{di_phpdoc_reader_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
## phpcompatinfo (computed from version 5.2.2)
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                                     >= %{php_min_ver}
Requires:      php-composer(container-interop/container-interop) >= %{container_interop_min_ver}
Requires:      php-composer(container-interop/container-interop) <  %{container_interop_max_ver}
Requires:      php-composer(php-di/invoker)                      >= %{di_invoker_min_ver}
Requires:      php-composer(php-di/invoker)                      <  %{di_invoker_max_ver}
Requires:      php-composer(php-di/phpdoc-reader)                >= %{di_phpdoc_reader_min_ver}
Requires:      php-composer(php-di/phpdoc-reader)                <  %{di_phpdoc_reader_max_ver}
# phpcompatinfo (computed from version 5.2.2)
Requires:      php-json
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)
# Weak dependencies
%if 0%{?fedora} >= 21
Suggests:      php-composer(doctrine/annotations)                >= %{doctrine_annotations_min_ver}
Suggests:      php-composer(doctrine/annotations)                <  %{doctrine_annotations_max_ver}
Suggests:      php-composer(doctrine/cache)                      >= %{doctrine_cache_min_ver}
Suggests:      php-composer(doctrine/cache)                      <  %{doctrine_cache_max_ver}
Suggests:      php-composer(mnapoli/phpunit-easymock)            >= %{phpunit_easymock_min_ver}
Suggests:      php-composer(mnapoli/phpunit-easymock)            <  %{phpunit_easymock_max_ver}
Suggests:      php-composer(ocramius/proxy-manager)              >= %{proxy_manager_min_ver}
Suggests:      php-composer(ocramius/proxy-manager)              <  %{proxy_manager_max_ver}
%endif

# php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}
Provides:      php-%{composer_vendor}-%{composer_project}           = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}
Provides:      php-composer(container-interop/container-interop-implementation) = 1.0

%description
%{summary}.

Autoloader: %{phpdir}/DI/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Remove executable bit
: https://github.com/PHP-DI/PHP-DI/pull/392
chmod a-x src/DI/Definition/Source/DefinitionArray.php

: Create autoloader
cat <<'AUTOLOAD' | tee src/DI/autoload.php
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

$fedoraClassLoader->addPrefix('DI\\', dirname(__DIR__));
require_once __DIR__.'/functions.php';

// Required dependencies
require_once '%{phpdir}/Interop/Container/autoload.php';
require_once '%{phpdir}/Invoker/autoload.php';
require_once '%{phpdir}/PhpDocReader/autoload.php';

// Optional dependencies
@include_once '%{phpdir}/Doctrine/Common/Annotations/autoload.php';
@include_once '%{phpdir}/Doctrine/Common/Cache/autoload.php';
@include_once '%{phpdir}/ProxyManager/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing to build


%install
rm -rf   %{buildroot}
mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Make PSR-0 tests
mkdir -p tests-psr0/DI/Test
ln -s ../../../tests/IntegrationTest tests-psr0/DI/Test/IntegrationTest
ln -s ../../../tests/UnitTest tests-psr0/DI/Test/UnitTest

: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
$fedoraClassLoader = require '%{buildroot}%{phpdir}/DI/autoload.php';
$fedoraClassLoader->addPrefix('DI\\Test\\IntegrationTest\\', __DIR__.'/tests-psr0');
$fedoraClassLoader->addPrefix('DI\\Test\\UnitTest\\', __DIR__.'/tests-psr0');

require_once '%{phpdir}/EasyMock/autoload.php';
BOOTSTRAP

: Run tests
%{_bindir}/phpunit --verbose --bootstrap bootstrap.php

if which php70; then
   php70 %{_bindir}/phpunit --verbose --bootstrap bootstrap.php  || :
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
%doc change-log.md
%doc composer.json
%doc README.md
%{phpdir}/DI


%changelog
* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 5.3.0-1
- update to 5.3.0
- raise dependency on php >=5.5.0
- allow ocramius/proxy-manager 2.0

* Fri Mar 11 2016 Shawn Iwinski <shawn@iwin.ski> - 5.2.2-1
- Updated to 5.2.2 (RHBZ #1298928)

* Thu Jan  7 2016 Remi Collet <remi@remirepo.net> - 5.2.0-1
- backport for #remirepo

* Sun Jan 03 2016 Shawn Iwinski <shawn@iwin.ski> - 5.2.0-1
- Initial package
