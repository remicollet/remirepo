%global libname libevent

Name:           libevent2
Version:        2.0.18
Release:        1%{?dist}
Summary:        Abstract asynchronous event notification library

Group:          System Environment/Libraries
License:        BSD
URL:            http://sourceforge.net/projects/levent/
Source0:        http://downloads.sourceforge.net/levent/%{libname}-%{version}-stable.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  openssl-devel

Patch00:        %{libname}-2.0.10-stable-configure.patch


%description
The libevent API provides a mechanism to execute a callback function
when a specific event occurs on a file descriptor or after a timeout
has been reached. libevent is meant to replace the asynchronous event
loop found in event driven network servers. An application just needs
to call event_dispatch() and can then add or remove events dynamically
without having to change the event loop.


%package devel
Summary: Header files, libraries and development documentation for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
# same headers provided by both versions.
Conflicts: %{libname}-devel

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.


%prep
%setup -q -n %{libname}-%{version}-stable

# 477685 -  libevent-devel multilib conflict
%patch00 -p1


%build
%configure \
    --disable-dependency-tracking --disable-static
make %{?_smp_mflags} all


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,0755)
%doc README
%{_libdir}/libevent-*.so.*
%{_libdir}/libevent_core-*.so.*
%{_libdir}/libevent_extra-*.so.*
%{_libdir}/libevent_openssl-*.so.*
%{_libdir}/libevent_pthreads-*.so.*

%files devel
%defattr(-,root,root,0755)
%{_includedir}/event.h
%{_includedir}/evdns.h
%{_includedir}/evhttp.h
%{_includedir}/evrpc.h
%{_includedir}/evutil.h
%{_includedir}/event2
%{_libdir}/libevent.so
%{_libdir}/libevent_core.so
%{_libdir}/libevent_extra.so
%{_libdir}/libevent_openssl.so
%{_libdir}/libevent_pthreads.so
%{_libdir}/pkgconfig/libevent.pc
%{_libdir}/pkgconfig/libevent_openssl.pc
%{_libdir}/pkgconfig/libevent_pthreads.pc
%{_bindir}/event_rpcgen.*


%changelog
* Fri Jul 26 2013 Remi Collet <remi@fedoraproject.org> - 2.0.18-1
- rename to libevent2 for EPEL
- drop -doc sub-package
- own /usr/include/event2

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
