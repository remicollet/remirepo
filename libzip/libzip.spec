# Fedora Review Request #393041
# https://bugzilla.redhat.com/show_bug.cgi?id=393041

Name:           libzip2
Version:        0.10
Release:        1%{?dist}
Summary:        C library for reading, creating, and modifying zip archives

Group:          Applications/File
License:        BSD
URL:            http://www.nih.at/libzip/index.html
Source0:        http://www.nih.at/libzip/libzip-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  automake libtool
BuildRequires:  zlib-devel
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}


%description
libzip is a C library for reading, creating, and modifying zip archives. Files
can be added from data buffers, files, or compressed data copied directly from 
other zip archives. Changes made without closing the archive can be reverted. 
The API is documented by man pages.

%package devel
Summary:   Development files for %{name}
Group:     Development/Libraries
Requires:  %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package libs
Summary: Tools files for %{name}
Group:   System Environment/Libraries

%description libs
The %{name}-tools package contains tools that use %{name}.


%prep
%setup -q -n libzip-%{version}

# Avoid lib64 rpaths (FIXME: recheck this on newer releases)
#if "%{_libdir}" != "/usr/lib"
#sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
autoreconf -f -i
#endif


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Need to check this, for multilib
mv $RPM_BUILD_ROOT%{_libdir}/libzip/include/zipconf.h $RPM_BUILD_ROOT%{_includedir}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/zipcmp
%{_bindir}/zipmerge
%{_bindir}/ziptorrent
%{_mandir}/man1/*zip*

%files libs
%defattr(-,root,root,-)
%doc AUTHORS NEWS README THANKS TODO
%{_libdir}/libzip.so.2*

%files devel
%defattr(-,root,root,-)
%{_includedir}/zip*.h
%{_libdir}/libzip.so
%{_libdir}/pkgconfig/libzip.pc
%{_mandir}/man3/*zip*


%changelog
* Sun Mar 20 2011 Remi Collet <Fedora@FamilleCollet.com> 0.10-1
- update to 0.10
- rename to libzip2 and split tools in sub package

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

* Wed Nov 20 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.8-3
- require pkgconfig in devel subpkg
- move api description to devel subpkg
- keep timestamps in %%install
- avoid lib64 rpaths 

* Thu Nov 15 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.8-2
- Change License to BSD

* Thu Nov 15 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.8-1
- Initial version for Fedora
