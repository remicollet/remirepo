%{!?phpname:		%{expand: %%global phpname     php}}

%global contentdir  /var/www
# API/ABI check
%global apiver      20100412
%global zendver     20100525
%global pdover      20080721
# Extension version
%global fileinfover 1.0.5-dev
%global pharver     2.0.1
%global zipver      1.9.1
%global jsonver     1.2.1
%global oci8ver     1.4.7

%global httpd_mmn %(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)

%ifarch ppc ppc64
%global oraclever 10.2.0.2
%else
%global oraclever 11.2
%endif

# Regression tests take a long time, you can skip 'em with this
%{!?runselftest: %{expand: %%global runselftest 1}}

# Use the arch-specific mysql_config binary to avoid mismatch with the
# arch detection heuristic used by bindir/mysql_config.
%global mysql_config %{_libdir}/mysql/mysql_config

%global phpversion 5.4.0RC5
#global snapdate   201201041830
%global rcver      RC5

# Optional components; pass "--with mssql" etc to rpmbuild.
%global with_oci8 	%{?_with_oci8:1}%{!?_with_oci8:0}
%global with_ibase 	%{?_with_ibase:1}%{!?_with_ibase:0}
%if 0%{?rhel}%{?fedora} > 4
%global with_enchant 1
%else
%global with_enchant 0
%endif
%if 0%{?rhel} >= 5 || 0%{?fedora} >= 12
%ifarch %{ix86} x86_64
%global with_fpm 1
%else
%global with_fpm 0
%endif
%else
%global with_fpm 0
%endif

%if 0%{?__isa:1}
%global isasuffix -%{__isa}
%else
%global isasuffix %nil
%endif

# Flip these to 1 and zip respectively to enable zip support again
%global with_zip 1
%global zipmod zip

Summary: PHP scripting language for creating dynamic web sites
Name: %{phpname}
Version: 5.4.0
%if 0%{?snapdate}
Release: 0.7.%{snapdate}%{?dist}
%else
Release: 0.8.%{rcver}%{?dist}
%endif
License: PHP
Group: Development/Languages
URL: http://www.php.net/

%if 0%{?snapdate}
Source0: http://www.php.net/distributions/php5.4-%{snapdate}.tar.bz2
%else
Source0: http://www.php.net/distributions/php-%{version}%{?rcver}.tar.bz2
%endif
Source1: php.conf
Source2: php.ini
%if %{phpname} == php
Source3: macros.php
%else
Source3: macros.phpname
%endif
Source4: php-fpm.conf
Source5: php-fpm-www.conf
Source6: php-fpm.init
Source7: php-fpm.logrotate
Source8: php-fpm.service

# Build fixes
#Patch1: php-5.3.7-gnusrc.patch
#Patch2: php-5.3.0-install.patch
#Patch3: php-5.2.4-norpath.patch
#Patch4: php-5.3.0-phpize64.patch
Patch5: php-5.2.0-includedir.patch
Patch6: php-5.2.4-embed.patch
Patch7: php-5.3.0-recode.patch
# fix harcoded mysql.sock path, see https://bugs.php.net/60748
Patch9: php-5.4.0-sock.patch

# Fixes for extension modules
#Patch20: php-4.3.11-shutdown.patch
#Patch21: php-5.3.3-macropen.patch

# Functional changes
#Patch40: php-5.0.4-dlopen.patch
#Patch41: php-5.3.0-easter.patch
Patch42: php-5.3.1-systzdata-v7.patch
# See http://bugs.php.net/53436
#Patch43: php-5.3.4-phpize.patch

# Fixes for tests
#Patch61: php-5.0.4-tests-wddx.patch
#Patch62: php-5.3.3-tests.patch

# RC Patch
Patch91: php-5.3.7-oci8conf.patch

# Missing functions when build with libedit
# See http://bugs.php.net/54450
#Patch92: php-5.3.7-readline.patch

# On EL4, include order breaks build against MySQL 5.5
#Patch93: php-5.3.6-mysqli.patch


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: bzip2-devel, curl-devel >= 7.9, db4-devel, gmp-devel
BuildRequires: httpd-devel >= 2.0.46-1, pam-devel
BuildRequires: libstdc++-devel, openssl-devel
%if 0%{?fedora} >= 9 || 0%{?rhel} >= 6
# For Sqlite3 extension
BuildRequires: sqlite-devel >= 3.5.9
%else
BuildRequires: sqlite-devel >= 3.0.0
%endif
BuildRequires: zlib-devel, smtpdaemon, libedit-devel
%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
BuildRequires: pcre-devel >= 7.8
%endif
BuildRequires: bzip2, perl, libtool >= 1.4.3, gcc-c++
%if 0%{?rhel}%{?fedora} > 4
BuildRequires: libtool-ltdl-devel
%endif
BuildRequires: bison

Obsoletes: %{phpname}-dbg, php3, phpfi, stronghold-php, %{phpname}-zts
Provides: %{phpname}-zts = %{version}-%{release}
Provides: %{phpname}-zts%{?_isa} = %{version}-%{release}
Requires: httpd-mmn = %{httpd_mmn}
Provides: mod_php = %{version}-%{release}
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}
# For backwards-compatibility, require php-cli for the time being:
Requires: %{phpname}-cli%{?_isa} = %{version}-%{release}
# To ensure correct /var/lib/php/session ownership:
Requires(pre): httpd


%{expand: %%define _origbindir %{_bindir}}
%{expand: %%define _originitdir %{_initrddir}}
%{expand: %%define _origincludedir %{_includedir}}
%{expand: %%define _origsysconfdir %{_sysconfdir}}
%if %{phpname} == php
%global peardir      %{_datadir}/pear
%else
%global _bindir      /usr/bin/%{phpname}
%global _includedir  /usr/include/%{phpname}
%global _sysconfdir  /etc/%{phpname}
%global peardir      %{_datadir}/%{phpname}/pear
%endif

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{_libdir}/%{phpname}/modules/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{_libdir}/%{phpname}-zts/modules/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{_libdir}/%{phpname}/modules/.*\\.so$
%global __provides_exclude_from %{__provides_exclude_from}|%{_libdir}/%{phpname}-zts/modules/.*\\.so$


%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts. 

