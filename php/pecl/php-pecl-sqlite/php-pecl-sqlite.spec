# spec file for php-pecl-sqlite
#
# Copyright (c) 2011-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package        php-pecl-ssdeep}

%global pecl_name   sqlite
%global svnver      332053
%global extver      2.0-dev
%global with_zts    0%{?__ztsphp:1}
%global with_tests  %{?_without_tests:0}%{!?_without_tests:1}
%if "%{php_version}" < "5.6"
# After pdo
%global ini_name  %{pecl_name}.ini
%else
# After 20-pdo
%global ini_name  40-%{pecl_name}.ini
%endif


Summary:        Extension for the SQLite V2 Embeddable SQL Database Engine
Name:           %{?scl_prefix}php-pecl-sqlite
Version:        2.0.0
Release:        0.9.svn%{svnver}%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
Group:          Development/Languages
License:        PHP
URL:            http://pecl.php.net/package/%{pecl_name}
%if 0%{?svnver}
# svn export -r 332053 https://svn.php.net/repository/pecl/sqlite/trunk sqlite
# tar czf sqlite-svn332053.tgz sqlite
Source0:        sqlite-svn%{svnver}.tgz
%else
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-pdo
BuildRequires:  sqlite2-devel

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-pdo%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

# Was provided by php until 5.4.0
Obsoletes:      %{?scl_prefix}php-%{pecl_name}               < 5.4.0
Provides:       %{?scl_prefix}php-%{pecl_name}               = 1:%{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = 1:%{version}
Obsoletes:      %{?scl_prefix}php-%{pecl_name}2              < 5.4.0
Provides:       %{?scl_prefix}php-%{pecl_name}2              = 1:%{version}
Provides:       %{?scl_prefix}php-%{pecl_name}2%{?_isa}      = 1:%{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
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
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This is an extension for the SQLite 2 Embeddable SQL Database Engine.
http://www.sqlite.org/

SQLite is a C library that implements an embeddable SQL database engine.
Programs that link with the SQLite library can have SQL database access
without running a separate RDBMS process.

SQLite is not a client library used to connect to a big database server.
SQLite is the server. The SQLite library reads and writes directly to and from
the database files on disk

Notice: this extension is deprecated, you should consider
- sqlite3      http://php.net/sqlite3
- pdo_sqlite   http://php.net/pdo_sqlite

Documentation: http://php.net/sqlite

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -c -q

%if 0%{?svnver}
mv %{pecl_name}/package.xml .
mv %{pecl_name} NTS
# fix package release state (stability)
sed -i \
 -e '/<release>stable/s/stable/beta/' \
 package.xml
%else
mv %{pecl_name}-%{version} NTS
%endif

sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS
# Check version
extver=$(sed -n '/#define PHP_SQLITE_MODULE_VERSION/{s/.*\t"//;s/".*$//;p}' sqlite.c)
if test "x${extver}" != "x%{extver}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

cat >%{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

cp -pr NTS ZTS


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-sqlite=%{_prefix} \
    --enable-pdo \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-sqlite=%{_prefix} \
    --enable-pdo \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}
make install -C NTS INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Test & Documentation
cd NTS
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
# ignore this test for now
# TODO need investigation
rm -f ?TS/tests/sqlite_oo_026.phpt
# cannot be run, need ext/pdo/test tree
rm -f ?TS/tests/pdo/common.phpt
rm -f ?TS/tests/bug38759.phpt

: Minimal load test for NTS extension
cd NTS
%{__php} --no-php-ini \
    --define extension=pdo.so \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep -i %{pecl_name}

%if %{with_tests}
: Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__php} -n run-tests.php \
    -n -q \
    -d extension=pdo.so \
    -d extension=$PWD/modules/%{pecl_name}.so
%endif

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=pdo.so \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep -i %{pecl_name}

%if %{with_tests}
: Upstream test suite for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__ztsphp} -n run-tests.php \
    -n -q \
    -d extension=pdo.so \
    -d extension=$PWD/modules/%{pecl_name}.so
%endif
%endif


%clean
rm -rf %{buildroot}


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


%files
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{pecl_name}
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Tue Mar  8 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.9.svn332053
- adapt for F24
- drop runtime dependency on pear, new scriptlets
- don't install/register tests

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.8.svn332053
- Fedora 21 SCL mass rebuild

* Tue Aug 26 2014 Remi Collet <rcollet@redhat.com> - 2.0.0-0.7.svn332053
- improve SCL build

* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.6.svn332053
- add numerical prefix to extension configuration file (php 5.6)

* Tue Mar 25 2014 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-0.5.svn332053
- allow SCL build

* Sun Nov  3 2013 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-0.4.svn332053
- cleanup for Copr
- lastest SVN snapshot
- enable sqlite2 PDO driver
- install doc in pecl doc_dir
- install tests in pecl test_dir
- drop empty devel sub-package

* Fri Nov 30 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-0.3.svn313074
- rebuild with system Sqlite2

* Sun Oct 21 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-0.2.svn313074
- rebuild

* Sun Nov 27 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-0.1.svn313074
- initial RPM as pecl extension
