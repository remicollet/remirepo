%global github_owner    doctrine
%global github_name     cache
%global github_version  1.3.0
%global github_commit   e16d7adf45664a50fa86f515b6d5e7f670130449

# "php": ">=5.3.2"
%global php_min_ver     5.3.2
# "phpunit/phpunit": ">=3.7"
%global phpunit_min_ver 3.7

%global summary_base    Doctrine Cache

Name:          php-%{github_owner}-%{github_name}
Version:       %{github_version}
Release:       2%{?dist}
Summary:       %{summary_base}

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# For tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit) >= %{phpunit_min_ver}
# For tests: phpcompatinfo (computed from v1.3.0)
BuildRequires: php-date
BuildRequires: php-hash
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from git commit v1.3.0)
Requires:      php-date
Requires:      php-hash
Requires:      php-pcre
Requires:      php-spl

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
%setup -q -n %{github_name}-%{github_commit}

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
cat phpunit.xml.dist \
    | sed 's/colors="true"/colors="false"/' \
    > phpunit.xml

# Skip tests requiring a server to connect to
rm -f \
    tests/Doctrine/Tests/Common/Cache/CouchbaseCacheTest.php \
    tests/Doctrine/Tests/Common/Cache/MongoDBCacheTest.php \
    tests/Doctrine/Tests/Common/Cache/RiakCacheTest.php

%{_bindir}/phpunit --include-path ./lib:./tests -d date.timezone="UTC"


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE *.md composer.json
%dir %{_datadir}/php/Doctrine
%dir %{_datadir}/php/Doctrine/Common
     %{_datadir}/php/Doctrine/Common/Cache


%changelog
* Sat Jan 11 2014 Remi Collet <rpms@famillecollet.com> 1.3.0-2
- backport for remi repo

* Fri Jan 03 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.0-2
- Conditional %%{?dist}
- Removed sub-packages
- Skip all tests requiring a server to connect to

* Mon Dec 23 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.0-1
- Initial package
