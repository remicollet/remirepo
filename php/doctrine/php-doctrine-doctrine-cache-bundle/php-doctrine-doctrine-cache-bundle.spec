#
# RPM spec file for php-doctrine-doctrine-cache-bundle
#
# Copyright (c) 2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      DoctrineCacheBundle
%global github_version   1.0.1
%global github_commit    e4b6f810aa047f9cbfe41c3d6a3d7e83d7477a9d

%global composer_vendor  doctrine
%global composer_project doctrine-cache-bundle

# "php": ">=5.3.2"
%global php_min_ver 5.3.2
# "doctrine/cache": "~1.3"
%global cache_min_ver 1.3
%global cache_max_ver 2.0
# "doctrine/inflector": "~1.0"
%global inflector_min_ver 1.0
%global inflector_max_ver 2.0
# "symfony/doctrine-bridge":  "~2.2"
# "symfony/framework-bundle": "~2.2"
# "symfony/security":         "~2.2"
%global symfony_min_ver 2.2
%global symfony_max_ver 3.0

# Build using "--without tests" to disable tests
%global with_tests  %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       2%{?dist}
Summary:       Symfony2 Bundle for Doctrine Cache

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: %{_bindir}/phpunit
BuildRequires: php(language)                          >= %{php_min_ver}
BuildRequires: php-composer(doctrine/cache)           >= %{cache_min_ver}
BuildRequires: php-composer(doctrine/inflector)       >= %{inflector_min_ver}
BuildRequires: php-composer(symfony/console)          >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/doctrine-bridge)  >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/finder)           >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/framework-bundle) >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/security)         >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/validator)        >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/yaml)             >= %{symfony_min_ver}
## phpcompatinfo (computed from version 1.0.1)
BuildRequires: php-hash
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                          >= %{php_min_ver}
Requires:      php-composer(doctrine/cache)           >= %{cache_min_ver}
Requires:      php-composer(doctrine/cache)           <  %{cache_max_ver}
Requires:      php-composer(doctrine/inflector)       >= %{inflector_min_ver}
Requires:      php-composer(doctrine/inflector)       <  %{inflector_max_ver}
Requires:      php-composer(symfony/doctrine-bridge)  >= %{symfony_min_ver}
Requires:      php-composer(symfony/doctrine-bridge)  <  %{symfony_max_ver}
Requires:      php-composer(symfony/framework-bundle) >= %{symfony_min_ver}
Requires:      php-composer(symfony/framework-bundle) <  %{symfony_max_ver}
Requires:      php-composer(symfony/security)         >= %{symfony_min_ver}
Requires:      php-composer(symfony/security)         <  %{symfony_max_ver}
# phpcompatinfo (computed from version 1.0.1)
Requires:      php-hash
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.

Optional:
* Memcache (php-pecl-memcache)
* Memcached (php-pecl-memcached)
* Mongo (php-pecl-mongo)


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

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once 'Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Doctrine\\Bundle\\DoctrineCacheBundle', dirname(dirname(dirname(__DIR__))));
$fedoraClassLoader->setUseIncludePath(true);

return $fedoraClassLoader;
AUTOLOAD
) | tee autoload.php


%build
# Empty build section, nothing required


%install
mkdir -p %{buildroot}%{phpdir}/Doctrine/Bundle/DoctrineCacheBundle
cp -pr Acl Command DependencyInjection Resources Tests *.php \
    %{buildroot}%{phpdir}/Doctrine/Bundle/DoctrineCacheBundle/


%check
%if %{with_tests}
: Modify PHPUnit config
sed -e 's#\./#%{buildroot}%{phpdir}/Doctrine/Bundle/DoctrineCacheBundle/#g' \
    -e 's#>\.<#>%{buildroot}%{phpdir}/Doctrine/Bundle/DoctrineCacheBundle<#' \
    -i phpunit.xml.dist

%{_bindir}/phpunit -v \
    --bootstrap %{buildroot}%{phpdir}/Doctrine/Bundle/DoctrineCacheBundle/autoload.php
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%dir %{phpdir}/Doctrine/Bundle
     %{phpdir}/Doctrine/Bundle/DoctrineCacheBundle
%exclude %{phpdir}/Doctrine/Bundle/DoctrineCacheBundle/Tests


%changelog
* Tue Jun 16 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.1-2
- Fix dependencies

* Thu Jun 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.1-1
- Initial package