The php package contains the module which adds support for the PHP
language to Apache HTTP Server.

%package cli
Group: Development/Languages
Summary: Command-line interface for PHP
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}
Provides: %{phpname}-cgi = %{version}-%{release}, %{phpname}-cgi%{?_isa} = %{version}-%{release}
Provides: %{phpname}-pcntl, %{phpname}-pcntl%{?_isa}
Provides: %{phpname}-readline, %{phpname}-readline%{?_isa}

%description cli
The %{phpname}-cli package contains the command-line interface 
executing PHP scripts, /usr/bin/php, and the CGI interface.


%if %{with_fpm}
%package fpm
Group: Development/Languages
Summary: PHP FastCGI Process Manager
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}
BuildRequires: libevent-devel >= 1.4.11
%if 0%{?fedora} >= 15
BuildRequires: systemd-units
Requires: systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
# This is actually needed for the %%triggerun script but Requires(triggerun)
# is not valid.  We can use %%post because this particular %%triggerun script
# should fire just after this package is installed.
Requires(post): systemd-sysv
%else
# This is for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts
%endif

%description fpm
PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI
implementation with some additional features useful for sites of
any size, especially busier sites.
%endif

%package common
Group: Development/Languages
Summary: Common files for PHP
# ABI/API check - Arch specific
Provides: %{phpname}-api = %{apiver}%{isasuffix}, %{phpname}-zend-abi = %{zendver}%{isasuffix}
Provides: %{phpname}(api) = %{apiver}%{isasuffix}, %{phpname}(zend-abi) = %{zendver}%{isasuffix}
# Provides for all builtin/shared modules:
Provides: %{phpname}-bz2, %{phpname}-bz2%{?_isa}
Provides: %{phpname}-calendar, %{phpname}-calendar%{?_isa}
Provides: %{phpname}-ctype, %{phpname}-ctype%{?_isa}
Provides: %{phpname}-curl, %{phpname}-curl%{?_isa}
Provides: %{phpname}-date, %{phpname}-date%{?_isa}
Provides: %{phpname}-exif, %{phpname}-exif%{?_isa}
Provides: %{phpname}-fileinfo, %{phpname}-fileinfo%{?_isa}
Provides: %{phpname}-pecl-Fileinfo = %{fileinfover}, %{phpname}-pecl-Fileinfo%{?_isa} = %{fileinfover}
Provides: %{phpname}-pecl(Fileinfo) = %{fileinfover}, %{phpname}-pecl(Fileinfo)%{?_isa} = %{fileinfover}
Provides: %{phpname}-ftp, %{phpname}-ftp%{?_isa}
Provides: %{phpname}-gettext, %{phpname}-gettext%{?_isa}
Provides: %{phpname}-gmp, %{phpname}-gmp%{?_isa}
Provides: %{phpname}-hash, %{phpname}-hash%{?_isa}
Provides: %{phpname}-mhash = %{version}, %{phpname}-mhash%{?_isa} = %{version}
Provides: %{phpname}-iconv, %{phpname}-iconv%{?_isa}
Provides: %{phpname}-json, %{phpname}-json%{?_isa}
Provides: %{phpname}-pecl-json = %{jsonver}, %{phpname}-pecl-json%{?_isa} = %{jsonver}
Provides: %{phpname}-pecl(json) = %{jsonver}, %{phpname}-pecl(json)%{?_isa} = %{jsonver}
Provides: %{phpname}-libxml, %{phpname}-libxml%{?_isa}
Provides: %{phpname}-openssl, %{phpname}-openssl%{?_isa}
Provides: %{phpname}-pecl-phar = %{pharver}, %{phpname}-pecl-phar%{?_isa} = %{pharver}
Provides: %{phpname}-pecl(phar) = %{pharver}, %{phpname}-pecl(phar)%{?_isa} = %{pharver}
Provides: %{phpname}-pcre, %{phpname}-pcre%{?_isa}
Provides: %{phpname}-reflection, %{phpname}-reflection%{?_isa}
Provides: %{phpname}-session, %{phpname}-session%{?_isa}
Provides: %{phpname}-shmop, %{phpname}-shmop%{?_isa}
Provides: %{phpname}-simplexml, %{phpname}-simplexml%{?_isa}
Provides: %{phpname}-sockets, %{phpname}-sockets%{?_isa}
Provides: %{phpname}-spl, %{phpname}-spl%{?_isa}
Provides: %{phpname}-tokenizer, %{phpname}-tokenizer%{?_isa}
%if %{with_zip}
Provides: %{phpname}-zip, %{phpname}-zip%{?_isa}
Provides: %{phpname}-pecl-zip = %{zipver}, %{phpname}-pecl-zip%{?_isa} = %{zipver}
Provides: %{phpname}-pecl(zip) = %{zipver}, %{phpname}-pecl(zip)%{?_isa} = %{zipver}
Obsoletes: %{phpname}-pecl-zip
%endif
Provides: %{phpname}-zlib, %{phpname}-zlib%{?_isa}
Obsoletes: %{phpname}-openssl, %{phpname}-pecl-json, %{phpname}-json, %{phpname}-pecl-phar, %{phpname}-pecl-Fileinfo
Obsoletes: %{phpname}-mhash < 5.3.0

%description common
The %{phpname}-common package contains files used by both the php
package and the %{phpname}-cli package.

%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions
Requires: %{phpname}%{?_isa} = %{version}-%{release}, autoconf, automake
Obsoletes: %{phpname}-pecl-pdo-devel
Provides: php-zts-devel = %{version}-%{release}
Provides: php-zts-devel%{?_isa} = %{version}-%{release}

%description devel
The %{phpname}-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%package imap
Summary: A module for PHP applications that use IMAP
Group: Development/Languages
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}
Obsoletes: mod_php3-imap, stronghold-php-imap
BuildRequires: krb5-devel, openssl-devel, libc-client-devel

%description imap
The %{phpname}-imap package contains a dynamic shared object (DSO) for the
Apache Web server. When compiled into Apache, the %{phpname}-imap module will
add IMAP (Internet Message Access Protocol) support to PHP. IMAP is a
protocol for retrieving and uploading e-mail messages on mail
servers. PHP is an HTML-embedded scripting language. If you need IMAP
support for PHP applications, you will need to install this package
and the php package.

