#
# RPM spec file for php-doctrine-cache
#
# Copyright (c) 2013-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      cache
%global github_version   1.4.0
%global github_commit    2346085d2b027b233ae1d5de59b07440b9f288c8

%global composer_vendor  doctrine
%global composer_project cache

# "php": ">=5.3.2"
%global php_min_ver      5.3.2

# Build using "--without tests" to disable tests
%global with_tests       %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:     %global phpdir     %{_datadir}/php}
%{!?__phpunit:  %global __phpunit  %{_bindir}/phpunit}

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
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: %{_bindir}/phpunit
# For tests: phpcompatinfo (computed from version 1.4.0)
BuildRequires: php-date
BuildRequires: php-hash
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
%endif

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.4.0)
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
mkdir -p %{buildroot}/%{phpdir}
cp -rp lib/* %{buildroot}/%{phpdir}/


%check
%if %{with_tests}
# Create tests' bootstrap
cat > bootstrap.php <<'BOOTSTRAP'
<?php

spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', str_replace('_', '/', $class)).'.php';
    @include_once $src;
});
BOOTSTRAP

# Skip tests requiring a server to connect to
rm -f \
    tests/Doctrine/Tests/Common/Cache/CouchbaseCacheTest.php \
    tests/Doctrine/Tests/Common/Cache/MongoDBCacheTest.php \
    tests/Doctrine/Tests/Common/Cache/PredisCacheTest.php \
    tests/Doctrine/Tests/Common/Cache/RiakCacheTest.php

%{__phpunit} \
    --bootstrap bootstrap.php \
    --include-path %{buildroot}/%{phpdir}:./tests
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
%dir %{_datadir}/php/Doctrine
%dir %{_datadir}/php/Doctrine/Common
     %{_datadir}/php/Doctrine/Common/Cache


%changelog
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
