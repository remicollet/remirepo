%global contentdir  /var/www
# API/ABI check
%global apiver      20090626
%global zendver     20090626
%global pdover      20080721
# Extension version
%global fileinfover 1.0.5-dev
%global pharver     2.0.1
%global zipver      1.9.1
%global jsonver     1.2.1

%define httpd_mmn %(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)

%ifarch ppc ppc64
%define oraclever 10.2.0.2
%else
%define oraclever 11.1.0.7
%endif

# Regression tests take a long time, you can skip 'em with this
%{!?runselftest: %{expand: %%global runselftest 1}}

%global snapdate 201005090630
%global phpversion 5.3.3-dev

# Optional components; pass "--with mssql" etc to rpmbuild.
%define with_oci8 	%{?_with_oci8:1}%{!?_with_oci8:0}
%define with_ibase 	%{?_with_ibase:1}%{!?_with_ibase:0}
%if %{?rhel}%{?fedora} > 4
%define with_enchant 1
%else
%define with_enchant 0
%endif

%define tidyver 	0.99.0-12.20070228

Summary: PHP scripting language for creating dynamic web sites
Name: php
Version: 5.3.3
Release: 0.1.%{snapdate}%{?dist}
License: PHP
Group: Development/Languages
URL: http://www.php.net/

%if 0%{?snapdate:1}
Source0: http://www.php.net/distributions/php5.3-%{snapdate}.tar.bz2
%else
Source0: http://downloads.php.net/ilia/php-%{phpversion}.tar.bz2
%endif
Source1: php.conf
Source2: php-53-remi.ini
Source3: macros.php

# Build fixes
Patch1: php-5.3.3-gnusrc.patch
Patch2: php-5.3.0-install.patch
Patch3: php-5.2.4-norpath.patch
Patch4: php-5.3.0-phpize64.patch
Patch5: php-5.2.0-includedir.patch
Patch6: php-5.2.4-embed.patch
Patch7: php-5.3.0-recode.patch
Patch8: php-5.3.3-aconf26x.patch

# http://bugs.php.net/50578
Patch9: php-5.3.2-phar.patch

# Fixes for extension modules
Patch20: php-4.3.11-shutdown.patch
Patch21: php-5.2.3-macropen.patch

# Functional changes
Patch40: php-5.0.4-dlopen.patch
Patch41: php-5.3.0-easter.patch
Patch42: php-5.3.1-systzdata-v7.patch

# Fixes for tests
Patch61: php-5.0.4-tests-wddx.patch

# RC Patch
Patch91: php-5.3.2-oci8conf.patch


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: bzip2-devel, curl-devel >= 7.9, db4-devel, gmp-devel
BuildRequires: httpd-devel >= 2.0.46-1, pam-devel
BuildRequires: libstdc++-devel, openssl-devel, sqlite-devel >= 3.0.0
%if 0%{?fedora} >= 9
BuildRequires: sqlite-devel >= 3.5.9
%endif
BuildRequires: sqlite2-devel >= 2.8.0
BuildRequires: zlib-devel, smtpdaemon, libedit-devel
%if 0%{?fedora} >= 8
BuildRequires: pcre-devel >= 7.3
%endif
BuildRequires: bzip2, perl, libtool >= 1.4.3, gcc-c++
Obsoletes: php-dbg, php3, phpfi, stronghold-php
Requires: httpd-mmn = %{httpd_mmn}
Provides: mod_php = %{version}-%{release}
Requires: php-common = %{version}-%{release}
# For backwards-compatibility, require php-cli for the time being:
Requires: php-cli = %{version}-%{release}
# To ensure correct /var/lib/php/session ownership:
Requires(pre): httpd

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated webpages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts. 

The php package contains the module which adds support for the PHP
language to Apache HTTP Server.

%package cli
Group: Development/Languages
Summary: Command-line interface for PHP
Requires: php-common = %{version}-%{release}
Provides: php-cgi = %{version}-%{release}
Provides: php-pcntl, php-readline

%description cli
The php-cli package contains the command-line interface 
executing PHP scripts, /usr/bin/php, and the CGI interface.

%package zts
Group: Development/Languages
Summary: Thread-safe PHP interpreter for use with the Apache HTTP Server
Requires: php-common = %{version}-%{release}
Requires: httpd-mmn = %{httpd_mmn}
BuildRequires: libtool-ltdl-devel

%description zts
The php-zts package contains a module for use with the Apache HTTP
Server which can operate under a threaded server processing model.

%package common
Group: Development/Languages
Summary: Common files for PHP
Provides: php-api = %{apiver}, php-zend-abi = %{zendver}
Provides: php(api) = %{apiver}, php(zend-abi) = %{zendver}
# Provides for all builtin modules:
Provides: php-bz2, php-calendar, php-ctype, php-curl, php-date, php-exif
Provides: php-ftp, php-gettext, php-gmp, php-hash, php-iconv, php-libxml
Provides: php-reflection, php-session, php-shmop, php-simplexml, php-sockets
Provides: php-spl, php-tokenizer, php-openssl, php-pcre
Provides: php-zlib, php-json, php-zip, php-fileinfo
Obsoletes: php-openssl, php-pecl-zip, php-pecl-json, php-json, php-pecl-phar, php-pecl-Fileinfo
# For obsoleted pecl extension
Provides: php-pecl-json = %{jsonver}, php-pecl(json) = %{jsonver}
Provides: php-pecl-zip = %{zipver}, php-pecl(zip) = %{zipver}
Provides: php-pecl-phar = %{pharver}, php-pecl(phar) = %{pharver}
Provides: php-pecl-Fileinfo = %{fileinfover}, php-pecl(Fileinfo) = %{fileinfover}

%description common
The php-common package contains files used by both the php
package and the php-cli package.

%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions
Requires: php = %{version}-%{release}, autoconf, automake
Obsoletes: php-pecl-pdo-devel

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%package imap
Summary: A module for PHP applications that use IMAP
Group: Development/Languages
Requires: php-common = %{version}-%{release}
Obsoletes: mod_php3-imap, stronghold-php-imap
BuildRequires: krb5-devel, openssl-devel, libc-client-devel

%description imap
The php-imap package contains a dynamic shared object (DSO) for the
Apache Web server. When compiled into Apache, the php-imap module will
add IMAP (Internet Message Access Protocol) support to PHP. IMAP is a
protocol for retrieving and uploading e-mail messages on mail
servers. PHP is an HTML-embedded scripting language. If you need IMAP
support for PHP applications, you will need to install this package
and the php package.

%package ldap
Summary: A module for PHP applications that use LDAP
Group: Development/Languages
Requires: php-common = %{version}-%{release}
Obsoletes: mod_php3-ldap, stronghold-php-ldap
BuildRequires: cyrus-sasl-devel, openldap-devel, openssl-devel

%description ldap
The php-ldap package is a dynamic shared object (DSO) for the Apache
Web server that adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language. If you need LDAP support for PHP applications, you will
need to install this package in addition to the php package.

%package pdo
Summary: A database access abstraction module for PHP applications
Group: Development/Languages
Requires: php-common = %{version}-%{release}
Obsoletes: php-pecl-pdo-sqlite, php-pecl-pdo, php-sqlite2
Provides: php-pdo-abi = %{pdover}
Provides: php-sqlite, php-sqlite2, php-sqlite3, php-pdo_sqlite

