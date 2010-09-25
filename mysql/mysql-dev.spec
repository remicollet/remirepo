%global postver -rc
Name: mysql
Version: 5.5.6
Release: 1%{?dist}
Summary: MySQL client programs and shared libraries
Group: Applications/Databases
URL: http://www.mysql.com
# exceptions allow client libraries to be linked with most open source SW,
# not only GPL code.
License: GPLv2 with exceptions

# Regression tests take a long time, you can skip 'em with this
%{!?runselftest:%global runselftest 1}

# Upstream has a mirror redirector for downloads, so the URL is hard to
# represent statically.  You can get the tarball by following a link from
# http://dev.mysql.com/downloads/mysql/
Source0: mysql-%{version}%{?postver}.tar.gz
# The upstream tarball includes non-free documentation that we cannot ship.
# To remove the non-free documentation, run this script after downloading
# the tarball into the current directory:
# ./generate-tarball.sh $VERSION
# Source1: generate-tarball.sh not used for remi repo
Source2: mysql.init
Source3: my-5.5.cnf
Source4: scriptstub.c
Source5: my_config.h
Source6: README.mysql-docs
Source9: mysql-embedded-check.c
# Working around perl dependency checking bug in rpm FTTB. Remove later.
Source999: filter-requires-mysql.sh

Patch1:  mysql-ssl-multilib.patch
Patch2:  mysql-5.5-errno.patch
# Patch3: mysql-stack.patch
# only for SSL, Patch4: mysql-testing.patch
Patch5:  mysql-5.5-install-test.patch
# mainly ppc, Patch6: mysql-stack-guard.patch
# test suite, Patch7: mysql-plugin-bug.patch
# selinux related, Patch8: mysql-setschedparam.patch
Patch9:  mysql-5.5-no-docs.patch
Patch10: mysql-5.5-strmov.patch
# Patch13: mysql-expired-certs.patch
Patch14: mysql-missing-string-code.patch
Patch15: mysql-lowercase-bug.patch
Patch16: mysql-chain-certs.patch
# mysql.sock path
Patch17: mysql-5.5-tests.patch
# missing rpl_reporting in embedded lib
Patch18: mysql-5.5-report.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gperf, perl, readline-devel, openssl-devel
BuildRequires: gcc-c++, ncurses-devel, zlib-devel
BuildRequires: libtool automake autoconf gawk
BuildRequires: libaio-devel
# make test requires time and ps
BuildRequires: time procps
# Socket is needed to run regression tests
BuildRequires: perl(Socket)
# DBI and DBD::mysql are needed to run regression tests
# This cause mysql BR mysql :(
BuildRequires: perl(DBD::mysql)
# This is required old EL4
BuildRequires: perl(Time::HiRes)

Requires: grep, fileutils
Requires: %{name}-libs = %{version}-%{release}
Requires: bash

# MySQL (with caps) is upstream's spelling of their own RPMs for mysql
Conflicts: MySQL
# mysql-cluster used to be built from this SRPM, but no more
Obsoletes: mysql-cluster < 5.1.44

# Working around perl dependency checking bug in rpm FTTB. Remove later.
%global __perl_requires %{SOURCE999}

%description
MySQL is a multi-user, multi-threaded SQL database server. MySQL is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. The base package
contains the standard MySQL client programs and generic MySQL files.

%package libs

Summary: The shared libraries required for MySQL clients
Group: Applications/Databases
Requires: /sbin/ldconfig
Obsoletes: mysqlclient16

%description libs
The mysql-libs package provides the essential shared libraries for any 
MySQL client program or interface. You will need to install this package
to use any other MySQL package or any clients that need to connect to a
MySQL server.

%package server

Summary: The MySQL server and related files
Group: Applications/Databases
Requires: %{name} = %{version}-%{release}
Requires: sh-utils
Requires(pre): /usr/sbin/useradd
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts
# mysqlhotcopy needs DBI/DBD support
Requires: perl-DBI, perl-DBD-MySQL
Conflicts: MySQL-server

