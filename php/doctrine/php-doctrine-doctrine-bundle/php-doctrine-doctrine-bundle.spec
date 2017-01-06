# remirepo spec file for php-doctrine-doctrine-bundle, from:
#
# Fedora spec file for php-doctrine-doctrine-bundle
#
# Copyright (c) 2015-2017 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      DoctrineBundle
%global github_version   1.6.4
%global github_commit    dd40b0a7fb16658cda9def9786992b8df8a49be7

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
# "symfony/console": "~2.3|~3.0"
# "symfony/dependency-injection": "~2.3|~3.0"
# "symfony/doctrine-bridge": "~2.2|~3.0"
# "symfony/framework-bundle": "~2.3|~3.0"
# "symfony/property-info": "~2.8|~3.0"
# "symfony/validator": "~2.2|~3.0"
# "symfony/yaml": "~2.2|~3.0"
%global symfony_min_ver 2.8
%global symfony_max_ver 4.0
# "twig/twig": "~1.10"
%global twig_min_ver 1.10
%global twig_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       2%{?dist}
Summary:       Symfony Bundle for Doctrine

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language)                                >= %{php_min_ver}
BuildRequires: php-composer(doctrine/dbal)                  >= %{dbal_min_ver}
BuildRequires: php-composer(doctrine/doctrine-cache-bundle) >= %{cache_bundle_min_ver}
BuildRequires: php-composer(doctrine/orm)                   >= %{orm_min_ver}
BuildRequires: php-composer(jdorn/sql-formatter)            >= %{sql_formatter_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(symfony/console)                >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/dependency-injection)   >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/doctrine-bridge)        >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/framework-bundle)       >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/property-info)          >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/validator)              >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/yaml)                   >= %{symfony_min_ver}
BuildRequires: php-composer(twig/twig)                      <  %{twig_max_ver}
BuildRequires: php-composer(twig/twig)                      >= %{twig_min_ver}
## phpcompatinfo (computed from version 1.6.4)
BuildRequires: php-dom
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
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
Requires:      php-composer(symfony/dependency-injection)   >= %{symfony_min_ver}
Requires:      php-composer(symfony/dependency-injection)   <  %{symfony_max_ver}
Requires:      php-composer(symfony/doctrine-bridge)        >= %{symfony_min_ver}
Requires:      php-composer(symfony/doctrine-bridge)        <  %{symfony_max_ver}
Requires:      php-composer(symfony/framework-bundle)       >= %{symfony_min_ver}
Requires:      php-composer(symfony/framework-bundle)       <  %{symfony_max_ver}
# phpcompatinfo (computed from version 1.6.4)
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

# Weak dependencies
%if 0%{?fedora} >= 21
Suggests:      php-composer(doctrine/orm)
Suggests:      php-composer(symfony/web-profiler-bundle)
Suggests:      php-composer(twig/twig)                   <  %{twig_max_ver}
%endif
Conflicts:     php-composer(doctrine/orm)                <  %{orm_min_ver}
Conflicts:     php-composer(doctrine/orm)                >= %{orm_max_ver}
Conflicts:     php-composer(symfony/web-profiler-bundle) <  %{symfony_min_ver}
Conflicts:     php-composer(symfony/web-profiler-bundle) >= %{symfony_max_ver}
Conflicts:     php-composer(twig/twig)                   <  %{twig_min_ver}

%description
Doctrine DBAL & ORM Bundle for the Symfony Framework.

Autoloader: %{phpdir}/Doctrine/Bundle/DoctrineBundle/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Licenses and docs
mkdir -p .rpm/{docs,licenses}
mv *.md composer.* .rpm/docs
mkdir -p .rpm/docs/Resources
mv Resources/doc .rpm/docs/Resources/
mv LICENSE .rpm/licenses


%build
: Create autoloader
cat <<'AUTOLOAD' | tee autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 */
require_once '%{phpdir}/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Doctrine\\Bundle\\DoctrineBundle\\', __DIR__);

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/Doctrine/Bundle/DoctrineCacheBundle/autoload.php',
    '%{phpdir}/Doctrine/DBAL/autoload.php',
    '%{phpdir}/jdorn-sql-formatter/autoload.php',
    '%{phpdir}/Symfony/Bridge/Doctrine/autoload.php',
    '%{phpdir}/Symfony/Bundle/FrameworkBundle/autoload.php',
    '%{phpdir}/Symfony/Component/Console/autoload.php',
    '%{phpdir}/Symfony/Component/DependencyInjection/autoload.php',
));

\Fedora\Autoloader\Dependencies::optional(array(
    '%{phpdir}/Doctrine/ORM/autoload.php',
    '%{phpdir}/Symfony/Bundle/WebProfilerBundle/autoload.php',
    '%{phpdir}/Twig/autoload.php',
));
AUTOLOAD


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}/Doctrine/Bundle/DoctrineBundle
cp -pr * %{buildroot}%{phpdir}/Doctrine/Bundle/DoctrineBundle/


%check
%if %{with_tests}
BOOTSTRAP=%{buildroot}%{phpdir}/Doctrine/Bundle/DoctrineBundle/autoload.php

: Upstream tests
%{_bindir}/phpunit --verbose --bootstrap $BOOTSTRAP

: Upstream tests with SCLs if available
SCL_RETURN_CODE=0
for SCL in php56 php70 php71; do
    if which $SCL; then
        $SCL %{_bindir}/phpunit --verbose --bootstrap $BOOTSTRAP || SCL_RETURN_CODE=1
    fi
done
exit $SCL_RETURN_CODE
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license .rpm/licenses/*
%doc .rpm/docs/*
%{phpdir}/Doctrine/Bundle/DoctrineBundle
%exclude %{phpdir}/Doctrine/Bundle/DoctrineBundle/phpunit.*
%exclude %{phpdir}/Doctrine/Bundle/DoctrineBundle/Tests


%changelog
* Fri Jan  6 2017 Remi Collet <remi@fedoraproject.org> - 1.6.4-2
- drop conflict with twig 2
- ensure twig 1 is used during the build

* Fri Dec 30 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.6.4-1
- Updated to 1.6.4 (RHBZ #1279827)
- Use php-composer(fedora/autoloader)
- Run upstream tests with SCLs if they are available
- Set Resources/doc as %%doc

* Sat Sep 05 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.5.2-1
- Updated to 1.5.2 (RHBZ #1253092 / CVE-2015-5723)
- Updated autoloader to load dependencies after self registration

* Sat Jun 27 2015 Remi Collet <remi@remirepo.net> - 1.5.0-3
- backport for remi repo

* Fri Jun 26 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.5.0-3
- Autoloader updates

* Tue Jun 16 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.5.0-2
- Fixed dependencies
- Added optional dependency version conflicts

* Thu Jun 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.5.0-1
- Initial package
