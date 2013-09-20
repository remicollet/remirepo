%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
%global with_dtrace 1
%else
%global with_dtrace 0
%endif

Name: mysql
Version: 5.5.34
Release: 1%{?dist}

Summary: MySQL client programs and shared libraries
Group: Applications/Databases
URL: http://www.mysql.com
# exceptions allow client libraries to be linked with most open source SW,
# not only GPL code.  See README.mysql-license
# Some innobase code from Percona and Google is under BSD license
# Some code related to test-suite is under LGPLv2
License: GPLv2 with exceptions and LGPLv2 and BSD

# Regression tests take a long time, you can skip 'em with this
%{!?runselftest:%global runselftest 1}

# Upstream has a mirror redirector for downloads, so the URL is hard to
# represent statically.  You can get the tarball by following a link from
# http://dev.mysql.com/downloads/mysql/
Source0: mysql-%{version}.tar.gz
# The upstream tarball includes non-free documentation that we cannot ship.
# To remove the non-free documentation, run this script after downloading
# the tarball into the current directory:
# ./generate-tarball.sh $VERSION
# Source1: generate-tarball.sh not used for remi repo
Source1: mysql.sysconfig
Source2: mysql.init
Source3: my.cnf
Source4: scriptstub.c
Source5: my_config.h
Source6: README.mysql-docs
Source7: README.mysql-license
Source8: libmysql.version
Source9: mysql-embedded-check.c
Source10: mysql.tmpfiles.d
# systemd files
Source11: mysqld.service
Source12: mysqld-prepare-db-dir
Source13: mysqld-wait-ready
Source14: rh-skipped-tests-base.list
Source15: rh-skipped-tests-arm.list
# Working around perl dependency checking bug in rpm FTTB. Remove later.
Source999: filter-requires-mysql.sh

# Comments for these patches are in the patch files.
Patch1: mysql-errno.patch
Patch2: mysql-strmov.patch
Patch3: mysql-install-test.patch
Patch4: mysql-expired-certs.patch
Patch5: mysql-stack-guard.patch
Patch6: mysql-chain-certs.patch
Patch7: mysql-versioning.patch
Patch8: mysql-dubious-exports.patch
Patch10: mysql-plugin-bool.patch
Patch11: mysql-s390-tsc.patch
Patch14: mysql-va-list.patch
Patch15: mysql-netdevname.patch
Patch16: mysql-logrotate.patch
Patch17: mysql-plugin-test.patch
Patch18: mysql-cipherspec.patch
Patch19: mysql-file-contents.patch
Patch20: mysql-string-overflow.patch
Patch21: mysql-dh1024.patch
Patch22: mysql-innodbwarn.patch
# http://bugs.mysql.com/68999
Patch23: mysql-openssl.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gperf
BuildRequires: perl, readline-devel, openssl-devel
BuildRequires: gcc-c++, cmake, ncurses-devel, zlib-devel, libaio-devel
%if %{with_dtrace}
BuildRequires: systemtap-sdt-devel >= 1.3
%endif
# make test requires time and ps
BuildRequires: time procps
# Socket and Time::HiRes are needed to run regression tests
BuildRequires: perl(Socket), perl(Time::HiRes)
%if %{with_systemd}
BuildRequires: systemd-units
%endif

Requires: grep, fileutils
Requires: real-%{name}-libs%{?_isa} = %{version}-%{release}
Requires: bash

# We can use real- prefix to distinguish from other MySQL implementations
# like MariaDB unambiguously
Provides: real-%{name} = %{version}-%{release}
Provides: real-%{name}%{?_isa} = %{version}-%{release}

# MySQL (with caps) is upstream's spelling of their own RPMs for mysql
Conflicts: MySQL
# mysql-cluster used to be built from this SRPM, but no more
Obsoletes: mysql-cluster < 5.1.44
# Virtual provides present in upstream's RPM (used by some app)
Provides: mysql-client = %{version}-%{release}

# When rpm 4.9 is universal, this could be cleaned up:
%global __perl_requires %{SOURCE999}
%global __perllib_requires %{SOURCE999}

# By default, patch(1) creates backup files when chunks apply with offsets.
# Turn that off to ensure such files don't get included in RPMs (cf bz#884755).
%global _default_patch_flags --no-backup-if-mismatch

%description
MySQL is a multi-user, multi-threaded SQL database server. MySQL is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. The base package
contains the standard MySQL client programs and generic MySQL files.

%package libs

Summary: The shared libraries required for MySQL clients
Group: Applications/Databases
Requires: /sbin/ldconfig
Provides: real-%{name}-libs = %{version}-%{release}
Provides: real-%{name}-libs%{?_isa} = %{version}-%{release}
Obsoletes: compat-mysql55 <= %{version}
%if 0%{?rhel} == 5
# EL-5 mysql 5.0.x have no mysql/mysql-libs
# This circular dep. should make update simpler
Requires: %{name}%{?_isa} = %{version}-%{release}
%endif

%description libs
The mysql-libs package provides the essential shared libraries for any 
MySQL client program or interface. You will need to install this package
to use any other MySQL package or any clients that need to connect to a
MySQL server.

%package server

Summary: The MySQL server and related files
Group: Applications/Databases
Requires: real-%{name}%{?_isa} = %{version}-%{release}
Requires: real-%{name}-libs%{?_isa} = %{version}-%{release}
Requires: sh-utils
Requires(pre): /usr/sbin/useradd
Requires(post): chkconfig
Requires(preun): chkconfig
%if %{with_systemd}
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires: systemd-units
# Make sure it's there when scriptlets run, too
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
# mysqlhotcopy needs DBI/DBD support
Requires: perl-DBI, perl-DBD-MySQL
Conflicts: MySQL-server
Provides: real-%{name}-server = %{version}-%{release}
Provides: real-%{name}-server%{?_isa} = %{version}-%{release}

%description server
MySQL is a multi-user, multi-threaded SQL database server. MySQL is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. This package contains
the MySQL server and some accompanying files and directories.

%package devel

Summary: Files for development of MySQL applications
Group: Applications/Databases
Requires: real-%{name}%{?_isa} = %{version}-%{release}
Requires: real-%{name}-libs%{?_isa} = %{version}-%{release}
Requires: openssl-devel%{?_isa}
Conflicts: MySQL-devel
Provides: real-%{name}-devel = %{version}-%{release}
Provides: real-%{name}-devel%{?_isa} = %{version}-%{release}

%description devel
MySQL is a multi-user, multi-threaded SQL database server. This
package contains the libraries and header files that are needed for
developing MySQL client applications.

%package embedded

Summary: MySQL as an embeddable library
Group: Applications/Databases
Provides: real-%{name}-embedded = %{version}-%{release}
Provides: real-%{name}-embedded%{?_isa} = %{version}-%{release}

%description embedded
MySQL is a multi-user, multi-threaded SQL database server. This
package contains a version of the MySQL server that can be embedded
into a client application instead of running as a separate process.

%package embedded-devel

Summary: Development files for MySQL as an embeddable library
Group: Applications/Databases
Requires: real-%{name}-embedded%{?_isa} = %{version}-%{release}
Requires: real-%{name}-devel%{?_isa} = %{version}-%{release}
Provides: real-%{name}-embedded-devel = %{version}-%{release}
Provides: real-%{name}-embedded-devel%{?_isa} = %{version}-%{release}

%description embedded-devel
MySQL is a multi-user, multi-threaded SQL database server. This
package contains files needed for developing and testing with
the embedded version of the MySQL server.

%package bench

Summary: MySQL benchmark scripts and data
Group: Applications/Databases
Requires: real-%{name}%{?_isa} = %{version}-%{release}
Conflicts: MySQL-bench
Provides: real-%{name}-bench = %{version}-%{release}
Provides: real-%{name}-bench%{?_isa} = %{version}-%{release}

%description bench
MySQL is a multi-user, multi-threaded SQL database server. This
package contains benchmark scripts and data for use when benchmarking
MySQL.

%package test

Summary: The test suite distributed with MySQL
Group: Applications/Databases
Requires: real-%{name}%{?_isa} = %{version}-%{release}
Requires: real-%{name}-libs%{?_isa} = %{version}-%{release}
Requires: real-%{name}-server%{?_isa} = %{version}-%{release}
Conflicts: MySQL-test
Provides: real-%{name}-test  = %{version}-%{release}
Provides: real-%{name}-test%{?_isa} = %{version}-%{release}

%description test
MySQL is a multi-user, multi-threaded SQL database server. This
package contains the regression test suite distributed with
the MySQL sources.