%package ldap
Summary: A module for PHP applications that use LDAP
Group: Development/Languages
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}
Obsoletes: mod_php3-ldap, stronghold-php-ldap
BuildRequires: cyrus-sasl-devel, openldap-devel, openssl-devel

%description ldap
The %{phpname}-ldap package is a dynamic shared object (DSO) for the Apache
Web server that adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language. If you need LDAP support for PHP applications, you will
need to install this package in addition to the php package.

%package pdo
Summary: A database access abstraction module for PHP applications
Group: Development/Languages
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}
Obsoletes: %{phpname}-pecl-pdo-sqlite, %{phpname}-pecl-pdo
# ABI/API check - Arch specific
Provides: %{phpname}-pdo-abi = %{pdover}%{isasuffix}
Provides: %{phpname}-sqlite3, %{phpname}-sqlite3%{?_isa}
Provides: %{phpname}-pdo_sqlite, %{phpname}-pdo_sqlite%{?_isa}

%description pdo
The %{phpname}-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other 
databases.

%package mysql
Summary: A module for PHP applications that use MySQL databases
Group: Development/Languages
Requires: %{phpname}-pdo%{?_isa} = %{version}-%{release}
Provides: %{phpname}_database
Provides: %{phpname}-mysqli = %{version}-%{release}
Provides: %{phpname}-mysqli%{?_isa} = %{version}-%{release}
Provides: %{phpname}-pdo_mysql, %{phpname}-pdo_mysql%{?_isa}
Obsoletes: mod_php3-mysql, stronghold-php-mysql
BuildRequires: mysql-devel >= 4.1.0
Conflicts: %{phpname}-mysqlnd

%description mysql
The %{phpname}-mysql package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

%package mysqlnd
Summary: A module for PHP applications that use MySQL databases
Group: Development/Languages
Requires: %{phpname}-pdo%{?_isa} = %{version}-%{release}
Provides: %{phpname}_database
Provides: %{phpname}-mysql, %{phpname}-mysql%{?_isa}
Provides: %{phpname}-mysqli = %{version}-%{release}
Provides: %{phpname}-mysqli%{?_isa} = %{version}-%{release}
Provides: %{phpname}-pdo_mysql, %{phpname}-pdo_mysql%{?_isa}

%description mysqlnd
The %{phpname}-mysqlnd package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

This package use the MySQL Native Driver

%package pgsql
Summary: A PostgreSQL database module for PHP
Group: Development/Languages
Requires: %{phpname}-pdo%{?_isa} = %{version}-%{release}
Provides: %{phpname}_database
Provides: %{phpname}-pdo_pgsql, %{phpname}-pdo_pgsql%{?_isa}
Obsoletes: mod_php3-pgsql, stronghold-php-pgsql
BuildRequires: krb5-devel, openssl-devel, postgresql-devel

%description pgsql
The %{phpname}-pgsql package includes a dynamic shared object (DSO) that can
be compiled in to the Apache Web server to add PostgreSQL database
support to PHP. PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.

%package process
Summary: Modules for PHP script using system process interfaces
Group: Development/Languages
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}
Provides: %{phpname}-posix, %{phpname}-posix%{?_isa}
Provides: %{phpname}-sysvsem, %{phpname}-sysvsem%{?_isa}
Provides: %{phpname}-sysvshm, %{phpname}-sysvshm%{?_isa}
Provides: %{phpname}-sysvmsg, %{phpname}-sysvmsg%{?_isa}

%description process
The %{phpname}-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.

%package odbc
Group: Development/Languages
Requires: %{phpname}-pdo%{?_isa} = %{version}-%{release}
Summary: A module for PHP applications that use ODBC databases
Provides: %{phpname}_database
Provides: %{phpname}-pdo_odbc, %{phpname}-pdo_odbc%{?_isa}
Obsoletes: stronghold-php-odbc
BuildRequires: unixODBC-devel

%description odbc
The %{phpname}-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.

%package soap
Group: Development/Languages
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}
Summary: A module for PHP applications that use the SOAP protocol
BuildRequires: libxml2-devel

%description soap
The %{phpname}-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.

%if %{with_ibase}
%package interbase
Summary: 	A module for PHP applications that use Interbase/Firebird databases
Group: 		Development/Languages
BuildRequires:  firebird-devel
Requires: 	%{phpname}-pdo%{?_isa} = %{version}-%{release}
Provides: 	%{phpname}_database
Provides: 	%{phpname}-firebird, %{phpname}-firebird%{?_isa}
Provides: 	%{phpname}-pdo_firebird, %{phpname}-pdo_firebird%{?_isa}

%description interbase
The %{phpname}-interbase package contains a dynamic shared object that will add
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
BuildRequires: 	oracle-instantclient-devel >= %{oraclever}
Requires: 	%{phpname}-pdo%{?_isa} = %{version}-%{release}
Provides: 	%{phpname}_database 
Provides: 	%{phpname}-pdo_oci = %{oci8ver}, %{phpname}-pdo_oci%{?_isa} = %{oci8ver}
Provides:       %{phpname}-pecl-oci8 = %{oci8ver}, %{phpname}-pecl-oci8%{?_isa} = %{oci8ver}
Provides:       %{phpname}-pecl(oci8) = %{oci8ver}, %{phpname}-pecl(oci8)%{?_isa} = %{oci8ver}
# Should requires libclntsh.so.11.1, but it's not provided by Oracle RPM.
AutoReq: 	0

%description oci8
The %{phpname}-oci8 package contains a dynamic shared object that will add
support for accessing OCI8 databases to PHP.
%endif

%package snmp
Summary: A module for PHP applications that query SNMP-managed devices
Group: Development/Languages
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}, net-snmp
BuildRequires: net-snmp-devel

%description snmp
The %{phpname}-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the php package.

%package xml
Summary: A module for PHP applications which use XML
Group: Development/Languages
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}
Obsoletes: %{phpname}-domxml, %{phpname}-dom
Provides: %{phpname}-dom, %{phpname}-dom%{?_isa}
Provides: %{phpname}-xsl, %{phpname}-xsl%{?_isa}
Provides: %{phpname}-domxml, %{phpname}-domxml%{?_isa}
Provides: %{phpname}-wddx, %{phpname}-wddx%{?_isa}
BuildRequires: libxslt-devel >= 1.0.18-1, libxml2-devel >= 2.4.14-1

