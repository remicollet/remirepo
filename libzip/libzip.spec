# remirepo spec file for libzip-last
# renamed for parallel installation, from:
#
# Fedora spec file for libzip
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global multilib_archs x86_64 %{ix86} ppc64 ppc s390x s390 sparc64 sparcv9
%global libname libzip
%if 0%{?rhel} == 5
# Perl is too old
%global with_tests     0
%else
%if %{?runselftest}%{!?runselftest:1}
%global with_tests     0%{!?_without_tests:1}
%else
%global with_tests     0%{?_with_tests:1}
%endif
%endif

%if 0%{?fedora} < 23
Name:    %{libname}-last
%else
Name:    %{libname}
%endif
Version: 1.1.3
Release: 1%{?dist}
Group:   System Environment/Libraries
Summary: C library for reading, creating, and modifying zip archives

License: BSD
URL:     http://www.nih.at/libzip/index.html
Source0: http://www.nih.at/libzip/libzip-%{version}.tar.xz
# to handle multiarch headers, ex from mysql-devel package
Source1: zipconf.h

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  zlib-devel
# Needed to run the test suite
# find regress/ -type f | /usr/lib/rpm/perl.req
BuildRequires:  perl
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(UNIVERSAL)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
%if "%{name}" == "%{libname}"
Obsoletes:      %{libname}-last <= %{version}
%endif


%description
libzip is a C library for reading, creating, and modifying zip archives. Files
can be added from data buffers, files, or compressed data copied directly from 
other zip archives. Changes made without closing the archive can be reverted. 
The API is documented by man pages.
%if "%{name}" != "%{libname}"
%{name} is designed to be installed beside %{libname}.
%endif


%package devel
Group:    Development/Libraries
Summary:  Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%if "%{name}" != "%{libname}"
Conflicts: %{libname}-devel < %{version}
Provides:  %{libname}-devel = %{version}-%{release}
%else
Obsoletes: %{libname}-last-devel <= %{version}
%endif

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package tools
Summary:  Command line tools from %{name}
Group:    Applications/System
Requires: %{name}%{?_isa} = %{version}-%{release}
%if "%{name}" != "%{libname}"
Conflicts: %{libname} < %{version}
Provides:  %{libname} = %{version}-%{release}
%else
Obsoletes: %{libname}-last-tools <= %{version}
%endif

%description tools
The %{name}-tools package provides command line tools split off %{name}:
- zipcmp
- zipmerge
- ziptool


%prep
%setup -q -n %{libname}-%{version}

# Avoid lib64 rpaths (FIXME: recheck this on newer releases)
%if "%{_libdir}" != "/usr/lib"
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
#autoreconf -f -i
%endif


%build
%configure \
  --disable-static

make %{?_smp_mflags}


%install

make install DESTDIR=%{buildroot} INSTALL='install -p'

## unpackaged files
rm -fv %{buildroot}%{_libdir}/lib*.la

## FIXME: someday fix consumers of libzip to properly handle
## header @ %%{_libdir}/libzip/include/zipconf.h -- rex
%ifarch %{multilib_archs}
ln -s ../%{_lib}/libzip/include/zipconf.h \
      %{buildroot}%{_includedir}/zipconf-%{__isa_bits}.h
install -D -m644 -p %{SOURCE1} %{buildroot}%{_includedir}/zipconf.h
%else
ln -s ../%{_lib}/libzip/include/zipconf.h \
      %{buildroot}%{_includedir}/zipconf.h
%endif


%check
%if %{with_tests}
make check
%else
: Test suite disabled
%endif


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/libzip.so.4*

%files tools
%defattr(-,root,root,-)
%{_bindir}/zipcmp
%{_bindir}/zipmerge
%{_bindir}/ziptool
%{_mandir}/man1/zip*

%files devel
%defattr(-,root,root,-)
%doc API-CHANGES AUTHORS THANKS *.md
%{_includedir}/zip.h
%{_includedir}/zipconf*.h
%dir %{_libdir}/libzip
%{_libdir}/libzip/include
%{_libdir}/libzip.so
%{_libdir}/pkgconfig/libzip.pc
%{_mandir}/man3/libzip*
%{_mandir}/man3/zip*
%{_mandir}/man3/ZIP*


%changelog
* Sat May 28 2016 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- update to 1.1.3

* Sat Feb 20 2016 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- update to 1.1.2

* Sat Feb 13 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 1.1-1
- update to 1.1
- new ziptool command
- add fix for undefined optopt in ziptool.c (upstream)

* Thu Jan 14 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-3
- libzip obsoletes libzip-last

* Tue May  5 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- soname bump from .2 to .4
- drop ziptorrent
- create "tools" sub package
- rename to libzip-last to allow parallel installation

* Mon Mar 23 2015 Rex Dieter <rdieter@fedoraproject.org> 0.11.2-5
- actually apply patch (using %%autosetup)

* Mon Mar 23 2015 Rex Dieter <rdieter@fedoraproject.org> 0.11.2-4
- CVE-2015-2331: integer overflow when processing ZIP archives (#1204676,#1204677)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Dec 19 2013 Remi Collet <remi@fedoraproject.org> - 0.11.2-1
- update to 0.11.2
- run test during build

* Thu Oct 24 2013 Remi Collet <remi@fedoraproject.org> - 0.11.1-3
- replace php patch with upstream one

* Fri Aug 23 2013 Remi Collet <remi@fedoraproject.org> - 0.11.1-2
- include API-CHANGES and LICENSE in package doc

* Thu Aug 08 2013 Remi Collet <remi@fedoraproject.org> - 0.11.1-1
- update to 0.11.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 15 2012 Remi Collet <remi@fedoraproject.org> - 0.10.1-5
- fix typo in multiarch (#866171)

* Wed Sep 05 2012 Rex Dieter <rdieter@fedoraproject.org> 0.10.1-4
- Warning about conflicting contexts for /usr/lib64/libzip/include/zipconf.h versus /usr/include/zipconf-64.h (#853954)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Rex Dieter <rdieter@fedoraproject.org> 0.10.1-2
- spec cleanup, better multilib fix

* Wed Mar 21 2012 Remi Collet <remi@fedoraproject.org> - 0.10.1-1
- update to 0.10.1 (security fix only)
- fixes for CVE-2012-1162 and CVE-2012-1163

* Sun Mar 04 2012 Remi Collet <remi@fedoraproject.org> - 0.10-2
- try to fix ARM issue (#799684)

* Sat Feb 04 2012 Remi Collet <remi@fedoraproject.org> - 0.10-1
- update to 0.10
- apply patch with changes from php bundled lib (thanks spot)
- handle multiarch headers (ex from MySQL)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 04 2010 Kalev Lember <kalev@smartlink.ee> - 0.9.3-2
- Cleaned up pkgconfig deps which are now automatically handled by RPM.

* Thu Feb 04 2010 Kalev Lember <kalev@smartlink.ee> - 0.9.3-1
- Updated to libzip 0.9.3

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.9-4
- Use bzipped upstream tarball.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 0.9-1
- libzip-0.9

* Sat Feb 09 2008 Sebastian Vahl <fedora@deadbabylon.de> 0.8-5
- rebuild for new gcc-4.3

* Fri Jan 11 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 0.8-4
- use better workaround for removing rpaths

* Tue Nov 20 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.8-3
- require pkgconfig in devel subpkg
- move api description to devel subpkg
- keep timestamps in %%install
- avoid lib64 rpaths 

* Thu Nov 15 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.8-2
- Change License to BSD

* Thu Nov 15 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.8-1
- Initial version for Fedora
