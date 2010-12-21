Name: mysqlclient16
Version: 5.1.54
Release: 1%{dist}
Summary: MySQL shared libraries.
License: GPL
Group: Applications/Databases
URL: http://www.mysql.com

Source0: http://dev.mysql.com/get/Downloads/MySQL-5.1/mysql-%{version}%{-srctype}.tar.gz
Source5: my_config.h
Source6: ndbd.init
Source7: ndb_mgmd.init
Source8: ndb_types.h
# Working around perl dependency checking bug in rpm FTTB. Remove later.
Source999: filter-requires-mysql.sh 

Patch1: mysql-ssl-multilib.patch
Patch2: mysql-errno.patch
Patch6: mysql-stack-guard.patch
# add by a simple echo - Patch7: mysql-disable-test.patch
Patch8: mysql-setschedparam.patch
Patch10: mysql-strmov.patch
Patch12: mysql-cve-2008-7247.patch
Patch16: mysql-chain-certs.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: gperf, perl, readline-devel, openssl-devel
BuildRequires: gcc-c++, ncurses-devel, zlib-devel
BuildRequires: libtool automake autoconf
# make test requires time and ps
BuildRequires: time procps

Requires: bash

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
were created using MySQL %[version}.

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
%patch6 -p1
%patch10 -p1
%patch12 -p1
%patch16 -p1

libtoolize --force
aclocal
automake --add-missing -Wno-portability
autoconf
autoheader

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
%doc README COPYING
%{_origlibdir}/mysql/libmysqlclient*.so.*
/etc/ld.so.conf.d/*

%files devel
%defattr(-,root,root)
%{_includedir}
%{_libdir}

%changelog
* Tue Dec 21 2010 Remi Collet <RPMS@FamilleCollet.com> 5.1.54-1
- update to 5.1.54

* Fri Jan 09 2009 Remi Collet <RPMS@FamilleCollet.com> 5.1.30-1.###.remi
- first build of mysqlclient16
