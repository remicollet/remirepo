# remirepo spec file for libevent-last
# renamed for parallel installation, from:
#
# Fedora spec file for libevent
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%{?scl:             %scl_package         %{libname}}

%if 0%{?fedora} && 0%{?fedora} >= 20
%global develdocdir %{_docdir}/%{name}-devel
%else
%global develdocdir %{_docdir}/%{name}-devel-%{version}
%endif

%global libname     libevent

# Regression tests take a long time, you can skip 'em with this
%if %{?runselftest}%{!?runselftest:1}
%global with_tests  %{?_without_tests:0}%{!?_without_tests:1}
%else
%global with_tests  %{?_with_tests:1}%{!?_with_tests:0}
%endif

%global with_doc    1

# libevent >= 2.0.9 have soname .5
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
# Standard build
Name:           %{libname}
%global with_conflicts 0

%else
# Build for parallel install - SCL
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
Name:           %{sub_prefix}%{libname}
%global with_conflicts 0

%else
# Build for parallel install - last
Name:           %{libname}-last
%global with_conflicts 1
%endif
%endif

Version:        2.0.22
Release:        2%{?dist}
Summary:        Abstract asynchronous event notification library

Group:          System Environment/Libraries
License:        BSD
URL:            http://sourceforge.net/projects/levent/
Source0:        http://downloads.sourceforge.net/levent/%{libname}-%{version}-stable.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  openssl-devel
%if %{with_doc}
BuildRequires:  doxygen
%endif

Patch00: libevent-2.0.10-stable-configure.patch
# Disable network tests
Patch01: libevent-nonettests.patch

%if 0%{?scl:1}
# Filter in the SCL collection
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so}
%{?filter_requires_in: %filter_requires_in %{_libdir}/.*\.so}
%{?filter_setup}
Requires:  %{scl}-runtime
Requires:  openssl%{?_isa}
%endif


%description
The libevent API provides a mechanism to execute a callback function
when a specific event occurs on a file descriptor or after a timeout
has been reached. libevent is meant to replace the asynchronous event
loop found in event driven network servers. An application just needs
to call event_dispatch() and can then add or remove events dynamically
without having to change the event loop.


%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%if %{with_conflicts}
%{!?scl:Conflicts: %{libname}-devel < %{version}}
%{!?scl:Provides:  %{libname}-devel = %{version}}
%endif

%description devel
This package contains the header files and libraries for developing
with %{name}.


%if %{with_doc}
%package doc
Summary: Development documentation for %{name}
Group: Documentation
%if 0%{?rhel} != 5
BuildArch: noarch
%endif
%if %{with_conflicts}
%{!?scl:Conflicts: %{libname}-doc < %{version}}
%{!?scl:Provides:  %{libname}-doc = %{version}}
%endif

%description doc
This package contains the development documentation for %{name}.
%endif


%prep
%setup -q -n  %{libname}-%{version}-stable

# 477685 -  libevent-devel multilib conflict
#patch00 -p1
%patch01 -p1 -b .nonettests


%build
%configure \
    --disable-dependency-tracking \
    --disable-static
make %{?_smp_mflags} all

%if %{with_doc}
# Create the docs
make doxygen
%endif


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%if %{with_doc}
mkdir -p $RPM_BUILD_ROOT/%{develdocdir}/html
(cd doxygen/html; \
	install -p -m 644 *.* $RPM_BUILD_ROOT/%{develdocdir}/html)

