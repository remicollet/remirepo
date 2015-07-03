# remirepo spec file for php-doctrine-datafixtures, from Fedora:
#
# RPM spec file for php-doctrine-datafixtures
#
# Copyright (c) 2013-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      data-fixtures
%global github_version   1.1.1
%global github_commit    bd44f6b6e40247b6530bc8abe802e4e4d914976a

%global composer_vendor  doctrine
%global composer_project data-fixtures

# "php": ">=5.3.2"
%global php_min_ver 5.3.2
# "doctrine/common": "~2.2"
#     NOTE: Min version not 2.2 because autoloader required
%global doctrine_common_min_ver 2.5
%global doctrine_common_max_ver 3.0
# "doctrine/orm": "~2.4"
%global doctrine_orm_min_ver 2.4
%global doctrine_orm_max_ver 3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-datafixtures
Version:       %{github_version}
Release:       1%{?dist}
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
BuildRequires: %{_bindir}/phpunit
BuildRequires: php(language)                 >= %{php_min_ver}
BuildRequires: php-composer(doctrine/common) >= %{doctrine_common_min_ver}
BuildRequires: php-composer(doctrine/common) <  %{doctrine_common_max_ver}
BuildRequires: php-composer(doctrine/orm)    >= %{doctrine_orm_min_ver}
BuildRequires: php-composer(doctrine/orm)    <  %{doctrine_orm_max_ver}
## phpcompatinfo (computed from version 1.1.1)
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
# phpcompatinfo (computed from version 1.1.1)
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
(cat <<'AUTOLOAD'
<?php
/**
 * Autoloader created by %{name}-%{version}-%{release}
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

require_once '%{phpdir}/Doctrine/Common/autoload.php';

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Doctrine\\Common\\DataFixtures\\', dirname(dirname(dirname(__DIR__))));

// Doctrine ORM does not provide its' own autoloader yet. Use it when it is
// available otherwise fall back to using include path.
if (file_exists('%{phpdir}/Doctrine/ORM/autoload.php')) {
    require_once '%{phpdir}/Doctrine/ORM/autoload.php';
} else {
    $fedoraClassLoader->setUseIncludePath(true);
}

return $fedoraClassLoader;
AUTOLOAD
) | tee lib/Doctrine/Common/DataFixtures/autoload.php


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}
cp -rp lib/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create tests bootstrap
(cat <<'BOOTSTRAP'
<?php

$fedoraClassLoader =
    require_once '%{buildroot}%{phpdir}/Doctrine/Common/DataFixtures/autoload.php';

$fedoraClassLoader->addPrefix('Doctrine\\Tests\\', __DIR__ . '/tests');
BOOTSTRAP
) | tee bootstrap.php

%{_bindir}/phpunit -v --bootstrap ./bootstrap.php
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
