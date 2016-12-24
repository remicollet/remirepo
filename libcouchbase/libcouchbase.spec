# remirepo spec file for libcouchbase
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

# Tests require some need which are downloaded during make
%global with_tests  0%{?_with_tests:1}

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 6
%global with_dtrace 1
%else
%global with_dtrace 0
%endif

Name:          libcouchbase
Version:       2.7.0
Release:       1%{?dist}
Summary:       Couchbase client library
Group:         System Environment/Libraries
License:       ASL 2.0
URL:           http://www.couchbase.com/communities/c/getting-started
Source0:       http://packages.couchbase.com/clients/c/%{name}-%{version}.tar.gz

BuildRequires: libtool
BuildRequires: openssl-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: cmake >= 2.8.9
%if "%{?vendor}" == "Remi Collet"
# ensure we use latest version (libevent-last)
BuildRequires: libevent-devel >= 2.0.20
%else
BuildRequires: libevent-devel >= 1.4
%endif
BuildRequires: libev-devel >= 3
%if %{with_dtrace}
BuildRequires: systemtap-sdt-devel >= 1.8
%endif


%description
The C library provides fast access to documents in Couchbase Server 2.0.
With JSON documents and Couchbase server 2.0 you have new ways to index
and query data stored in the cluster through views. This client library,
libcouchbase, also simplifies requests to Views through its handling of
HTTP transport.

This Couchbase Client Library for C and C++ provides a complete interface
to the functionality of Couchbase Server.


%package       devel
Summary:       Development files for Couchbase client library
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package       tools
Summary:       Couchbase tools
Group:         Applications/System
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description tools
The %{name}-tools package contains some command line tools to manage
a Couchbase Server.


%prep
%setup -q


%build
%cmake \
  -DLCB_NO_TESTS=1 \
  -DLCB_BUILD_LIBUV=OFF

make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}

# Remove uneeded files
rm -f %{buildroot}%{_libdir}/*.la


%check
%if %{with_tests}
make check
%else
: check disabled, missing '--with tests' option
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/%{name}.so.2*
# Backends
%{_libdir}/%{name}_libevent.so
%{_libdir}/%{name}_libev.so

%files devel
%doc RELEASE_NOTES.markdown
%{_includedir}/%{name}
#{_mandir}/man3/libcouch*
#{_mandir}/man3/lcb*
#{_mandir}/man5/lcb*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files tools
%{_bindir}/cbc*
%{_mandir}/man1/cbc*
%{_mandir}/man4/cbc*


%changelog
* Sat Dec 24 2016 Remi Collet <remi@feoraproject.org> - 2.7.0-1
- update to 2.7.0

* Tue Nov 29 2016 Remi Collet <remi@feoraproject.org> - 2.6.4-1
- update to 2.6.4

* Wed Sep 28 2016 Remi Collet <remi@feoraproject.org> - 2.6.3-1
- update to 2.6.3

* Thu Jul 28 2016 Remi Collet <remi@feoraproject.org> - 2.6.2-1
- update to 2.6.2

* Fri Jun 24 2016 Remi Collet <remi@feoraproject.org> - 2.6.1-1
- update to 2.6.1

* Thu May 26 2016 Remi Collet <remi@feoraproject.org> - 2.6.0-1
- update to 2.6.0

* Wed Apr 20 2016 Remi Collet <remi@feoraproject.org> - 2.5.8-1
- update to 2.5.8

* Thu Nov  5 2015 Remi Collet <remi@feoraproject.org> - 2.5.3-1
- update to 2.5.3

* Wed Apr 22 2015 Remi Collet <remi@feoraproject.org> - 2.4.9-1
- update to 2.4.9
- switch to cmake

* Wed Nov  5 2014 Remi Collet <remi@feoraproject.org> - 2.4.3-1
- update to 2.4.3

* Sat Sep 20 2014 Remi Collet <remi@feoraproject.org> - 2.4.1-1
- update to 2.4.1

* Mon May 12 2014 Remi Collet <remi@feoraproject.org> - 2.3.1-1
- update to 2.3.1
- always use libevent 2

* Sat Oct  5 2013 Remi Collet <remi@feoraproject.org> - 2.1.3-1
- update to 2.1.3

* Sun Apr 14 2013 Remi Collet <remi@feoraproject.org> - 2.0.5-1
- Initial package