%description pdo
The php-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other 
databases.

%package mysql
Summary: A module for PHP applications that use MySQL databases
Group: Development/Languages
Requires: php-common = %{version}-%{release}, php-pdo
Provides: php_database, php-mysqli, php-pdo_mysql
Obsoletes: mod_php3-mysql, stronghold-php-mysql
BuildRequires: mysql-devel >= 4.1.0

%description mysql
The php-mysql package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

%package pgsql
Summary: A PostgreSQL database module for PHP
Group: Development/Languages
Requires: php-common = %{version}-%{release}, php-pdo
Provides: php_database, php-pdo_pgsql
Obsoletes: mod_php3-pgsql, stronghold-php-pgsql
BuildRequires: krb5-devel, openssl-devel, postgresql-devel

%description pgsql
The php-pgsql package includes a dynamic shared object (DSO) that can
be compiled in to the Apache Web server to add PostgreSQL database
support to PHP. PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.

%package process
Summary: Modules for PHP script using system process interfaces
Group: Development/Languages
Requires: php-common = %{version}-%{release}
Provides: php-posix, php-sysvsem, php-sysvshm, php-sysvmsg

%description process
The php-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.

%package odbc
Group: Development/Languages
Requires: php-common = %{version}-%{release}, php-pdo
Summary: A module for PHP applications that use ODBC databases
Provides: php_database, php-pdo_odbc
Obsoletes: stronghold-php-odbc
BuildRequires: unixODBC-devel

%description odbc
The php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.

%package soap
Group: Development/Languages
Requires: php-common = %{version}-%{release}
Summary: A module for PHP applications that use the SOAP protocol
BuildRequires: libxml2-devel

%description soap
The php-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.

%if %{with_ibase}
%package interbase
Summary: 	A module for PHP applications that use Interbase/Firebird databases
Group: 		Development/Languages
BuildRequires:  firebird-devel
Requires: 	php-common = %{version}-%{release}, php-pdo
Provides: 	php_database, php-firebird, php-pdo_firebird

%description interbase
The php-interbase package contains a dynamic shared object that will add
database support through Interbase/Firebird to PHP.

InterBase is the name of the closed-source variant of this RDBMS that was
developed by Borland/Inprise. 

Firebird is a commercially independent project of C and C++ programmers, 
technical advisors and supporters developing and enhancing a multi-platform 
relational database management system based on the source code released by 
Inprise Corp (now known as Borland Software Corp) under the InterBase Public
License.
%endif

%if %{with_oci8}
%package oci8
Summary: 	A module for PHP applications that use OCI8 databases
Group: 		Development/Languages
BuildRequires: 	oracle-instantclient-devel = %{oraclever}
Requires: 	php-common = %{version}-%{release}, php-pdo
Provides: 	php_database, php-pdo_oci
# Should requires libclntsh.so.11.1, but it's not provided by Oracle RPM.
AutoReq: 	0

%description oci8
The php-oci8 package contains a dynamic shared object that will add
support for accessing OCI8 databases to PHP.
%endif

%package snmp
Summary: A module for PHP applications that query SNMP-managed devices
Group: Development/Languages
Requires: php-common = %{version}-%{release}, net-snmp
BuildRequires: net-snmp-devel

%description snmp
The php-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the php package.

%package xml
Summary: A module for PHP applications which use XML
Group: Development/Languages
Requires: php-common = %{version}-%{release}
Obsoletes: php-domxml, php-dom
Provides: php-dom, php-xsl, php-domxml, php-wddx
BuildRequires: libxslt-devel >= 1.0.18-1, libxml2-devel >= 2.4.14-1

%description xml
The php-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.

%package xmlrpc
Summary: A module for PHP applications which use the XML-RPC protocol
Group: Development/Languages
Requires: php-common = %{version}-%{release}

%description xmlrpc
The php-xmlrpc package contains a dynamic shared object that will add
support for the XML-RPC protocol to PHP.

%package mbstring
Summary: A module for PHP applications which need multi-byte string handling
Group: Development/Languages
Requires: php-common = %{version}-%{release}

%description mbstring
The php-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.

%package gd
Summary: A module for PHP applications for using the gd graphics library
Group: Development/Languages
Requires: php-common = %{version}-%{release}
# Required to build the bundled GD library
BuildRequires: libjpeg-devel, libpng-devel, freetype-devel
%if 0%{?rhel}%{?fedora} > 4
BuildRequires: t1lib-devel >= 5.0.0
BuildRequires: libXpm-devel
%else
BuildRequires: xorg-x11-devel
%endif

%description gd
The php-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.

%package bcmath
Summary: A module for PHP applications for using the bcmath library
Group: Development/Languages
Requires: php-common = %{version}-%{release}

%description bcmath
The php-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.

%package dba
Summary: A database abstraction layer module for PHP applications
Group: Development/Languages
Requires: php-common = %{version}-%{release}

%description dba
The php-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.

%package mcrypt
Summary: Standard PHP module provides mcrypt library support
Group: Development/Languages
Requires: php-common = %{version}-%{release}
BuildRequires: libmcrypt-devel

%description mcrypt
The php-mcrypt package contains a dynamic shared object that will add
support for using the mcrypt library to PHP.

%package tidy
Summary: Standard PHP module provides tidy library support
Group: Development/Languages
Requires: php-common = %{version}-%{release}
BuildRequires: libtidy-devel

%description tidy
The php-tidy package contains a dynamic shared object that will add
support for using the tidy library to PHP.

%package mssql
Summary: MSSQL database module for PHP
Group: Development/Languages
Requires: php-common = %{version}-%{release}, php-pdo
BuildRequires: freetds-devel
Provides: php-pdo_dblib

%description mssql
The php-mssql package contains a dynamic shared object that will
add MSSQL database support to PHP.  It uses the TDS (Tabular
DataStream) protocol through the freetds library, hence any
database server which supports TDS can be accessed.

%package embedded
Summary: PHP library for embedding in applications
Group: System Environment/Libraries
Requires: php-common = %{version}-%{release}
# doing a real -devel package for just the .so symlink is a bit overkill
Provides: php-embedded-devel = %{version}-%{release}

%description embedded
The php-embedded package contains a library which can be embedded
into applications to provide PHP scripting language support.

%package pspell
Summary: A module for PHP applications for using pspell interfaces
Group: System Environment/Libraries
Requires: php-common = %{version}-%{release}
BuildRequires: aspell-devel >= 0.50.0

%description pspell
The php-pspell package contains a dynamic shared object that will add
support for using the pspell library to PHP.

%package recode
Summary: A module for PHP applications for using the recode library
Group: System Environment/Libraries
Requires: php-common = %{version}-%{release}
BuildRequires: recode-devel

%description recode
The php-recode package contains a dynamic shared object that will add
support for using the recode library to PHP.

%package intl
Summary: Internationalization extension for PHP applications
Group: System Environment/Libraries
Requires: php-common = %{version}-%{release}
BuildRequires: libicu-devel >= 3.6

%description intl
The php-intl package contains a dynamic shared object that will add
support for using the ICU library to PHP.

%if %{with_enchant}
%package enchant
Summary: Human Language and Character Encoding Support
Group: System Environment/Libraries
Requires: php-common = %{version}-%{release}
BuildRequires: enchant-devel >= 1.2.4