%description xml
The %{phpname}-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.

%package xmlrpc
Summary: A module for PHP applications which use the XML-RPC protocol
Group: Development/Languages
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}

%description xmlrpc
The %{phpname}-xmlrpc package contains a dynamic shared object that will add
support for the XML-RPC protocol to PHP.

%package mbstring
Summary: A module for PHP applications which need multi-byte string handling
Group: Development/Languages
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}

%description mbstring
The %{phpname}-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.

%package gd
Summary: A module for PHP applications for using the gd graphics library
Group: Development/Languages
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}
# Required to build the bundled GD library
BuildRequires: libjpeg-devel, libpng-devel, freetype-devel
%if 0%{?rhel}%{?fedora} > 4
BuildRequires: libXpm-devel, t1lib-devel
%else
BuildRequires: xorg-x11-devel
%endif

%description gd
The %{phpname}-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.

%package bcmath
Summary: A module for PHP applications for using the bcmath library
Group: Development/Languages
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}

%description bcmath
The %{phpname}-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.

%package dba
Summary: A database abstraction layer module for PHP applications
Group: Development/Languages
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}

%description dba
The %{phpname}-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.

%package mcrypt
Summary: Standard PHP module provides mcrypt library support
Group: Development/Languages
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}
BuildRequires: libmcrypt-devel

%description mcrypt
The %{phpname}-mcrypt package contains a dynamic shared object that will add
support for using the mcrypt library to PHP.

%package tidy
Summary: Standard PHP module provides tidy library support
Group: Development/Languages
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}
BuildRequires: libtidy-devel

%description tidy
The %{phpname}-tidy package contains a dynamic shared object that will add
support for using the tidy library to PHP.

%package mssql
Summary: MSSQL database module for PHP
Group: Development/Languages
Requires: %{phpname}-pdo%{?_isa} = %{version}-%{release}
BuildRequires: freetds-devel
Provides: %{phpname}-pdo_dblib, %{phpname}-pdo_dblib%{?_isa}

%description mssql
The %{phpname}-mssql package contains a dynamic shared object that will
add MSSQL database support to PHP.  It uses the TDS (Tabular
DataStream) protocol through the freetds library, hence any
database server which supports TDS can be accessed.

%package embedded
Summary: PHP library for embedding in applications
Group: System Environment/Libraries
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}
# doing a real -devel package for just the .so symlink is a bit overkill
Provides: %{phpname}-embedded-devel = %{version}-%{release}
Provides: %{phpname}-embedded-devel%{?_isa} = %{version}-%{release}

%description embedded
The %{phpname}-embedded package contains a library which can be embedded
into applications to provide PHP scripting language support.

%package pspell
Summary: A module for PHP applications for using pspell interfaces
Group: System Environment/Libraries
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}
BuildRequires: aspell-devel >= 0.50.0

%description pspell
The %{phpname}-pspell package contains a dynamic shared object that will add
support for using the pspell library to PHP.

%package recode
Summary: A module for PHP applications for using the recode library
Group: System Environment/Libraries
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}
BuildRequires: recode-devel

%description recode
The %{phpname}-recode package contains a dynamic shared object that will add
support for using the recode library to PHP.

%package intl
Summary: Internationalization extension for PHP applications
Group: System Environment/Libraries
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}
BuildRequires: libicu-devel >= 3.6

%description intl
The %{phpname}-intl package contains a dynamic shared object that will add
support for using the ICU library to PHP.

%if %{with_enchant}
%package enchant
Summary: Human Language and Character Encoding Support
Group: System Environment/Libraries
Requires: %{phpname}-common%{?_isa} = %{version}-%{release}
BuildRequires: enchant-devel >= 1.2.4

%description enchant
The %{phpname}-intl package contains a dynamic shared object that will add
support for using the enchant library to PHP.
%endif


%prep
echo CIBLE = %{name}-%{version}-%{release}
%if 0%{?snapdate}
%setup -q -n php5.4-%{snapdate}
%else
%setup -q -n php-%{version}%{?rcver}
%endif

#%patch1 -p1 -b .gnusrc
#%patch2 -p1 -b .install
#%patch3 -p1 -b .norpath
#%patch4 -p1 -b .phpize64
%patch5 -p1 -b .includedir
%patch6 -p1 -b .embed
%patch7 -p1 -b .recode
%patch9 -p1 -b .sock

#%patch20 -p1 -b .shutdown
#%patch21 -p1 -b .macropen

#%patch40 -p1 -b .dlopen
#%patch41 -p1 -b .easter
%if %{?fedora}%{?rhel:99} >= 15
%patch42 -p1 -b .systzdata
%endif
#%patch43 -p0 -b .headers

#%patch61 -p1 -b .tests-wddx
#%patch62 -p0 -b .tests

%patch91 -p1 -b .remi-oci8
#%patch92 -p1 -b .libedit
#%patch93 -p1 -b .mysqli


# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp ext/ereg/regex/COPYRIGHT regex_COPYRIGHT
cp ext/gd/libgd/README gd_README

# Multiple builds for multiple SAPIs
mkdir build-cgi build-apache build-embedded build-zts build-ztscli \
%if %{with_fpm}
    build-fpm
%endif

