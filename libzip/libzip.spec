
%define multilib_archs x86_64 %{ix86} ppc64 ppc s390x s390 sparc64 sparcv9

Name:    libzip
Version: 0.11.1
Release: 1%{?dist}
Summary: C library for reading, creating, and modifying zip archives

License: BSD
URL:     http://www.nih.at/libzip/index.html
Source0: http://www.nih.at/libzip/libzip-%{version}.tar.xz

#BuildRequires:  automake libtool
BuildRequires:  zlib-devel

# to handle multiarch headers, ex from mysql-devel package
Source1: zipconf.h

# fonctionnal changes from php bundled library
Patch0: libzip-0.11-php.patch


%description
libzip is a C library for reading, creating, and modifying zip archives. Files
can be added from data buffers, files, or compressed data copied directly from 
other zip archives. Changes made without closing the archive can be reverted. 
The API is documented by man pages.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

%patch0 -p1 -b .forphp

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


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS NEWS README THANKS TODO
%{_bindir}/zipcmp
%{_bindir}/zipmerge
%{_bindir}/ziptorrent
%{_libdir}/libzip.so.2*
%{_mandir}/man1/*zip*

%files devel
%{_includedir}/zip.h
%{_includedir}/zipconf*.h
%dir %{_libdir}/libzip
%{_libdir}/libzip/include
%{_libdir}/libzip.so
%{_libdir}/pkgconfig/libzip.pc
%{_mandir}/man3/*zip*


%changelog
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
