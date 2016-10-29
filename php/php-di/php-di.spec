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
%global github_version   5.4.0
%global github_commit    e348393488fa909e4bc0707ba5c9c44cd602a1cb

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
# "php-di/invoker": "^1.3.2"
%global di_invoker_min_ver 1.3.2
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
## phpcompatinfo (computed from version 5.4.0)
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
# phpcompatinfo (computed from version 5.4.0)
Requires:      php-json
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)
# Weak dependencies
%if 0%{?fedora} >= 21
Suggests:      php-composer(doctrine/annotations)
Suggests:      php-composer(doctrine/cache)
Suggests:      php-composer(mnapoli/phpunit-easymock)
Suggests:      php-composer(ocramius/proxy-manager)
%endif
Conflicts:     php-composer(doctrine/annotations)                <  %{doctrine_annotations_min_ver}
Conflicts:     php-composer(doctrine/annotations)                >= %{doctrine_annotations_max_ver}
Conflicts:     php-composer(doctrine/cache)                      <  %{doctrine_cache_min_ver}
Conflicts:     php-composer(doctrine/cache)                      >= %{doctrine_cache_max_ver}
Conflicts:     php-composer(mnapoli/phpunit-easymock)            <  %{phpunit_easymock_min_ver}
Conflicts:     php-composer(mnapoli/phpunit-easymock)            >= %{phpunit_easymock_max_ver}
Conflicts:     php-composer(ocramius/proxy-manager)              <  %{proxy_manager_min_ver}
Conflicts:     php-composer(ocramius/proxy-manager)              >= %{proxy_manager_max_ver}

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

// Dependencies (autoloader => required)
foreach(array(
    // Required dependencies
    '%{phpdir}/Interop/Container/autoload.php'           => true,
    '%{phpdir}/Invoker/autoload.php'                     => true,
    '%{phpdir}/PhpDocReader/autoload.php'                => true,
    // Optional dependencies
    '%{phpdir}/Doctrine/Common/Annotations/autoload.php' => false,
    '%{phpdir}/Doctrine/Common/Cache/autoload.php'       => false,
    '%{phpdir}/ProxyManager/autoload.php'                => false,
) as $dependencyAutoloader => $required) {
    if ($required || file_exists($dependencyAutoloader)) {
        require_once $dependencyAutoloader;
    }
}


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

: Skip tests known to fail with "php-composer(php-di/invoker)" >= 1.3.2
: See https://github.com/PHP-DI/Invoker/issues/13
sed 's/function test_not_callable/function SKIP_test_not_callable/' \
    -i tests/IntegrationTest/CallFunctionTest.php
sed 's/function test_not_callable_factory_definition/function SKIP_test_not_callable_factory_definition/' \
    -i tests/IntegrationTest/Definitions/FactoryDefinitionTest.php
sed 's/function test_factory_not_callable/function SKIP_test_factory_not_callable/' \
    -i tests/IntegrationTest/ErrorMessages/ErrorMessagesTest.php
sed -e '/@test/d' \
    -e 's/public function should_/public function test_should_/g' \
    -e 's/function test_should_throw_if_the_factory_is_not_callable/function SKIP_test_should_throw_if_the_factory_is_not_callable/' \
    -i tests/UnitTest/Definition/Resolver/FactoryResolverTest.php

: Run tests
ret=0
run=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap bootstrap.php || : ignore
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap bootstrap.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose --bootstrap bootstrap.php
fi
exit $ret
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
* Fri Oct 28 2016 Remi Collet <remi@fedoraproject.org> - 5.4.0-1
- update to 5.4.0
- raise dependency on php-di/invoker >= 1.3.2

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
