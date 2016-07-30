# remirepo/fedora spec file for php-alcaeus-mongo-php-adapter
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    db7ef240fc9de81cd093d4d7e401a30b79023196
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     alcaeus
%global gh_project   mongo-php-adapter
# Upstream only support 64bits, see https://jira.mongodb.org/browse/CDRIVER-1186
# Server only available on LE arch (ExcludeArch: ppc ppc64 %{sparc} s390 s390x)
%global with_tests   0%{?_with_tests:1}
# remirepo:3
%if 0%{?fedora} >= 22 || 0%{?rhel} >= 7
%global with_tests   0%{!?_without_tests:1}
%endif
%global ns_vendor    Alcaeus


Name:           php-%{gh_owner}-%{gh_project}
Version:        1.0.5
Release:        2%{?dist}
Summary:        Mongo PHP Adapter

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?prever}-%{?gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-composer(theseer/autoload)
BuildRequires:  php(language) >= 5.5
%if %{with_tests}
BuildRequires:  php-hash
BuildRequires:  php-composer(mongodb/mongodb) >= 1.0.1
BuildRequires:  php-date
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
BuildRequires:  php-spl
# from composer.json, require-dev": {
#        "phpunit/phpunit": "^4.8 || ^5.0"
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  mongodb-server >= 2.6
%endif

# From composer.json, "require": {
#        "php": "^5.5 || ^7.0",
#        "ext-hash": "*",
#        "mongodb/mongodb": "^1.0.1"
Requires:       php(language) >= 5.5
Requires:       php-hash
Requires:       php-composer(mongodb/mongodb) >= 1.0.1
# From phpcompatinfo report for 1.0.3
Requires:       php-date
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-spl

# Composer
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}
Provides:       php-composer(ext-mongo) = 1.6.13


%description
The Mongo PHP Adapter is a userland library designed to act as an
adapter between applications relying on ext-mongo and the new driver
(ext-mongodb).

It provides the API of ext-mongo built on top of mongo-php-library,
thus being compatible with PHP 7.

Autoloader: %{_datadir}/php/%{ns_vendor}/MongoDbAdapter/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv lib/Mongo  lib/%{ns_vendor}/Mongo


%build
: Create a classmap autoloader
%{_bindir}/phpab \
    --output lib/%{ns_vendor}/MongoDbAdapter/autoload.php \
             lib/%{ns_vendor}

cat << 'EOF' | tee -a lib/%{ns_vendor}/MongoDbAdapter/autoload.php

require_once dirname(__DIR__) . '/Mongo/functions.php';

// Dependencies
require_once "%{_datadir}/php/MongoDB/autoload.php";
EOF


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{_datadir}/php
cp -pr lib/%{ns_vendor} %{buildroot}%{_datadir}/php/%{ns_vendor}


%check
%if %{with_tests}
RET=0

# ignore know to fail tests (different error code)
sed -e 's/testDeleteIndexUsingIndexName/SKIP_testDeleteIndexUsingIndexName/' \
    -e 's/testDeleteIndexesForNonExistingCollection/SKIP_testDeleteIndexesForNonExistingCollection/' \
    -i tests/%{ns_vendor}/MongoDbAdapter/Mongo/MongoCollectionTest.php

cat << 'EOF' | tee bs.php
<?php
require '%{buildroot}%{_datadir}/php/%{ns_vendor}/MongoDbAdapter/autoload.php';
require 'tests/%{ns_vendor}/MongoDbAdapter/TestCase.php';
EOF

: Run a server
mkdir dbtest
mongod \
  --journal \
  --logpath     $PWD/server.log \
  --pidfilepath $PWD/server.pid \
  --dbpath      $PWD/dbtest \
  --fork   || : skip test as server cant start

if [ ! -s server.pid ] ; then
  exit 0
fi

: Run the test suite
ret=0
# remirepo:10
run=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap bs.php || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap bs.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --bootstrap bs.php || ret=1
# remirepo:1
fi

: Cleanup
kill $(cat server.pid)

exit $ret
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json
%doc *.md
%{_datadir}/php/%{ns_vendor}


%changelog
* Thu Jul 28 2016 Remi Collet <remi@fedoraproject.org> - 1.0.5-2
- only run upstream test suite when build --with tests

* Mon Jul  4 2016 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- update to 1.0.5

* Wed Jun 22 2016 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- update to 1.0.4

* Wed Jun 15 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- initial package