%prep
%setup -q -n mysql-%{version}

# Can't provide this file (by licence)
rm -f Docs/mysql.info


%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch10 -p1
%patch11 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1

# workaround for upstream bug #56342
rm -f mysql-test/t/ssl_8k_key-master.opt

# upstream has fallen down badly on symbol versioning, do it ourselves
cp %{SOURCE8} libmysql/libmysql.version

# generate a list of tests that fail, but are not disabled by upstream
cat %{SOURCE14} > mysql-test/rh-skipped-tests.list
# disable some tests failing on ARM architectures
%ifarch %{arm}
cat %{SOURCE15} >> mysql-test/rh-skipped-tests.list
%endif

%build

# fail quickly and obviously if user tries to build as root
%if %runselftest
	if [ x"`id -u`" = x0 ]; then
		echo "mysql's regression tests fail if run as root."
		echo "If you really need to build the RPM as root, use"
		echo "--define='runselftest 0' to skip the regression tests."
		exit 1
	fi
%endif

CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
# MySQL 4.1.10 definitely doesn't work under strict aliasing; also,
# gcc 4.1 breaks MySQL 5.0.16 without -fwrapv
CFLAGS="$CFLAGS -fno-strict-aliasing -fwrapv"
# force PIC mode so that we can build libmysqld.so
CFLAGS="$CFLAGS -fPIC"
# gcc seems to have some bugs on sparc as of 4.4.1, back off optimization
# submitted as bz #529298
%ifarch sparc sparcv9 sparc64
CFLAGS=`echo $CFLAGS| sed -e "s|-O2|-O1|g" `
%endif
CXXFLAGS="$CFLAGS"
export CFLAGS CXXFLAGS

# The INSTALL_xxx macros have to be specified relative to CMAKE_INSTALL_PREFIX
# so we can't use %%{_datadir} and so forth here.

cmake . -DBUILD_CONFIG=mysql_release \
	-DCOMPILATION_COMMENT="MySQL Community Server (GPL) by Remi" \
	-DFEATURE_SET="community" \
	-DINSTALL_LAYOUT=RPM \
	-DCMAKE_INSTALL_PREFIX="%{_prefix}" \
	-DINSTALL_INCLUDEDIR=include/mysql \
	-DINSTALL_INFODIR=share/info \
	-DINSTALL_LIBDIR="%{_lib}/mysql" \
	-DINSTALL_MANDIR=share/man \
	-DINSTALL_MYSQLSHAREDIR=share/mysql \
	-DINSTALL_MYSQLTESTDIR=share/mysql-test \
	-DINSTALL_PLUGINDIR="%{_lib}/mysql/plugin" \
	-DINSTALL_SBINDIR=libexec \
	-DINSTALL_SCRIPTDIR=bin \
	-DINSTALL_SQLBENCHDIR=share \
	-DINSTALL_SUPPORTFILESDIR=share/mysql \
	-DMYSQL_DATADIR="/var/lib/mysql" \
	-DMYSQL_UNIX_ADDR="/var/lib/mysql/mysql.sock" \
	-DENABLED_LOCAL_INFILE=ON \
%if %{with_dtrace}
	-DENABLE_DTRACE=ON \
%endif
	-DWITH_EMBEDDED_SERVER=ON \
	-DWITH_READLINE=ON \
	-DWITH_SSL=system \
	-DWITH_ZLIB=system

gcc $CFLAGS $LDFLAGS -o scriptstub "-DLIBDIR=\"%{_libdir}/mysql\"" %{SOURCE4}

make %{?_smp_mflags} VERBOSE=1

# regular build will make libmysqld.a but not libmysqld.so :-(
mkdir libmysqld/work
cd libmysqld/work
ar -x ../libmysqld.a
# these result in missing dependencies: (filed upstream as bug 59104)
rm -f sql_binlog.cc.o rpl_utility.cc.o
gcc $CFLAGS $LDFLAGS -shared -Wl,-soname,libmysqld.so.0 -o libmysqld.so.0.0.1 \
	*.o \
%if %{with_dtrace}
	../../probes_mysql.o \
%endif
	-lpthread -laio -lcrypt -lssl -lcrypto -lz -lrt -lstdc++ -ldl -lm -lc
# this is to check that we built a complete library
cp %{SOURCE9} .
ln -s libmysqld.so.0.0.1 libmysqld.so.0
gcc -I../../include $CFLAGS mysql-embedded-check.c libmysqld.so.0
LD_LIBRARY_PATH=. ldd ./a.out
cd ../..

%if %runselftest
  # hack to let 32- and 64-bit tests run concurrently on same build machine
  case `uname -m` in
    ppc64 | ppc64p7 | s390x | x86_64 | sparc64 )
      MTR_BUILD_THREAD=7
      ;;
    *)
      MTR_BUILD_THREAD=11
      ;;
  esac
  export MTR_BUILD_THREAD

  # Sometine, test fails because of this lib.
  LD_LIBRARY_PATH=$PWD/libservices
  export LD_LIBRARY_PATH

  make test VERBOSE=1

  # The cmake build scripts don't provide any simple way to control the
  # options for mysql-test-run, so ignore the make target and just call it
  # manually.  Nonstandard options chosen are:
  # --force to continue tests after a failure
  # no retries please
  # test SSL with --ssl
  # skip tests that are listed in rh-skipped-tests.list
  # avoid redundant test runs with --binlog-format=mixed
  # increase timeouts to prevent unwanted failures during mass rebuilds
  (
    cd mysql-test
    perl ./mysql-test-run.pl --force --retry=0 --ssl \
	--skip-test-list=rh-skipped-tests.list \
	--mysqld=--binlog-format=mixed \
	--suite-timeout=720 --testcase-timeout=30 --suite=main
    # cmake build scripts will install the var cruft if left alone :-(
    rm -rf var
  ) 
%endif

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

# List the installed tree for RPM package maintenance purposes.
find $RPM_BUILD_ROOT -print | sed "s|^$RPM_BUILD_ROOT||" | sort > ROOTFILES

# multilib header hacks
# we only apply this to known Red Hat multilib arches, per bug #181335
case `uname -i` in
  i386 | x86_64 | ppc | ppc64 | ppc64p7 | s390 | s390x | sparc | sparc64 )
    mv $RPM_BUILD_ROOT/usr/include/mysql/my_config.h $RPM_BUILD_ROOT/usr/include/mysql/my_config_`uname -i`.h
    install -m 644 %{SOURCE5} $RPM_BUILD_ROOT/usr/include/mysql/
    ;;
  *)
    ;;
esac

# cmake generates some completely wacko references to -lprobes_mysql when
# building with dtrace support.  Haven't found where to shut that off,
# so resort to this blunt instrument.  While at it, let's not reference
# libmysqlclient_r anymore either.
sed -e 's/-lprobes_mysql//' -e 's/-lmysqlclient_r/-lmysqlclient/' \
	${RPM_BUILD_ROOT}%{_bindir}/mysql_config >mysql_config.tmp
cp -f mysql_config.tmp ${RPM_BUILD_ROOT}%{_bindir}/mysql_config
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/mysql_config

# install INFO_SRC, INFO_BIN into libdir (upstream thinks these are doc files,
# but that's pretty wacko --- see also mysql-file-contents.patch)
install -m 644 Docs/INFO_SRC ${RPM_BUILD_ROOT}%{_libdir}/mysql/
install -m 644 Docs/INFO_BIN ${RPM_BUILD_ROOT}%{_libdir}/mysql/

mkdir -p $RPM_BUILD_ROOT/var/log
touch $RPM_BUILD_ROOT/var/log/mysqld.log

mkdir -p $RPM_BUILD_ROOT/var/run/mysqld
install -m 0755 -d $RPM_BUILD_ROOT/var/lib/mysql

mkdir -p $RPM_BUILD_ROOT/etc
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT/etc/my.cnf
%if %{with_systemd}
sed -i -e '/user=mysql/d' $RPM_BUILD_ROOT/etc/my.cnf
%endif

%if %{with_systemd}
# install systemd unit files and scripts for handling server startup
mkdir -p ${RPM_BUILD_ROOT}%{_unitdir}
install -m 644 %{SOURCE11} ${RPM_BUILD_ROOT}%{_unitdir}/
%if 0%{?fedora} == 15
# PrivateTmp only work on fedora >= 16
sed -i -e '/PrivateTmp/s/true/false/' ${RPM_BUILD_ROOT}%{_unitdir}/mysqld.service
%endif
install -m 755 %{SOURCE12} ${RPM_BUILD_ROOT}%{_libexecdir}/
install -m 755 %{SOURCE13} ${RPM_BUILD_ROOT}%{_libexecdir}/

mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d
install -m 0644 %{SOURCE10} $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/mysql.conf

%else
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/mysqld

# sysconfig is only provided by remi
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/mysqld
%endif

# Fix funny permissions that cmake build scripts apply to config files
chmod 644 ${RPM_BUILD_ROOT}%{_datadir}/mysql/config.*.ini

# Fix scripts for multilib safety
mv ${RPM_BUILD_ROOT}%{_bindir}/mysqlbug ${RPM_BUILD_ROOT}%{_libdir}/mysql/mysqlbug
install -m 0755 scriptstub ${RPM_BUILD_ROOT}%{_bindir}/mysqlbug
mv ${RPM_BUILD_ROOT}%{_bindir}/mysql_config ${RPM_BUILD_ROOT}%{_libdir}/mysql/mysql_config
install -m 0755 scriptstub ${RPM_BUILD_ROOT}%{_bindir}/mysql_config

# Remove libmysqld.a, install libmysqld.so
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqld.a
install -m 0755 libmysqld/work/libmysqld.so.0.0.1 ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqld.so.0.0.1
ln -s libmysqld.so.0.0.1 ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqld.so.0
ln -s libmysqld.so.0 ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqld.so

# libmysqlclient_r is no more.  Upstream tries to replace it with symlinks
# but that really doesn't work (wrong soname in particular).  We'll keep
# just the devel libmysqlclient_r.so link, so that rebuilding without any
# source change is enough to get rid of dependency on libmysqlclient_r.
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqlclient_r.so*
ln -s libmysqlclient.so ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqlclient_r.so

# mysql-test includes one executable that doesn't belong under /usr/share,
# so move it and provide a symlink
mv ${RPM_BUILD_ROOT}%{_datadir}/mysql-test/lib/My/SafeProcess/my_safe_process ${RPM_BUILD_ROOT}%{_bindir}
ln -s ../../../../../bin/my_safe_process ${RPM_BUILD_ROOT}%{_datadir}/mysql-test/lib/My/SafeProcess/my_safe_process

# Remove files that %%doc will install in preferred location
rm -f ${RPM_BUILD_ROOT}/usr/COPYING
rm -f ${RPM_BUILD_ROOT}/usr/README

