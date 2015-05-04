Name:           lcms2
Version:        2.7
Release:        1%{?dist}
Summary:        Color Management Engine
Group:          System Environment/Libraries
License:        MIT
URL:            http://www.littlecms.com/
Source0:        http://www.littlecms.com/lcms2-2.7.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  zlib-devel

%description
LittleCMS intends to be a small-footprint, speed optimized color management
engine in open source form. LCMS2 is the current version of LCMS, and can be
parallel installed with the original (deprecated) lcms.

%package        utils
Summary:        Utility applications for %{name}
Group:          Applications/Productivity
Requires:       %{name} = %{version}-%{release}

%description    utils
The %{name}-utils package contains utility applications for %{name}.

%package        devel
Summary:        Development files for LittleCMS
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:       littlecms-devel = %{version}-%{release}

%description    devel
Development files for LittleCMS.

%prep
%setup -q -n lcms2-2.7
%build
%configure --disable-static --program-suffix=2

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="install -p"
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'
install -D -m 644 include/lcms2.h $RPM_BUILD_ROOT/usr/include/lcms2.h
install -D -m 644 include/lcms2_plugin.h $RPM_BUILD_ROOT/usr/include/lcms2_plugin.h

# install docs as this is all we've got
install -D -m 644 doc/LittleCMS2.?\ tutorial.pdf $RPM_BUILD_ROOT/usr/share/doc/lcms2-devel-2.6/tutorial.pdf
install -D -m 644 doc/LittleCMS2.?\ API.pdf $RPM_BUILD_ROOT/usr/share/doc/lcms2-devel-2.6/api.pdf
install -D -m 644 doc/LittleCMS2.?\ Plugin\ API.pdf $RPM_BUILD_ROOT/usr/share/doc/lcms2-devel-2.6/plugin-api.pdf

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_libdir}/*.so.*

%files utils
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_datadir}/doc/lcms2-devel-2.6/*.pdf
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Mon May  4 2015 Remi Collet <RPMS@FamilleCollet.com> - 2.7-1
- backport for EL-5

* Sun Mar 22 2015 Richard Hughes <richard@hughsie.com> - 2.7-1
- Update to new upstream version.

* Tue Mar 17 2015 Richard Hughes <richard@hughsie.com> - 2.7-0.1rc3
- Update to new upstream RC version.

* Thu Feb 05 2015 Richard Hughes <richard@hughsie.com> - 2.7-0.1rc1
- Update to new upstream version.
- Added a flag  to clip negative values in unbounded transforms
- Added a global optimization that merges consecutive matrices in pipelines.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Brent Baude <baude@us.ibm.com> - 2.6-2
- Correct assumption about ppc64 endianess

* Mon Mar 17 2014 Richard Hughes <richard@hughsie.com> 2.6-1
- Update to new upstream version.
- Added a way to retrieve matrix shaper always, no matter LUT is present
- Added pthread dependency
- Big revamp on Contexts, from Artifex
- Fixed a bug in PCS/Colorspace order when reading V2 Lab devicelinks
- Fixed some indexing out of bounds in floating point interpolation
- Fix for delete tag memory corruption
- New locking plug-in, from Artifex

* Wed Feb 19 2014 Richard Hughes <richard@hughsie.com> 2.6-0.1.rc3
- Update to new prerelease upstream version.

* Fri Feb 14 2014 Richard Hughes <richard@hughsie.com> 2.6-0.1.rc1
- Update to new prerelease upstream version.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 01 2013 Richard Hughes <richard@hughsie.com> 2.5-1
- Update to new upstream version.
- Added a reference for Mac MLU tag
- Added a way to read the profile creator from header
- Added error descriptions on cmsSmoothToneCurve
- Added identity curves support for write V2 LUT
- Added new cmsPlugInTHR() and fixed some race conditions
- Added TIFF Lab16 handling on tifficc
- Fixed a bug on big endian platforms not supporting uint64 or long long.
- Fixed a multithead bug on optimization
- Fixed devicelink generation for 8 bits
- Fixed some 64 bit warnings on size_t to uint32 conversions
- Rendering intent used when creating the transform is now propagated to profile
- RGB profiles store only one copy of the curve to save space
- Transform2Devicelink now keeps white point when guessing deviceclass is enabled
- Update black point detection algorithm to reflect ICC changes
- User defined parametric curves can now be saved in ICC profiles

* Thu Jun 27 2013 Richard Hughes <richard@hughsie.com> 2.5-0.2
- Update to new release candidate version.

* Thu May 30 2013 Richard Hughes <richard@hughsie.com> 2.5-0.1
- Update to new release candidate version.

* Thu Apr 25 2013 Tim Waugh <twaugh@redhat.com> - 2.4-6
- Applied upstream fixes for threading (bug #951984).

* Thu Mar  7 2013 Tim Waugh <twaugh@redhat.com> - 2.4-5
- Added upstream fix for threading issue with plugin registration
  (bug #912307).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.4-3
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 2.4-2
- rebuild against new libjpeg

* Sat Sep 15 2012 Richard Hughes <richard@hughsie.com> 2.4-1
- Update to new upstream version.
- Black point detection from the algorithm disclosed by Adobe
- Added support for transforms on planar data with different stride
- Added a new plug-in type for optimizing full transforms
- Linear (gamma 1.0) profiles can now operate in unbounded mode
- Added "half" float support

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 10 2011 Richard Hughes <richard@hughsie.com> 2.3-1
- Update to new upstream version which incorporates many bugfixes.

* Fri Jun 10 2011 Richard Hughes <richard@hughsie.com> 2.2-2
- Actually update the sources...

* Fri Jun 10 2011 Richard Hughes <richard@hughsie.com> 2.2-1
- Update to new upstream version
- Stability and efficienty fixes
- Adds support for dictionary metatag

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 01 2010 Richard Hughes <richard@hughsie.com> 2.1-1
- Update to new upstream version.

* Fri Jun 18 2010 Richard Hughes <richard@hughsie.com> 2.0a-3
- Address some more review comments.
- Resolves #590387

* Fri Jun 18 2010 Richard Hughes <richard@hughsie.com> 2.0a-2
- Address some review comments.
- Resolves #590387

* Fri Jun 18 2010 Richard Hughes <richard@hughsie.com> 2.0a-1
- Initial package for Fedora review
