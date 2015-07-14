# remirepo spec file for php-Metadata, from Fedora:
#
# RPM spec file for php-Metadata
#
# Copyright (c) 2013-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     schmittjoh
%global github_name      metadata
%global github_version   1.5.1
%global github_commit    22b72455559a25777cfd28c4ffda81ff7639f353

%global composer_vendor  jms
%global composer_project metadata

# "php": ">=5.3.0"
%global php_min_ver 5.3.0
# "doctrine/cache" : "~1.0"
#     NOTE: min version not 1.0 because autoloader required
%global doctrine_cache_min_ver 1.4.1
%global doctrine_cache_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-Metadata
Version:       %{github_version}
Release:       3%{?github_release}%{?dist}
Summary:       A library for class/method/property metadata management in PHP

Group:         Development/Libraries
License:       ASL 2.0
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: %{_bindir}/phpunit
BuildRequires: php-composer(symfony/dependency-injection)
## composer.json
BuildRequires: php(language)                >= %{php_min_ver}
BuildRequires: php-composer(doctrine/cache) >= %{doctrine_cache_min_ver}
BuildRequires: php-composer(doctrine/cache) <  %{doctrine_cache_max_ver}
## phpcompatinfo (computed from version 1.5.1)
BuildRequires: php-date
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

Requires:      php-composer(doctrine/cache) >= %{doctrine_cache_min_ver}
Requires:      php-composer(doctrine/cache) <  %{doctrine_cache_max_ver}
Requires:      php-composer(symfony/dependency-injection)
# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.5.1)
Requires:      php-date
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming
Provides:      php-%{composer_vendor}-%{composer_project} = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
This library provides some commonly needed base classes for managing metadata
for classes, methods and properties. The metadata can come from many different
sources (annotations, YAML/XML/PHP configuration files).

The metadata classes are used to abstract away that source and provide a common
interface for all of them.


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee src/Metadata/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 *
 * Created by %{name}-%{version}-%{release}
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

require_once '%{phpdir}/Doctrine/Common/Cache/autoload.php';

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Metadata\\', dirname(__DIR__));

// Not all dependency autoloaders exist or are in every dist yet so fallback
// to using include path for dependencies for now
$fedoraClassLoader->setUseIncludePath(true);

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php

$fedoraClassLoader =
    require_once '%{buildroot}%{phpdir}/Metadata/autoload.php';

$fedoraClassLoader->addprefix('Metadata\\Tests\\', __DIR__ . '/tests');
BOOTSTRAP

%{_bindir}/phpunit --verbose --bootstrap ./bootstrap.php
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
%{phpdir}/Metadata


%changelog
* Sat Jul 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.5.1-3
- Added autoloader
- Added standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming provides

* Sat Jul 19 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.5.1-1
- Updated to 1.5.1 (BZ #1119425)
- Added "php-composer(jms/metadata)" virtual provide
- Added option to build without tests ("--without tests")

* Mon Jun  2 2014 Remi Collet <RPMS@famillecollet.com> 1.5.0-2
- merge rawhide change

* Fri May 30 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.5.0-2
- Updated dependencies to match newly available pkgs
  -- php-pear(pear.doctrine-project.org/DoctrineCommon) => php-doctrine-cache
     (cache separated out from common)
  -- php-pear(pear.symfony.com/DependencyInjection) => php-symfony-dependencyinjection
- Doctrine cache required instead of just build requirement

* Sat Nov 16 2013 Remi Collet <RPMS@famillecollet.com> 1.5.0-1
- backport 1.5.0 for remi repo

* Fri Nov 15 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.5.0-1
- Updated to 1.5.0

* Tue Apr  2 2013 Remi Collet <RPMS@famillecollet.com> 1.3.0-1
- backport 1.3.0 for remi repo

* Sat Mar 30 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.0-1
- Updated to version 1.3.0
- Removed tests sub-package

* Fri Jan 25 2013 Remi Collet <RPMS@famillecollet.com> 1.1.1-1
- backport 1.1.1 for remi repo

* Wed Jan 23 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.1-1
- Initial package
