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
Version: 5.6.10
Release: 1%{?dist}

Summary: MySQL client programs and shared libraries
Group: Applications/Databases
URL: http://www.mysql.com
# exceptions allow client libraries to be linked with most open source SW,
# not only GPL code.  See README.mysql-license
License: GPLv2 with exceptions

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
# ppc64 Patch5: mysql-stack-guard.patch
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
Requires: real-%{name}%{?_isa} = %{version}-%{release}
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
#patch5 -p1
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
    ppc64 | s390x | x86_64 | sparc64 )
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

  make test

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
  i386 | x86_64 | ppc | ppc64 | s390 | s390x | sparc | sparc64 )
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

%clean
rm -rf $RPM_BUILD_ROOT

%pre libs
echo -e "\nWARNING : This MySQL RPM is not an official Fedora / Red Hat build and it"
echo -e "overrides the official one. Don't file bugs on Fedora Project nor Red Hat."
echo -e "Use dedicated forums http://forums.famillecollet.com/\n"

%if %{?fedora}%{!?fedora:99} <= 15
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
* Wed Feb 13 2013 Remi Collet <RPMS@FamilleCollet.com> - 5.6.10-1
- MySQL 5.5.30 Community Server GA
- first spec from mysql-5.5.30

