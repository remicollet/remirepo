Name:      libmemcached
Summary:   Client library and command line tools for memcached server
Version:   0.46
Release:   1%{?dist}.1
License:   BSD
Group:     System Environment/Libraries
URL:       http://libmemcached.org/
# Original sources:
#   http://launchpad.net/libmemcached/1.0/%{version}/+download/libmemcached-%{version}.tar.gz
# The source tarball must be repackaged to remove the Hsieh hash
# code, since the license is non-free.  When upgrading, download the new
# source tarball, and run "./strip-hsieh.sh <version>" to produce the
# "-exhsieh" tarball.
Source0:   libmemcached-%{version}-exhsieh.tar.gz

# Add -lsasl2 to libmemcached.pc
# See http://lists.libmemcached.org/pipermail/libmemcached-discuss/2010-October/002207.html
Patch0:    libmemcached-sasl.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cyrus-sasl-devel
%if 0%{?fedora} >= 12
BuildRequires: systemtap-sdt-devel
%endif
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
BuildRequires: libevent-devel
%endif


%description
libmemcached is a C client library to the memcached server
(http://danga.com/memcached). It has been designed to be light on memory
usage, and provide full access to server side methods.

It also implements several command line tools:

memcat - Copy the value of a key to standard output.
memflush - Flush the contents of your servers.
memrm - Remove a key(s) from the server.
memstat - Dump the stats of your servers to standard output.
memslap - Generate testing loads on a memcached cluster.
memcp - Copy files to memcached servers.
memerror - Creates human readable messages from libmemcached error codes.


%package devel
Summary: Header files and development libraries for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: cyrus-sasl-devel%{?_isa}

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, 
you will need to install %{name}-devel.


%prep
%setup -q

%patch0 -p1 -b .sasl

%{__mkdir} examples
%{__cp} -p tests/*.{c,cpp,h} examples/


%build
# option --with-memcached=false to disable server binary check (as we don't run test)
%configure --with-memcached=false
%{__make} %{_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install  DESTDIR="%{buildroot}" AM_INSTALL_PROGRAM_FLAGS=""


%check
# For documentation only:
# test suite cannot run in mock (same port use for memcache servers on all arch)
# All tests completed successfully
# diff output.res output.cmp fails but result depend on server version
#%{__make} test


%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig
 

%files
%defattr (-,root,root,-) 
%doc AUTHORS COPYING README THANKS TODO ChangeLog
%{_bindir}/mem*
%exclude %{_libdir}/libmemcached.la
%exclude %{_libdir}/libmemcachedprotocol.la
%exclude %{_libdir}/libmemcachedutil.la
%exclude %{_libdir}/libhashkit.la
%{_libdir}/libhashkit.so.0*
%{_libdir}/libmemcached.so.6*
%{_libdir}/libmemcachedprotocol.so.0*
%{_libdir}/libmemcachedutil.so.1*
%{_mandir}/man1/mem*


%files devel
%defattr (-,root,root,-) 
%doc examples
%{_includedir}/libmemcached
%{_includedir}/libhashkit
%{_libdir}/libhashkit.so
%{_libdir}/libmemcached.so
%{_libdir}/libmemcachedprotocol.so
%{_libdir}/libmemcachedutil.so
%{_libdir}/pkgconfig/libmemcached.pc
%{_mandir}/man3/libmemcached*
%{_mandir}/man3/memcached_*
%{_mandir}/man3/hashkit*


%changelog
* Sat Feb 19 2011 Remi Collet <Fedora@famillecollet.com> - 0.46-1.1
- update sasl.patch to avoid need of autoconf
- rebuild for remi repo with SASL for fedora <= 10 and EL <= 5

* Fri Feb 18 2011 Remi Collet <Fedora@famillecollet.com> - 0.46-1
- rebuild for remi repo without SASL for fedora <= 10 and EL <= 5

* Fri Feb 18 2011 Remi Collet <Fedora@famillecollet.com> - 0.46-1
- update to 0.46

* Sat Feb 12 2011 Remi Collet <Fedora@famillecollet.com> - 0.44-6
- arch specific requires

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 24 2010 Joe Orton <jorton@redhat.com> - 0.44-4
- repackage source tarball to remove non-free Hsieh hash code

* Sat Oct 02 2010 Remi Collet <Fedora@famillecollet.com> - 0.44-3
- improves SASL patch

* Sat Oct 02 2010 Remi Collet <Fedora@famillecollet.com> - 0.44-2
- enable SASL support

* Fri Oct 01 2010 Remi Collet <Fedora@famillecollet.com> - 0.44-1
- update to 0.44
- add soname version in %%file to detect change

* Fri Jul 30 2010 Remi Collet <Fedora@famillecollet.com> - 0.43-1
- update to 0.43

* Wed Jul 07 2010 Remi Collet <Fedora@famillecollet.com> - 0.42-1
- update to 0.42

* Tue May 04 2010 Remi Collet <Fedora@famillecollet.com> - 0.40-1
- update to 0.40 (new soname for libmemcached.so.5)
- new URI (site + source)

* Sat Mar 13 2010 Remi Collet <Fedora@famillecollet.com> - 0.38-1
- update to 0.38

* Sat Feb 06 2010 Remi Collet <Fedora@famillecollet.com> - 0.37-1
- update to 0.37 (soname bump)
- new libhashkit (should be a separated project in the futur)

* Sun Sep 13 2009 Remi Collet <Fedora@famillecollet.com> - 0.31-1
- update to 0.31

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 14 2009 Remi Collet <Fedora@famillecollet.com> - 0.30-1
- update to 0.30

* Tue May 19 2009 Remi Collet <Fedora@famillecollet.com> - 0.29-1
- update to 0.29

* Fri May 01 2009 Remi Collet <Fedora@famillecollet.com> - 0.28-2
- add upstream patch to disable nonfree hsieh hash method

* Sat Apr 25 2009 Remi Collet <Fedora@famillecollet.com> - 0.28-1
- Initial RPM from Brian Aker spec
- create -devel subpackage
- add %%post %%postun %%check section