mkdir -p $RPM_BUILD_ROOT/%{develdocdir}/sample
(cd sample; \
	install -p -m 644 *.c Makefile* $RPM_BUILD_ROOT/%{develdocdir}/sample)
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%check
%if %{with_tests}
make check
%endif


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE README
%{_libdir}/libevent-*.so.*
%{_libdir}/libevent_core-*.so.*
%{_libdir}/libevent_extra-*.so.*
%{_libdir}/libevent_openssl-*.so.*
%{_libdir}/libevent_pthreads-*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/event.h
%{_includedir}/evdns.h
%{_includedir}/evhttp.h
%{_includedir}/evrpc.h
%{_includedir}/evutil.h
%dir %{_includedir}/event2
%{_includedir}/event2/*.h
%{_libdir}/libevent.so
%{_libdir}/libevent_core.so
%{_libdir}/libevent_extra.so
%{_libdir}/libevent_openssl.so
%{_libdir}/libevent_pthreads.so
%{_libdir}/pkgconfig/libevent.pc
%{_libdir}/pkgconfig/libevent_openssl.pc
%{_libdir}/pkgconfig/libevent_pthreads.pc
%{_bindir}/event_rpcgen.*

%if %{with_doc}
%files doc
%defattr(-,root,root,-)
%{develdocdir}/
%endif


%changelog
* Fri Jun 19 2015 Remi Collet <remi@fedoraproject.org> - 2.0.22-2
- allow build against rh-php56 (as more-php56)

* Wed Apr 15 2015 Remi Collet <remi@fedoraproject.org> - 2.0.22-1
- Update to 2.0.22

* Sat May 10 2014 Remi Collet <remi@fedoraproject.org> - 2.0.21-4
- merge changes from rawhide:
  - Add missing directory /usr/include/event2
  - Correct summary and description of -devel and -doc packages
- re-add doc sub-package

* Tue Mar 25 2014 Remi Collet <remi@fedoraproject.org> - 2.0.21-3
- improve SCL build

* Sun Mar 23 2014 Remi Collet <remi@fedoraproject.org> - 2.0.21-2
- allow SCL build

* Tue Nov 12 2013 Remi Collet <remi@fedoraproject.org> - 2.0.21-1
- backport 2.0.21 for remi repo

* Thu Jul 25 2013 Remi Collet <remi@fedoraproject.org> - 2.0.18-3
- rename to libevent-last
- drop -doc sub-package

* Thu May  2 2013 Orion Poplawski <orion@cora.nwra.com> - 2.0.21-1
- Update to 2.0.21
- Add %%check

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr  4 2012 Steve Dickson <steved@redhat.com> 2.0.18-1
- Updated to latest stable upstream version: 2.0.18-stable
- Moved documentation into its own rpm (bz 810138)

* Mon Mar 12 2012 Steve Dickson <steved@redhat.com> 2.0.17-1
- Updated to latest stable upstream version: 2.0.17-stable

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 10 2011 Steve Dickson <steved@redhat.com> 2.0.14-1
- Updated to latest stable upstream version: 2.0.14-stable (bz 727129)
- Removed the installion of the outdate man pages and the latex raw docs.
- Corrected where the other doc are installed.

* Wed Aug 10 2011 Steve Dickson <steved@redhat.com> 2.0.13-1
- Updated to latest stable upstream version: 2.0.13-stable (bz 727129)

* Tue Aug  2 2011 Steve Dickson <steved@redhat.com> 2.0.12-1
- Updated to latest stable upstream version: 2.0.12-stable

* Wed Feb 09 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 2.0.10-2
- Fix build
- Update spec to match current guidelines
- drop no longer needed patch

* Tue Feb  8 2011 Steve Dickson <steved@redhat.com> 2.0.10-1
- Updated to latest stable upstream version: 2.0.10-stable

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.14b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 22 2010 Steve Dickson <steved@redhat.com> 1.4.14b-1
- Updated to latest stable upstream version: 1.4.14b

* Fri May 21 2010 Tom "spot" Callaway <tcallawa@redhat.com> 1.4.13-2
- disable static libs (bz 556067)

* Tue Dec 15 2009 Steve Dickson <steved@redhat.com> 1.4.13-1
- Updated to latest stable upstream version: 1.4.13

* Tue Aug 18 2009 Steve Dickson <steved@redhat.com> 1.4.12-1
- Updated to latest stable upstream version: 1.4.12
- API documentation is now installed (bz 487977)
- libevent-devel multilib conflict (bz 477685)
- epoll backend allocates too much memory (bz 517918)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 20 2009 Steve Dickson <steved@redhat.com> 1.4.10-1
- Updated to latest stable upstream version: 1.4.10

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul  1 2008 Steve Dickson <steved@redhat.com> 1.4.5-1
- Updated to latest stable upstream version 1.4.5-stable

* Mon Jun  2 2008 Steve Dickson <steved@redhat.com> 1.4.4-1
- Updated to latest stable upstream version 1.4.4-stable

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3e-2
- Autorebuild for GCC 4.3

* Tue Jan 22 2008 Steve Dickson <steved@redhat.com> 1.3e-1
- Updated to latest stable upstream version 1.3e

* Fri Mar  9 2007 Steve Dickson <steved@redhat.com> 1.3b-1
- Updated to latest upstream version 1.3b
- Incorporated Merge Review comments (bz 226002)
- Increased the polling timeout (bz 204990)

* Tue Feb 20 2007 Steve Dickson <steved@redhat.com> 1.2a-1
- Updated to latest upstream version 1.2a

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.1a-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.1a-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 24 2006 Warren Togami <wtogami@redhat.com> - 1.1a-3
- rebuild (#177697)

* Mon Jul 04 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1a-2
- Removed unnecessary -r from rm

* Fri Jun 17 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1a-1
- Upstream update

* Wed Jun 08 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1-2
- Added some docs
- Moved "make verify" into %%check

* Mon Jun 06 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1-1
- Initial build for Fedora Extras, based on the package
  by Dag Wieers