%description server
MySQL is a multi-user, multi-threaded SQL database server. MySQL is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. This package contains
the MySQL server and some accompanying files and directories.

%package devel

Summary: Files for development of MySQL applications
Group: Applications/Databases
Requires: %{name} = %{version}-%{release}
Requires: openssl-devel
Conflicts: MySQL-devel

%description devel
MySQL is a multi-user, multi-threaded SQL database server. This
package contains the libraries and header files that are needed for
developing MySQL client applications.

%package embedded

Summary: MySQL as an embeddable library
Group: Applications/Databases

%description embedded
MySQL is a multi-user, multi-threaded SQL database server. This
package contains a version of the MySQL server that can be embedded
into a client application instead of running as a separate process.

%package embedded-devel

Summary: Development files for MySQL as an embeddable library
Group: Applications/Databases
Requires: %{name}-embedded = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description embedded-devel
MySQL is a multi-user, multi-threaded SQL database server. This
package contains files needed for developing and testing with
the embedded version of the MySQL server.

%package bench

Summary: MySQL benchmark scripts and data
Group: Applications/Databases
Requires: %{name} = %{version}-%{release}
Conflicts: MySQL-bench

%description bench
MySQL is a multi-user, multi-threaded SQL database server. This
package contains benchmark scripts and data for use when benchmarking
MySQL.

%package test

Summary: The test suite distributed with MySQL
Group: Applications/Databases
Requires: %{name} = %{version}-%{release}
Requires: %{name}-server = %{version}-%{release}
Conflicts: MySQL-test

%description test
MySQL is a multi-user, multi-threaded SQL database server. This
package contains the regression test suite distributed with
the MySQL sources.

%prep
%setup -q -n mysql-%{version}%{?postver}

%patch1 -p1
%patch2 -p1
# %patch3 -p1
# %patch4 -p1
%patch5 -p1
# %patch6 -p1
# %patch7 -p1
# %patch8 -p1
%patch9 -p1
%patch10 -p1
# %patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1

# workaround for upstream bug #56342
rm -f mysql-test/t/ssl_8k_key-master.opt

libtoolize --force
aclocal
automake --add-missing -Wno-portability
autoconf
autoheader

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
# extra C++ flags as per recommendations in mysql's INSTALL-SOURCE doc
CXXFLAGS="$CFLAGS -felide-constructors -fno-rtti -fno-exceptions"
export CFLAGS CXXFLAGS

# mysql 5.1.30 fails regression tests on x86 unless we use --with-big-tables,
# suggesting that upstream doesn't bother to test the other case ...
# note: the with-plugin and without-plugin options do actually work; ignore
# warnings from configure suggesting they are ignored ...
%configure \
	--with-readline \
	--with-ssl=/usr \
	--without-debug \
	--enable-shared \
	--with-embedded-server \
	--localstatedir=/var/lib/mysql \
	--with-unix-socket-path=/var/lib/mysql/mysql.sock \
	--with-mysqld-user="mysql" \
	--with-extra-charsets=all \
	--with-big-tables \
	--with-pic \
	--with-plugin-partition \
	--without-example-storage-engine \
	--without-plugin-daemon_example \
	--without-plugin-ftexample \
	--without-plugin-audit_null \
	--enable-local-infile \
	--enable-largefile \
	--enable-thread-safe-client \
	--with-comment="MySQL Community Server (GPL) by Remi" \
	--disable-dependency-tracking

gcc $CFLAGS $LDFLAGS -o scriptstub "-DLIBDIR=\"%{_libdir}/mysql\"" %{SOURCE4}

# Not enabling assembler

make %{?_smp_mflags}

# regular build will make libmysqld.a but not libmysqld.so :-(
mkdir libmysqld/work
cd libmysqld/work
ar -x ../libmysqld.a
# define twice ??
#rm ha_federated.o
gcc $CFLAGS $LDFLAGS -shared -Wl,-soname,libmysqld.so.0 -o libmysqld.so.0.0.1 \
	*.o \
	-lpthread -lcrypt -lnsl -lssl -lcrypto -lz -lrt -lstdc++ -lm -lc