# Remove files we don't want installed at all
rm -f ${RPM_BUILD_ROOT}/usr/INSTALL-BINARY
rm -f ${RPM_BUILD_ROOT}/usr/docs/ChangeLog
rm -f ${RPM_BUILD_ROOT}/usr/data/mysql/.empty
rm -f ${RPM_BUILD_ROOT}/usr/data/test/.empty
# should move this to /etc/ ?
rm -f ${RPM_BUILD_ROOT}%{_bindir}/mysqlaccess.conf
rm -f ${RPM_BUILD_ROOT}%{_bindir}/mysql_embedded
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/*.a
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/binary-configure
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/magic
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/ndb-config-2-node.ini
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/mysql.server
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/mysqld_multi.server
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/comp_err.1*
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/mysql-stress-test.pl.1*
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/mysql-test-run.pl.1*

# put logrotate script where it needs to be
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mv ${RPM_BUILD_ROOT}%{_datadir}/mysql/mysql-log-rotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/mysqld
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/mysqld

mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo "%{_libdir}/mysql" > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{_arch}.conf

# copy additional docs into build tree so %%doc will find them
cp %{SOURCE6} README.mysql-docs
cp %{SOURCE7} README.mysql-license

# install the list of skipped tests to be available for user runs
install -m 0644 mysql-test/rh-skipped-tests.list ${RPM_BUILD_ROOT}%{_datadir}/mysql-test

# we don't care about scripts for solaris
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/solaris/postinstall-solaris

%clean
rm -rf $RPM_BUILD_ROOT

%pre libs
echo -e "\nWARNING : This MySQL RPM is not an official Fedora / Red Hat build and it"
echo -e "overrides the official one. Don't file bugs on Fedora Project nor Red Hat."
echo -e "Use dedicated forums http://forums.famillecollet.com/\n"

%if %{?fedora}%{!?fedora:99} <= 16
echo -e "WARNING : Fedora %{fedora} is now EOL :"
echo -e "You should consider upgrading to a supported release.\n"
%endif


%pre server
/usr/sbin/groupadd -g 27 -o -r mysql >/dev/null 2>&1 || :
%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
/usr/sbin/useradd -M -N -g mysql -o -r -d /var/lib/mysql -s /bin/bash \
	-c "MySQL Server" -u 27 mysql >/dev/null 2>&1 || :
%else
# -N options used on Fedora not available on fedora <= 8 and EL <= 5
/usr/sbin/useradd -M -g mysql -o -r -d /var/lib/mysql -s /bin/bash \
	-c "MySQL Server" -u 27 mysql >/dev/null 2>&1 || :
%endif 

%post libs
/sbin/ldconfig

%post server
%if 0%{?systemd_post:1}
%systemd_post mysqld.service
%else
if [ $1 = 1 ]; then
    # Initial installation
%if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add mysqld
%endif
fi
%endif
/bin/chmod 0755 /var/lib/mysql
/bin/touch /var/log/mysqld.log

# Handle upgrading from SysV initscript to native systemd unit.
# We can tell if a SysV version of mysql was previously installed by
# checking to see if the initscript is present.
%triggerun server -- mysql-server
%if %{with_systemd}
if [ -f /etc/rc.d/init.d/mysqld ]; then
    # Save the current service runlevel info
    # User must manually run systemd-sysv-convert --apply mysqld
    # to migrate them to systemd targets
    /usr/bin/systemd-sysv-convert --save mysqld >/dev/null 2>&1 || :

    # Run these because the SysV package being removed won't do them
    /sbin/chkconfig --del mysqld >/dev/null 2>&1 || :
    /bin/systemctl try-restart mysqld.service >/dev/null 2>&1 || :
fi
%endif

%preun server
%if 0%{?systemd_preun:1}
%systemd_preun mysqld.service
%else
if [ $1 = 0 ]; then
    # Package removal, not upgrade
%if %{with_systemd}
    /bin/systemctl --no-reload disable mysqld.service >/dev/null 2>&1 || :
    /bin/systemctl stop mysqld.service >/dev/null 2>&1 || :
%else
    /sbin/service mysqld stop >/dev/null 2>&1
    /sbin/chkconfig --del mysqld
%endif
fi
%endif

%postun libs
if [ $1 = 0 ] ; then
    /sbin/ldconfig
fi

%postun server
%if 0%{?systemd_postun_with_restart:1}
%systemd_postun_with_restart mysqld.service
%else
%if %{with_systemd}
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ]; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart mysqld.service >/dev/null 2>&1 || :
fi
%else
if [ $1 -ge 1 ]; then
    /sbin/service mysqld condrestart >/dev/null 2>&1 || :
fi
%endif
%endif


%files
%defattr(-,root,root)
%doc README COPYING README.mysql-license
%doc README.mysql-docs
%doc Docs

%{_bindir}/msql2mysql
%{_bindir}/mysql
%{_bindir}/mysql_config
%{_bindir}/mysql_find_rows
%{_bindir}/mysql_waitpid
%{_bindir}/mysqlaccess
%{_bindir}/mysqladmin
%{_bindir}/mysqlbinlog
%{_bindir}/mysqlcheck
%{_bindir}/mysqldump
%{_bindir}/mysqlimport
%{_bindir}/mysqlshow
%{_bindir}/mysqlslap
%{_bindir}/my_print_defaults

%{_mandir}/man1/mysql.1*
%{_mandir}/man1/mysql_config.1*
%{_mandir}/man1/mysql_find_rows.1*
%{_mandir}/man1/mysql_waitpid.1*
%{_mandir}/man1/mysqlaccess.1*
%{_mandir}/man1/mysqladmin.1*
%{_mandir}/man1/mysqldump.1*
%{_mandir}/man1/mysqlshow.1*
%{_mandir}/man1/mysqlslap.1*
%{_mandir}/man1/my_print_defaults.1*

%{_libdir}/mysql/mysql_config

%files libs
%defattr(-,root,root)
%doc README COPYING README.mysql-license
# although the default my.cnf contains only server settings, we put it in the
# libs package because it can be used for client settings too.
%config(noreplace) /etc/my.cnf
%dir %{_libdir}/mysql
%{_libdir}/mysql/libmysqlclient.so.18*
/etc/ld.so.conf.d/*

%dir %{_datadir}/mysql
%{_datadir}/mysql/english
%lang(cs) %{_datadir}/mysql/czech
%lang(da) %{_datadir}/mysql/danish
%lang(nl) %{_datadir}/mysql/dutch
%lang(et) %{_datadir}/mysql/estonian
%lang(fr) %{_datadir}/mysql/french
%lang(de) %{_datadir}/mysql/german
%lang(el) %{_datadir}/mysql/greek
%lang(hu) %{_datadir}/mysql/hungarian
%lang(it) %{_datadir}/mysql/italian
%lang(ja) %{_datadir}/mysql/japanese
%lang(ko) %{_datadir}/mysql/korean
%lang(no) %{_datadir}/mysql/norwegian
%lang(no) %{_datadir}/mysql/norwegian-ny
%lang(pl) %{_datadir}/mysql/polish
%lang(pt) %{_datadir}/mysql/portuguese
%lang(ro) %{_datadir}/mysql/romanian
%lang(ru) %{_datadir}/mysql/russian
%lang(sr) %{_datadir}/mysql/serbian
%lang(sk) %{_datadir}/mysql/slovak
%lang(es) %{_datadir}/mysql/spanish
%lang(sv) %{_datadir}/mysql/swedish
%lang(uk) %{_datadir}/mysql/ukrainian
%{_datadir}/mysql/charsets

%files server
%defattr(-,root,root)
%doc support-files/*.cnf

%{_bindir}/myisamchk
%{_bindir}/myisam_ftdump
%{_bindir}/myisamlog
%{_bindir}/myisampack
%{_bindir}/mysql_convert_table_format
%{_bindir}/mysql_fix_extensions
%{_bindir}/mysql_install_db
%{_bindir}/mysql_plugin
%{_bindir}/mysql_secure_installation
%{_bindir}/mysql_setpermission
%{_bindir}/mysql_tzinfo_to_sql
%{_bindir}/mysql_upgrade
%{_bindir}/mysql_zap
%{_bindir}/mysqlbug
%{_bindir}/mysqldumpslow
%{_bindir}/mysqld_multi
%{_bindir}/mysqld_safe
%{_bindir}/mysqlhotcopy
%{_bindir}/mysqltest
%{_bindir}/innochecksum
%{_bindir}/perror
%{_bindir}/replace
%{_bindir}/resolve_stack_dump
%{_bindir}/resolveip

/usr/libexec/mysqld

%{_libdir}/mysql/INFO_SRC
%{_libdir}/mysql/INFO_BIN

%{_libdir}/mysql/mysqlbug

%{_libdir}/mysql/plugin

%{_mandir}/man1/msql2mysql.1*
%{_mandir}/man1/myisamchk.1*
%{_mandir}/man1/myisamlog.1*
%{_mandir}/man1/myisampack.1*
%{_mandir}/man1/mysql_convert_table_format.1*
%{_mandir}/man1/myisam_ftdump.1*
%{_mandir}/man1/mysql.server.1*
%{_mandir}/man1/mysql_fix_extensions.1*
%{_mandir}/man1/mysql_install_db.1*
%{_mandir}/man1/mysql_plugin.1*
%{_mandir}/man1/mysql_secure_installation.1*
%{_mandir}/man1/mysql_upgrade.1*
%{_mandir}/man1/mysql_zap.1*
%{_mandir}/man1/mysqlbug.1*
%{_mandir}/man1/mysqldumpslow.1*
%{_mandir}/man1/mysqlbinlog.1*
%{_mandir}/man1/mysqlcheck.1*
%{_mandir}/man1/mysqld_multi.1*
%{_mandir}/man1/mysqld_safe.1*
%{_mandir}/man1/mysqlhotcopy.1*
%{_mandir}/man1/mysqlimport.1*
%{_mandir}/man1/mysqlman.1*
%{_mandir}/man1/mysql_setpermission.1*
%{_mandir}/man1/mysqltest.1*
%{_mandir}/man1/innochecksum.1*
%{_mandir}/man1/perror.1*
%{_mandir}/man1/replace.1*
%{_mandir}/man1/resolve_stack_dump.1*
%{_mandir}/man1/resolveip.1*
%{_mandir}/man1/mysql_tzinfo_to_sql.1*
%{_mandir}/man8/mysqld.8*

%{_datadir}/mysql/errmsg-utf8.txt
%{_datadir}/mysql/fill_help_tables.sql
%{_datadir}/mysql/mysql_system_tables.sql
%{_datadir}/mysql/mysql_system_tables_data.sql
%{_datadir}/mysql/mysql_test_data_timezone.sql
%{_datadir}/mysql/my-*.cnf
%{_datadir}/mysql/config.*.ini

%if %{with_systemd}
%{_unitdir}/mysqld.service
%{_libexecdir}/mysqld-prepare-db-dir
%{_libexecdir}/mysqld-wait-ready

%{_prefix}/lib/tmpfiles.d/mysql.conf
%else
/etc/rc.d/init.d/mysqld
%config(noreplace) /etc/sysconfig/mysqld
%endif
%attr(0755,mysql,mysql) %dir /var/run/mysqld
%attr(0755,mysql,mysql) %dir /var/lib/mysql
%attr(0640,mysql,mysql) %config(noreplace) %verify(not md5 size mtime) /var/log/mysqld.log
%config(noreplace) %{_sysconfdir}/logrotate.d/mysqld

%files devel
%defattr(-,root,root)
/usr/include/mysql
/usr/share/aclocal/mysql.m4
%{_libdir}/mysql/libmysqlclient.so
%{_libdir}/mysql/libmysqlclient_r.so

%files embedded
%defattr(-,root,root)
%doc README COPYING README.mysql-license
%{_libdir}/mysql/libmysqld.so.*

%files embedded-devel
%defattr(-,root,root)
%{_libdir}/mysql/libmysqld.so
%{_bindir}/mysql_client_test_embedded
%{_bindir}/mysqltest_embedded
%{_mandir}/man1/mysql_client_test_embedded.1*
%{_mandir}/man1/mysqltest_embedded.1*

%files bench
%defattr(-,root,root)
%{_datadir}/sql-bench

%files test
%defattr(-,root,root)
%{_bindir}/mysql_client_test
%{_bindir}/my_safe_process
%attr(-,mysql,mysql) %{_datadir}/mysql-test

%{_mandir}/man1/mysql_client_test.1*

%changelog
* Fri Sep 20 2013 Remi Collet <RPMS@FamilleCollet.com> - 5.5.34-1
- update to MySQL 5.5.34 Community Server GA
  http://dev.mysql.com/doc/relnotes/mysql/5.5/en/news-5-5-34.html

* Thu Aug  1 2013 Remi Collet <RPMS@FamilleCollet.com> - 5.5.33-1
- update to MySQL 5.5.33 Community Server GA
  http://dev.mysql.com/doc/relnotes/mysql/5.5/en/news-5-5-33.html

* Fri Jun 14 2013 Honza Horak <hhorak@redhat.com> 5.5.32-1
- Use man pages from 5.5.30, because their license do not
  allow us to ship them since 5.5.31
- Update to MySQL 5.5.32, for various fixes described at
  http://dev.mysql.com/doc/relnotes/mysql/5.5/en/news-5-5-32.html

* Tue Jun  4 2013 Remi Collet <RPMS@FamilleCollet.com> - 5.5.32-1
- update to MySQL 5.5.32 Community Server GA
  http://dev.mysql.com/doc/relnotes/mysql/5.5/en/news-5-5-32.html

* Fri Apr 19 2013 Honza Horak <hhorak@redhat.com> 5.5.31-1
- Update to MySQL 5.5.31, for various fixes described at
  http://dev.mysql.com/doc/relnotes/mysql/5.5/en/news-5-5-31.html

* Thu Feb 28 2013 Remi Collet <RPMS@FamilleCollet.com> - 5.5.31-1
- update to MySQL 5.5.31 Community Server GA
  http://dev.mysql.com/doc/relnotes/mysql/5.5/en/news-5-5-31.html

* Tue Feb 12 2013 Honza Horak <hhorak@redhat.com> 5.5.30-1
- Update to MySQL 5.5.30, for various fixes described at
  http://dev.mysql.com/doc/relnotes/mysql/5.5/en/news-5-5-30.html

* Tue Feb 12 2013 Honza Horak <hhorak@redhat.com> 5.5.29-3
- Use real- prefix for cross-package requirements

* Mon Feb 11 2013 Honza Horak <hhorak@redhat.com> 5.5.29-2
- Provide own symbols with real- prefix to distinguish packages from other
  MySQL implementations unambiguously

* Fri Feb  8 2013 Remi Collet <RPMS@FamilleCollet.com> - 5.5.30-1
- update to MySQL 5.5.30 Community Server GA
  http://dev.mysql.com/doc/relnotes/mysql/5.5/en/news-5-5-30.html

* Wed Jan  2 2013 Tom Lane <tgl@redhat.com> 5.5.29-1
- Update to MySQL 5.5.29, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-29.html
- Fix inaccurate default for socket location in mysqld-wait-ready
Resolves: #890535

* Fri Dec 28 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.5.29-1
- update to MySQL 5.5.29 Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-29.html

* Sat Dec  8 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.5.28-3
- sync with rawhide, rebuild for security
- use with_systemd and with_dtrace macro instead of version test

* Thu Dec  6 2012 Honza Horak <hhorak@redhat.com> 5.5.28-3
- Rebase patches to not leave backup files when not applied smoothly
- Use --no-backup-if-mismatch to prevent including backup files

* Wed Dec  5 2012 Tom Lane <tgl@redhat.com> 5.5.28-2
- Add patch for CVE-2012-5611
Resolves: #883642
- Widen DH key length from 512 to 1024 bits to meet minimum requirements
  of FIPS 140-2
Related: #877124

* Sat Sep 29 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.5.28-2
- sync with rawhide

* Sat Sep 29 2012 Tom Lane <tgl@redhat.com> 5.5.28-1
- Update to MySQL 5.5.28, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-28.html
- Clean up partially-created database files when mysql_install_db fails
Related: #835131
- Honor user and group settings from service file in mysqld-prepare-db-dir
Resolves: #840431
- Export THR_KEY_mysys as a workaround for inadequate threading support
Resolves: #846602
- Adopt new systemd macros for server package install/uninstall triggers
Resolves: #850222
- Use --no-defaults when invoking mysqladmin to wait for the server to start
Related: #855704

* Sat Sep 29 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.5.28-1
- update to MySQL 5.5.28 Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-28.html

* Sun Aug  5 2012 Tom Lane <tgl@redhat.com> 5.5.27-1
- Update to MySQL 5.5.27, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-27.html

* Fri Aug 03 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.5.27-1
- update to MySQL 5.5.27 Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-27.html
- enable dtrace on EL6
- cleanup old stuff (EL4)

* Sat Jul 07 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.5.25a-1.1
- sync with rawhide

* Fri Jul  6 2012 Tom Lane <tgl@redhat.com> 5.5.25a-1
- Update to MySQL 5.5.25a, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-25a.html
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-25.html
- Don't use systemd's Restart feature; rely on mysqld_safe instead
Resolves: #832029

* Fri Jul 06 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.5.25a-1
- update to MySQL 5.5.25a Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-25a.html

* Mon Jun 11 2012 Tom Lane <tgl@redhat.com> 5.5.24-1
- Update to MySQL 5.5.24, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-24.html
   including the fix for CVE-2012-2122
Resolves: #830680
- Tweak logrotate script to put the right permissions on mysqld.log
- Minor specfile fixes for recent packaging guidelines changes

* Fri Jun 01 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.5.25-1
- update to MySQL 5.5.25 Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-25.html

* Thu May 10 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.5.24-1
- update to MySQL 5.5.24 Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-24.html

* Sat Apr 28 2012 Tom Lane <tgl@redhat.com> 5.5.23-1
- Update to MySQL 5.5.23, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-23.html

* Fri Apr 13 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.5.23-1
- update to MySQL 5.5.23 Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-23.html
- export my_net_read for mydumper
- sync patches with rawhide

* Sat Mar 24 2012 Tom Lane <tgl@redhat.com> 5.5.22-1
- Update to MySQL 5.5.22, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-22.html
- Turn on PrivateTmp in service file
Resolves: #782513
- Comment out the contents of /etc/logrotate.d/mysqld, so that manual
  action is needed to enable log rotation.  Given the multiple ways in
  which the rotation script can fail, it seems imprudent to try to make
  it run by default.
Resolves: #799735

* Fri Mar 23 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.5.22-1
- update to MySQL 5.5.22 Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-22.html
- sync with latest changes in rawhide for 5.5.21

* Tue Mar 20 2012 Honza Horak <hhorak@redhat.com> 5.5.21-3
- Revise mysql_plugin test patch which moves plugin files to 
  a temporary directory now
Resolves: #789530

* Tue Mar 13 2012 Honza Horak <hhorak@redhat.com> 5.5.21-2
- Fix ssl-related tests to specify expected cipher explicitly
Related: #789600
- Fix several strcpy calls to check destination size

* Mon Feb 27 2012 Tom Lane <tgl@redhat.com> 5.5.21-1
- Update to MySQL 5.5.21, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-21.html
- Hack openssl regression test to still work with rawhide's openssl
- Fix assorted failures in post-install regression tests (mysql-test RPM)
Resolves: #789530

* Tue Feb 21 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.5.21-1
- update to MySQL 5.5.21 Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-21.html

* Sun Feb 12 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.5.20-2
- sync with rawhide
- circular dep for mysql / mysql-libs to fix EL5 update
- provides mysql-client (per user request)

* Fri Feb 10 2012 Tom Lane <tgl@redhat.com> 5.5.20-2
- Revise our test-disabling method to make it possible to disable tests on a
  platform-specific basis, and also to get rid of mysql-disable-test.patch,
  which broke in just about every upstream update (Honza Horak)
- Disable cycle-counter-dependent regression tests on ARM, since there is
  not currently any support for that in Fedora ARM kernels
Resolves: #773116
- Add some comments to mysqld.service documenting how to customize it
Resolves: #785243

* Fri Jan 27 2012 Tom Lane <tgl@redhat.com> 5.5.20-1
- Update to MySQL 5.5.20, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-20.html
  as well as security fixes described at
  http://www.oracle.com/technetwork/topics/security/cpujan2012-366304.html
Resolves: #783828
- Re-include the mysqld logrotate script, now that it's not so bogus
Resolves: #547007

* Thu Jan 12 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.5.20-1
- update to MySQL 5.5.20 Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-20.html

* Sat Dec 10 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.5.19-1
- update to MySQL 5.5.19 Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-19.html
- switch to systemd on fedora >= 15 (from rawhide)

* Mon Nov 21 2011 Tom Lane <tgl@redhat.com> 5.5.18-1
- Update to MySQL 5.5.18, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-18.html
- Don't assume all ethernet devices are named ethX
Resolves: #682365

* Mon Nov 21 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.5.18-1
- update to MySQL 5.5.18 Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-18.html

* Sat Oct 22 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.5.17-1
- update to MySQL 5.5.17 Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-17.html

* Sun Oct 16 2011 Tom Lane <tgl@redhat.com> 5.5.15-1.1
- Fix unportable usage associated with va_list arguments
Resolves: #744707

* Fri Sep 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.5.16-1
- update to MySQL 5.5.16 Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-16.html

* Fri Jul 29 2011 Tom Lane <tgl@redhat.com> 5.5.15-1
- Update to MySQL 5.5.15, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-15.html

* Thu Jul 28 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.5.15-1
- update to MySQL 5.5.15 Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-15.html

* Sat Jul 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.5.14-2
- sync with rawhide

* Tue Jul 12 2011 Tom Lane <tgl@redhat.com> 5.5.14-2
- Remove make_scrambled_password and make_scrambled_password_323 from mysql.h,
  since we're not allowing clients to call those functions anyway
Related: #690346

* Mon Jul 11 2011 Tom Lane <tgl@redhat.com> 5.5.14-1
- Update to MySQL 5.5.14, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-14.html

* Wed Jul  6 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.5.14-1
- update to MySQL 5.5.14 Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-14.html

* Wed Jul  6 2011 Tom Lane <tgl@redhat.com> 5.5.13-2
- Remove erroneously-included Default-Start line from LSB init block
Resolves: #717024

* Thu Jun  2 2011 Tom Lane <tgl@redhat.com> 5.5.13-1
- Update to MySQL 5.5.13, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-13.html

* Tue May 31 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.5.13-1
- update to MySQL 5.5.13 Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-13.html

* Tue May 10 2011 Tom Lane <tgl@redhat.com> 5.5.12-1
- Update to MySQL 5.5.12, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-12.html

* Tue May 10 2011 Tom Lane <tgl@redhat.com> 5.5.10-3
- Add LSB init block to initscript, to ensure sane ordering at system boot
Resolves: #703214
- Improve initscript start action to notice when mysqladmin is failing
  because of configuration problems
Related: #703476
- Remove exclusion of "gis" regression test, since upstream bug 59908
  is fixed (for some value of "fixed") as of 5.5.10.

* Mon May 09 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.5.12-1
- update to MySQL 5.5.12 Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-12.html

* Sat Apr 30 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.5.11-1.fc15
- f15 build
- add Obsoletes for compat-mysql55

* Tue Apr 05 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.5.11-1
- update to MySQL 5.5.11 Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-11.html

* Wed Mar 23 2011 Tom Lane <tgl@redhat.com> 5.5.10-2
- Add my_make_scrambled_password to the list of symbols exported by
  libmysqlclient.so.  Needed at least by pure-ftpd.

* Mon Mar 21 2011 Tom Lane <tgl@redhat.com> 5.5.10-1
- Update to MySQL 5.5.10, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-10.html
  Note that this includes a rather belated soname version bump for
  libmysqlclient.so, from .16 to .18
- Add tmpfiles.d config file so that /var/run/mysqld is recreated at boot
  (only needed in Fedora 15 and later)
Resolves: #658938

* Tue Mar 15 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.5.10-1
- update to MySQL 5.5.10 Community Server GA
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-10.html
- provides /etc/sysconfig/mysqld
- fix default my.cnf
- client ABI bump to .18 by upstream

* Mon Feb 07 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.5.9-1
- sync with rawhide (latest patches for 5.5.8)
- update to MySQL 5.5.9 Community Server GA
- disable main.information_schema test which have strange result

* Fri Feb  4 2011 Tom Lane <tgl@redhat.com> 5.5.8-9
- Support s390/s390x in performance schema's cycle-counting functions
  (needed to make regression tests pass on these platforms)

* Thu Feb  3 2011 Tom Lane <tgl@redhat.com> 5.5.8-8
- PPC64 floating-point differences are not masked by -ffloat-store after all,
  so let's just disable gis regression test till upstream makes it less picky
Resolves: #674253
- Add __perllib_requires setting to make rpm 4.9 do what we need

* Wed Feb  2 2011 Tom Lane <tgl@redhat.com> 5.5.8-7
- Work around some portability issues on PPC64
Resolves: #674253

* Thu Jan 20 2011 Tom Lane <tgl@redhat.com> 5.5.8-6
- Remove no-longer-needed special switches in CXXFLAGS, per yesterday's
  discussion in fedora-devel about -fexceptions.
- Rebuild needed anyway to check compatibility with latest systemtap.

* Thu Jan 13 2011 Tom Lane <tgl@redhat.com> 5.5.8-5
- Fix failure to honor MYSQL_HOME environment variable
Resolves: #669364

* Thu Jan 13 2011 Tom Lane <tgl@redhat.com> 5.5.8-4
- Fix crash during startup of embedded mysqld library
Resolves: #667365

* Sat Jan 08 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.5.8-3
- sync with rawhide

* Mon Jan  3 2011 Tom Lane <tgl@redhat.com> 5.5.8-3
- my_print_help, load_defaults, free_defaults, and handle_options all turn
  out to be documented/recommended in Paul DuBois' MySQL book, so we'd better
  consider them part of the de-facto API.
Resolves: #666728

* Tue Dec 28 2010 Remi Collet <RPMS@FamilleCollet.com> - 5.5.8-2
- sync with rawhide

* Mon Dec 27 2010 Tom Lane <tgl@redhat.com> 5.5.8-2
- Add mysql_client_errors[] to the set of exported libmysqlclient symbols;
  needed by PHP.

* Thu Dec 23 2010 Tom Lane <tgl@redhat.com> 5.5.8-1
- Update to MySQL 5.5.8 (major version bump).  Note this includes removal
  of libmysqlclient_r.so.
- Add a linker version script to hide libmysqlclient functions that aren't
  part of the documented API.

* Fri Dec 17 2010 Remi Collet <RPMS@FamilleCollet.com> - 5.5.8-1
- Update to MySQL Community Server 5.5.8 GA
- move from autotools to cmake
- remove EXCEPTIONS-CLIENT (no more provided upstream)
- force soname to .161 (compat-mysql51 provides .16)

* Wed Nov 10 2010 Remi Collet <RPMS@FamilleCollet.com> - 5.5.7-1
- Update to MySQL Community Server 5.5.7 RC
- add startsos to init script (--skip-grant-tables --skip-networking)

* Fri Sep 24 2010 Remi Collet <RPMS@FamilleCollet.com> - 5.5.6-1
- Update to MySQL Community Server 5.5.6 RC

* Sat Aug 28 2010 Tom Lane <tgl@redhat.com> 5.1.50-2
- Include my_compiler.h in distribution, per upstream bug #55846.
  Otherwise PHP, for example, won't build.

* Sat Aug 28 2010 Remi Collet <RPMS@FamilleCollet.com> - 5.1.50-2
- sync with rawhide
- add patch for missing header (and notify mysql-owner)
  http://lists.mysql.com/commits/116644

* Sat Aug 28 2010 Tom Lane <tgl@redhat.com> 5.1.50-1
- Update to MySQL 5.1.50, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-50.html
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-49.html

* Fri Aug 20 2010 Remi Collet <RPMS@FamilleCollet.com> - 5.1.50-1
- Update to MySQL 5.1.50 Community Server GA
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-50.html
- add BR perl(Time::HiRes) for EL-4

* Fri Jul 23 2010 Remi Collet <RPMS@FamilleCollet.com> - 5.1.49-1
- sync with rawhide
- Update to MySQL 5.1.49 Community Server GA

* Tue Jul 13 2010 Tom Lane <tgl@redhat.com> 5.1.48-2
- Duplicate COPYING and EXCEPTIONS-CLIENT in -libs and -embedded subpackages,
  to ensure they are available when any subset of mysql RPMs are installed,
  per revised packaging guidelines
- Allow init script's STARTTIMEOUT/STOPTIMEOUT to be overridden from sysconfig
Related: #609734

* Fri Jun 25 2010 Remi Collet <RPMS@FamilleCollet.com> - 5.1.48-1.1
- fix useradd command (-N not supported everywhere)

* Mon Jun 21 2010 Tom Lane <tgl@redhat.com> 5.1.48-1
- Update to MySQL 5.1.48, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-48.html
  including a fix for CVE-2010-2008
Related: #614214

* Thu Jun 17 2010 Remi Collet <RPMS@FamilleCollet.com> - 5.1.48-1
- sync with rawhide
- Update to MySQL 5.1.48 Community Server GA

* Fri Jun  4 2010 Tom Lane <tgl@redhat.com> 5.1.47-2
- Add back "partition" storage engine
Resolves: #597390
- Fix broken "federated" storage engine plugin
Related: #587170
- Read all certificates in SSL certificate files, to support chained certs
Related: #598656

* Mon May 24 2010 Tom Lane <tgl@redhat.com> 5.1.47-1
- Update to MySQL 5.1.47, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-47.html
  including fixes for CVE-2010-1848, CVE-2010-1849, CVE-2010-1850
Resolves: #592862
Resolves: #583717
- Create mysql group explicitly in pre-server script, to ensure correct GID
Related: #594155

* Fri May 21 2010 Remi Collet <RPMS@FamilleCollet.com> - 5.1.47-1
- Update to MySQL 5.1.47 Community Server GA

* Mon Apr 26 2010 Remi Collet <RPMS@FamilleCollet.com> - 5.1.46-1.###.remi
- Update to MySQL 5.1.46 Community Server GA

* Sat Apr 24 2010 Tom Lane <tgl@redhat.com> 5.1.46-1
- Update to MySQL 5.1.46, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-46.html

* Thu Mar 25 2010 Tom Lane <tgl@redhat.com> 5.1.45-2
- Fix multiple problems described in upstream bug 52019, because regression
  tests fail on PPC if we don't.

* Thu Mar 18 2010 Remi Collet <RPMS@FamilleCollet.com> - 5.1.45-1.###.remi
- Update to MySQL 5.1.45 Community Server GA

* Fri Feb 19 2010 Remi Collet <RPMS@FamilleCollet.com> - 5.1.44-1.###.remi
- Update to MySQL 5.1.44 Community Server GA
- sync with rawhide spec (drop ndb)

* Sat Feb 13 2010 Tom Lane <tgl@redhat.com> 5.1.43-2
- Remove mysql-cluster, which is no longer supported by upstream in this
  source distribution.  If we want it we'll need a separate SRPM for it.

* Mon Feb 01 2010 Remi Collet <RPMS@FamilleCollet.com> - 5.1.43-1.###.remi
- Update to MySQL 5.1.43 Community Server GA
- sync with rawhide spec

* Thu Dec 31 2009 Remi Collet <RPMS@FamilleCollet.com> - 5.1.42-1.###.remi
- Update to MySQL 5.1.42 Community Server GA

* Thu Dec 17 2009 Tom Lane <tgl@redhat.com> 5.1.41-2
- Stop waiting during "service mysqld start" if mysqld_safe exits
Resolves: #544095

* Mon Nov 23 2009 Tom Lane <tgl@redhat.com> 5.1.41-1
- Update to MySQL 5.1.41, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-41.html
  including fixes for CVE-2009-4019
Related: #540906
- Don't set old_passwords=1; we aren't being bug-compatible with 3.23 anymore
Resolves: #540735

* Wed Nov 18 2009 Remi Collet <RPMS@FamilleCollet.com> - 5.1.41-1.###.remi
- Update to MySQL 5.1.41 Community Server GA
- no chm for this version

* Tue Nov 10 2009 Tom Lane <tgl@redhat.com> 5.1.40-1
- Update to MySQL 5.1.40, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-40.html
- Do not force the --log-error setting in mysqld init script
Resolves: #533736

* Thu Oct 22 2009 Remi Collet <RPMS@FamilleCollet.com> - 5.1.40-1.###.remi
- Update to MySQL 5.1.40 Community Server GA
- no chm for this version

* Sat Oct 17 2009 Tom Lane <tgl@redhat.com> 5.1.39-4
- Replace kluge fix for ndbd sparc crash with a real fix (mysql bug 48132)

* Thu Oct 15 2009 Tom Lane <tgl@redhat.com> 5.1.39-3
- Work around two different compiler bugs on sparc, one by backing off
  optimization from -O2 to -O1, and the other with a klugy patch
Related: #529298, #529299
- Clean up bogosity in multilib stub header support: ia64 should not be
  listed (it's not multilib), sparc and sparc64 should be

* Wed Sep 23 2009 Tom Lane <tgl@redhat.com> 5.1.39-2
- Work around upstream bug 46895 by disabling outfile_loaddata test

* Tue Sep 22 2009 Tom Lane <tgl@redhat.com> 5.1.39-1
- Update to MySQL 5.1.39, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-39.html

* Sat Sep 19 2009 Remi Collet <RPMS@FamilleCollet.com> - 5.1.39-1.###.remi
- Update to MySQL 5.1.39 Community Server GA
- no chm for this version

* Sat Sep 05 2009 Remi Collet <RPMS@FamilleCollet.com> - 5.1.38-1.###.remi
- Update to MySQL 5.1.38 Community Server GA
- snc with lastest rawhide patches

* Mon Aug 03 2009 Remi Collet <RPMS@FamilleCollet.com> - 5.1.37-1.###.remi
- Update to MySQL 5.1.37 Community Server GA

* Sun Aug  2 2009 Tom Lane <tgl@redhat.com> 5.1.37-1
- Update to MySQL 5.1.37, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-37.html

* Fri Jul 10 2009 Tom Lane <tgl@redhat.com> 5.1.36-1
- Update to MySQL 5.1.36, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-36.html

* Thu Jul 02 2009 Remi Collet <RPMS@FamilleCollet.com> - 5.1.36-1.###.remi
- Update to MySQL 5.1.36 Community Server GA

* Tue Jun 09 2009 Remi Collet <RPMS@FamilleCollet.com> - 5.1.35-2.###.remi
- split manual in subpackage
- sync with fedora init script

* Sat Jun  6 2009 Tom Lane <tgl@redhat.com> 5.1.35-1
- Update to MySQL 5.1.35, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-35.html
- Ensure that /var/lib/mysql is created with the right SELinux context
Resolves: #502966

* Sat Jun 06 2009 Remi Collet <RPMS@FamilleCollet.com> - 5.1.35-1.###.remi
- Update to MySQL 5.1.35 Community Server GA
- add manual.chm in mysql package

* Fri May 15 2009 Tom Lane <tgl@redhat.com> 5.1.34-1
- Update to MySQL 5.1.34, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-34.html
- Increase startup timeout per bug #472222

* Fri Apr 17 2009 Remi Collet <RPMS@FamilleCollet.com> - 5.1.34-1.###.remi
- Update to MySQL 5.1.34 Community Server GA

* Wed Apr 15 2009 Tom Lane <tgl@redhat.com> 5.1.33-2
- Increase stack size of ndbd threads for safety's sake.
Related: #494631

* Tue Apr  7 2009 Tom Lane <tgl@redhat.com> 5.1.33-1
- Update to MySQL 5.1.33.
- Disable use of pthread_setschedparam; doesn't work the way code expects.
Related: #477624

* Fri Apr 03 2009 Remi Collet <RPMS@FamilleCollet.com> - 5.1.33-1.###.remi
- Update to MySQL 5.1.33 Community Server GA
- add --federated option in init script

* Wed Mar  4 2009 Tom Lane <tgl@redhat.com> 5.1.32-1
- Update to MySQL 5.1.32.

* Wed Mar 04 2009 Remi Collet <RPMS@FamilleCollet.com> - 5.1.32-1.###.remi
- Update to MySQL 5.1.32 Community Server GA

* Fri Feb 27 2009 Remi Collet <RPMS@FamilleCollet.com> - 5.1.31-1.###.remi
- Update to MySQL 5.1.31 Community Server GA

* Thu Jan 22 2009 Tom Lane <tgl@redhat.com> 5.1.30-2
- hm, apparently --with-innodb and --with-ndbcluster are still needed
  even though no longer documented ...

* Thu Jan 22 2009 Tom Lane <tgl@redhat.com> 5.1.30-1
- Update to MySQL 5.1.30.  Note that this includes an ABI break for
  libmysqlclient (it's now got .so major version 16).
- This also updates mysql for new openssl build

* Sat Nov 29 2008 Remi Collet <RPMS@FamilleCollet.com> - 5.1.30-1.fc10.remi
- Update to MySQL 5.1.30 Community Server GA
- add embeded and embeded-dev sub-packages (as in rawhide)

* Sat Nov 08 2008 Remi Collet <RPMS@FamilleCollet.com> - 5.1.29-0.1.rc.fc10.remi
- Fedora 10 rebuild

* Mon Oct 27 2008 Remi Collet <RPMS@FamilleCollet.com> - 5.1.29-0.1.rc.###.remi
- Update to MySQL 5.1.28 Community Server

* Sun Sep 14 2008 Remi Collet <RPMS@FamilleCollet.com> - 5.1.28-0.1.rc.###.remi
- Update to MySQL 5.1.28 Community Server

* Sun Jun 15 2008 Remi Collet <RPMS@FamilleCollet.com> - 5.1.26-0.1.rc.###.remi
- Update to MySQL 5.1.26 Community Server

* Mon Jun 09 2008 Remi Collet <RPMS@FamilleCollet.com> - 5.1.25-0.1.rc.###.remi
- Update to MySQL 5.1.25 Community Server

* Sat Apr 19 2008 Remi Collet <RPMS@FamilleCollet.com> - 5.1.24-0.1.rc.fc8.remi
- Update to MySQL 5.1.24 Community Server

* Sun Mar 30 2008 Remi Collet <RPMS@FamilleCollet.com> - 5.1.23-0.1.rc.fc8.remi
- Update to MySQL 5.1.23a Community Server - Release Candidate Development Release
- enable maria storage engine

* Fri Feb 15 2008 Remi Collet <RPMS@FamilleCollet.com> - 5.1.23-0.rc.fc7.remi
- Update to MySQL 5.1.23 Community Server - Release Candidate Development Release

* Sat Aug 25 2007 Remi Collet <RPMS@FamilleCollet.com> - 5.1.22-0.rc.fc7.remi
- Update to MySQL 5.1.22 Community Server

* Sat Aug 25 2007 Remi Collet <RPMS@FamilleCollet.com> - 5.1.21-0.beta.fc7.remi
- Update to MySQL 5.1.21 Community Server
- switch back from Yassl to Openssl

* Tue Aug 14 2007 Remi Collet <RPMS@FamilleCollet.com> - 5.1.20-0.beta.fc7.remi
- Update to MySQL 5.1.20 Community Server
- try sub-package mysql-server-extras but not ok (plugin must be activated)

* Sat Jul 14 2007 Remi Collet <RPMS@FamilleCollet.com> - 5.0.45-1.###.remi
- Update to MySQL 5.0.45 Community Server
- add mysql-5.0.45-upgrade-test.patch

* Wed May 09 2007 Remi Collet <RPMS@FamilleCollet.com> - 5.0.41-1.###.remi
- Update to MySQL 5.0.41 Community Server

* Thu Mar 29 2007 Tom Lane <tgl@redhat.com> 5.0.37-2
- Use a less hacky method of getting default values in initscript
Related: #233771, #194596
- Improve packaging of mysql-libs per suggestions from Remi Collet
Resolves: #233731
- Update default /etc/my.cnf ([mysql.server] has been bogus for a long time)

* Tue Mar 27 2007 Remi Collet <RPMS@FamilleCollet.com> - 5.0.37-2.fc{3-6}.remi
- rebuild from rawhide (new mysql-libs sub-package)
- provide mysql/my_config_i386.h on i386.

* Mon Mar 12 2007 Tom Lane <tgl@redhat.com> 5.0.37-1
- Update to MySQL 5.0.37
Resolves: #231838
- Put client library into a separate mysql-libs RPM to reduce dependencies
Resolves: #205630

* Fri Mar  9 2007 Remi Collet <RPMS@FamilleCollet.com> - 5.0.37-1.fc{3-6}.remi
- Update to MySQL Community Server 5.0.37

* Sat Mar 03 2007 Remi Collet <RPMS@FamilleCollet.com> - 5.0.36-1.fc{3-6}.remi
- Update to MySQL 5.0.36

* Sat Feb 17 2007 Remi Collet <RPMS@FamilleCollet.com> - 5.0.33-1.fc{3-6}.remi
- rebuild from rawhide
- (re)add archive, csv, blackhole and federated "storage-engine"

* Fri Feb  9 2007 Tom Lane <tgl@redhat.com> 5.0.33-1
- Update to MySQL 5.0.33
- Install band-aid fix for "view" regression test designed to fail after 2006
- Don't chmod -R the entire database directory tree on every startup
  Related: #221085
- Fix unsafe use of install-info
  Resolves: #223713
- Cope with new automake in F7
  Resolves: #224171

* Sat Jan 20 2007 Remi Collet <RPMS@FamilleCollet.com> - 5.0.33-0.fc{3-6}.remi
- update to MySQL 5.0.33 Community Server

* Sat Nov 11 2006 Remi Collet <RPMS@FamilleCollet.com> - 5.0.27-1.fc6.remi
- x86_64 rebuild from rawhide spec.

* Thu Nov  9 2006 Tom Lane <tgl@redhat.com> 5.0.27-1
- Update to MySQL 5.0.27 (see CVE-2006-4031, CVE-2006-4226, CVE-2006-4227)
Resolves: #202247, #202675, #203427, #203428, #203432, #203434, #208641
- Fix init script to return status 1 on server start timeout
Resolves: #203910
- Move mysqldumpslow from base package to mysql-server
Resolves: #193559
- Adjust link options for BDB module
Resolves: #199368

* Sun Oct 29 2006 Remi Collet <RPMS@FamilleCollet.com> - 5.0.27-1.fc{3-6}.remi
- Update to MySQL 5.0.27

* Wed Oct 25 2006 Remi Collet <RPMS@FamilleCollet.com> - 5.0.26-1.fc6.remi
- FC6 build

* Wed Oct 11 2006 Remi Collet <RPMS@FamilleCollet.com> - 5.0.26-1.fc{3,4,5}.remi
- Update to MySQL 5.0.26
- add mysql-5.0.26-upgrade.patch (default basedir)

* Thu Sep 14 2006 Remi Collet <RPMS@FamilleCollet.com> - 5.0.24a-1.fc{3,4,5}.remi
- Update to MySQL 5.0.24a

* Sat Aug 19 2006 Remi Collet <RPMS@FamilleCollet.com> - 5.0.24-1.fc{3,4,5}.remi
- Fix bogus perl Requires for mysql-test (as in 5.0.22-2.1 from Rawhide)
- Update to MySQL 5.0.24

* Sat Jun 10 2006 Tom Lane <tgl@redhat.com> 5.0.22-2
- Work around brew's tendency not to clean up failed builds completely,
  by adding code in mysql-testing.patch to kill leftover mysql daemons.

* Thu Jun  8 2006 Tom Lane <tgl@redhat.com> 5.0.22-1
- Update to MySQL 5.0.22 (fixes CVE-2006-2753)
- Install temporary workaround for gcc bug on s390x (bz #193912)

* Thu Jun 01 2006 Remi Collet <RPMS@FamilleCollet.com> - 5.0.22-1.fc{3,4,5}.remi
- Update to MySQL 5.0.22

* Tue May  2 2006 Tom Lane <tgl@redhat.com> 5.0.21-2
- Fix bogus perl Requires for mysql-test

* Tue May 02 2006 Remi Collet <RPMS@FamilleCollet.com> - 5.0.21-1.fc{3,4,5}.remi
- rebuilt for FC3, FC4 & FC5 with news spec from FC5 "testing"
- (re)add archive, csv, blackhole and federated "storage-engine"

* Tue May  2 2006 Tom Lane <tgl@redhat.com> 5.0.21-1.FC5.1
- Update to MySQL 5.0.21
- Modify multilib header hack to not break non-RH arches, per bug #181335
- Remove logrotate script, per bug #180639.
- Add a new mysql-test RPM to carry the regression test files;
  hack up test scripts as needed to make them run in /usr/share/mysql-test.

* Thu Apr 13 2006 Remi Collet <RPMS@FamilleCollet.com> - 5.0.20-1.fc{3,4,5}.remi
- update to 5.0.20

* Wed Apr 05 2006 Remi Collet <RPMS@FamilleCollet.com> - 5.0.19-2.fc5.remi
- del example "storage-engine"
- FC5 build

* Sat Mar 11 2006 Remi Collet <RPMS@FamilleCollet.com> - 5.0.19-1.fc{3,4}.remi
- update to 5.0.19
- add mysql_upgrade to mysql-server

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.0.18-2.1
- bump again for double-long bug on ppc(64)

* Thu Feb  9 2006 Tom Lane <tgl@redhat.com> 5.0.18-2
- err-log option has been renamed to log-error, fix my.cnf and initscript

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.0.18-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan  5 2006 Remi Collet <Remi.Collet@univ-reims.fr> 5.0.18-1.fc{3,4}.remi
- rebuilt for FC3 & FC4 with news spec from rawhide
- (re)add archive, csv, example, blackhole and federated "storage-engine"

* Thu Jan  5 2006 Tom Lane <tgl@redhat.com> 5.0.18-1
- Update to MySQL 5.0.18

* Thu Dec 15 2005 Tom Lane <tgl@redhat.com> 5.0.16-4
- fix my_config.h for ppc platforms

* Thu Dec 15 2005 Tom Lane <tgl@redhat.com> 5.0.16-3
- my_config.h needs to guard against 64-bit platforms that also define the
  32-bit symbol

* Wed Dec 14 2005 Tom Lane <tgl@redhat.com> 5.0.16-2
- oops, looks like we want uname -i not uname -m

* Mon Dec 12 2005 Tom Lane <tgl@redhat.com> 5.0.16-1
- Update to MySQL 5.0.16
- Add EXCEPTIONS-CLIENT license info to the shipped documentation
- Make my_config.h architecture-independent for multilib installs;
  put the original my_config.h into my_config_$ARCH.h
- Add -fwrapv to CFLAGS so that gcc 4.1 doesn't break it

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov 26 2005 Remi Collet <Remi.Collet@univ-reims.fr> 5.0.16-0.fc4.remi
- rebuild from fedora spec in rawhide (very few differences : add "mysql-rpl_ddl.patch" del "--with-vio" )
- add archive, csv, example, blackhole and federated "storage-engine"
- see https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=173253
- Update to MySQL 5.0.16

* Mon Nov 14 2005 Tom Lane <tgl@redhat.com> 5.0.15-3
- Make stop script wait for daemon process to disappear (bz#172426)

* Wed Nov  9 2005 Tom Lane <tgl@redhat.com> 5.0.15-2
- Rebuild due to openssl library update.

* Thu Nov  3 2005 Tom Lane <tgl@redhat.com> 5.0.15-1
- Update to MySQL 5.0.15 (scratch build for now)

* Mon Oct 24 2005 Remi Collet <Remi.Collet@univ-reims.fr> 5.0.15-0.1.fc4.remi
- mysql-5.0.15 "Generally Available"

* Sat Oct 15 2005 Remi Collet <Remi.Collet@univ-reims;.fr> 5.0.13-0.2.fc4.remi
- add archive, csv, example, blackhole and federated "storage-engine"

* Sat Oct  8 2005 Remi Collet <Remi.Collet@univ-reims.fr> 5.0.13-0.1.fc4.remi
- first build of mysql 5.0.13 for Fedora