# Remove bogus test; position of read position after fopen(, "a+")
# is not defined by C standard, so don't presume anything.
rm -f ext/standard/tests/file/bug21131.phpt
# php_egg_logo_guid() removed by patch41
rm -f tests/basic/php_egg_logo_guid.phpt

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
ver=$(sed -n '/#define PHP_OCI8_VERSION /{s/.* "//;s/".*$//;p}' ext/oci8/php_oci8.h)
if test "$ver" != "%{oci8ver}"; then
   : Error: Upstream OCI8 version is now ${ver}, expecting %{oci8ver}.
   : Update the oci8ver macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_JSON_VERSION /{s/.* "//;s/".*$//;p}' ext/json/php_json.h)
if test "$ver" != "%{jsonver}"; then
   : Error: Upstream JSON version is now ${ver}, expecting %{jsonver}.
   : Update the jsonver macro and rebuild.
   exit 1
fi

# Fix some bogus permissions
find . -name \*.[ch] -exec chmod 644 {} \;
chmod 644 README.*

# php-fpm configuration files for tmpfiles.d
echo "d %{_localstatedir}/run/php-fpm 755 root root" >php-fpm.tmpfiles

: Build for oci8=%{with_oci8} ibase=%{with_ibase}


%build
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
# aclocal workaround - to be improved
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >>aclocal.m4
%endif

# Force use of system libtool:
libtoolize --force --copy
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4
%else
cat `aclocal --print-ac-dir`/libtool.m4 > build/libtool.m4
%endif

# Regenerate configure scripts (patches change config.m4's)
touch configure.in
./buildconf --force
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
%if 0%{?rhel} < 5
	CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%endif
export CFLAGS

# Install extension modules in %{_libdir}/php/modules.
EXTENSION_DIR=%{_libdir}/%{phpname}/modules; export EXTENSION_DIR

# Set PEAR_INSTALLDIR to ensure that the hard-coded include_path
# includes the PEAR directory even though pear is packaged
# separately.
PEAR_INSTALLDIR=%{peardir}; export PEAR_INSTALLDIR

# Shell function to configure and build a PHP tree.
build() {
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
%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
        --with-pcre-regex=%{_prefix} \
%endif
	--with-zlib \
	--with-layout=GNU \
	--enable-exif \
	--enable-ftp \
	--enable-magic-quotes \
	--enable-sockets \
	--with-kerberos \
	--enable-ucd-snmp-hack \
	--enable-shmop \
	--enable-calendar \
        --with-libxml-dir=%{_prefix} \
	--enable-xml \
%if %{?fedora}%{?rhel:99} >= 10
        --with-system-tzdata \
%endif
	--with-mhash \
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

build --enable-force-cgi-redirect \
      --libdir=%{_libdir}/%{phpname} \
      --enable-pcntl \
      --with-imap=shared --with-imap-ssl \
      --enable-mbstring=shared \
      --enable-mbregex \
      --with-gd=shared \
      --enable-bcmath=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysql=shared,mysqlnd \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=/var/lib/mysql/mysql.sock \
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
%if 0%{?fedora} >= 9 || 0%{?rhel} >= 6
      --with-sqlite3=shared,%{_prefix} \
%else
      --without-sqlite3 \
%endif
      --enable-json=shared \
%if %{with_zip}
      --enable-zip=shared \
%endif
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

without_shared="--without-gd \
      --disable-dom --disable-dba --without-unixODBC \
      --disable-xmlreader --disable-xmlwriter \
      --without-sqlite3 --disable-phar --disable-fileinfo \
      --disable-json --without-pspell --disable-wddx \
      --without-curl --disable-posix \
      --disable-sysvmsg --disable-sysvshm --disable-sysvsem"

# Build Apache module, and the CLI SAPI, /usr/bin/php
pushd build-apache
build --with-apxs2=%{_sbindir}/apxs \
      --libdir=%{_libdir}/%{phpname} \
      --enable-pdo=shared \
      --with-mysql=shared,%{_prefix} \
      --with-mysqli=shared,%{mysql_config} \
      --with-mysql-sock=/var/lib/mysql/mysql.sock \
      --with-pdo-mysql=shared,%{mysql_config} \
      --with-pdo-sqlite=shared,%{_prefix} \
      ${without_shared}
popd

%if %{with_fpm}
# Build php-fpm
pushd build-fpm
build --enable-fpm \
      --libdir=%{_libdir}/%{phpname} \
      --without-mysql --disable-pdo \
      ${without_shared}
popd
%endif

# Build for inclusion as embedded script language into applications,
# /usr/lib[64]/libphp5.so
pushd build-embedded
build --enable-embed \
      --without-mysql --disable-pdo \
      ${without_shared}
popd

# Build a special thread-safe (mainly for modules)
pushd build-ztscli

EXTENSION_DIR=%{_libdir}/%{phpname}-zts/modules
build --enable-force-cgi-redirect \
      --bindir=%{_origbindir}/%{phpname}-zts \
      --includedir=%{_origincludedir}/%{phpname}-zts \
      --libdir=%{_libdir}/%{phpname}-zts \
      --enable-maintainer-zts \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d \
      --enable-pcntl \
      --with-imap=shared --with-imap-ssl \
      --enable-mbstring=shared \
      --enable-mbregex \
      --with-gd=shared \
      --enable-bcmath=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysql=shared,mysqlnd \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=/var/lib/mysql/mysql.sock \
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
%if 0%{?fedora} >= 9 || 0%{?rhel} >= 6
      --with-sqlite3=shared,%{_prefix} \
%else
      --without-sqlite3 \
%endif
      --enable-json=shared \
%if %{with_zip}
      --enable-zip=shared \
%endif
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

# Build a special thread-safe Apache SAPI
pushd build-zts
build --with-apxs2=%{_sbindir}/apxs \
      --bindir=%{_origbindir}/%{phpname}-zts \
      --includedir=%{_origincludedir}/%{phpname}-zts \
      --libdir=%{_libdir}/%{phpname}-zts \
      --enable-maintainer-zts \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d \
      --enable-pdo=shared \
      --with-mysql=shared,%{_prefix} \
      --with-mysqli=shared,%{mysql_config} \
      --with-mysql-sock=/var/lib/mysql/mysql.sock \
      --with-pdo-mysql=shared,%{mysql_config} \
      --with-pdo-sqlite=shared,%{_prefix} \
      ${without_shared}
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
make -C build-ztscli install \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# rename extensions build with mysqlnd
mv $RPM_BUILD_ROOT%{_libdir}/%{phpname}-zts/modules/mysql.so \
   $RPM_BUILD_ROOT%{_libdir}/%{phpname}-zts/modules/mysqlnd_mysql.so
mv $RPM_BUILD_ROOT%{_libdir}/%{phpname}-zts/modules/mysqli.so \
   $RPM_BUILD_ROOT%{_libdir}/%{phpname}-zts/modules/mysqlnd_mysqli.so
mv $RPM_BUILD_ROOT%{_libdir}/%{phpname}-zts/modules/pdo_mysql.so \
   $RPM_BUILD_ROOT%{_libdir}/%{phpname}-zts/modules/pdo_mysqlnd.so

# Install the extensions for the ZTS version modules for libmysql
make -C build-zts install-modules \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the version for embedded script language in applications + php_embed.h
make -C build-embedded install-sapi install-headers \
     INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with_fpm}
# Install the php-fpm binary
make -C build-fpm install-fpm \
     INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# Install everything from the CGI SAPI build
make -C build-cgi install \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# rename extensions build with mysqlnd
mv $RPM_BUILD_ROOT%{_libdir}/%{phpname}/modules/mysql.so \
   $RPM_BUILD_ROOT%{_libdir}/%{phpname}/modules/mysqlnd_mysql.so
mv $RPM_BUILD_ROOT%{_libdir}/%{phpname}/modules/mysqli.so \
   $RPM_BUILD_ROOT%{_libdir}/%{phpname}/modules/mysqlnd_mysqli.so
mv $RPM_BUILD_ROOT%{_libdir}/%{phpname}/modules/pdo_mysql.so \
   $RPM_BUILD_ROOT%{_libdir}/%{phpname}/modules/pdo_mysqlnd.so

# Install the mysql extension build with libmysql
make -C build-apache install-modules \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the default configuration file and icons
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/
#install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/php.ini
%{__sed} -e '/session.save_path/s/php/%{phpname}/' %{SOURCE2} >$RPM_BUILD_ROOT%{_sysconfdir}/php.ini
install -m 755 -d $RPM_BUILD_ROOT%{contentdir}/icons
install -m 644 php.gif $RPM_BUILD_ROOT%{contentdir}/icons/%{phpname}.gif

# For third-party packaging:
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/%{phpname}

# install the DSO
install -m 755 -d $RPM_BUILD_ROOT%{_libdir}/httpd/modules
%if %{phpname} == php
install -m 755 build-apache/libs/libphp5.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules
%else
install -m 755 build-apache/libs/libphp5.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/lib%{phpname}.so
%endif

# install the ZTS DSO
%if %{phpname} == php
install -m 755 build-zts/libs/libphp5.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/libphp5-zts.so
%else
install -m 755 build-zts/libs/libphp5.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/lib%{phpname}-zts.so
%endif

# Apache config fragment
install -m 755 -d $RPM_BUILD_ROOT/%{_origsysconfdir}/httpd/conf.d
%if %{phpname} == php
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_origsysconfdir}/httpd/conf.d
%else
%{__sed} -e s'/libphp5/lib%{phpname}/' %{SOURCE1} \
  >$RPM_BUILD_ROOT/%{_origsysconfdir}/httpd/conf.d/%{phpname}.conf
