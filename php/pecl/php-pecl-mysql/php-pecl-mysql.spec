# remirepo spec file for php-pecl-mysql
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package       php-pecl-mysql
%endif

# https://github.com/php/pecl-database-mysql/commits/master
%global gh_commit   230a8287c04c69dfc49f6a68a5debb4e4198e98f
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    php
%global gh_project  pecl-database-mysql
%global gh_date     20160812
%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name   mysql
%global with_tests  0%{?_with_tests:1}
# After 40-mysqlnd
%global ini_name    50-%{pecl_name}.ini
%global mysql_sock  %(mysql_config --socket 2>/dev/null || echo /var/lib/mysql/mysql.sock)

Summary:        MySQL database access functions
Name:           %{?sub_prefix}php-pecl-%{pecl_name}
Version:        1.0.0
%if 0%{?gh_date:1}
Release:        0.15.%{gh_date}git%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%else
Release:        3%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%endif

License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{pecl_name}-%{version}-%{gh_short}.tar.gz
Source1:        %{pecl_name}.ini

BuildRequires:  %{?scl_prefix}php-devel > 7
BuildRequires:  %{?scl_prefix}php-mysqlnd
BuildRequires:  %{?scl_prefix}php-pear
%if %{with_tests}
BuildRequires:  mariadb-server
%endif

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-mysqlnd%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

# Set epoch so provides is > 0:7.0.0 (obsoleted by php-mysqlnd)
Provides:       %{?scl_prefix}php-%{pecl_name}               = 1:%{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = 1:%{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
%if "%{php_version}" > "7.1"
Obsoletes:     php71u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php71w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This extension provides the mysql family of functions that were provided
with PHP 3-5. These functions have been superseded by MySQLi and PDO_MySQL,
which continue to be bundled with PHP 7.

Although it should be possible to use this extension with PHP 7.0, you are
strongly encouraged to port your code to use either MySQLi or PDO_MySQL,
as this extension is not maintained and is available for historical reasons only.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -qc
mv %{gh_project}-%{gh_commit} NTS
%{__php} -r '
  $pkg = simplexml_load_file("NTS/package.xml");
  $pkg->date = substr("%{gh_date}",0,4)."-".substr("%{gh_date}",4,2)."-".substr("%{gh_date}",6,2);
  $pkg->version->release = "%{version}dev";
  $pkg->stability->release = "devel";
  $pkg->asXML("package.xml");
'

# Don't install (register) the tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS
# Check version as upstream often forget to update this
extver=$(sed -n '/#define PHP_MYSQL_VERSION/{s/.* "//;s/".*$//;p}' php_mysql.h)
if test "x${extver}" != "x%{version}%{?prever}%{?gh_date:-dev}"; then
   : Error: Upstream YAC version is ${extver}, expecting %{version}%{?prever}%{?gh_date:-dev}.
   exit 1
fi
cd ..


%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif


%build
peclconf() {
%configure \
    --with-mysql=mysqlnd \
    --with-mysql-sock=%{mysql_sock} \
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
# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Install the ZTS stuff
%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in LICENSE $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do [ -f NTS/$i ] &&  install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd NTS

: Minimal load test for NTS extension
%{_bindir}/php --no-php-ini \
    --define extension=mysqlnd.so \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

%if %{with_zts}
cd ../ZTS

: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=mysqlnd.so \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

%endif

%if %{with_tests}
cd ../NTS
RET=0

: Running a server
MYSQL_TEST_HOST=127.0.0.1
MYSQL_TEST_PORT=3308
MYSQL_TEST_SOCKET=$PWD/mysql.sock
MYSQL_PID_FILE=$PWD/mysql.pid

rm -rf data
mkdir  data
%{_bindir}/mysql_install_db \
   --datadir=$PWD/data

%{_libexecdir}/mysqld \
   --socket=$MYSQL_TEST_SOCKET \
   --log-error=$PWD/mysql.log \
   --pid-file=$MYSQL_PID_FILE \
   --port=$MYSQL_TEST_PORT \
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

: Known to fail
rm tests/bug55473.phpt
rm tests/mysql_pconn_max_links.phpt
rm tests/mysql_query_load_data_openbasedir.phpt

if [ $n -gt 0 ]; then
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=mysqlnd.so -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
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


%changelog
* Thu Dec  9 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.15.20160812git230a828
- refresh to more recent snapshot

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.14.20160428git45881bd
- rebuild with PHP 7.1.0 GA

* Thu Sep 22 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.13.20160428git45881bd
- run upstream test suite when build using --with tests option

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.12.20160428git45881bd
- rebuild for PHP 7.1 new API version

* Wed Jun  8 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.11.20160428git45881bd
- refresh for PHP 7.1

* Sun Mar  6 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.10.20150628git3c79a97
- adapt for F24

* Tue Jan 26 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.9.20150628git3c79a97
- missing dep on php-mysqlnd

* Sun Jan 10 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.8.20150628git3c79a97
- set stability=devel in package.xml

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.7.20151007git294ce3b
- rebuild for PHP 7.0.0RC5 new API version
- new snapshot

* Wed Oct  7 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.6.20151007gitbe23da1
- refresh, new snapshot

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.5.20150703git617e510
- F23 rebuild with rh_layout

* Fri Jul 24 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.4.20150703git617e510
- provide php-mysql 1:1.0.0 > 0:7.0.0 which is obsoleted by php-mysqlnd

* Wed Jul 22 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3.20150703git617e510
- rebuild against php 7.0.0beta2

* Wed Jul  8 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.20150703git617e510
- new snapshot, rebuild against php 7.0.0beta1

* Wed Jun 24 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.20150305git01751ce
- initial package, version 1.0.0-dev
