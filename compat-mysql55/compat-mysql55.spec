Name: compat-mysql55
Version: 5.5.11
Release: 1%{?dist}
Summary: MySQL shared libraries
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
Source5: my_config.h
Source6: README.mysql-docs
Source7: README.mysql-license
Source8: libmysql.version

Patch1: mysql-errno.patch
Patch2: mysql-strmov.patch
Patch3: mysql-install-test.patch
Patch4: mysql-expired-certs.patch
Patch5: mysql-stack-guard.patch
Patch6: mysql-chain-certs.patch
Patch7: mysql-versioning.patch
Patch8: mysql-dubious-exports.patch
# Patch9: mysql-disable-test.patch
Patch10: mysql-embedded-crash.patch
Patch11: mysql-home.patch
Patch12: mysql-plugin-bool.patch
Patch13: mysql-s390-tsc.patch

# RC patch for backports
Patch21: mysql-readline.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gperf, perl, readline-devel, openssl-devel
BuildRequires: gcc-c++, cmake, ncurses-devel, zlib-devel, libaio-devel
%if 0%{?fedora} >= 12
BuildRequires: systemtap-sdt-devel >= 1.3
%endif
# This is required old EL4
BuildRequires: bison


%description
This package contains backlevel versions of the MySQL client libraries
for use with applications linked against them.  These shared libraries
were created using MySQL %{version}.

%package devel

Summary: Files for development of MySQL applications
Group: Applications/Databases
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: openssl-devel%{?_isa}
Conflicts: MySQL-devel

%description devel
This package contains the libraries and header files that are needed for
developing MySQL applications using client libraries.

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
# %patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
# Backports specific patches
%patch21 -p1 -b .readline

# upstream has fallen down badly on symbol versioning, do it ourselves
cp %{SOURCE8} libmysql/libmysql.version


%build
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
	-DWITHOUT_SERVER=ON \
	-DCMAKE_INSTALL_PREFIX="%{_prefix}" \
	-DINSTALL_INCLUDEDIR=include/mysql \
	-DINSTALL_INFODIR=share/info \
	-DINSTALL_LIBDIR="%{_lib}/mysql" \
	-DINSTALL_MANDIR=share/man \
	-DINSTALL_MYSQLSHAREDIR=share/mysql \
	-DINSTALL_SBINDIR=libexec \
	-DINSTALL_SUPPORTFILESDIR=share/mysql \
	-DMYSQL_UNIX_ADDR="/var/lib/mysql/mysql.sock" \
	-DENABLED_LOCAL_INFILE=ON \
%if 0%{?fedora} >= 12
	-DENABLE_DTRACE=ON \
%endif
	-DWITH_EMBEDDED_SERVER=ON \
	-DWITH_READLINE=ON \
%if 0%{?fedora} >= 9 || 0%{?rhel} >= 5
	-DWITH_SSL=system \
%else
	-DWITH_SSL=bundled \
%endif
	-DWITH_ZLIB=system

make %{?_smp_mflags} VERBOSE=1


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

# libmysqlclient_r is no more.  Upstream tries to replace it with symlinks
# but that really doesn't work (wrong soname in particular).  We'll keep
# just the devel libmysqlclient_r.so link, so that rebuilding without any
# source change is enough to get rid of dependency on libmysqlclient_r.
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqlclient_r.so*
ln -s libmysqlclient.so ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqlclient_r.so

mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo "%{_libdir}/mysql" > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{_arch}.conf

# copy additional docs into build tree so %%doc will find them
cp %{SOURCE6} README.mysql-docs
cp %{SOURCE7} README.mysql-license

# Clean not wanted files
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/*.a
rm -f ${RPM_BUILD_ROOT}%{_bindir}/innochecksum
rm -f ${RPM_BUILD_ROOT}%{_bindir}/my_print_defaults
rm -f ${RPM_BUILD_ROOT}%{_bindir}/mysql_waitpid
rm -f ${RPM_BUILD_ROOT}%{_bindir}/perror
rm -f ${RPM_BUILD_ROOT}%{_bindir}/replace
rm -f ${RPM_BUILD_ROOT}%{_bindir}/resolveip
rm -f ${RPM_BUILD_ROOT}%{_bindir}/resolve_stack_dump


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc README COPYING README.mysql-license
%doc README.mysql-docs
%dir %{_libdir}/mysql
%{_libdir}/mysql/libmysqlclient.so.18*
/etc/ld.so.conf.d/*

%files devel
%defattr(-,root,root)
%{_includedir}/mysql
%{_libdir}/mysql/libmysqlclient.so
%{_libdir}/mysql/libmysqlclient_r.so


%changelog
* Fri Apr 15 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.5.11-1
- first RPM