%endif

install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/%{phpname}/session

%if %{with_fpm}
# PHP-FPM stuff
# Log
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/log/php-fpm
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/run/php-fpm
# Config
install -m 755 -d $RPM_BUILD_ROOT%{_origsysconfdir}/php-fpm.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_origsysconfdir}/php-fpm.d/www.conf
mv $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf.default .
%if 0%{?fedora} >= 15
# tmpfiles.d
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d
install -m 644 php-fpm.tmpfiles $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d/php-fpm.conf
# install systemd unit files and scripts for handling server startup
mkdir -p ${RPM_BUILD_ROOT}%{_unitdir}
install -m 644 %{SOURCE8} ${RPM_BUILD_ROOT}%{_unitdir}/
%else
# Service
install -m 755 -d $RPM_BUILD_ROOT%{_originitdir}
install -m 755 %{SOURCE6} $RPM_BUILD_ROOT%{_originitdir}/php-fpm
%endif
# LogRotate
install -m 755 -d $RPM_BUILD_ROOT%{_origsysconfdir}/logrotate.d
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_origsysconfdir}/logrotate.d/php-fpm
%endif

# Fix the link
(cd $RPM_BUILD_ROOT%{_bindir}; ln -sfn phar.phar phar)

# Generate files lists and stub .ini files for each subpackage
for mod in pgsql mysql mysqli odbc ldap snmp xmlrpc imap \
    mysqlnd mysqlnd_mysql mysqlnd_mysqli pdo_mysqlnd \
    mbstring gd dom xsl soap bcmath dba xmlreader xmlwriter \
    %{?_with_oci8:oci8} %{?_with_oci8:pdo_oci} %{?_with_ibase:interbase} %{?_with_ibase:pdo_firebird} \
    pdo pdo_mysql pdo_pgsql pdo_odbc pdo_sqlite json zip \
%if 0%{?fedora} >= 9  || 0%{?rhel} >= 6
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
    cat > files.${mod} <<EOF
%attr(755,root,root) %{_libdir}/%{phpname}/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php.d/${mod}.ini
EOF

    cat > $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/${mod}.ini <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
    cat >> files.${mod} <<EOF
%attr(755,root,root) %{_libdir}/%{phpname}-zts/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php-zts.d/${mod}.ini
EOF

done

# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xml{reader,writer} files.wddx > files.xml

# The mysql and mysqli modules are both packaged in php-mysql
cat files.mysqli >> files.mysql
# mysqlnd
cat files.mysqlnd_mysql \
    files.mysqlnd_mysqli \
    files.pdo_mysqlnd \
    >> files.mysqlnd

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
#cat files.sqlite >> files.pdo
cat files.pdo_sqlite >> files.pdo
%if 0%{?fedora} >= 9 || 0%{?rhel} >= 6
cat files.sqlite3 >> files.pdo
%endif

# Package json, zip, curl, phar and fileinfo in -common.
cat files.json files.curl files.phar files.fileinfo > files.common
%if %{with_zip}
cat files.zip >> files.common
%endif

# Install the macros file:
install -d $RPM_BUILD_ROOT%{_origsysconfdir}/rpm
sed -e "s/@PHP_APIVER@/%{apiver}%{isasuffix}/" \
    -e "s/@PHP_ZENDVER@/%{zendver}%{isasuffix}/" \
    -e "s/@PHP_PDOVER@/%{pdover}%{isasuffix}/" \
    -e "s/@PHPNAME@/%{phpname}/" \
    < %{SOURCE3} > macros.php
