# remirepo spec file for php-pecl-mongodb
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
%scl_package       php-pecl-mongodb
%else
%global _root_prefix %{_prefix}
%endif

%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name  mongodb
%if "%{php_version}" < "5.6"
%global ini_name   z-%{pecl_name}.ini
%else
# After 40-smbclient.ini, see https://jira.mongodb.org/browse/PHPC-658
%global ini_name   50-%{pecl_name}.ini
%endif
#global prever     RC0
# Still needed because of some private API
%global buildver %(pkg-config --silence-errors --modversion libmongoc-priv 2>/dev/null || echo 65536)

%ifarch x86_64
%global with_tests   0%{?_with_tests:1}
%else
# See https://jira.mongodb.org/browse/CDRIVER-1186
# 32-bit MongoDB support was officially deprecated
# in MongoDB 3.2, and support is being removed in 3.4.
%global with_tests   0%{?_with_tests:1}
%endif

Summary:        MongoDB driver for PHP
Name:           %{?sub_prefix}php-pecl-%{pecl_name}
Version:        1.1.8
Release:        2%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz

# Fix tests when using system libraries
Patch0:         %{pecl_name}-tests.patch

BuildRequires:  %{?scl_prefix}php-devel > 5.4
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  cyrus-sasl-devel
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig(libbson-1.0)    >= 1.3.0
BuildRequires:  pkgconfig(libmongoc-1.0)  >= 1.3.0
BuildRequires:  pkgconfig(libmongoc-priv) >= 1.3.0
BuildRequires:  pkgconfig(libmongoc-priv) <  1.4
%if %{with_tests}
BuildRequires:  mongodb-server
%endif

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       mongo-c-driver%{?_isa} >= %{buildver}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

# Don't provide php-mongodb which is the pure PHP library
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php53u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php54-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php54w-pecl-%{pecl_name} <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.1"
Obsoletes:     php71u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php71w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The purpose of this driver is to provide exceptionally thin glue between
MongoDB and PHP, implementing only fundemental and performance-critical
components necessary to build a fully-functional MongoDB driver.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
mv %{pecl_name}-%{version}%{?prever} NTS

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS
%patch0 -p0 -b .rpm

# Sanity check, really often broken
extver=$(sed -n '/#define MONGODB_VERSION_S/{s/.* "//;s/".*$//;p}' php_phongo.h)
if test "x${extver}" != "x%{version}%{?prever:%{prever}}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever:%{prever}}.
   exit 1
fi
cd ..

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif

# Create configuration file
cat << 'EOF' | tee %{ini_name}
; Enable %{summary} extension module
extension=%{pecl_name}.so

; Configuration
;mongodb.debug=''
EOF


%build
peclbuild() {
  %{_bindir}/${1}ize

  # Ensure we use system library
  # Need to be removed only after phpize because of m4_include
  rm -r src/libbson
  rm -r src/libmongoc

  %configure \
    --with-php-config=%{_bindir}/${1}-config \
    --with-libbson \
    --with-libmongoc \
    --enable-mongodb

  make %{?_smp_mflags}
}

cd NTS
peclbuild php

%if %{with_zts}
cd ../ZTS
peclbuild zts-php
%endif


%install
make -C NTS \
     install INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS \
     install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%if 0%{?fedora} < 24
# when pear installed alone, after us
%triggerin -- %{?scl_prefix}php-pear
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

# posttrans as pear can be installed after us
%posttrans
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

