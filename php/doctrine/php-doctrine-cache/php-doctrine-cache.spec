# remirepo spec file for php-doctrine-cache, from:
#
# Fedora spec file for php-doctrine-cache
#
# Copyright (c) 2013-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      cache
%global github_version   1.6.0
%global github_commit    f8af318d14bdb0eff0336795b428b547bd39ccb6

%global composer_vendor  doctrine
%global composer_project cache

# "php": "~5.5|~7.0"
%global php_min_ver 5.5
%global php_max_ver 8.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       Doctrine Cache

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
## phpcompatinfo (computed from version 1.6.0)
BuildRequires: php-date
BuildRequires: php-hash
BuildRequires: php-reflection
BuildRequires: php-spl
%if 0%{?rhel} != 5
BuildRequires: php-sqlite3
%endif
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php(language) <  %{php_max_ver}
# phpcompatinfo (computed from version 1.6.0)
Requires:      php-date
Requires:      php-hash
Requires:      php-spl
%if 0%{?rhel} != 5
Requires:      php-sqlite3
%endif
# Autoloader
Requires:      php-composer(symfony/class-loader)
# Weak dependencies
%if 0%{?fedora} > 21
Suggests:      php-composer(predis/predis)
Suggests:      php-pecl(apcu)
Suggests:      php-pecl(memcache)
Suggests:      php-pecl(memcached)
Suggests:      php-pecl(mongo)
Suggests:      php-pecl(redis)
Suggests:      php-xcache
%endif

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

# Extracted from Doctrine Common as of version 2.4
Conflicts:     php-pear(pear.doctrine-project.org/DoctrineCommon) < 2.4

%description
Cache component extracted from the Doctrine Common project.

Autoloader: %{phpdir}/Doctrine/Common/Cache/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Remove files that will never be used
find . -name '*WinCache*' -delete
find . -name '*ZendDataCache*' -delete

: Create autoloader
cat <<'AUTOLOAD' | tee lib/Doctrine/Common/Cache/autoload.php
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

$fedoraClassLoader->addPrefix('Doctrine\\Common\\Cache\\', dirname(dirname(dirname(__DIR__))));

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
: Create tests autoloader
cat <<'AUTOLOAD' | tee autoload.php
<?php

$fedoraClassLoader =
    require_once '%{buildroot}%{phpdir}/Doctrine/Common/Cache/autoload.php';

$fedoraClassLoader->addPrefix('Doctrine\\Tests', __DIR__ . '/tests');
AUTOLOAD

: Skip tests known to fail
rm -f tests/Doctrine/Tests/Common/Cache/ApcCacheTest.php

: Skip tests requiring a server to connect to
rm -f \
    tests/Doctrine/Tests/Common/Cache/CouchbaseCacheTest.php \
    tests/Doctrine/Tests/Common/Cache/MemcacheCacheTest.php \
    tests/Doctrine/Tests/Common/Cache/MemcachedCacheTest.php \
    tests/Doctrine/Tests/Common/Cache/MongoDBCacheTest.php \
    tests/Doctrine/Tests/Common/Cache/PredisCacheTest.php \
    tests/Doctrine/Tests/Common/Cache/RedisCacheTest.php \
    tests/Doctrine/Tests/Common/Cache/RiakCacheTest.php
%if 0%{?rhel} == 5
rm  tests/Doctrine/Tests/Common/Cache/SQLite3CacheTest.php
%endif

: Run tests
run=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap autoload.php
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap autoload.php
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose --bootstrap autoload.php
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
%dir %{phpdir}/Doctrine
%dir %{phpdir}/Doctrine/Common
     %{phpdir}/Doctrine/Common/Cache


%changelog
* Sat Mar 12 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.6.0-1
- Updated to 1.6.0 (RHBZ #1295634)
- Removed "phpunit without assertNotFalse() function" patch since
  this version will never be built for EL6 (b/c of PHP min version
  dependency)

* Fri Dec 25 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.5.4-1
- Updated to 1.5.4 (RHBZ #1276019)
- Added "Suggests" weak dependencies

* Sat Sep 05 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.4.2-1
- Updated to 1.4.2 (RHBZ #1258670 / CVE-2015-5723)

* Sat Jun 27 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.4.1-2
- Updated autoloader with trailing separator

* Wed Jun 24 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.4.1-1
- Updated to 1.4.1 (RHBZ #1211817)
- Added autoloader

* Fri Jan 30 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.4.0-1
- Updated to 1.4.0 (BZ #1183598)

* Wed Sep 24 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.1-1
- Updated to 1.3.1 (BZ #1142986)
- Tests update
- %%license usage

* Tue Sep 23 2014 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- update to 1.3.1

* Fri Jun 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.0-4
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide
- Removed %%{summary_base}
- Added option to build without tests

* Sat Jan 11 2014 Remi Collet <rpms@famillecollet.com> 1.3.0-2
- backport for remi repo

* Fri Jan 03 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.0-2
- Conditional %%{?dist}
- Removed sub-packages
- Skip all tests requiring a server to connect to

* Mon Dec 23 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.0-1
- Initial package