%description enchant
The php-intl package contains a dynamic shared object that will add
support for using the enchant library to PHP.
%endif


%prep
echo CIBLE = %{name}-%{version}-%{release}
%if 0%{?snapdate:1}
%setup -q -n php5.3-%{snapdate}
%else
%setup -q -n php-%{phpversion}
%endif

%patch1 -p1 -b .gnusrc
%patch2 -p1 -b .install
%patch3 -p1 -b .norpath
%patch4 -p1 -b .phpize64
%patch5 -p1 -b .includedir
%patch6 -p1 -b .embed
%patch7 -p1 -b .recode
%if 0%{?fedora} >= 13
%patch8 -p1 -b .aconf26x
%endif
%patch9 -p1 -b .bang

%patch20 -p1 -b .shutdown
%patch21 -p1 -b .macropen

%patch40 -p1 -b .dlopen
%patch41 -p1 -b .easter
%if %{?fedora}%{?rhel:99} >= 11
%patch42 -p1 -b .systzdata
%endif

#%patch60 -p1 -b .tests-dashn
%patch61 -p1 -b .tests-wddx

%patch91 -p0 -b .remi-oci8


# Awful hack for mysqlnd driver default mysql socket patch
sed -i -e s#/tmp/mysql.sock#%{_localstatedir}/lib/mysql/mysql.sock# ext/pdo_mysql/pdo_mysql.c
sed -i -e s#/tmp/mysql.sock#%{_localstatedir}/lib/mysql/mysql.sock# ext/mysqlnd/mysqlnd.c


# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp ext/ereg/regex/COPYRIGHT regex_COPYRIGHT
cp ext/gd/libgd/README gd_README

# Multiple builds for multiple SAPIs
mkdir build-cgi build-apache build-embedded build-zts
 
# Remove bogus test; position of read position after fopen(, "a+")
# is not defined by C standard, so don't presume anything.
rm -f ext/standard/tests/file/bug21131.phpt

# Tests that fail.
rm -f ext/standard/tests/file/bug22414.phpt \
      ext/iconv/tests/bug16069.phpt

# Safety check for API version change.
pver=$(sed -n '/#define PHP_VERSION /{s/.* "//;s/".*$//;p}' main/php_version.h)
if test "x${pver}" != "x%{phpversion}"; then
   : Error: Upstream PHP version is now ${pver}, expecting %{phpversion}.
   : Update the phpversion macro and rebuild.
   exit 1
fi

vapi=`sed -n '/#define PHP_API_VERSION/{s/.* //;p}' main/php.h`
if test "x${vapi}" != "x%{apiver}"; then
   : Error: Upstream API version is now ${vapi}, expecting %{apiver}.
   : Update the apiver macro and rebuild.
   exit 1
fi

vzend=`sed -n '/#define ZEND_MODULE_API_NO/{s/^[^0-9]*//;p;}' Zend/zend_modules.h`
if test "x${vzend}" != "x%{zendver}"; then
   : Error: Upstream Zend ABI version is now ${vzend}, expecting %{zendver}.
   : Update the zendver macro and rebuild.
   exit 1
fi

# Safety check for PDO ABI version change
vpdo=`sed -n '/#define PDO_DRIVER_API/{s/.*[ 	]//;p}' ext/pdo/php_pdo_driver.h`
if test "x${vpdo}" != "x%{pdover}"; then
   : Error: Upstream PDO ABI version is now ${vpdo}, expecting %{pdover}.
   : Update the pdover macro and rebuild.
   exit 1
fi