install -m 644 -c macros.php \
           $RPM_BUILD_ROOT%{_origsysconfdir}/rpm/macros.%{phpname}

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{phpname}/modules/*.a \
       $RPM_BUILD_ROOT%{_libdir}/%{phpname}-zts/modules/*.a \
       $RPM_BUILD_ROOT%{_bindir}/{phptar} \
       $RPM_BUILD_ROOT%{_bindir}/%{phpname}-zts/phar* \
       $RPM_BUILD_ROOT%{_bindir}/%{phpname}-zts/php-cgi \
       $RPM_BUILD_ROOT%{peardir} \
       $RPM_BUILD_ROOT%{_libdir}/libphp5.la

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
rm files.* macros.php

%pre common
echo -e "\nWARNING : These %{name}-* RPM are not official Fedora/Redhat build and"
echo -e "overrides the official ones. Don't file bugs on Fedora Project nor Redhat.\n"
echo -e "Use dedicated forums http://forums.famillecollet.com/\n"

%if %{?fedora}%{!?fedora:99} <= 12
echo -e "WARNING : Fedora %{fedora} is now EOL :"
echo -e "You should consider upgrading to a supported release.\n"
%endif


%if %{with_fpm}
%post fpm
if [ $1 = 1 ]; then
    # Initial installation
%if 0%{?fedora} >= 15
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add php-fpm
%endif
fi

%preun fpm
if [ $1 = 0 ]; then
    # Package removal, not upgrade
%if 0%{?fedora} >= 15
    /bin/systemctl --no-reload disable php-fpm.service >/dev/null 2>&1 || :
    /bin/systemctl stop php-fpm.service >/dev/null 2>&1 || :
%else
    /sbin/service php-fpm stop >/dev/null 2>&1
    /sbin/chkconfig --del php-fpm
%endif
fi

%postun fpm
%if 0%{?fedora} >= 15
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ]; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart php-fpm.service >/dev/null 2>&1 || :
fi
%else
if [ $1 -ge 1 ]; then
    /sbin/service php-fpm condrestart >/dev/null 2>&1 || :
fi
%endif

# Handle upgrading from SysV initscript to native systemd unit.
# We can tell if a SysV version of php-fpm was previously installed by
# checking to see if the initscript is present.
%triggerun fpm -- php-fpm
%if 0%{?fedora} >= 15
if [ -f /etc/rc.d/init.d/php-fpm ]; then
    # Save the current service runlevel info
    # User must manually run systemd-sysv-convert --apply php-fpm
    # to migrate them to systemd targets
    /usr/bin/systemd-sysv-convert --save php-fpm >/dev/null 2>&1 || :

    # Run these because the SysV package being removed won't do them
    /sbin/chkconfig --del php-fpm >/dev/null 2>&1 || :
    /bin/systemctl try-restart php-fpm.service >/dev/null 2>&1 || :
fi
%endif
%endif

%post embedded -p /sbin/ldconfig
%postun embedded -p /sbin/ldconfig

%files
%defattr(-,root,root)
%if %{phpname} == php
%{_libdir}/httpd/modules/libphp5.so
%{_libdir}/httpd/modules/libphp5-zts.so
%else
%{_libdir}/httpd/modules/lib%{phpname}.so
%{_libdir}/httpd/modules/lib%{phpname}-zts.so
%endif
%attr(0770,root,apache) %dir %{_localstatedir}/lib/%{phpname}/session
%config(noreplace) %{_origsysconfdir}/httpd/conf.d/%{phpname}.conf
%{contentdir}/icons/%{phpname}.gif

%files common -f files.common
%defattr(-,root,root)
%doc CODING_STANDARDS CREDITS EXTENSIONS INSTALL LICENSE NEWS README*
%doc Zend/ZEND_* TSRM_LICENSE regex_COPYRIGHT
%doc php.ini-*
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_sysconfdir}/php-zts.d
%dir %{_libdir}/%{phpname}
%dir %{_libdir}/%{phpname}/modules
%dir %{_libdir}/%{phpname}-zts
%dir %{_libdir}/%{phpname}-zts/modules
%dir %{_localstatedir}/lib/php
%dir %{_datadir}/%{phpname}

%files cli
%defattr(-,root,root)
%{_bindir}/php
%{_bindir}/php-cgi
%{_bindir}/phar.phar
%{_bindir}/phar
# provides phpize here (not in -devel) for pecl command
%{_bindir}/phpize
%if %{phpname} == php
%{_mandir}/man1/php.1*
%{_mandir}/man1/phpize.1*
%else
%exclude %{_mandir}/man1/php.1*
%exclude %{_mandir}/man1/phpize.1*
%endif
%doc sapi/cgi/README* sapi/cli/README

%if %{with_fpm}
%files fpm
%defattr(-,root,root)
%doc php-fpm.conf.default
%config(noreplace) %{_sysconfdir}/php-fpm.conf
%config(noreplace) %{_origsysconfdir}/php-fpm.d/www.conf
%config(noreplace) %{_origsysconfdir}/logrotate.d/php-fpm
%if 0%{?fedora} >= 15
%config(noreplace) %{_sysconfdir}/tmpfiles.d/php-fpm.conf
%{_unitdir}/php-fpm.service
%else
%{_originitdir}/php-fpm
%endif
%{_sbindir}/php-fpm
%dir %{_origsysconfdir}/php-fpm.d
# log owned by apache for log
%attr(770,apache,apache) %dir %{_localstatedir}/log/php-fpm
%dir %{_localstatedir}/run/php-fpm
%{_mandir}/man8/php-fpm.8*
%{_datadir}/fpm/status.html
%endif

%files devel
%defattr(-,root,root)
%{_bindir}/php-config
%{_origbindir}/%{phpname}-zts/php-config
%{_origbindir}/%{phpname}-zts/phpize
# usefull only to test other module during build
%{_origbindir}/%{phpname}-zts/php
%dir %{_origincludedir}/%{phpname}
%{_includedir}/php
%{_origincludedir}/%{phpname}-zts
%{_libdir}/%{phpname}/build
%{_libdir}/%{phpname}-zts/build
%if %{phpname} == php
%{_mandir}/man1/php-config.1*
%else
%exclude %{_mandir}/man1/php-config.1*
%endif
%config %{_origsysconfdir}/rpm/macros.%{phpname}

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
%files mysqlnd -f files.mysqlnd

%if %{with_oci8}
%files oci8 -f files.oci8
%endif

%if %{with_ibase}
%files interbase -f files.interbase
%endif

%changelog
* Fri Jan 13 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.8.RC5
- update to 5.4.0RC5
- patch for https://bugs.php.net/60748 (mysql.sock hardcoded)
- move session.path from php.ini to httpd/conf.d/php.conf
- provides both ZTS mysql extensions (libmysql/mysqlnd)
- build php cli ZTS binary, in -devel, mainly for test

* Wed Jan 04 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.7.201201041830
- new snapshot (5.4.0RC5-dev) with fix for https://bugs.php.net/60627

* Fri Dec 30 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.6.201112300630
- new snapshot (5.4.0RC5-dev)

* Mon Dec 26 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.6.201112261030
- new snapshot (5.4.0RC5-dev)

* Sat Dec 17 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.5.201112170630
- new snapshot (5.4.0RC4-dev)

* Mon Dec 12 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.4.201112121330
- new snapshot (5.4.0RC4-dev)
- switch to systemd

* Fri Dec 09 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.3.201112091730
- new snapshot (5.4.0RC4-dev)
- removed patch merged upstream for https://bugs.php.net/60392
- clean ini (from upstream production default)

* Sun Nov 13 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.3.201111260730
- new snapshot (5.4.0RC3-dev)
- patch for https://bugs.php.net/60392 (old libicu on EL-5)

* Sun Nov 13 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.3.201111130730
- new snapshot (5.4.0RC2-dev)
- sync with latest changes in 5.3 spec

* Thu Sep 08 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.2.201109081430
- new snapshot
- build mysql/mysqli against both libmysql and mysqlnd (new mysqlnd sub-package)

* Sat Sep 03 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.1.201109031230
- first work on php 5.4
- remove -sqlite subpackage
- move php/modules-zts to php-zts/modules

* Wed Aug 24 2011 Remi Collet <Fedora@famillecollet.com> 5.3.8-2
- provides zts devel stuff

* Tue Aug 23 2011 Remi Collet <Fedora@famillecollet.com> 5.3.8-1.1
- EL-5 build with latest libcurl 7.21.7

* Tue Aug 23 2011 Remi Collet <Fedora@famillecollet.com> 5.3.8-1
- update to 5.3.8
  http://www.php.net/ChangeLog-5.php#5.3.8

* Sun Aug 21 2011 Remi Collet <Fedora@famillecollet.com> 5.3.7-2.1
- EL-5 build with latest libcurl 7.21.7

* Sat Aug 20 2011 Remi Collet <Fedora@famillecollet.com> 5.3.7-2
- add patch for https://bugs.php.net/55439

* Fri Aug 19 2011 Remi Collet <Fedora@famillecollet.com> 5.3.7-1.1
- EL-5 build with latest libcurl 7.21.7

* Thu Aug 18 2011 Remi Collet <Fedora@famillecollet.com> 5.3.7-1
- update to 5.3.7
  http://www.php.net/ChangeLog-5.php#5.3.7
- merge php-zts into php (#698084)

* Mon May 16 2011 Remi Collet <rpms@famillecollet.com> 5.3.6-4
- backport patch for #50755 (multiple rowset in pdo_dblib)

* Fri Apr 15 2011 Remi Collet <Fedora@famillecollet.com> 5.3.6-3
- add patch to fix build against MySQL 5.5 on EL-4

* Mon Apr  4 2011 Remi Collet <Fedora@famillecollet.com> 5.3.6-3
- enable mhash extension (emulated by hash extension)

* Wed Mar 29 2011 Remi Collet <Fedora@famillecollet.com> 5.3.6-2
- fix relocated (php53) build

* Thu Mar 17 2011 Remi Collet <Fedora@famillecollet.com> 5.3.6-1
- update to 5.3.6
  http://www.php.net/ChangeLog-5.php#5.3.6

* Tue Mar 15 2011 Joe Orton <jorton@redhat.com> - 5.3.5-6
- disable zip extension per "No Bundled Libraries" policy (#551513)

* Mon Mar 07 2011 Caolán McNamara <caolanm@redhat.com> 5.3.5-5
- rebuild for icu 4.6

* Mon Feb 28 2011 Remi Collet <Fedora@famillecollet.com> 5.3.5-4
- fix systemd-units requires

* Thu Feb 24 2011 Remi Collet <Fedora@famillecollet.com> 5.3.5-3
- add tmpfiles.d configuration for php-fpm
- add Arch specific requires/provides

* Fri Feb 11 2011 Remi Collet <rpms@famillecollet.com> 5.3.5-1.2
- rebuild against MySQL 5.5 (fedora <= 8)

* Sat Jan 22 2011 Remi Collet <rpms@famillecollet.com> 5.3.5-1.1
- rebuild against freetds 0.82 (EL <= 5, fedora <= 10)

* Fri Jan 07 2011 Remi Collet <rpms@famillecollet.com> 5.3.5-1
- update to 5.3.5
  http://www.php.net/ChangeLog-5.php#5.3.5

* Sun Dec 26 2010 Remi Collet <rpms@famillecollet.com> 5.3.4-3
- relocate using phpname macro
- rebuild against MySQL 5.5

* Sun Dec 12 2010 Remi Collet <rpms@famillecollet.com> 5.3.4-2
- security patch from upstream for #660517

* Sat Dec 11 2010 Remi Collet <rpms@famillecollet.com> 5.3.4-1
- update to 5.3.4
  http://www.php.net/ChangeLog-5.php#5.3.4
- move phpize to php-cli (see #657812)
- create php-sqlite subpackage (for old sqlite2 ext)

* Wed Sep 29 2010 Remi Collet <rpms@famillecollet.com> 5.3.3-1.2
- use SIGUSR2 for service reload
- fix slowlog comment + set default value

* Fri Jul 30 2010 Remi Collet <rpms@famillecollet.com> 5.3.3-1.1
- use system pcre only on fedora >= 10 (version 7.8)
- rebuild

* Thu Jul 22 2010 Remi Collet <rpms@famillecollet.com> 5.3.3-1.
- update to 5.3.3
- add php-fpm sub-package
- systzdata-v7.patch

* Tue Apr 26 2010 Remi Collet <rpms@famillecollet.com> 5.3.2-2
- garbage collector upstream  patches

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


