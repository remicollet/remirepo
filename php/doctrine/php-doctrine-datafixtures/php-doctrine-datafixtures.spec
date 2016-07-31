# remirepo spec file for php-doctrine-datafixtures, from Fedora:
#
# Fedora spec file for php-doctrine-datafixtures
#
# Copyright (c) 2013-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      data-fixtures
%global github_version   1.0.2
%global github_commit    422952ccf7151c02bb5c01fadb305dce266a3b5f

%global composer_vendor  doctrine
%global composer_project data-fixtures

# "php": ">=5.3.2"
%global php_min_ver 5.3.2
# "doctrine/common": "~2.2"
#     NOTE: Min version not 2.2 because autoloader required
%global doctrine_common_min_ver 2.5
%global doctrine_common_max_ver 3.0
# "doctrine/orm": "~2.2"
#     NOTE: Min version not 2.2 because autoloader required
%global doctrine_orm_min_ver 2.4.8
%global doctrine_orm_max_ver 3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-datafixtures
Version:       %{github_version}
Release:       3%{?dist}
Summary:       Data Fixtures for all Doctrine Object Managers

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language)                 >= %{php_min_ver}
BuildRequires: php-composer(doctrine/common) >= %{doctrine_common_min_ver}
BuildRequires: php-composer(doctrine/orm)    >= %{doctrine_orm_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
## phpcompatinfo (computed from version 1.0.2)
BuildRequires: php-json
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                 >= %{php_min_ver}
Requires:      php-composer(doctrine/common) >= %{doctrine_common_min_ver}
Requires:      php-composer(doctrine/common) <  %{doctrine_common_max_ver}
# composer.json: optional
Requires:      php-composer(doctrine/orm)    >= %{doctrine_orm_min_ver}
Requires:      php-composer(doctrine/orm)    <  %{doctrine_orm_max_ver}
# phpcompatinfo (computed from version 1.0.2)
Requires:      php-json
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming
Provides:      php-%{composer_vendor}-%{composer_project} = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
This extension aims to provide a simple way to manage and execute the loading
of data fixtures for the Doctrine ORM or ODM.


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee lib/Doctrine/Common/DataFixtures/autoload.php
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

$fedoraClassLoader->addPrefix('Doctrine\\Common\\DataFixtures\\', dirname(dirname(dirname(__DIR__))));

// Dependencies (autoloader => required)
foreach(array(
    // Required dependency
    '%{phpdir}/Doctrine/Common/autoload.php' => true,
    // Optional dependency
    '%{phpdir}/Doctrine/ORM/autoload.php'    => false,
) as $dependencyAutoloader => $required) {
    if ($required || file_exists($dependencyAutoloader)) {
        require_once $dependencyAutoloader;
    }
}

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}
cp -rp lib/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
%if 0%{?el6}
: Skip tests known to fail
sed -e 's#function testSharedFixtures#function SKIP_testSharedFixtures#' \
    -i tests/Doctrine/Tests/Common/DataFixtures/Executor/ORMExecutorSharedFixtureTest.php
sed -e 's#function testReferenceIdentityPopulation#function SKIP_testReferenceIdentityPopulation#' \
    -e 's#function testReferenceReconstruction#function SKIP_testReferenceReconstruction#' \
    -e 's#function testReferenceMultipleEntries#function SKIP_testReferenceMultipleEntries#' \
    -i tests/Doctrine/Tests/Common/DataFixtures/ProxyReferenceRepositoryTest.php
sed -e 's#function testReferenceIdentityPopulation#function SKIP_testReferenceIdentityPopulation#' \
    -e 's#function testReferenceReconstruction#function SKIP_testReferenceReconstruction#' \
    -e 's#function testReferenceMultipleEntries#function SKIP_testReferenceMultipleEntries#' \
    -i tests/Doctrine/Tests/Common/DataFixtures/ReferenceRepositoryTest.php
%endif

: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php

$fedoraClassLoader =
    require_once '%{buildroot}%{phpdir}/Doctrine/Common/DataFixtures/autoload.php';

$fedoraClassLoader->addPrefix('Doctrine\\Tests\\', __DIR__ . '/tests');
BOOTSTRAP

ret=0
run=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap ./bootstrap.php || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap ./bootstrap.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose --bootstrap ./bootstrap.php
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
%doc *.md
%doc UPGRADE
%doc composer.json
%{phpdir}/Doctrine/Common/DataFixtures


%changelog
* Sun Jul 31 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.2-1
- Updated/fixed php-composer(doctrine/*) dependencies min version for autoloaders
- Modified autoloader

* Fri Jul 03 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.2-1
- Updated to 1.0.2 (RHBZ #1206860)
- Added standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming provides
- Added autoloader
- %%license usage

* Thu Jul 02 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.1-1
- Updated to 1.1.1 (RHBZ #1206860)
- Added standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming provides
- Added autoloader
- %%license usage

* Sat Jun 21 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.0-4
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide
- Added option to build without tests ("--without tests")
- Updated Doctrine dependencies to use php-composer virtual provides

* Sat Jan 11 2014 Remi Collet <rpms@famillecollet.com> 1.0.0-2
- backport for remi repo

* Sun Jan 05 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-2
- Use non-PEAR Doctrine pkgs
- Conditional %%{?dist}

* Fri Dec 20 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-1
- Initial package
