# remirepo/fedora spec file for php-mongodb
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    318d4b95438a2ea68a550c2878678097f63fb9fe
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     mongodb
#global gh_date      20151102
%global gh_project   mongo-php-library
# Upstream only support 64bits, see https://jira.mongodb.org/browse/CDRIVER-1186
# Server only available on LE arch (ExcludeArch: ppc ppc64 %{sparc} s390 s390x)
%global with_tests   0%{?_with_tests:1}
# remirepo:3
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 6
%global with_tests   0%{!?_without_tests:1}
%endif
%global psr0         MongoDB
#global prever       beta2

Name:           php-%{gh_owner}
Version:        1.1.1
%if 0%{?gh_date}
Release:        0.2.%{gh_date}git%{gh_short}%{?dist}
%else
Release:        1%{?dist}
%endif
Summary:        MongoDB driver library

Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?prever}-%{?gh_short}.tar.gz

# Autoloader
Source1:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.4
BuildRequires:  php-hash
BuildRequires:  php-json
BuildRequires:  php-spl
BuildRequires:  php-pecl(mongodb)
BuildRequires:  mongodb-server >= 2.4
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "^4.8"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.8
# For autoloader
BuildRequires:  php-composer(fedora/autoloader)
%endif

# From composer.json, "require": {
#        "php": ">=5.4"
#        "ext-mongodb": "^1.2.0"
Requires:       php(language) >= 5.4
Requires:       php-pecl(mongodb) >= 1.2.0
# From phpcompatinfo report for 1.1.1
Requires:       php-hash
Requires:       php-json
Requires:       php-spl
# For autoloader
Requires:       php-composer(fedora/autoloader)

# Composer
Provides:       php-composer(%{gh_owner}/%{gh_owner}) = %{version}%{?prever}


%description
This library provides a high-level abstraction around the lower-level drivers
for PHP and HHVM (i.e. the mongodb extension).

While the extension provides a limited API for executing commands, queries,
and write operations, this library implements an API similar to that of the
legacy PHP driver. It contains abstractions for client, database, and
collection objects, and provides methods for CRUD operations and common
commands (e.g. index and collection management).

Autoloader: %{_datadir}/php/%{psr0}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE1} src/autoload.php


%build
# Nothing


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{_datadir}/php
cp -pr src %{buildroot}%{_datadir}/php/%{psr0}


%check
%if %{with_tests}
: Run a server
mkdir dbtest

: Choose a port to allow parallel build
port=$(php -r 'echo (27010+PHP_INT_SIZE);')

mongod \
  --journal \
  --logpath     $PWD/server.log \
  --pidfilepath $PWD/server.pid \
  --dbpath      $PWD/dbtest \
  --port        $port \
  --fork

sed -e "s/27017/$port/" phpunit.xml.dist >phpunit.xml
cat << 'EOF' | tee tests/bootstrap.php
<?php
// Library
require_once '%{buildroot}%{_datadir}/php/%{psr0}/autoload.php';
// Test suite
\Fedora\Autoloader\Autoload::addPsr4('MongoDB\\Tests\\', __DIR__);
EOF

: Run the test suite
RET=0
# remirepo:10
run=0
if which php56; then
  php56 %{_bindir}/phpunit --verbose || RET=1
  run=1
fi
if which php71; then
  php71 %{_bindir}/phpunit --verbose || RET=1
  run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose || RET=1
# remirepo:1
fi

: Cleanup
[ -s server.pid ] && kill $(cat server.pid)

exit $RET
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
%doc docs
%{_datadir}/php/%{psr0}


%changelog
* Thu Jan 19 2017 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1

* Wed Dec  7 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0
- raise dependency on php-pecl-mongodb 1.2.0
- switch to fedora/autoloader

* Tue Dec  6 2016 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- update to 1.0.4

* Tue Sep 27 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- update to 1.0.3

* Thu Jul 28 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-2
- only run upstream test suite when build --with tests

* Thu Mar 31 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2

* Sat Mar  5 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1

* Fri Jan 22 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- update to 1.0.0

* Mon Jan  4 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.4.beta2
- update to 1.0.0beta2
- raise dependency on pecl/mongodb ^1.1.1
- run test suite with both PHP 5 and 7 when available

* Tue Nov  3 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3.beta1
- update to 1.0.0beta1

* Mon Nov  2 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.20151102gita3c0b97
- git snapshot

* Sat Oct 31 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.alpha1
- initial package

