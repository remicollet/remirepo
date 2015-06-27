#
# Fedora spec file for php-doctrine-doctrine-bundle
#
# Copyright (c) 2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      DoctrineBundle
%global github_version   1.5.0
%global github_commit    0b9e27037c4fdbad515ee5ec89842e9091a6480f

%global composer_vendor  doctrine
%global composer_project doctrine-bundle

# "php": ">=5.3.2"
%global php_min_ver 5.3.2
# "doctrine/dbal": "~2.3"
%global dbal_min_ver 2.3
%global dbal_max_ver 3.0
# "doctrine/doctrine-cache-bundle": "~1.0"
%global cache_bundle_min_ver 1.0
%global cache_bundle_max_ver 2.0
# "doctrine/orm": "~2.3"
%global orm_min_ver 2.3
%global orm_max_ver 3.0
# "jdorn/sql-formatter": "~1.1"
%global sql_formatter_min_ver 1.1
%global sql_formatter_max_ver 2.0
# "symfony/console": "~2.3"
# "symfony/doctrine-bridge": "~2.2"
# "symfony/framework-bundle": "~2.3"
# "symfony/validator": "~2.2"
# "symfony/yaml": "~2.2"
%global symfony_min_ver 2.3
%global symfony_max_ver 3.0
# "twig/twig": "~1.10"
%global twig_min_ver 1.10
%global twig_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       3%{?dist}
Summary:       Symfony Bundle for Doctrine

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: %{_bindir}/phpunit
BuildRequires: php(language)                                >= %{php_min_ver}
BuildRequires: php-composer(doctrine/dbal)                  >= %{dbal_min_ver}
BuildRequires: php-composer(doctrine/doctrine-cache-bundle) >= %{cache_bundle_min_ver}
BuildRequires: php-composer(doctrine/orm)                   >= %{orm_min_ver}
BuildRequires: php-composer(jdorn/sql-formatter)            >= %{sql_formatter_min_ver}
BuildRequires: php-composer(symfony/console)                >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/doctrine-bridge)        >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/framework-bundle)       >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/validator)              >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/yaml)                   >= %{symfony_min_ver}
BuildRequires: php-composer(twig/twig)                      >= %{twig_min_ver}
## phpcompatinfo (computed from version 1.5.0)
BuildRequires: php-dom
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                                >= %{php_min_ver}
Requires:      php-composer(doctrine/dbal)                  >= %{dbal_min_ver}
Requires:      php-composer(doctrine/dbal)                  <  %{dbal_max_ver}
Requires:      php-composer(doctrine/doctrine-cache-bundle) >= %{cache_bundle_min_ver}
Requires:      php-composer(doctrine/doctrine-cache-bundle) <  %{cache_bundle_max_ver}
Requires:      php-composer(jdorn/sql-formatter)            >= %{sql_formatter_min_ver}
Requires:      php-composer(jdorn/sql-formatter)            <  %{sql_formatter_max_ver}
Requires:      php-composer(symfony/console)                >= %{symfony_min_ver}
Requires:      php-composer(symfony/console)                <  %{symfony_max_ver}
Requires:      php-composer(symfony/doctrine-bridge)        >= %{symfony_min_ver}
Requires:      php-composer(symfony/doctrine-bridge)        <  %{symfony_max_ver}
Requires:      php-composer(symfony/framework-bundle)       >= %{symfony_min_ver}
Requires:      php-composer(symfony/framework-bundle)       <  %{symfony_max_ver}
# phpcompatinfo (computed from version 1.5.0)
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

# Optional dependency version conflicts
Conflicts:     php-composer(doctrine/orm)                <  %{orm_min_ver}
Conflicts:     php-composer(doctrine/orm)                >= %{orm_max_ver}
Conflicts:     php-composer(symfony/web-profiler-bundle) <  %{symfony_min_ver}
Conflicts:     php-composer(symfony/web-profiler-bundle) >= %{symfony_max_ver}
Conflicts:     php-composer(twig/twig)                   <  %{twig_min_ver}
Conflicts:     php-composer(twig/twig)                   >= %{twig_max_ver}

%description
Doctrine DBAL & ORM Bundle for the Symfony Framework.

Optional:
* Doctrine ORM (%{orm_min_ver} <= php-doctrine-orm < %{orm_max_ver})
* Symfony Web Profile Bundle (%{symfony_min_ver} <= php-symfony-web-profiler-bundle < %{symfony_max_ver})
* Twig (%{twig_min_ver} <= php-twig < %{twig_max_ver})


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

require_once '%{phpdir}/Doctrine/Bundle/DoctrineCacheBundle/autoload.php';
require_once '%{phpdir}/jdorn-sql-formatter/autoload.php';

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Doctrine\\Bundle\\DoctrineBundle\\', dirname(dirname(dirname(__DIR__))));
$fedoraClassLoader->setUseIncludePath(true);

return $fedoraClassLoader;
AUTOLOAD
) | tee autoload.php


%build
# Empty build section, nothing required


%install
mkdir -p %{buildroot}%{phpdir}/Doctrine/Bundle/DoctrineBundle
cp -pr Command Controller DataCollector DependencyInjection Mapping Resources Tests Twig *.php \
    %{buildroot}%{phpdir}/Doctrine/Bundle/DoctrineBundle/


%check
%if %{with_tests}
%{_bindir}/phpunit -v \
    --bootstrap %{buildroot}%{phpdir}/Doctrine/Bundle/DoctrineBundle/autoload.php
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{phpdir}/Doctrine/Bundle/DoctrineBundle
%exclude %{phpdir}/Doctrine/Bundle/DoctrineBundle/Tests


%changelog
* Fri Jun 26 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.5.0-3
- Autoloader updates

* Tue Jun 16 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.5.0-2
- Fixed dependencies
- Added optional dependency version conflicts

* Thu Jun 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.5.0-1
- Initial package
