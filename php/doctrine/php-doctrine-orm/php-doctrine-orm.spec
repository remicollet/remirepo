# remirepo spec file for php-doctrine-orm, from
#
# Fedora spec file for php-doctrine-orm
#
# Copyright (c) 2013-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#                         Remi Collet <remi@fedoraproject.org>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      doctrine2
%global github_version   2.4.8
%global github_commit    5aedac1e5c5caaeac14798822c70325dc242d467

%global composer_vendor  doctrine
%global composer_project orm

# "php": ">=5.3.2"
%global php_min_ver 5.3.2
# "doctrine/collections": "~1.1"
#     NOTE: Min version not 1.1 because autoloader required
%global collections_min_ver 1.3.0
%global collections_max_ver 2.0
# "doctrine/dbal": "~2.4"
#     NOTE: Min version not 2.4 because autoloader required
%global dbal_min_ver 2.5.4
%global dbal_max_ver 3.0
# "symfony/console": "~2.0"
# "symfony/yaml": "~2.1"
#     NOTE: Min version not 2.1 because autoloader required
%global symfony_min_ver 2.7.1
%global symfony_max_ver 3.0

%{!?phpdir:  %global phpdir  %{_datadir}/php}

# Build using "--without tests" to disable tests
%global with_tests %{?_without_tests:0}%{!?_without_tests:1}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       Doctrine Object-Relational-Mapper (ORM)

Group:         Development/Libraries
License:       MIT
URL:           http://www.doctrine-project.org/projects/orm.html

# Run "php-doctrine-orm-get-source.sh" to create source
Source0:       %{name}-%{version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

# Update bin script:
# 1) Add she-bang
# 2) Auto-load using Doctrine\Common\ClassLoader
Patch0:        %{name}-bin.patch

# Fix test suite using PHPUnit 5.4
Patch1:        %{name}-phpunit54.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
%if %{with_tests}
BuildRequires: php-composer(phpunit/phpunit)
# composer.json
BuildRequires: php(language)                      >= %{php_min_ver}
BuildRequires: php-composer(doctrine/collections) <  %{collections_max_ver}
BuildRequires: php-composer(doctrine/collections) >= %{collections_min_ver}
BuildRequires: php-composer(doctrine/dbal)        <  %{dbal_max_ver}
BuildRequires: php-composer(doctrine/dbal)        >= %{dbal_min_ver}
BuildRequires: php-composer(symfony/console)      <  %{symfony_max_ver}
BuildRequires: php-composer(symfony/console)      >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/yaml)         <  %{symfony_max_ver}
BuildRequires: php-composer(symfony/yaml)         >= %{symfony_min_ver}
BuildRequires: php-pdo
# phpcompatinfo (computed from version 2.4.8)
BuildRequires: php-ctype
BuildRequires: php-date
BuildRequires: php-dom
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-simplexml
BuildRequires: php-spl
BuildRequires: php-tokenizer
%endif

# composer.json
Requires:      php(language)                      >= %{php_min_ver}
Requires:      php-composer(doctrine/collections) <  %{collections_max_ver}
Requires:      php-composer(doctrine/collections) >= %{collections_min_ver}
Requires:      php-composer(doctrine/dbal)        <  %{dbal_max_ver}
Requires:      php-composer(doctrine/dbal)        >= %{dbal_min_ver}
Requires:      php-composer(symfony/console)      <  %{symfony_max_ver}
Requires:      php-composer(symfony/console)      >= %{symfony_min_ver}
Requires:      php-composer(symfony/yaml)         <  %{symfony_max_ver}
Requires:      php-composer(symfony/yaml)         >= %{symfony_min_ver}
Requires:      php-pdo
# phpcompatinfo (computed from version 2.4.8)
Requires:      php-ctype
Requires:      php-dom
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-simplexml
Requires:      php-spl
Requires:      php-tokenizer

