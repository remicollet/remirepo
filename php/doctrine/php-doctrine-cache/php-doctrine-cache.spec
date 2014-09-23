#
# RPM spec file for php-doctrine-cache
#
# Copyright (c) 2013-2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      cache
%global github_version   1.3.1
%global github_commit    cf483685798a72c93bf4206e3dd6358ea07d64e7

%global composer_vendor  doctrine
%global composer_project cache

# "php": ">=5.3.2"
%global php_min_ver      5.3.2
# "phpunit/phpunit": ">=3.7"
%global phpunit_min_ver  3.7

# Build using "--without tests" to disable tests
%global with_tests       %{?_without_tests:0}%{!?_without_tests:1}

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
%if %{with_tests}
# For tests
BuildRequires: php(language)       >= %{php_min_ver}
BuildRequires: php-phpunit-PHPUnit >= %{phpunit_min_ver}
# For tests: phpcompatinfo (computed from v1.3.0)
BuildRequires: php-date
BuildRequires: php-hash
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
%endif

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from git commit v1.3.0)
Requires:      php-date
Requires:      php-hash
Requires:      php-pcre
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

# Extracted from Doctrine Common as of version 2.4
Conflicts:     php-pear(pear.doctrine-project.org/DoctrineCommon) < 2.4

%description
Cache component extracted from the Doctrine Common project.

Optional:
* APC (php-pecl-apc)
* Couchbase (http://pecl.php.net/package/couchbase)
* Memcache (php-pecl-memcache)
* Memcached (php-pecl-memcached)
* MongoDB (php-pecl-mongo)
* Redis (php-pecl-redis)
* Riak (http://pecl.php.net/package/riak)
* XCache (php-xcache)


%prep
%setup -qn %{github_name}-%{github_commit}

# Remove files that will never be used
find . -name '*WinCache*' -delete
find . -name '*ZendDataCache*' -delete


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/php
cp -rp lib/* %{buildroot}/%{_datadir}/php/


%check
%if %{with_tests}
# Create tests' init
cat > tests/Doctrine/Tests/TestInit.php <<'TESTINIT'
<?php
namespace Doctrine\Tests;

spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', str_replace('_', '/', $class)).'.php';
    @include_once $src;
});
TESTINIT

# Create PHPUnit config w/ colors turned off
sed 's/colors="true"/colors="false"/' phpunit.xml.dist > phpunit.xml

# Skip tests requiring a server to connect to
rm -f \
    tests/Doctrine/Tests/Common/Cache/CouchbaseCacheTest.php \
    tests/Doctrine/Tests/Common/Cache/MongoDBCacheTest.php \
    tests/Doctrine/Tests/Common/Cache/RiakCacheTest.php

%{_bindir}/phpunit --include-path ./lib:./tests -d date.timezone="UTC"
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE *.md composer.json
%dir %{_datadir}/php/Doctrine
%dir %{_datadir}/php/Doctrine/Common
     %{_datadir}/php/Doctrine/Common/Cache


%changelog
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
