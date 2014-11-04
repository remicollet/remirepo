#
# RPM spec file for php-doctrine-orm
#
# Copyright (c) 2013-2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#                         Remi Collet <remi@fedoraproject.org>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      doctrine2
%global github_version   2.4.6
%global github_commit    bebacf79d8d4dae9168f0f9bc6811e6c2cb6a4d9

%global composer_vendor  doctrine
%global composer_project orm

# "php": ">=5.3.2"
%global php_min_ver         5.3.2
# "doctrine/collections": "~1.1"
%global collections_min_ver 1.1
%global collections_max_ver 2.0
# "doctrine/dbal": "~2.4"
%global dbal_min_ver        2.4
%global dbal_max_ver        3.0
# "symfony/console": "~2.0"
# "symfony/yaml": "~2.1"
%global symfony_min_ver     2.1
%global symfony_max_ver     3.0

%{!?__phpunit:  %global __phpunit  %{_bindir}/phpunit}

# Build using "--without tests" to disable tests
%global with_tests %{?_without_tests:0}%{!?_without_tests:1}

Name:      php-%{composer_vendor}-%{composer_project}
Version:   %{github_version}
Release:   2%{?dist}
Summary:   Doctrine Object-Relational-Mapper (ORM)

Group:     Development/Libraries
License:   MIT
URL:       http://www.doctrine-project.org/projects/orm.html

# Run "php-doctrine-orm-get-source.sh" to create source
Source0:   %{name}-%{version}-%{github_commit}.tar.gz
Source1:   %{name}-get-source.sh

# Update bin script:
# 1) Add she-bang
# 2) Auto-load using Doctrine\Common\ClassLoader
Patch0:    %{name}-bin.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
%if %{with_tests}
BuildRequires: php-phpunit-PHPUnit
# composer.json
BuildRequires: php(language)                      >= %{php_min_ver}
BuildRequires: php-composer(doctrine/collections) >= %{collections_min_ver}
BuildRequires: php-composer(doctrine/collections) <  %{collections_max_ver}
BuildRequires: php-composer(doctrine/dbal)        >= %{dbal_min_ver}
BuildRequires: php-composer(doctrine/dbal)        <  %{dbal_max_ver}
BuildRequires: php-symfony-console                >= %{symfony_min_ver}
BuildRequires: php-symfony-console                <  %{symfony_max_ver}
BuildRequires: php-symfony-yaml                   >= %{symfony_min_ver}
BuildRequires: php-symfony-yaml                   <  %{symfony_max_ver}
# phpcompatinfo (computed from version 2.4.6)
BuildRequires: php-ctype
BuildRequires: php-date
BuildRequires: php-dom
BuildRequires: php-pcre
BuildRequires: php-pdo
BuildRequires: php-reflection
BuildRequires: php-simplexml
BuildRequires: php-spl
BuildRequires: php-tokenizer
%endif

# composer.json
Requires:      php(language)                      >= %{php_min_ver}
Requires:      php-composer(doctrine/collections) >= %{collections_min_ver}
Requires:      php-composer(doctrine/collections) <  %{collections_max_ver}
Requires:      php-composer(doctrine/dbal)        >= %{dbal_min_ver}
Requires:      php-composer(doctrine/dbal)        <  %{dbal_max_ver}
Requires:      php-symfony-console                >= %{symfony_min_ver}
Requires:      php-symfony-console                <  %{symfony_max_ver}
Requires:      php-symfony-yaml                   >= %{symfony_min_ver}
Requires:      php-symfony-yaml                   <  %{symfony_max_ver}
# phpcompatinfo (computed from version 2.4.6)
Requires:      php-ctype
Requires:      php-dom
Requires:      php-pcre
Requires:      php-pdo
Requires:      php-reflection
Requires:      php-simplexml
Requires:      php-spl
Requires:      php-tokenizer

# Composer
Provides:  php-composer(%{composer_vendor}/%{composer_project}) = %{version}
# PEAR
Provides:  php-pear(pear.doctrine-project.org/DoctrineORM) = %{version}
# Rename
Obsoletes: php-doctrine-DoctrineORM < %{version}
Provides:  php-doctrine-DoctrineORM = %{version}

%description
Object relational mapper (ORM) for PHP that sits on top of a powerful database
abstraction layer (DBAL). One of its' key features is the option to write
database queries in a proprietary object oriented SQL dialect called Doctrine
Query Language (DQL), inspired by Hibernate's HQL. This provides developers
with a powerful alternative to SQL that maintains flexibility without requiring
unnecessary code duplication.

Optional caches (see Doctrine\ORM\Tools\Setup::createConfiguration()):
* APC (php-pecl-apc)
* Memcache (php-pecl-memcache)
* Redis (php-pecl-redis)
* XCache (php-xcache)


%prep
%setup -qn %{github_name}-%{github_commit}

# Patch bin script
%patch0 -p1

# Remove empty file
rm -f lib/Doctrine/ORM/README.markdown

# Remove unnecessary executable bits
chmod a-x lib/Doctrine/ORM/Tools/Pagination/Paginator.php


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_datadir}/php
cp -rp lib/Doctrine %{buildroot}/%{_datadir}/php/

mkdir -p %{buildroot}/%{_bindir}
install -pm 0755 bin/doctrine.php %{buildroot}/%{_bindir}/doctrine


%check
%if %{with_tests}
# Rewrite "tests/Doctrine/Tests/TestInit.php"
mv tests/Doctrine/Tests/TestInit.php tests/Doctrine/Tests/TestInit.php.dist
cat > tests/Doctrine/Tests/TestInit.php <<'TEST_INIT'
<?php

spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', $class).'.php';
    @include_once $src;
});
TEST_INIT

# Weird el6 error
# TODO: Investigate and submit upstream patch
%if 0%{?el6}
sed 's#$this->_em->clear();#if (isset($this->_em)) { $this->_em->clear(); }#' \
    -i tests/Doctrine/Tests/OrmFunctionalTestCase.php
%endif

%{__phpunit} --include-path ./lib:./tests -d date.timezone="UTC" -d memory_limit="512M"
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
