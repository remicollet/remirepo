Name: compat-mysql51
Version: 5.1.73
Release: 1%{dist}
Summary: MySQL shared libraries.
License: GPL
Group: Applications/Databases
URL: http://www.mysql.com

# Upstream has a mirror redirector for downloads, so the URL is hard to
# represent statically.  You can get the tarball by following a link from
# http://dev.mysql.com/downloads/mysql/
Source0: mysql-%{version}-nodocs.tar.gz
# The upstream tarball includes non-free documentation that we cannot ship.
# To remove the non-free documentation, run this script after downloading
# the tarball into the current directory:
# ./generate-tarball.sh $VERSION
Source1: generate-tarball.sh
Source5: my_config.h
Source6: README.mysql-docs
Source7: README.mysql-license
# Working around perl dependency checking bug in rpm FTTB. Remove later.
Source999: filter-requires-mysql.sh 

Patch1: mysql-ssl-multilib.patch
Patch2: mysql-errno.patch
# Patch3: mysql-stack.patch
Patch4: mysql-testing.patch
Patch5: mysql-install-test.patch
Patch6: mysql-stack-guard.patch
Patch7: mysql-disable-test.patch
Patch8: mysql-setschedparam.patch
Patch9: mysql-no-docs.patch
Patch10: mysql-strmov.patch
Patch12: mysql-cve-2008-7247.patch
Patch13: mysql-expired-certs.patch
Patch16: mysql-chain-certs.patch
Patch17: mysql-cve-2012-5611.patch
Patch18: mysql-dump-log-tables.patch
Patch19: mysql-logrotate.patch
Patch20: mysql-rhbz1059545.patch
Patch21: mysql-dh1024.patch
Patch22: mysql-openssl-test.patch
Patch23: mysql-test-events_1.patch
Patch24: mysql-tls.patch
Patch25: mysql-relay-logging.patch
Patch26: mysql-cve-2016-6663.patch
Patch27: mysql-cve-2016-6662-b-1ebbc61e.patch
Patch28: mysql-cve-2016-6662-c-2135853b.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: gperf, perl, readline-devel, openssl-devel
BuildRequires: gcc-c++, ncurses-devel, zlib-devel
BuildRequires: libtool automake autoconf
# make test requires time and ps
BuildRequires: time procps
Requires: bash

Obsoletes: mysqlclient16 < %{version}
Provides: mysqlclient16 = %{version}

# Working around perl dependency checking bug in rpm FTTB. Remove later.
%define __perl_requires %{SOURCE999}

# Force include and library files into a nonstandard place
%{expand: %%define _origincludedir %{_includedir}}
%{expand: %%define _origlibdir %{_libdir}}
%define _includedir %{_origincludedir}/mysql51
%define _libdir %{_origlibdir}/mysql51

%description
This package contains backlevel versions of the MySQL client libraries
for use with applications linked against them.  These shared libraries
were created using MySQL %{version}.

%package devel

Summary: Files for development of MySQL applications.
License: GPL
Group: Applications/Databases
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the libraries and header files that are needed for
developing MySQL applications using client libraries.

%prep
%setup -q -n mysql-%{version}

%patch1 -p1
%patch2 -p1
# %%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch12 -p1
%patch13 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1

libtoolize --force
aclocal
automake --add-missing -Wno-portability
autoconf
autoheader

cp %{SOURCE6} README.mysql-docs
cp %{SOURCE7} README.mysql-license


%build
CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
CFLAGS="$CFLAGS -fno-strict-aliasing -fwrapv"
%ifarch alpha
# Can't link C++ objects into an executable without this. Odd!
# -ECL 2002-12-19
CFLAGS="$CFLAGS -fPIC"
%endif
CXXFLAGS="$CFLAGS -fno-rtti -fno-exceptions"
export CFLAGS CXXFLAGS

%configure \
	--with-readline \
	--with-ssl \
	--without-debug \
	--enable-shared \
	--without-bench \
	--without-server \
	--without-docs \
	--without-man \
	--localstatedir=/var/lib/mysql \
	--with-unix-socket-path=/var/lib/mysql/mysql.sock \
	--with-mysqld-user="mysql" \
	--with-extra-charsets=all \
	--without-plugin-archive \
	--without-plugin-blackhole \
	--without-plugin-example \
	--without-plugin-federated \
	--without-plugin-innobase \
	--enable-local-infile \
	--enable-largefile \
	--enable-thread-safe-client \
	--disable-dependency-tracking \
	--with-named-thread-libs="-lpthread"

make %{?_smp_mflags}
make check

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

install -m 644 include/my_config.h $RPM_BUILD_ROOT%{_includedir}/mysql/my_config_`uname -i`.h
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_includedir}/mysql/

# We want the .so files both in regular _libdir (for execution) and
# in special _libdir/mysql4 directory (for convenient building of clients).
# The ones in the latter directory should be just symlinks though.
mkdir -p ${RPM_BUILD_ROOT}%{_origlibdir}/mysql
pushd ${RPM_BUILD_ROOT}%{_origlibdir}/mysql
mv -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqlclient.so.16.*.* .
mv -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqlclient_r.so.16.*.* .
cp -p -d ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqlclient*.so.* .
popd
pushd ${RPM_BUILD_ROOT}%{_libdir}/mysql
ln -s ../../mysql/libmysqlclient.so.16.*.* .
ln -s ../../mysql/libmysqlclient_r.so.16.*.* .
popd

# Put the config script into special libdir
cp -p $RPM_BUILD_ROOT%{_bindir}/mysql_config ${RPM_BUILD_ROOT}%{_libdir}/mysql

rm -rf $RPM_BUILD_ROOT%{_prefix}/mysql-test
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/mysql
rm -rf $RPM_BUILD_ROOT%{_bindir}
rm -rf $RPM_BUILD_ROOT%{_libexecdir}
rm -rf $RPM_BUILD_ROOT%{_infodir}/*
rm -rf $RPM_BUILD_ROOT%{_mandir}/man?/*
rm -rf $RPM_BUILD_ROOT%{_prefix}/sql-bench
rm -rf $RPM_BUILD_ROOT%{_datadir}/aclocal/mysql.m4



mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo "%{_origlibdir}/mysql" > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{_arch}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README COPYING README.mysql-license
%doc README.mysql-docs
%{_origlibdir}/mysql/libmysqlclient*.so.*
/etc/ld.so.conf.d/*

%files devel
%defattr(-,root,root)
%{_includedir}
%{_libdir}

%changelog
* Sat Feb 11 2017 Remi Collet <remi@remirepo.net> 5.1.73-1
- update to 5.1.73
- sync patch with mysql-5.1.73-8.el6_8

* Tue Dec 21 2010 Remi Collet <RPMS@FamilleCollet.com> 5.1.54-1
- update to 5.1.54

* Fri Jan 09 2009 Remi Collet <RPMS@FamilleCollet.com> 5.1.30-1.###.remi
- first build of mysqlclient16