# Weak dependencies
%if 0%{?fedora} >= 21
## Optional caches (see Doctrine\ORM\Tools\Setup::createConfiguration())
Suggests:      php-pecl(apcu)
Suggests:      php-pecl(memcache)
Suggests:      php-pecl(redis)
Suggests:      php-xcache
%endif

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}
# PEAR
Provides:      php-pear(pear.doctrine-project.org/DoctrineORM) = %{version}
# Rename
Obsoletes:     php-doctrine-DoctrineORM < %{version}
Provides:      php-doctrine-DoctrineORM = %{version}

%description
Object relational mapper (ORM) for PHP that sits on top of a powerful database
abstraction layer (DBAL). One of its' key features is the option to write
database queries in a proprietary object oriented SQL dialect called Doctrine
Query Language (DQL), inspired by Hibernate's HQL. This provides developers
with a powerful alternative to SQL that maintains flexibility without requiring
unnecessary code duplication.

Autoloader: %{phpdir}/Doctrine/ORM/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Patch bin script
%patch0 -p1

if %{_bindir}/phpunit --atleast-version 5.4; then
: Fix test suite using PHPUnit 5.4
%patch1 -p0
fi

: Remove empty file
rm -f lib/Doctrine/ORM/README.markdown

: Remove unnecessary executable bits
chmod a-x lib/Doctrine/ORM/Tools/Pagination/Paginator.php


%build
: Create autoloader
cat <<'AUTOLOAD' | tee lib/Doctrine/ORM/autoload.php
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

$fedoraClassLoader->addPrefix('Doctrine\\ORM\\', dirname(dirname(__DIR__)));

// Dependencies (autoloader => required)
foreach(array(
    '%{phpdir}/Doctrine/Common/Collections/autoload.php' => true,
    '%{phpdir}/Doctrine/DBAL/autoload.php'               => true,
    '%{phpdir}/Symfony/Component/Console/autoload.php'   => true,
    '%{phpdir}/Symfony/Component/Yaml/autoload.php'      => true,
) as $dependencyAutoloader => $required) {
    if ($required || file_exists($dependencyAutoloader)) {
        require_once $dependencyAutoloader;
    }
}

return $fedoraClassLoader;
AUTOLOAD


%install
rm -rf %{buildroot}

: Lib
mkdir -p %{buildroot}%{phpdir}
cp -rp lib/Doctrine %{buildroot}%{phpdir}/

: Bin
mkdir -p %{buildroot}/%{_bindir}
install -pm 0755 bin/doctrine.php %{buildroot}/%{_bindir}/doctrine


%check
%if %{with_tests}
: Remove load of TestInit
mv tests/Doctrine/Tests/TestInit.php tests/Doctrine/Tests/TestInit.php.dist
grep -r --files-with-matches 'TestInit' tests \
    | xargs sed '/TestInit/d' -i

: Load annotation register file from buildroot
sed 's#__DIR__\s*\.\s*"/\(\.\./\)*lib#"%{buildroot}%{phpdir}#' \
    -i tests/Doctrine/Tests/OrmTestCase.php

: Create tests bootstrap
cat > bootstrap.php <<'BOOTSTRAP'
<?php
$fedoraClassLoader =
    require_once '%{buildroot}%{phpdir}/Doctrine/ORM/autoload.php';

$fedoraClassLoader->addPrefix('Doctrine\\Tests\\', __DIR__.'/tests');
BOOTSTRAP

# Skip test known to fail
sed -e 's/function testQueryCache_DependsOnHints/function SKIP_testQueryCache_DependsOnHints/' \
    -e 's/function testQueryCache_NoHitSaveParserResult/function SKIP_testQueryCache_NoHitSaveParserResult/' \
    -i tests/Doctrine/Tests/ORM/Functional/QueryCacheTest.php
sed 's/function testNativeQueryResultCaching/function SKIP_testNativeQueryResultCaching/' \
    -i tests/Doctrine/Tests/ORM/Functional/ResultCacheTest.php