%postun
if [ $1 -eq 0 -a -x %{__pecl} ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%check
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif

%if %{with_tests}
ret=0

%global mongo_version  %(mongod --version | sed -n '/db version/{s/.*v//;p}' 2>/dev/null)

: Run a mongodb server version %{mongo_version}
mkdir dbtest
mongod \
  --journal \
  --bind_ip     127.0.0.1 \
  --unixSocketPrefix /tmp \
  --logpath     $PWD/server.log \
  --pidfilepath $PWD/server.pid \
  --dbpath      $PWD/dbtest \
  --fork   || : skip test as server cant start

if [ -s server.pid ] ; then
  : Drop known to fail tests
%if 1
    ### With mongodb 3.2
    rm ?TS/tests/manager/manager-debug-001.phpt
    rm ?TS/tests/manager/manager-debug-003.phpt
    rm ?TS/tests/manager/manager-executequery-without-assignment.phpt
    rm ?TS/tests/standalone/bug0487-002.phpt
    rm ?TS/tests/standalone/bug0655.phpt
%endif
%if "%{mongo_version}" < "3.2"
    ### With mongodb 3.0
    rm ?TS/tests/manager/manager-executeBulkWrite-011.phpt
    rm ?TS/tests/manager/manager-executeQuery-002.phpt
    rm ?TS/tests/readPreference/bug0146-002.phpt
%endif
%if "%{mongo_version}" < "3.0"
    ### Older mongodb
    rm ?TS/tests/bulk/write-0003.phpt
    rm ?TS/tests/manager/manager-executeBulkWrite_error-001.phpt
    rm ?TS/tests/manager/manager-executeBulkWrite_error-002.phpt
%endif

  : Run the test suite
  echo '{"STANDALONE": "mongodb://127.0.0.1:27017"}' | tee /tmp/PHONGO-SERVERS.json

  pushd NTS
    TEST_PHP_EXECUTABLE=%{__php} \
    TEST_PHP_ARGS="-n -d extension=json.so -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
    NO_INTERACTION=1 \
    REPORT_EXIT_STATUS=1 \
    php -n run-tests.php --show-diff || ret=1
  popd

%if %{with_zts}
  pushd ZTS
    TEST_PHP_EXECUTABLE=%{__ztsphp} \
    TEST_PHP_ARGS="-n -d extension=json.so -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so" \
    NO_INTERACTION=1 \
    REPORT_EXIT_STATUS=1 \
    php -n run-tests.php --show-diff || ret=1
  popd
%endif

  : Cleanup
  kill $(cat server.pid)
fi

exit $ret
%else
: check disabled, missing '--with tests' option
%endif


%files
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Wed Jul 06 2016 Remi Collet <remi@fedoraproject.org> - 1.1.8-1
- Update to 1.1.8

* Fri Jun  3 2016 Remi Collet <remi@fedoraproject.org> - 1.1.7-3
- run the test suite during the build (x86_64 only)
- ignore known to fail tests

* Thu Jun  2 2016 Remi Collet <remi@fedoraproject.org> - 1.1.7-2
- Update to 1.1.7

* Thu Apr  7 2016 Remi Collet <remi@fedoraproject.org> - 1.1.6-2
- Update to 1.1.6

* Thu Mar 31 2016 Remi Collet <remi@fedoraproject.org> - 1.1.5-4
- load after smbclient to workaround
  https://jira.mongodb.org/browse/PHPC-658

* Fri Mar 18 2016 Remi Collet <remi@fedoraproject.org> - 1.1.5-2
- Update to 1.1.5 (stable)

* Thu Mar 10 2016 Remi Collet <remi@fedoraproject.org> - 1.1.4-2
- Update to 1.1.4 (stable)

* Sat Mar  5 2016 Remi Collet <remi@fedoraproject.org> - 1.1.3-2
- Update to 1.1.3 (stable)

* Thu Jan 07 2016 Remi Collet <remi@fedoraproject.org> - 1.1.2-2
- Update to 1.1.2 (stable)

* Thu Dec 31 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-4
- fix patch for 32bits build
  open https://github.com/mongodb/mongo-php-driver/pull/191

* Sat Dec 26 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-2
- Update to 1.1.1 (stable)
- add patch for 32bits build,
  open https://github.com/mongodb/mongo-php-driver/pull/185

* Wed Dec 16 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0 (stable)
- raise dependency on libmongoc >= 1.3.0

* Tue Dec  8 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-2
- update to 1.0.1 (stable)
- ensure libmongoc >= 1.2.0 and < 1.3 is used

* Fri Oct 30 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- update to 1.0.0 (stable)

* Tue Oct 27 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.5.RC0
- Update to 1.0.0RC0 (beta)

* Tue Oct  6 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3-beta2
- Update to 1.0.0beta2 (beta)

* Fri Sep 11 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2-beta1
- Update to 1.0.0beta1 (beta)

* Mon Aug 31 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.alpha2
- Update to 1.0.0alpha2 (alpha)
- buid with system libmongoc

* Thu May 07 2015 Remi Collet <remi@fedoraproject.org> - 0.6.3-1
- Update to 0.6.3 (alpha)

* Wed May 06 2015 Remi Collet <remi@fedoraproject.org> - 0.6.2-1
- Update to 0.6.2 (alpha)

* Wed May 06 2015 Remi Collet <remi@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0 (alpha)

* Sat Apr 25 2015 Remi Collet <remi@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1 (alpha)

* Thu Apr 23 2015 Remi Collet <remi@fedoraproject.org> - 0.5.0-2
- build with system libbson
- open https://jira.mongodb.org/browse/PHPC-259

* Wed Apr 22 2015 Remi Collet <remi@fedoraproject.org> - 0.5.0-1
- initial package, version 0.5.0 (alpha)