# Check for some extension version
ver=$(sed -n '/#define PHP_FILEINFO_VERSION /{s/.* "//;s/".*$//;p}' ext/fileinfo/php_fileinfo.h)
if test "$ver" != "%{fileinfover}"; then
   : Error: Upstream FILEINFO version is now ${ver}, expecting %{fileinfover}.
   : Update the fileinfover macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_PHAR_VERSION /{s/.* "//;s/".*$//;p}' ext/phar/php_phar.h)
if test "$ver" != "%{pharver}"; then
   : Error: Upstream PHAR version is now ${ver}, expecting %{pharver}.
   : Update the pharver macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_ZIP_VERSION_STRING /{s/.* "//;s/".*$//;p}' ext/zip/php_zip.h)
if test "$ver" != "%{zipver}"; then
   : Error: Upstream ZIP version is now ${ver}, expecting %{zipver}.
   : Update the zipver macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_JSON_VERSION /{s/.* "//;s/".*$//;p}' ext/json/php_json.h)
if test "$ver" != "%{jsonver}"; then
   : Error: Upstream JSON version is now ${ver}, expecting %{jsonver}.
   : Update the jsonver macro and rebuild.
   exit 1
fi


: Build for oci8=%{with_oci8} ibase=%{with_ibase}

%build
%if 0%{?fedora} >= 11
# aclocal workaround - to be improved
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >>aclocal.m4
%endif

# Force use of system libtool:
libtoolize --force --copy
%if 0%{?fedora} >= 11
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4
%else
cat `aclocal --print-ac-dir`/libtool.m4 > build/libtool.m4
%endif

# Regenerate configure scripts (patches change config.m4's)
./buildconf --force
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
%if 0%{?rhel} < 5
	CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%endif
export CFLAGS

# Install extension modules in %{_libdir}/php/modules.
EXTENSION_DIR=%{_libdir}/php/modules; export EXTENSION_DIR

# Set PEAR_INSTALLDIR to ensure that the hard-coded include_path
# includes the PEAR directory even though pear is packaged
# separately.
PEAR_INSTALLDIR=%{_datadir}/pear; export PEAR_INSTALLDIR

# Shell function to configure and build a PHP tree.
build() {
# bison-1.875-2 seems to produce a broken parser; workaround.
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend
ln -sf ../configure
%configure \
	--cache-file=../config.cache \
        --with-libdir=%{_lib} \
	--with-config-file-path=%{_sysconfdir} \
	--with-config-file-scan-dir=%{_sysconfdir}/php.d \
	--disable-debug \
	--with-pic \
	--disable-rpath \
	--without-pear \
	--with-bz2 \
	--with-exec-dir=%{_bindir} \
	--with-freetype-dir=%{_prefix} \
	--with-png-dir=%{_prefix} \
	--with-xpm-dir=%{_prefix} \
	--enable-gd-native-ttf \
%if 0%{?rhel}%{?fedora} > 4
	--with-t1lib=%{_prefix} \
%endif
	--without-gdbm \
	--with-gettext \
	--with-gmp \
	--with-iconv \
	--with-jpeg-dir=%{_prefix} \
	--with-openssl \
%if 0%{?fedora} >= 8
        --with-pcre-regex=%{_prefix} \
%endif
	--with-zlib \
	--with-layout=GNU \
	--enable-exif \
	--enable-ftp \
	--enable-magic-quotes \
	--enable-sockets \
	--enable-sysvsem --enable-sysvshm --enable-sysvmsg \
	--with-kerberos \
	--enable-ucd-snmp-hack \
	--enable-shmop \
	--enable-calendar \
        --with-libxml-dir=%{_prefix} \
	--enable-xml \
%if %{?fedora}%{?rhel:99} >= 10
        --with-system-tzdata \
%endif
	$* 
if test $? != 0; then 
  tail -500 config.log
  : configure failed
  exit 1
fi

make %{?_smp_mflags}
}

# Build /usr/bin/php-cgi with the CGI SAPI, and all the shared extensions
pushd build-cgi

# RC patch ??? (only for EL-5 ??)
mkdir -p ext/sqlite/libsqlite/src
cp ../ext/sqlite/libsqlite/src/encode.c ext/sqlite/libsqlite/src/

build --enable-force-cgi-redirect \
      --enable-pcntl \
      --with-imap=shared --with-imap-ssl \
      --enable-mbstring=shared \
      --enable-mbregex \
      --with-gd=shared \
      --enable-bcmath=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --with-mysql=shared,%{_prefix} \
      --with-mysqli=shared,%{_bindir}/mysql_config \
%ifarch x86_64
      %{?_with_oci8:--with-oci8=shared,instantclient,%{_libdir}/oracle/%{oraclever}/client64/lib,%{oraclever}} \
%else
      %{?_with_oci8:--with-oci8=shared,instantclient,%{_libdir}/oracle/%{oraclever}/client/lib,%{oraclever}} \
%endif
      %{?_with_oci8:--with-pdo-oci=shared,instantclient,/usr,%{oraclever}} \
      %{?_with_ibase:--with-interbase=shared,%{_libdir}/firebird} \
      %{?_with_ibase:--with-pdo-firebird=shared,%{_libdir}/firebird} \
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-wddx=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,%{_prefix} \
      --enable-fastcgi \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,%{_prefix} \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared,%{_prefix} \
      --with-pdo-dblib=shared,%{_prefix} \
%if 0%{?fedora} >= 9
      --with-sqlite3=shared,%{_prefix} \
%else
      --without-sqlite3 \
%endif
      --with-sqlite=shared,%{_prefix} \
      --enable-json=shared \
      --enable-zip=shared \
      --without-readline \
      --with-libedit \
      --with-pspell=shared \
      --enable-phar=shared \
      --with-mcrypt=shared,%{_prefix} \
      --with-tidy=shared,%{_prefix} \
      --with-mssql=shared,%{_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --enable-intl=shared \
      --with-icu-dir=%{_prefix} \
%if %{with_enchant}
      --with-enchant=shared,%{_prefix} \
%endif
      --with-recode=shared,%{_prefix}
popd

without_shared="--without-mysql --without-gd \
      --disable-dom --disable-dba --without-unixODBC \
      --disable-pdo --disable-xmlreader --disable-xmlwriter \
      --without-sqlite \
      --without-sqlite3 --disable-phar --disable-fileinfo \
      --disable-json --without-pspell --disable-wddx \
      --without-curl --disable-posix \
      --disable-sysvmsg --disable-sysvshm --disable-sysvsem"

# Build Apache module, and the CLI SAPI, /usr/bin/php
pushd build-apache
build --with-apxs2=%{_sbindir}/apxs ${without_shared}
popd

# Build for inclusion as embedded script language into applications,
# /usr/lib[64]/libphp5.so
pushd build-embedded
build --enable-embed ${without_shared}
popd

# Build a special thread-safe Apache SAPI
pushd build-zts

# RC patch ??? (only for EL-5 ??)
mkdir -p ext/sqlite/libsqlite/src
cp ../ext/sqlite/libsqlite/src/encode.c ext/sqlite/libsqlite/src/

EXTENSION_DIR=%{_libdir}/php/modules-zts
build --with-apxs2=%{_sbindir}/apxs \
      --enable-maintainer-zts \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d \
      --enable-force-cgi-redirect \
      --enable-pcntl \
      --with-imap=shared --with-imap-ssl \
      --enable-mbstring=shared \
      --enable-mbregex \
      --with-gd=shared \
      --enable-bcmath=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --with-mysql=shared,mysqlnd \
      --with-mysqli=shared,mysqlnd \
      --enable-mysqlnd-threading \
%ifarch x86_64
      %{?_with_oci8:--with-oci8=shared,instantclient,%{_libdir}/oracle/%{oraclever}/client64/lib,%{oraclever}} \
%else
      %{?_with_oci8:--with-oci8=shared,instantclient,%{_libdir}/oracle/%{oraclever}/client/lib,%{oraclever}} \
%endif
      %{?_with_oci8:--with-pdo-oci=shared,instantclient,/usr,%{oraclever}} \
      %{?_with_ibase:--with-interbase=shared,%{_libdir}/firebird} \
      %{?_with_ibase:--with-pdo-firebird=shared,%{_libdir}/firebird} \
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-wddx=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,%{_prefix} \
      --enable-fastcgi \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared,%{_prefix} \
      --with-pdo-dblib=shared,%{_prefix} \
%if 0%{?fedora} >= 9
      --with-sqlite3=shared,%{_prefix} \
%else
      --without-sqlite3 \
%endif
      --with-sqlite=shared,%{_prefix} \
      --enable-json=shared \
      --enable-zip=shared \
      --without-readline \
      --with-libedit \
      --with-pspell=shared \
      --enable-phar=shared \
      --with-mcrypt=shared,%{_prefix} \
      --with-tidy=shared,%{_prefix} \
      --with-mssql=shared,%{_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --enable-intl=shared \
      --with-icu-dir=%{_prefix} \
%if %{with_enchant}
      --with-enchant=shared,%{_prefix} \
%endif
      --with-recode=shared,%{_prefix}
popd

### NOTE!!! EXTENSION_DIR was changed for the -zts build, so it must remain
### the last SAPI to be built.

%check
%if %runselftest
cd build-apache
# Run tests, using the CLI SAPI
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
unset TZ LANG LC_ALL
if ! make test; then
  set +x
  for f in `find .. -name \*.diff -type f -print`; do
    echo "TEST FAILURE: $f --"
    cat "$f"
    echo "-- $f result ends."
  done
  set -x
  #exit 1
fi
unset NO_INTERACTION REPORT_EXIT_STATUS MALLOC_CHECK_
%endif

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# Install the extensions for the ZTS version
make -C build-zts install-modules INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the version for embedded script language in applications + php_embed.h
make -C build-embedded install-sapi install-headers INSTALL_ROOT=$RPM_BUILD_ROOT

# Install everything from the CGI SAPI build
make -C build-cgi install INSTALL_ROOT=$RPM_BUILD_ROOT 

# Install the default configuration file and icons
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/php.ini
install -m 755 -d $RPM_BUILD_ROOT%{contentdir}/icons
install -m 644    *.gif $RPM_BUILD_ROOT%{contentdir}/icons/

# For third-party packaging:
install -m 755 -d $RPM_BUILD_ROOT%{_libdir}/php/pear \
                  $RPM_BUILD_ROOT%{_datadir}/php

# install the DSO
install -m 755 -d $RPM_BUILD_ROOT%{_libdir}/httpd/modules
install -m 755 build-apache/libs/libphp5.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules

# install the ZTS DSO
install -m 755 build-zts/libs/libphp5.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/libphp5-zts.so

# Apache config fragment
install -m 755 -d $RPM_BUILD_ROOT/etc/httpd/conf.d
install -m 644 $RPM_SOURCE_DIR/php.conf $RPM_BUILD_ROOT/etc/httpd/conf.d

install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/session

# Fix the link
(cd $RPM_BUILD_ROOT%{_bindir}; ln -sfn phar.phar phar)

# Generate files lists and stub .ini files for each subpackage
for mod in pgsql mysql mysqli odbc ldap snmp xmlrpc imap \
    mbstring gd dom xsl soap bcmath dba xmlreader xmlwriter \
    %{?_with_oci8:oci8} %{?_with_oci8:pdo_oci} %{?_with_ibase:interbase} %{?_with_ibase:pdo_firebird} sqlite \
    pdo pdo_mysql pdo_pgsql pdo_odbc pdo_sqlite json zip \
%if 0%{?fedora} >= 9
    sqlite3 \
%endif
%if %{with_enchant}
    enchant \
%endif
    phar fileinfo intl \
    mcrypt tidy pdo_dblib mssql pspell curl wddx \
    posix sysvshm sysvsem sysvmsg recode; do
    cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${mod}.ini <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
    cat > $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/${mod}.ini <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
    cat > files.${mod} <<EOF
%attr(755,root,root) %{_libdir}/php/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php.d/${mod}.ini
%attr(755,root,root) %{_libdir}/php/modules-zts/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php-zts.d/${mod}.ini
EOF
done

# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xml{reader,writer} files.wddx > files.xml

# The mysql and mysqli modules are both packaged in php-mysql
cat files.mysqli >> files.mysql

# Split out the PDO modules
cat files.pdo_dblib >> files.mssql
cat files.pdo_mysql >> files.mysql
cat files.pdo_pgsql >> files.pgsql
cat files.pdo_odbc >> files.odbc
%if %{with_oci8}
cat files.pdo_oci >> files.oci8
%endif
%if %{with_ibase}
cat files.pdo_firebird >> files.interbase
%endif

# sysv* and posix in packaged in php-process
cat files.sysv* files.posix > files.process

# Package sqlite and pdo_sqlite with pdo; isolating the sqlite dependency
# isn't useful at this time since rpm itself requires sqlite.
cat files.sqlite >> files.pdo
cat files.pdo_sqlite >> files.pdo
%if 0%{?fedora} >= 9
cat files.sqlite3 >> files.pdo
%endif

# Package json, zip, curl, phar and fileinfo in -common.
cat files.json files.zip files.curl files.phar files.fileinfo > files.common

# Install the macros file:
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rpm
sed -e "s/@PHP_APIVER@/%{apiver}/;s/@PHP_ZENDVER@/%{zendver}/;s/@PHP_PDOVER@/%{pdover}/" \
    < $RPM_SOURCE_DIR/macros.php > macros.php
install -m 644 -c macros.php \
           $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.php

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/php/modules/*.a \
       $RPM_BUILD_ROOT%{_bindir}/{phptar} \
       $RPM_BUILD_ROOT%{_datadir}/pear \
       $RPM_BUILD_ROOT%{_libdir}/libphp5.la

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
rm files.* macros.php

%pre common
echo -e "\nWARNING : This %{name}-* RPM are not official Fedora/Redhat build and"
echo -e "overrides the official ones. Don't file bugs on Fedora Project nor Redhat.\n"
echo -e "Use dedicated forums http://forums.famillecollet.com/\n"

%if %{?fedora}%{!?fedora:99} <= 10
echo -e "WARNING : Fedora %{fedora} is now EOL :"
echo -e "You should consider upgrading to a supported release.\n"
%endif


%post embedded -p /sbin/ldconfig
%postun embedded -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/httpd/modules/libphp5.so
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/session
%config(noreplace) %{_sysconfdir}/httpd/conf.d/php.conf
%{contentdir}/icons/php.gif

%files common -f files.common
%defattr(-,root,root)
%doc CODING_STANDARDS CREDITS EXTENSIONS INSTALL LICENSE NEWS README*
%doc Zend/ZEND_* TSRM_LICENSE regex_COPYRIGHT
%doc php.ini-*
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_sysconfdir}/php-zts.d
%dir %{_libdir}/php
%dir %{_libdir}/php/modules
%dir %{_libdir}/php/modules-zts
%dir %{_localstatedir}/lib/php
%dir %{_libdir}/php/pear
%dir %{_datadir}/php

%files cli
%defattr(-,root,root)
%{_bindir}/php
%{_bindir}/php-cgi
%{_bindir}/phar.phar
%{_bindir}/phar
%{_mandir}/man1/php.1*
%doc sapi/cgi/README* sapi/cli/README

%files zts
%defattr(-,root,root)
%{_libdir}/httpd/modules/libphp5-zts.so

%files devel
%defattr(-,root,root)
%{_bindir}/php-config
%{_bindir}/phpize
%{_includedir}/php
%{_libdir}/php/build
%{_mandir}/man1/php-config.1*
%{_mandir}/man1/phpize.1*
%config %{_sysconfdir}/rpm/macros.php

%files embedded
%defattr(-,root,root,-)
%{_libdir}/libphp5.so
%{_libdir}/libphp5-%{phpversion}.so

%files pgsql -f files.pgsql
%files mysql -f files.mysql
%files odbc -f files.odbc
%files imap -f files.imap
%files ldap -f files.ldap
%files snmp -f files.snmp
%files xml -f files.xml
%files xmlrpc -f files.xmlrpc
%files mbstring -f files.mbstring
%files gd -f files.gd
%defattr(-,root,root,-)
%doc gd_README
%files soap -f files.soap
%files bcmath -f files.bcmath
%files dba -f files.dba
%files pdo -f files.pdo
%files mcrypt -f files.mcrypt
%files tidy -f files.tidy
%files mssql -f files.mssql
%files pspell -f files.pspell
%files intl -f files.intl
%files process -f files.process
%files recode -f files.recode
%if %{with_enchant}
%files enchant -f files.enchant
%endif

%if %{with_oci8}
%files oci8 -f files.oci8
%endif

%if %{with_ibase}
%files interbase -f files.interbase
%endif

%changelog
* Sun May 09 2010 Remi Collet <rpms@famillecollet.com> 5.3.3-0.1.201005090630.###.remi
- new snapshot
- systzdata-v7.patch

* Fri Apr 16 2010 Remi Collet <rpms@famillecollet.com> 5.3.3-0.1.201004221630.###.remi
- try snapshot

* Thu Mar  5 2010 Remi Collet <rpms@famillecollet.com> 5.3.2-1.###.remi
- update to 5.3.2

* Wed Feb 24 2010 Remi Collet <rpms@famillecollet.com> 5.3.2-0.2.RC3.###.remi
- update to 5.3.2RC3

* Fri Feb 12 2010 Remi Collet <rpms@famillecollet.com> 5.3.2-0.1.RC2.###.remi
- update to 5.3.2RC2

* Sat Dec 26 2009 Remi Collet <rpms@famillecollet.com> 5.3.2-0.1.RC1.###.remi
- update to 5.3.2RC1
- remove mime_magic option (now provided by fileinfo, by emu)

* Fri Nov 20 2009 Remi Collet <rpms@famillecollet.com> 5.3.1-1.###.remi
- PHP 5.3.1 Released!

* Sat Nov 14 2009 Remi Collet <rpms@famillecollet.com> 5.3.1-0.6.RC4.###.remi
- fix mysql default socket

* Sat Nov 14 2009 Remi Collet <rpms@famillecollet.com> 5.3.1-0.5.RC4.###.remi
- Rebuild with most extension for ZTS

* Fri Nov 13 2009 Remi Collet <rpms@famillecollet.com> 5.3.1-0.4.RC4.###.remi
- update to 5.3.1RC4

* Wed Nov 04 2009 Remi Collet <rpms@famillecollet.com> 5.3.1-0.3.RC3.###.remi
- update to 5.3.1RC3

* Wed Oct 21 2009 Remi Collet <rpms@famillecollet.com> 5.3.1-0.2.RC2.###.remi
- update to 5.3.1RC2

* Sat Sep 05 2009 Remi Collet <rpms@famillecollet.com> 5.3.1-0.2.RC1.###.remi
- update to 5.3.1RC1

* Sat Aug 15 2009 Remi Collet <rpms@famillecollet.com> 5.3.1-0.1.200908150630.###.remi
- update to 5.3.1RC1
- swicth back to v6 of systzdata patch (to be synced with rawhide)

* Sat Jul 18 2009 Remi Collet <rpms@famillecollet.com> 5.3.0-2.###.remi.2
- update to v7 of systzdata patch (only enabled on maintained distro)

* Fri Jul 17 2009 Remi Collet <rpms@famillecollet.com> 5.3.0-2.###.remi.1
- update to v6 of systzdata patch

* Tue Jul 14 2009 Joe Orton <jorton@redhat.com> 5.3.0-2
- update to v5 of systzdata patch; parses zone.tab and extracts
  timezone->{country-code,long/lat,comment} mapping table

* Fri Jun 19 2009 Remi Collet <rpms@famillecollet.com> 5.3.0-1.###.remi
- PHP 5.3.0 Released!

* Fri Jun 19 2009 Remi Collet <rpms@famillecollet.com> 5.3.0-0.6.RC4.###.remi
- Version 5.3.0RC4
- fix session.save_path in php.ini
- obsolete php-pecl-json

* Fri Jun 12 2009 Remi Collet <rpms@famillecollet.com> 5.3.0-0.5.RC3.###.remi
- Version 5.3.0RC3

* Sat May 09 2009 Remi Collet <rpms@famillecollet.com> 5.3.0-0.5.RC2.###.remi
- add php-interbase subpackage

* Fri May 08 2009 Remi Collet <rpms@famillecollet.com> 5.3.0-0.4.RC2.###.remi
- Version 5.3.0RC2

* Thu Apr 30 2009 Remi Collet <rpms@famillecollet.com> 5.3.0-0.4.RC1.fc11.remi
- F11 build
- fix provides for obsoleted pecl extension

* Sun Apr 05 2009 Remi Collet <rpms@famillecollet.com> 5.3.0-0.4.RC1.el5.remi
- EL5 rebuild without new sqlite3 extension 

* Wed Mar 25 2009 Remi Collet <rpms@famillecollet.com> 5.3.0-0.4.RC1.fc10.remi
- add php-enchant sub-package (new extension)

* Tue Mar 24 2009 Remi Collet <rpms@famillecollet.com> 5.3.0-0.3.RC1.fc10.remi
- Version 5.3.0RC1
- new php.ini from upstream php.ini-production

* Sat Feb 28 2009 Remi Collet <rpms@famillecollet.com> 5.3.0-0.2.beta1.fc10.remi
- Sync with rawhide (add php-process + php-recode)

* Thu Jan 29 2009 Remi Collet <rpms@famillecollet.com> 5.3.0-0.1.beta1.fc10.remi
- Version 5.3.0beta1

* Sat Dec 27 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.1.alpha4-dev.200812271530.fc10.remi
- new snapshot (5.3.0alpha4-dev)

* Sat Dec 13 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.1.alpha4-dev.200812131330.fc10.remi
- new snapshot (5.3.0alpha4-dev)
- remove mhash sub-package

* Sat Oct 18 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.1.alpha3-dev.200810181430.fc9.remi
- new snapshot (5.3.0alpha3-dev)

* Sun Oct 12 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.1.alpha3-dev.200810120830.fc9.remi
- new snapshot (5.3.0alpha3-dev)

* Sat Oct  4 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.1.alpha3-dev.200810041630.fc9.remi
- new snapshot (5.3.0alpha3-dev)
- add Requires to Sqlite 3.5.9-2 to get the loadextension option

* Sat Sep 27 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.1.alpha3-dev.200809270830.fc9.remi
- new snapshot (5.3.0alpha3-dev)

* Sat Sep 13 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.1.alpha3-dev.200809131430.fc9.remi
- new snapshot (5.3.0alpha3-dev)
- switch to oracle instant client 11.1.0.6 on i386, x86_64

* Sun Sep 07 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.1.alpha3-dev.200809070630.fc9.remi
- new snapshot (5.3.0alpha3-dev)
- remove gd-devel from BR and add with-xpm-dir (bundled GD provided more functions)

* Sat Aug 30 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.1.alpha2-dev.200808300430.fc9.remi
- new snapshot (5.3.0alpha2-dev)
- (re)enable mime-magic
- use bundled GD (build fails with system one)

* Tue Aug 20 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.1.alpha2-dev.200808200630.fc9.remi
- new snapshot (5.3.0alpha2-dev)
- use system GD instead of bundled GD when >= 2.0.35 (Fedora >= 6)

* Sun Aug 17 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.1.alpha2-dev.200808170830.fc9.remi
- new snapshot (5.3.0alpha2-dev) 
- php-5.2.4-tests-dashn.patch applied upstream

* Sun Aug 10 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.1.alpha2-dev.200808101630.fc9.remi
- new snapshot (5.3.0alpha2-dev) 
- no more dbase extension

* Wed Aug 06 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.1.alpha2-dev.200808061630.fc9.remi
- new snapshot (5.3.0alpha2-dev) (not published)
- PHP Bug #45636 fixed

* Mon Aug 04 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.1.alpha2-dev.200808041430.fc9.remi
- new snapshot (5.3.0alpha2-dev) (not published)

* Sat Aug 02 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.1.alpha2-dev.200808020430.fc9.remi
- new snapshot (5.3.0alpha2-dev)
- add php-intl sub-package

* Thu Jul 31 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.dev.200807311430.fc9.remi
- new snapshot
- fix fileinfo in php-common (not in php-xml)

* Mon Jul 28 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.dev.200807281630.fc9.remi
- new snapshot
- awfull hack on fileinfo/libmagic/softmagic.c

* Sun Jul 27 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.dev.200807271430.fc9.remi
- new snapshot
- php-common now provide Fileinfo extension (obsoletes php-pecl-Fileinfo)
- php-pdo now provides SQLite3 extension

* Tue Jul 22 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.dev.200807221630.fc9.remi
- new snapshot
- PHP Bug #45557 fixed
- PHP Bug #45564 fixed

* Mon Jul 21 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.dev.200807211430.fc9.remi
- new snapshot
- PHP Bug #45572 fixed

* Sun Jul 20 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.dev.200807201630.fc9.remi
- new snapshot
- more visibility patch (mbfl)

* Sun Jul 20 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.dev.200807200630.fc9.remi
- new snapshot
- merge php-phar in php-commonn and php-cli (phar.phar command)
- get t2lib option back

* Sat Jul 19 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.dev.200807191230.fc9.remi
- new snapshot

* Fri Jul 18 2008 Remi Collet <rpms@famillecollet.com> 5.3.0-0.dev.200807181430.fc9.remi
- first 5.3.0 build

* Sat May 11 2008 Remi Collet <rpms@famillecollet.com> 5.2.6-2.###.remi
- sync with rawhide (add php-pspell)

* Thu May  8 2008 Joe Orton <jorton@redhat.com> 5.2.6-2
- update to 5.2.6

* Tue May  6 2008 Remi Collet <rpms@famillecollet.com> 5.2.6-1.###.remi
- update to 5.2.6

* Thu Apr 24 2008 Joe Orton <jorton@redhat.com> 5.2.5-7
- split pspell extension out into php-pspell (#443857)

* Sat Apr 12 2008 Remi Collet <rpms@famillecollet.com> 5.2.6-0.1.RC.fc8.remi
- update to 5.2.6RC5 for testing

* Wed Apr 09 2008 Remi Collet <rpms@famillecollet.com> 5.2.5-2.###.remi
- resync with rawhide
- use bundled pcre if system one too old
- enable t1lib in GD (Fedora >= 5 and EL >= 5)

* Fri Jan 11 2008 Joe Orton <jorton@redhat.com> 5.2.5-5
- ext/date: use system timezone database

* Sat Nov 10 2007 Remi Collet <rpms@famillecollet.com> 5.2.5-1.fc8.remi
- update to 5.2.5

* Fri Nov 09 2007 Remi Collet <rpms@famillecollet.com> 5.2.4-3.fc8.remi
- resync with rawhide, F-8 rebuild

* Mon Oct 15 2007 Joe Orton <jorton@redhat.com> 5.2.4-3
- correct pcre BR version (#333021)
- restore metaphone fix (#205714)
- add READMEs to php-cli

* Sat Sep  1 2007 Remi Collet <rpms@famillecollet.com> 5.2.4-1.fc7.remi.1
- F-7 rebuild to add missing oci8

* Fri Aug 31 2007 Remi Collet <rpms@famillecollet.com> 5.2.4-1.###.remi
- update to 5.2.4

* Wed Aug 15 2007 Remi Collet <rpms@famillecollet.com> 5.2.3-5.###.remi
- rebuild from lastest rawhide spec
- rebuild against MySQL 5.1.20

* Fri Aug 10 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 5.2.3-7
- add php-embedded sub-package

* Fri Aug 10 2007 Joe Orton <jorton@redhat.com> 5.2.3-6
- fix build with new glibc
- fix License

* Mon Jul 16 2007 Joe Orton <jorton@redhat.com> 5.2.3-5
- define php_extdir in macros.php

* Sun Jul 15 2007 Remi Collet <rpms@famillecollet.com> 5.2.3-4.###.remi
- rebuild from lastest rawhide spec

* Mon Jul  2 2007 Joe Orton <jorton@redhat.com> 5.2.3-4
- obsolete php-dbase

* Tue Jun 19 2007 Joe Orton <jorton@redhat.com> 5.2.3-3
- add mcrypt, mhash, tidy, mssql subpackages (Dmitry Butskoy)
- enable dbase extension and package in -common

* Fri Jun  8 2007 Remi Collet <rpms@famillecollet.com> 5.2.3-2.###.remi
- rebuild from lastest rawhide spec

* Fri Jun  8 2007 Joe Orton <jorton@redhat.com> 5.2.3-2
- update to 5.2.3 (thanks to Jeff Sheltren)

* Thu Jun 07 2007 Remi Collet <rpms@famillecollet.com> 5.2.3-1.fc#.remi.2
- see https://www.redhat.com/archives/fedora-php-devel-list/2007-June/msg00000.html

* Tue Jun 05 2007 Remi Collet <rpms@famillecollet.com> 5.2.3-1.fc#.remi.1
- rebuild against libtidy-0.99.0-12-20070228

* Sat Jun 02 2007 Remi Collet <rpms@famillecollet.com> 5.2.3-1.fc#.remi
- update to 5.2.3

* Tue May 22 2007 Remi Collet <rpms@famillecollet.com> 5.2.2-3.fc7.remi
- F7 rebuild with all extensions

* Tue May  8 2007 Joe Orton <jorton@redhat.com> 5.2.2-3
- rebuild against uw-imap-devel

* Fri May  4 2007 Remi Collet <rpms@famillecollet.com> 5.2.2-1.###.remi
- update to 5.2.2 (from rawhide)

* Fri May  4 2007 Joe Orton <jorton@redhat.com> 5.2.2-2
- update to 5.2.2
- synch changes from upstream recommended php.ini

* Sun Apr 01 2007 Remi Collet <rpms@famillecollet.com> 5.2.1-4.fc{3-6}.remi
- use system sqlite2 (not bundled copy)

* Sat Mar 31 2007 Remi Collet <rpms@famillecollet.com> 5.2.1-3.fc{3-6}.remi
- build --with-sqlite (in php-pdo)

* Thu Mar 29 2007 Joe Orton <jorton@redhat.com> 5.2.1-5
- enable SASL support in LDAP extension (#205772)

* Wed Mar 21 2007 Joe Orton <jorton@redhat.com> 5.2.1-4
- drop mime_magic extension (deprecated by php-pecl-Fileinfo)

* Sat Feb 17 2007 Remi Collet <rpms@famillecollet.com> 5.2.1-2.fc{3-6}.remi
- latest patches from rawhide
- fix regression in str_{i,}replace (from upstream)
- keep memory_limit to 128M (defaut php-5.2.1 value)

* Thu Feb 15 2007 Joe Orton <jorton@redhat.com> 5.2.1-2
- update to 5.2.1
- add Requires(pre) for httpd
- trim %%changelog to versions >= 5.0.0

* Fri Feb 09 2007 Remi Collet <rpms@famillecollet.com> 5.2.1-1.fc{3-6}.remi
- update to 5.2.1
- remove php-5.1.6-curl716.patch and php-5.2.0-filterm4.patch (included upstream)

* Thu Feb  8 2007 Joe Orton <jorton@redhat.com> 5.2.0-10
- bump default memory_limit to 32M (#220821)
- mark config files noreplace again (#174251)
- drop trailing dots from Summary fields
- use standard BuildRoot
- drop libtool15 patch (#226294)

* Sat Feb 03 2007 Remi Collet <rpms@famillecollet.com> 5.2.0-5.fc{3-6}.remi
- rebuild from rawhide
- del Requires libclntsh.so.10.1 (not provided by Oracle RPM)
- build with oracle-instantclient 10.2.0.3

* Tue Jan 30 2007 Joe Orton <jorton@redhat.com> 5.2.0-9
- add php(api), php(zend-abi) provides (#221302)
- package /usr/share/php and append to default include_path (#225434)

* Wed Dec 20 2006 Remi Collet <rpms@famillecollet.com> 5.2.0-4.fc{3-6}.remi
- rebuild from rawhide

* Tue Dec  5 2006 Joe Orton <jorton@redhat.com> 5.2.0-8
- fix filter.h installation path
- fix php-zend-abi version (Remi Collet, #212804)

* Fri Dec 01 2006 Remi Collet <rpms@famillecollet.com> 5.2.0-3.fc{3-6}.remi
- rebuild from rawhide

* Mon Nov 27 2006 Joe Orton <jorton@redhat.com> 5.2.0-5
- build json and zip shared, in -common (Remi Collet, #215966)
- obsolete php-json and php-pecl-zip
- build readline extension into /usr/bin/php* (#210585)
- change module subpackages to require php-common not php (#177821)

* Thu Nov 16 2006 Remi Collet <rpms@famillecollet.com> 5.2.0-2.fc6.remi
- rebuild with rawhide patches

* Wed Nov 15 2006 Joe Orton <jorton@redhat.com> 5.2.0-4
- provide php-zend-abi (#212804)
- add /etc/rpm/macros.php exporting interface versions
- synch with upstream recommended php.ini

* Wed Nov 15 2006 Joe Orton <jorton@redhat.com> 5.2.0-3
- update to 5.2.0 (#213837)
- php-xml provides php-domxml (#215656)
- fix php-pdo-abi provide (#214281)

* Sat Nov  4 2006 Remi Collet <rpms@famillecollet.com> 5.2.0-1.1.fc6.remi
- split php-json

* Thu Nov  2 2006 Remi Collet <rpms@famillecollet.com> 5.2.0-1.fc{3-6}.remi
- update to 5.2.0 final
- add disclaimer

* Sat Oct 14 2006 Remi Collet <rpms@famillecollet.com> 5.2.0-0.200610140830.fc5.remi
- latest snapshot 

* Sun Oct  8 2006 Remi Collet <rpms@famillecollet.com> 5.2.0-0.200610081430.fc5.remi
- latest snapshot 

* Sun Oct  1 2006 Remi Collet <rpms@famillecollet.com> 5.2.0-0.200610011230.fc5.remi
- latest snapshot for http://bugs.php.net/bug.php?id=37103

* Sun Sep 17 2006 Remi Collet <rpms@famillecollet.com> 5.2.0-0.200609171630.fc5.remi
- first try for php 5.2 from snaps.php.net
- add Requires pcre >= 6.6

* Thu Aug 31 2006 Remi Collet <rpms@famillecollet.com> 5.1.6-2.fc{3,4,5}.remi
- rebuild from FC3, FC4 & FC5 (from rawhide)

* Tue Aug 29 2006 Joe Orton <jorton@redhat.com> 5.1.6-2
- update to 5.1.6 (security fixes)
- bump default memory_limit to 16M (#196802)

* Sun Aug 20 2006 Remi Collet <rpms@famillecollet.com> 5.1.5-1.fc{3,4,5}.remi
- update to 5.1.5

* Sat Jul 24 2006 Remi Collet <rpms@famillecollet.com> 5.1.4-3.fc{3,4,5}.remi
- path to install libmbfl headers : http://bugs.php.net/bug.php?id=37103

* Sat Jun 24 2006 Remi Collet <rpms@famillecollet.com> 5.1.4-2.fc{3,4,5}.remi
- rebuild fromFC3, FC4 & FC5 (from rawhide)
- build with oracle-instantclient 10.2.0.2
- requires libclntsh.so.10.1 (not oracle-instantclient-basic) 

* Fri Jun  9 2006 Joe Orton <jorton@redhat.com> 5.1.4-8
- Provide php-posix (#194583)
- only provide php-pcntl from -cli subpackage
- add missing defattr's (thanks to Matthias Saou)

* Fri Jun  9 2006 Joe Orton <jorton@redhat.com> 5.1.4-7
- move Obsoletes for php-openssl to -common (#194501)
- Provide: php-cgi from -cli subpackage

* Fri Jun  2 2006 Joe Orton <jorton@redhat.com> 5.1.4-6
- split out php-cli, php-common subpackages (#177821)
- add php-pdo-abi version export (#193202)

* Wed May 24 2006 Radek Vokal <rvokal@redhat.com> 5.1.4-5.1
- rebuilt for new libnetsnmp

* Thu May 18 2006 Joe Orton <jorton@redhat.com> 5.1.4-5
- provide mod_php (#187891)
- provide php-cli (#192196)
- use correct LDAP fix (#181518)
- define _GNU_SOURCE in php_config.h and leave it defined
- drop (circular) dependency on php-pear

* Sat May 06 2006 Remi Collet <rpms@famillecollet.com> 5.1.4-1.fc{3,4,5}.remi
- update to 5.1.4

* Fri May 05 2006 Remi Collet <rpms@famillecollet.com> 5.1.3-1.fc{3,4,5}.remi
- rebuild with additional packages

* Wed May  3 2006 Joe Orton <jorton@redhat.com> 5.1.3-3
- update to 5.1.3

* Mon Apr 17 2006 Remi Collet <rpms@famillecollet.com> 5.1.2-5.2.fc5.remi
- path to install libmbfl headers : http://bugs.php.net/bug.php?id=37103

* Fri Apr  7 2006 Joe Orton <jorton@redhat.com> 5.1.2-5.1
- fix use of LDAP on 64-bit platforms (#181518)

* Sun Apr 02 2006 Remi Collet <rpms@famillecollet.com> 5.1.2-5.fc5.remi
- add dbase, readline & tidy from php-extras
- build for FC5 (for mssql & oci8 only)

* Tue Feb 28 2006 Joe Orton <jorton@redhat.com> 5.1.2-5
- provide php-api (#183227)
- add provides for all builtin modules (Tim Jackson, #173804)
- own %%{_libdir}/php/pear for PEAR packages (per #176733)
- add obsoletes to allow upgrade from FE4 PDO packages (#181863)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.1.2-4.3
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.1.2-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Joe Orton <jorton@redhat.com> 5.1.2-4
- rebuild for new libc-client soname

* Mon Jan 16 2006 Joe Orton <jorton@redhat.com> 5.1.2-3
- only build xmlreader and xmlwriter shared (#177810)

* Sat Jan 14 2006 Remi Collet <remi.collet@univ-reims.fr> 5.1.2-2.fc{3,4}.remi
- update to 5.1.2 (see #177810)

* Fri Jan 13 2006 Joe Orton <jorton@redhat.com> 5.1.2-2
- update to 5.1.2

* Sat Jan  7 2006 Remi Collet <remi.collet@univ-reims.fr> 5.1.1-2.fc{3,4}.remi
- rebuild with mhash and mcrypt 

* Thu Jan  5 2006 Joe Orton <jorton@redhat.com> 5.1.1-8
- rebuild again

* Mon Jan  2 2006 Joe Orton <jorton@redhat.com> 5.1.1-7
- rebuild for new net-snmp

* Mon Dec 12 2005 Joe Orton <jorton@redhat.com> 5.1.1-6
- enable short_open_tag in default php.ini again (#175381)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  8 2005 Joe Orton <jorton@redhat.com> 5.1.1-5
- require net-snmp for php-snmp (#174800)

* Sun Dec  4 2005 Joe Orton <jorton@redhat.com> 5.1.1-4
- add /usr/share/pear back to hard-coded include_path (#174885)

* Sat Dec  3 2005 Remi Collet <remi.collet@univ-reims.fr> 5.1.1-2.fc#.remi
- rebuild for FC3 et FC4 (with oci8 and mssql)

* Mon Nov 28 2005 Joe Orton <jorton@redhat.com> 5.1.1-2
- update to 5.1.1
- remove pear subpackage
- enable pdo extensions (php-pdo subpackage)
- remove non-standard conditional module builds
- enable xmlreader extension