sed 's/function testQueryCache_DependsOnFilters/function SKIP_testQueryCache_DependsOnFilters/' \
    -i tests/Doctrine/Tests/ORM/Functional/SQLFilterTest.php
%if 1
# PHP 7
sed 's/function testReusedSplObjectHashDoesNotConfuseUnitOfWork/function SKIP_testReusedSplObjectHashDoesNotConfuseUnitOfWork/' \
    -i tests/Doctrine/Tests/ORM/Functional/IdentityMapTest.php
%endif

# Weird el6 error
# TODO: Investigate and submit upstream patch
%if 0%{?el6}
sed 's#$this->_em->clear();#if (isset($this->_em)) { $this->_em->clear(); }#' \
    -i tests/Doctrine/Tests/OrmFunctionalTestCase.php
%endif
%if 0%{?el5}
# Seems to use sqlite3, not available
rm tests/Doctrine/Tests/ORM/Functional/QueryDqlFunctionTest.php
%endif

ret=0
run=0
if which php56; then
  php56 %{_bindir}/phpunit -d memory_limit="512M" --bootstrap bootstrap.php || ret=1
  run=1
fi
if which php71; then
  php71 %{_bindir}/phpunit -d memory_limit="512M" --bootstrap bootstrap.php || ret=1
  run=1
fi
if [ $run -eq 0 ]; then
  %{_bindir}/phpunit -d memory_limit="512M" --bootstrap bootstrap.php
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
%doc *.md *.markdown composer.json
%{_datadir}/php/Doctrine/ORM
%{_bindir}/doctrine


%changelog
* Sat Jul 09 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.4.8-1
- Updated to 2.4.8 (RHBZ #1347926 / CVE-2015-5723)
- Added autoloader

* Mon Jun 13 2016 Remi Collet <remi@fedoraproject.org> - 2.4.7-5
- add workaround for test suite with PHPUnit 5.4

* Sun Feb 28 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.4.7-4
- Skip additional tests known to fail (RHBZ #1307857)

* Sun Dec 28 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.4.7-1
- Updated to 2.4.7 (BZ #1175217)
- %%license usage

* Mon Nov 03 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.4.6-2
- Ensure 512M of memory (instead of default 128M) so mock x86_64
  builds pass (BZ #1159650)

* Tue Oct 14 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.4.6-1
- Updated to 2.4.6 (BZ #1108129)
- Manual git clone source instead of GitHub archive URL (to include tests)
- Removed Patch1 (%%{name}-upstream.patch)
- Added tests

* Tue Oct  7 2014 Remi Collet <remi@fedoraproject.org> 2.4.6-1
- Update to 2.4.6

* Tue Sep 23 2014 Remi Collet <remi@fedoraproject.org> 2.4.5-1
- Update to 2.4.5

* Sat Sep 13 2014 Remi Collet <remi@fedoraproject.org> 2.4.4-1
- Update to 2.4.4
- backport upstream patch to use doctrine/instantiator
- fix license handling

* Sat Jun 21 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.4.2-4
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide
- Updated Doctrine dependencies to use php-composer virtual provides

* Fri May 30 2014 Remi Collet <remi@fedoraproject.org> 2.4.2-2
- upstream fix for latest PHP (#1103219)

* Mon Feb 17 2014 Remi Collet <rpms@famillecollet.com> 2.4.2-1
- backport 2.4.2 for remi repo

* Wed Feb 12 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 2.4.2-1
- Updated to 2.4.2 (BZ #1063021)

* Sat Jan 11 2014 Remi Collet <rpms@famillecollet.com> 2.4.1-2
- backport for remi repo

* Sat Jan 04 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 2.4.1-2
- Conditional %%{?dist}
- Bin script patch instead of inline update and use Doctrine Common classloader
- Updated optional cache information in %%description
- Removed empty file
- Removed unnecessary executable bit

* Sat Dec 28 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.4.1-1
- Initial package
