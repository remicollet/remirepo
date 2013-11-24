# spec file for php-pecl-sqlite
#
# Copyright (c) 2011-2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?php_incldir: %global php_incldir %{_includedir}/php}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global pecl_name   sqlite
%global svnver      332053
%global extver      2.0-dev
%global with_zts    0%{?__ztsphp:1}
%global with_tests  %{?_without_tests:0}%{!?_without_tests:1}


Name:           php-pecl-sqlite
Version:        2.0.0
Release:        0.4.svn%{svnver}%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
Summary:        Extension for the SQLite V2 Embeddable SQL Database Engine
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
BuildRequires:  php-devel
BuildRequires:  php-pear
BuildRequires:  php-pdo
BuildRequires:  sqlite2-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires:       php-pdo%{?_isa}

Provides:       php-pecl(%{pecl_name}) = %{extver}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{extver}

# Was provided by php until 5.4.0
%if "%{php_version}" > "5.4"
Obsoletes:      php-sqlite < 5.4.0
Provides:       php-sqlite = 5.4.0
Provides:       php-sqlite%{?_isa} = 5.4.0
Obsoletes:      php-sqlite2 < 5.4.0
Provides:       php-sqlite2 = 5.4.0
Provides:       php-sqlite2%{?_isa} = 5.4.0
%endif

# Other third party repo stuff
%if "%{php_version}" > "5.4"
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
Obsoletes:     php54-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}
%endif

%if 0%{?fedora} < 20
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

cd NTS
# Check version
extver=$(sed -n '/#define PHP_SQLITE_MODULE_VERSION/{s/.*\t"//;s/".*$//;p}' sqlite.c)
if test "x${extver}" != "x%{extver}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

cat >%{pecl_name}.ini << 'EOF'
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
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
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
%{__php} run-tests.php \
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
%{__ztsphp} run-tests.php \
    -n -q \
    -d extension=pdo.so \
    -d extension=$PWD/modules/%{pecl_name}.so
%endif
%endif


%clean
rm -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ]  ; then
   %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{pecl_name}
%doc %{pecl_testdir}/%{pecl_name}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
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