# this is to check that we built a complete library
cp %{SOURCE9} .
ln -s libmysqld.so.0.0.1 libmysqld.so.0
gcc -I../../include $CFLAGS -laio -lstdc++ mysql-embedded-check.c libmysqld.so.0
LD_LIBRARY_PATH=. ldd ./a.out
cd ../..

make check

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

  # note: "make test" invokes two largely-duplicate sets of tests,
  # which makes the runtime really unacceptably long ...
  # if you want to change this, look at mysql-testing.patch too.
  #make test-ns
  #make force=--force  test-ns || :
  #make force=--force  test-pr || :

  # RC minimal test
  cd mysql-test
  %{__perl} ./mysql-test-run.pl \
    --ssl --mysqld=--binlog-format=mixed --suite=main
%endif

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

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

mkdir -p $RPM_BUILD_ROOT/var/log
touch $RPM_BUILD_ROOT/var/log/mysqld.log

# List the installed tree for RPM package maintenance purposes.
find $RPM_BUILD_ROOT -print | sed "s|^$RPM_BUILD_ROOT||" | sort > ROOTFILES

mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT/var/run/mysqld
install -m 0755 -d $RPM_BUILD_ROOT/var/lib/mysql
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/mysqld
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT/etc/my.cnf
mv $RPM_BUILD_ROOT/usr/sql-bench $RPM_BUILD_ROOT%{_datadir}/sql-bench
mv $RPM_BUILD_ROOT/usr/mysql-test $RPM_BUILD_ROOT%{_datadir}/mysql-test
# 5.1.32 forgets to install the mysql-test README file
install -m 0644 mysql-test/README $RPM_BUILD_ROOT%{_datadir}/mysql-test/README

mv ${RPM_BUILD_ROOT}%{_bindir}/mysqlbug ${RPM_BUILD_ROOT}%{_libdir}/mysql/mysqlbug
install -m 0755 scriptstub ${RPM_BUILD_ROOT}%{_bindir}/mysqlbug
mv ${RPM_BUILD_ROOT}%{_bindir}/mysql_config ${RPM_BUILD_ROOT}%{_libdir}/mysql/mysql_config
install -m 0755 scriptstub ${RPM_BUILD_ROOT}%{_bindir}/mysql_config

rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqld.a
install -m 0755 libmysqld/work/libmysqld.so.0.0.1 ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqld.so.0.0.1
ln -s libmysqld.so.0.0.1 ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqld.so.0
ln -s libmysqld.so.0 ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqld.so

