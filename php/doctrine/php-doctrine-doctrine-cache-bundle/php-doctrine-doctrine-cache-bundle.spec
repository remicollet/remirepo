# remirepo spec file for php-doctrine-doctrine-cache-bundle, from:
#
# Fedora spec file for php-doctrine-doctrine-cache-bundle
#
# Copyright (c) 2015-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      DoctrineCacheBundle
%global github_version   1.3.0
%global github_commit    18c600a9b82f6454d2e81ca4957cdd56a1cf3504

%global composer_vendor  doctrine
%global composer_project doctrine-cache-bundle

# "php": ">=5.3.2"
%global php_min_ver 5.3.2
# "doctrine/cache": "^1.4.2"
%global cache_min_ver 1.4.2
%global cache_max_ver 2.0
# "doctrine/inflector": "~1.0"
%global inflector_min_ver 1.0
%global inflector_max_ver 2.0
# "symfony/doctrine-bridge":  "~2.2|~3.0"
# "symfony/yaml":             "~2.2|~3.0",
# "symfony/validator":        "~2.2|~3.0",
# "symfony/console":          "~2.2|~3.0",
# "symfony/finder":           "~2.2|~3.0",
# "symfony/framework-bundle": "~2.2|~3.0",
# "symfony/security-acl":     "~2.3|~3.0",
# NOTE: Min version not 2.3 because autoloader required
%global symfony_min_ver 2.7.1
%global symfony_max_ver 4.0

# Build using "--without tests" to disable tests
%global with_tests  %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       Symfony2 Bundle for Doctrine Cache

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language)                          >= %{php_min_ver}
BuildRequires: php-composer(doctrine/cache)           >= %{cache_min_ver}
BuildRequires: php-composer(doctrine/inflector)       >= %{inflector_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(symfony/console)          >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/doctrine-bridge)  >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/finder)           >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/framework-bundle) >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/validator)        >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/yaml)             >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/security-acl)     >= %{symfony_min_ver}
## phpcompatinfo (computed from version 1.3.0)
BuildRequires: php-hash
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                         >= %{php_min_ver}
Requires:      php-composer(doctrine/cache)          >= %{cache_min_ver}
Requires:      php-composer(doctrine/cache)          <  %{cache_max_ver}
Requires:      php-composer(doctrine/inflector)      >= %{inflector_min_ver}
Requires:      php-composer(doctrine/inflector)      <  %{inflector_max_ver}
Requires:      php-composer(symfony/doctrine-bridge) >= %{symfony_min_ver}
Requires:      php-composer(symfony/doctrine-bridge) <  %{symfony_max_ver}
# phpcompatinfo (computed from version 1.3.0)
Requires:      php-hash
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)
# Weak dependencies
%if 0%{?fedora} >= 21
Suggests:      php-pecl(memcache)
Suggests:      php-pecl(memcached)
Suggests:      php-pecl(mongo)
Suggests:      php-composer(symfony/security-acl)
%endif
Conflicts:     php-symfony-security <  %{symfony_min_ver}
Conflicts:     php-symfony-security >= %{symfony_max_ver}

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.

Autoloader: %{phpdir}/Doctrine/Bundle/DoctrineCacheBundle/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once 'Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Doctrine\\Bundle\\DoctrineCacheBundle\\', dirname(dirname(dirname(__DIR__))));

// Required dependencies
require_once '%{phpdir}/Doctrine/Common/Cache/autoload.php';
require_once '%{phpdir}/Doctrine/Common/Inflector/autoload.php';
require_once '%{phpdir}/Symfony/Bridge/Doctrine/autoload.php';

// Optional dependencies
@include_once '%{phpdir}/Symfony/Component/Security/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}/Doctrine/Bundle/DoctrineCacheBundle
cp -pr Acl Command DependencyInjection Resources Tests *.php \
    %{buildroot}%{phpdir}/Doctrine/Bundle/DoctrineCacheBundle/


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
$fedoraClassLoader =
    require '%{buildroot}%{phpdir}/Doctrine/Bundle/DoctrineCacheBundle/autoload.php';

require_once '%{phpdir}/Symfony/Bundle/FrameworkBundle/autoload.php';
require_once '%{phpdir}/Symfony/Component/Console/autoload.php';
require_once '%{phpdir}/Symfony/Component/Finder/autoload.php';
require_once '%{phpdir}/Symfony/Component/Validator/autoload.php';
require_once '%{phpdir}/Symfony/Component/Yaml/autoload.php';
BOOTSTRAP
: Modify PHPUnit config
sed -e 's#\./#%{buildroot}%{phpdir}/Doctrine/Bundle/DoctrineCacheBundle/#g' \
    -e 's#>\.<#>%{buildroot}%{phpdir}/Doctrine/Bundle/DoctrineCacheBundle<#' \
    -i phpunit.xml.dist

: Remove tests requiring a server to connect to
pushd %{buildroot}%{phpdir}/Doctrine/Bundle/DoctrineCacheBundle/Tests
    rm -f \
        Functional/Fixtures/config/predis.xml \
        Functional/PredisCacheTest.php
%if 0%{?rhel} == 5
    rm DependencyInjection/XmlDoctrineCacheExtensionTest.php
    rm DependencyInjection/YmlDoctrineCacheExtensionTest.php
%endif
popd

%{_bindir}/phpunit --verbose --bootstrap bootstrap.php

if which php70; then
   php70 %{_bindir}/phpunit --verbose --bootstrap bootstrap.php
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
%dir %{phpdir}/Doctrine/Bundle
     %{phpdir}/Doctrine/Bundle/DoctrineCacheBundle
%exclude %{phpdir}/Doctrine/Bundle/DoctrineCacheBundle/Tests


%changelog
* Thu Mar 31 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.0-1
- Updated to 1.3.0 (RHBZ #1279828)
- Updated dependency versions for their autoloaders and modified autoloader
  to use those autoloaders

* Sat Jun 27 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.1-3
- Updated autoloader with trailing separator

* Fri Jun 26 2015 Remi Collet <remi@remirepo.net> - 1.0.1-2
- backport for remirepo

* Tue Jun 16 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.1-2
- Fix dependencies

* Thu Jun 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.1-1
- Initial package
