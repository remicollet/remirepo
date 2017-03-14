# remirepo spec file for php-pecl-mysql-xdevapi
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package       php-pecl-mysql-xdevapi
%endif

%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name   mysql_xdevapi
%global with_tests  0%{?_with_tests:1}
# After 20-json, 20-mysqlnd
%global ini_name    40-%{pecl_name}.ini

Summary:        MySQL database access functions
Name:           %{?sub_prefix}php-pecl-mysql-xdevapi
Version:        1.0.1
Release:        1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}

License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz

# Workaround for out-of-tree build
Patch0:         %{pecl_name}-build.patch

BuildRequires:  %{?scl_prefix}php-devel > 7.1
BuildRequires:  %{?scl_prefix}php-mysqlnd
BuildRequires:  %{?scl_prefix}php-json
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  protobuf-devel
BuildRequires:  protobuf-c-devel
BuildRequires:  boost-devel
BuildRequires:  openssl-devel
%if %{with_tests}
BuildRequires:  community-mysql-server >= 5.7.12
%endif

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-mysqlnd%{?_isa}
Requires:       %{?scl_prefix}php-json%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
# Notice pecl_name != name
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
Obsoletes:     php71u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php71w-pecl-%{pecl_name} <= %{version}
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The X DevAPI is he new common API for MySQL Connectors built on the X Protocol
introduced in MySQL 5.7.12.

The X DevAPI wraps powerful concepts in a simple API.

* A new high-level session concept enables you to write code that
  can transparently scale from single MySQL Server to a multiple server
  environment.
* Read operations are simple and easy to understand.

The X DevAPI introduces a new, modern and easy-to-learn way to work with your
data.

* Documents are stored in Collections and have their dedicated CRUD
  operation set.
* Work with your existing domain objects or generate code based on structure
  definitions for strictly typed languages.
* Focus is put on working with data via CRUD operations. 
  See Section 3.1, “CRUD Operations Overview”.
* Modern practices and syntax styles are used to get away from traditional
  SQL-String-Building. See Chapter 10, Building Expressions.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%package devel
Summary:       %{name} developer files (header)
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{?scl_prefix}php-devel%{?_isa}

%description devel
These are the files needed to compile programs using %{name}.


%prep
%setup -qc
mv %{pecl_name}-%{version} NTS

%{?_licensedir:sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml}

cd NTS
%patch0 -p1 -b .old

# Check version as upstream often forget to update this
extver=$(sed -n '/#define PHP_MYSQL_XDEVAPI_VERSION/{s/.* "//;s/".*$//;p}' php_mysql_xdevapi.h)
if test "x${extver}" != "x%{version}%{?prever}%{?gh_date:-dev}"; then
   : Error: Upstream YAC version is ${extver}, expecting %{version}%{?prever}%{?gh_date:-dev}.
   exit 1
fi
cd ..


%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif

# Create configuration file
cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; Configuration
;xmysqlnd.collect_statistics = 1
;xmysqlnd.collect_memory_statistics = 0
;xmysqlnd.debug = ''
;xmysqlnd.trace_alloc = ''
;xmysqlnd.net_read_timeout = 31536000
;xmysqlnd.mempool_default_size= 16000
EOF


%build
%{?dtsenable}

peclconf() {
%configure \
    --enable-mysql-xdevapi \
    --with-php-config=$1
}

cd NTS
%{_bindir}/phpize
peclconf %{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
peclconf %{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
%{?dtsenable}

# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Install the ZTS stuff
%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Test & Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do [ -f NTS/$i ] &&  install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd NTS

: Minimal load test for NTS extension
%{_bindir}/php --no-php-ini \
    --define extension=mysqlnd.so \
    --define extension=json.so \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

%if %{with_zts}
cd ../ZTS

: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=mysqlnd.so \
    --define extension=json.so \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

%endif

%if %{with_tests}
cd ../NTS
RET=0

: Running a server
MYSQLX_TEST_HOST=127.0.0.1
MYSQLX_TEST_PORT=3308
MYSQLX_TEST_SOCKET=$PWD/mysql.sock
MYSQLX_PID_FILE=$PWD/mysql.pid

rm -rf data
mkdir  data
%{_bindir}/mysql_install_db \
   --datadir=$PWD/data

%{_libexecdir}/mysqld \
   --socket=$MYSQLX_TEST_SOCKET \
   --log-error=$PWD/mysql.log \
   --pid-file=$MYSQLX_PID_FILE \
   --port=$MYSQLX_TEST_PORT \
   --datadir=$PWD/data &

n=15
while [ $n -gt 0 ]; do
  RESPONSE=$(%{_bindir}/mysqladmin --no-defaults --socket="$MYSQL_TEST_SOCKET" --user=root ping 2>&1 || :)
  if [ "$RESPONSE" == "mysqld is alive" ]; then
    break
  fi
  n=$(expr $n - 1)
  sleep 1
done

: Run upstream test suite
sed -e "s/localhost/$MYSQL_TEST_HOST/;s/3306/$MYSQL_TEST_PORT/" -i tests/connect.inc

if [ $n -gt 0 ]; then
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=mysqlnd.so -d extension=json.so -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff || RET=1
fi

: Cleanup
if [ -s $MYSQL_PID_FILE ]; then
  kill $(cat $MYSQL_PID_FILE)
fi

exit $RET
%endif


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
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%endif


%files devel
%doc %{pecl_testdir}/%{pecl_name}
%{php_incldir}/ext/%{pecl_name}

%if %{with_zts}
%{php_ztsincldir}/ext/%{pecl_name}
%endif


%changelog
* Tue Mar 14 2017 Remi Collet <remi@remirepo.net> - 1.0.1-1
- Update to 1.0.1

* Thu Dec  8 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package, version 1.0.0 (alpha)