rm -f ${RPM_BUILD_ROOT}%{_bindir}/comp_err
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/comp_err.1*
rm -f ${RPM_BUILD_ROOT}%{_bindir}/make_win_binary_distribution
rm -f ${RPM_BUILD_ROOT}%{_bindir}/make_win_src_distribution
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/make_win_bin_dist.1*
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/make_win_src_distribution.1*
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqlclient*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/plugin/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/plugin/*.a
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/binary-configure
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/make_binary_distribution
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/make_sharedlib_distribution
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/mi_test_all*
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/ndb-config-2-node.ini
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/mysql.server
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/mysqld_multi.server
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/MySQL-shared-compat.spec
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/*.plist
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/preinstall
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/postinstall
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/mysql-*.spec
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/mysql-log-rotate
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/ChangeLog
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/mysql-stress-test.pl.1*
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/mysql-test-run.pl.1*

mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo "%{_libdir}/mysql" > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{_arch}.conf

# copy additional docs into build tree so %%doc will find them
cp %{SOURCE6} README.mysql-docs

%clean
rm -rf $RPM_BUILD_ROOT

%pre libs
echo -e "\nWARNING : This MySQL RPM is not an official Fedora/Redhat build and it"
echo -e "overrides the official one. Don't file bugs on Fedora Project nor Redhat."
echo -e "Use dedicated forums http://forums.famillecollet.com/\n"

%if %{?fedora}%{!?fedora:99} <= 11
echo -e "WARNING : Fedora %{fedora} is now EOL :"
echo -e "You should consider upgrading to a supported release.\n"
%endif


%pre server
/usr/sbin/groupadd -g 27 -o -r mysql >/dev/null 2>&1 || :
# -N options used on Fedora not available on EL and fedora <= 8 and EL <= 5
/usr/sbin/useradd -M -g mysql -o -r -d /var/lib/mysql -s /bin/bash \
	-c "MySQL Server" -u 27 mysql >/dev/null 2>&1 || :

%post libs
/sbin/ldconfig

%post server
if [ $1 = 1 ]; then
    /sbin/chkconfig --add mysqld
fi
/bin/chmod 0755 /var/lib/mysql
/bin/touch /var/log/mysqld.log

%preun server
if [ $1 = 0 ]; then
    /sbin/service mysqld stop >/dev/null 2>&1
    /sbin/chkconfig --del mysqld
fi

%postun libs
if [ $1 = 0 ] ; then
    /sbin/ldconfig
fi

%postun server
if [ $1 -ge 1 ]; then
    /sbin/service mysqld condrestart >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root)
%doc README COPYING EXCEPTIONS-CLIENT
%doc README.mysql-docs

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

%{_libdir}/mysql/mysqlbug
%{_libdir}/mysql/mysql_config

%files libs
%defattr(-,root,root)
%doc COPYING EXCEPTIONS-CLIENT
# although the default my.cnf contains only server settings, we put it in the
# libs package because it can be used for client settings too.
%config(noreplace) /etc/my.cnf
%dir %{_libdir}/mysql
%{_libdir}/mysql/libmysqlclient*.so.*
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
#%{_bindir}/mysql_fix_privilege_tables
%{_bindir}/mysql_install_db
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
#/usr/libexec/mysqlmanager

%{_libdir}/mysql/plugin

%{_mandir}/man1/msql2mysql.1*
%{_mandir}/man1/myisamchk.1*
%{_mandir}/man1/myisamlog.1*
%{_mandir}/man1/myisampack.1*
%{_mandir}/man1/mysql_convert_table_format.1*
%{_mandir}/man1/myisam_ftdump.1*
%{_mandir}/man1/mysql.server.1*
%{_mandir}/man1/mysql_fix_extensions.1*
#%{_mandir}/man1/mysql_fix_privilege_tables.1*
%{_mandir}/man1/mysql_install_db.1*
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
#%{_mandir}/man8/mysqlmanager.8*

%{_datadir}/mysql/errmsg-utf8.txt
%{_datadir}/mysql/fill_help_tables.sql
%{_datadir}/mysql/mysql_fix_privilege_tables.sql
%{_datadir}/mysql/mysql_system_tables.sql
%{_datadir}/mysql/mysql_system_tables_data.sql
%{_datadir}/mysql/mysql_test_data_timezone.sql
%{_datadir}/mysql/my-*.cnf
%{_datadir}/mysql/config.*.ini

/etc/rc.d/init.d/mysqld
%attr(0755,mysql,mysql) %dir /var/run/mysqld
%attr(0755,mysql,mysql) %dir /var/lib/mysql
%attr(0640,mysql,mysql) %config(noreplace) %verify(not md5 size mtime) /var/log/mysqld.log

%files devel
%defattr(-,root,root)
/usr/include/mysql
/usr/share/aclocal/mysql.m4
%{_libdir}/mysql/libmysqlclient*.so

%files embedded
%defattr(-,root,root)
%doc COPYING EXCEPTIONS-CLIENT
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
%attr(-,mysql,mysql) %{_datadir}/mysql-test

%{_mandir}/man1/mysql_client_test.1*

%changelog
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

* Fri Feb 29 2009 Remi Collet <RPMS@FamilleCollet.com> - 5.1.31-1.###.remi
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

* Sun Jun 13 2008 Remi Collet <RPMS@FamilleCollet.com> - 5.1.26-0.1.rc.###.remi
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

* Sun Nov 11 2006 Remi Collet <RPMS@FamilleCollet.com> - 5.0.27-1.fc6.remi
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

