# remirepo spec file for vips, from:
#
# Fedora spec file for vips
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global vips_version_base 8.4
%global vips_version %{vips_version_base}.4
%global vips_soname_major 42

%global with_python2 1
%if 0%{?fedora}
%global with_python3 1
%global with_doc     1
%else
%global with_python3 0
%global with_doc     0
%endif

Name:		vips
Version:	%{vips_version}
Release:	4%{?dist}
Summary:	C/C++ library for processing large images

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://www.vips.ecs.soton.ac.uk/
Source0:	http://www.vips.ecs.soton.ac.uk/supported/%{vips_version_base}/%{name}-%{version}.tar.gz

BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(pygobject-3.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(fftw3)
# Ensure we use version 6 (same as imagick ext).
BuildRequires:	ImageMagick6-devel
BuildRequires:	pkgconfig(orc-0.4)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(matio)
BuildRequires:	pkgconfig(cfitsio)
BuildRequires:	pkgconfig(pangoft2)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(openslide)
BuildRequires:	pkgconfig(libgsf-1)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(poppler-glib)

BuildRequires:	libjpeg-turbo-devel
BuildRequires:	giflib-devel

BuildRequires:	gcc-c++
BuildRequires:	pkgconfig gettext


%description
VIPS is an image processing library. It is good for very large images
(even larger than the amount of RAM in your machine), and for working
with color.

This package should be installed if you want to use a program compiled
against VIPS.


%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	libjpeg-devel%{?_isa} libtiff-devel%{?_isa} zlib-devel%{?_isa}
Requires:	vips%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains the header files and
libraries necessary for developing programs using VIPS. It also
contains a C++ API and development documentation.


%package tools
Summary:	Command-line tools for %{name}
Group:		Applications/Multimedia
Requires:	vips%{?_isa} = %{version}-%{release}

%description tools
The %{name}-tools package contains command-line tools for working with VIPS.


%if %{with_python2}
%package python
Summary:	Python 2 support for %{name}
Group:		Development/Languages
BuildRequires: python2-devel
Requires:	vips%{?_isa} = %{version}-%{release}
Requires:	pygobject3-base >= 3.12.0
Provides:	python2-vipsCC = %{version}-%{release}
%{?python_provide:%python_provide python2-vipsCC}

%description python
The %{name}-python package contains Python 2 support for VIPS.
%endif


%if %{with_python3}
%package python3
Summary:	Python 3 support for %{name}
Group:		Development/Languages
BuildRequires: python3-devel
Requires:	vips%{?_isa} = %{version}-%{release}
Requires:	python3-gobject >= 3.12.0
# No provide for python3-vipsCC, since we only have the gi overrides

%description python3
The %{name}-python3 package contains Python 3 support for VIPS.
%endif


%if %{with_doc}
%package doc
Summary:	Documentation for %{name}
Group:		Documentation
BuildRequires: swig gtk-doc
Conflicts:	%{name} < %{version}-%{release}, %{name} > %{version}-%{release}

%description doc
The %{name}-doc package contains extensive documentation about VIPS in both
HTML and PDF formats.
%endif


%prep
%setup -q

# make the version string consistent for multiarch
export FAKE_BUILD_DATE=$(date -r %{SOURCE0})
sed -i "s/\\(VIPS_VERSION_STRING=\\)\$VIPS_VERSION-\`date\`/\\1\"\$VIPS_VERSION-$FAKE_BUILD_DATE\"/g" \
	configure
unset FAKE_BUILD_DATE

# Avoid setting RPATH to /usr/lib64 on 64-bit builds
# The DIE_RPATH_DIE trick breaks the build wrt gobject-introspection
sed -i 's|sys_lib_dlsearch_path_spec="|sys_lib_dlsearch_path_spec="/%{_lib} %{_libdir} |' configure


%build
# Upstream recommends enabling auto-vectorization of inner loops:
# https://github.com/jcupitt/libvips/pull/212#issuecomment-68177930
export CFLAGS="%{optflags} -ftree-vectorize"
export CXXFLAGS="%{optflags} -ftree-vectorize"
%configure \
%if %{with_doc}
    --enable-gtk-doc \
%endif
    --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT \( -name '*.la' -o -name '*.a' \) -exec rm -f {} ';'

# delete doc (we will get it later with %%doc)
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/doc/vips

# locale stuff
%find_lang vips%{vips_version_base}

%if %{with_python3}
# Upstream supports the GI override module on Python 3, but doesn't install
# it into the Python 3 path
mkdir -p ${RPM_BUILD_ROOT}%{python3_sitearch}
cp -a ${RPM_BUILD_ROOT}%{python2_sitearch}/gi \
	${RPM_BUILD_ROOT}%{python3_sitearch}
find ${RPM_BUILD_ROOT}%{python3_sitearch} \
	\( -name '*.pyc' -o -name '*.pyo' \) -delete
%endif


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f vips%{vips_version_base}.lang
%doc AUTHORS NEWS THANKS TODO ChangeLog
%license COPYING
%{_libdir}/*.so.%{vips_soname_major}*
%{_libdir}/girepository-1.0


%files devel
%{_includedir}/vips
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0
%{_datadir}/gtk-doc


%files tools
%{_bindir}/vips-%{vips_version_base}
%{_bindir}/*
%{_mandir}/man1/*


%if %{with_python2}
%files python
%{python2_sitearch}/gi/overrides/*
%{python2_sitearch}/vipsCC/
%endif


%if %{with_python3}
%files python3
%{python3_sitearch}/gi/overrides/*.py
%{python3_sitearch}/gi/overrides/__pycache__/*
%endif


%if %{with_doc}
%files doc
%doc doc/html
%license COPYING
%endif


%changelog
* Sun Jan 29 2017 Remi Collet <remi@remirepo.net> - 8.4.4-4
- rebuild against ImageMagick6 new soname (6.9.7-6)

* Mon Dec 12 2016 Remi Collet <remi@remirepo.net> - 8.4.4-3
- rebuild against ImageMagick6

* Tue Dec  6 2016 Remi Collet <remi@remirepo.net> - 8.4.4-2
- ensure ImageMagick v6 is used

* Thu Nov 24 2016 Remi Collet <remi@remirepo.net> - 8.4.4-1
- backport for repo repository
- disable python3 and doc sub-package

* Sun Nov 13 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.4.4-1
- New release

* Thu Oct 13 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.4.2-1
- New release

* Sun Sep 25 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.4.1-1
- New release

* Sat Aug 06 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.3.3-1
- New release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.3.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jul 05 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.3.1-2
- Rebuilt for matio 1.5.7

* Tue May 10 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.3.1-1
- New release
- Verify that wrapper script name matches base version

* Thu Apr 14 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.3.0-1
- New release
- Add giflib, librsvg2, poppler-glib dependencies

* Mon Mar 28 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.2.3-1
- New release

* Sun Feb 21 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.2.2-3
- BuildRequire gcc-c++ per new policy

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.2.2-1
- New release

* Thu Jan 21 2016 Orion Poplawski <orion@cora.nwra.com> - 8.2.1-2
- Rebuild for hdf5 1.8.16

* Mon Jan 11 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.2.1-1
- New release

* Mon Dec 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 8.1.1-3
- Rebuilt for libwebp soname bump

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sun Oct 18 2015 Benjamin Gilbert <bgilbert@backtick.net> - 8.1.1-1
- New release
- Update to new Python guidelines

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 17 2015 Orion Poplawski <orion@cora.nwra.com> - 8.0.2-2
- Rebuild for hdf5 1.8.15

* Wed May 06 2015 Benjamin Gilbert <bgilbert@backtick.net> - 8.0.2-1
- New release

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 7.42.3-2
- Rebuilt for GCC 5 C++11 ABI change

* Sat Feb 14 2015 Benjamin Gilbert <bgilbert@backtick.net> - 7.42.3-1
- New release

* Thu Feb 05 2015 Benjamin Gilbert <bgilbert@backtick.net> - 7.42.2-1
- New release
- Move license files to %%license

* Wed Jan 07 2015 Orion Poplawski <orion@cora.nwra.com> - 7.42.1-2
- Rebuild for hdf5 1.8.14

* Sun Dec 28 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.42.1-1
- New release
- Package new Python bindings
- Build with auto-vectorization

* Tue Nov 25 2014 Rex Dieter <rdieter@fedoraproject.org> 7.40.11-2
- rebuild (openexr)

* Wed Nov 05 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.11-1
- New release

* Thu Sep 25 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.9-1
- New release

* Fri Aug 22 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.6-1
- New release

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.40.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.5-1
- New release

* Sat Jul 26 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.4-1
- New release

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 7.40.3-2
- Rebuilt for gobject-introspection 1.41.4

* Tue Jul 08 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.3-1
- New release

* Sun Jun 29 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.2-1
- New release
- Add libgsf dependency
- Fix version string consistency across architectures
- Use macros for package and soname versions

* Sun Jun 22 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.38.6-1
- New release

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.38.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.38.5-2
- Rebuild for ImageMagick

* Wed Mar 26 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.38.5-1
- New release

* Tue Jan 21 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.38.1-1
- New release

* Thu Jan 09 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.5-3
- Rebuild for cfitsio

* Thu Jan 02 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.5-2
- Rebuild for libwebp

* Mon Dec 23 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.5-1
- New release

* Thu Nov 28 2013 Rex Dieter <rdieter@fedoraproject.org> 7.36.3-2
- rebuild (openexr)

* Wed Nov 13 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.3-1
- New release
- BuildRequire libwebp

* Sat Oct 05 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.0-1
- New release

* Tue Sep 10 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.34.2-2
- Rebuild for ilmbase 2.0

* Tue Aug 06 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.34.2-1
- New release
- Update -devel description: there are no man pages anymore

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.34.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 11 2013 Orion Poplawski <orion@cora.nwra.com> - 7.34.0-2
- Rebuild for cfitsio 3.350

* Sat Jun 29 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.34.0-1
- New release

* Fri Jun 28 2013 Kalev Lember <kalevlember@gmail.com> - 7.32.4-2
- Rebuilt with libpng 1.6

* Thu Jun 13 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.4-1
- New release

* Thu May 16 2013 Orion Poplawski <orion@cora.nwra.com> - 7.32.3-2
- Rebuild for hdf5 1.8.11

* Fri Apr 26 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.3-1
- New release

* Thu Mar 21 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.1-1
- New release

* Thu Mar 21 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.0-4
- Rebuild for cfitsio

* Sun Mar 17 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.0-3
- Rebuild for ImageMagick

* Sun Mar 10 2013 Rex Dieter <rdieter@fedoraproject.org> 7.32.0-2
- rebuild (OpenEXR)

* Thu Mar 07 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.0-1
- New release
- Stop setting rpath on 64-bit builds

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.30.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 7.30.7-2
- rebuild due to "jpeg8-ABI" feature drop

* Thu Jan 17 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.30.7-1
- New release
- Modify %%files glob to catch accidental soname bumps
- Update BuildRequires

* Wed Nov 14 2012 Benjamin Gilbert <bgilbert@backtick.net> - 7.30.5-1
- New release

* Mon Oct 15 2012 Benjamin Gilbert <bgilbert@backtick.net> - 7.30.3-1
- New release
- Enable gobject introspection
- Add versioned dependency on base package
- Minor specfile cleanups

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.28.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Adam Jackson <ajax@redhat.com> 7.28.2-2
- Rebuild for new libmatio

* Fri Apr 13 2012 Adam Goode <adam@spicenitz.org> - 7.28.2-1
- New upstream release
   * libvips rewrite
   * OpenSlide support
   * better jpeg, png, tiff support
   * sequential mode read
   * operation cache

* Mon Jan 16 2012 Adam Goode <adam@spicenitz.org> - 7.26.7-1
- New upstream release
   * Minor fixes, mostly with reading and writing

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.26.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 7.26.3-2
- Rebuild for new libpng

* Sat Sep  3 2011 Adam Goode <adam@spicenitz.org> - 7.26.3-1
- New upstream release
   * More permissive operators
   * Better TIFF, JPEG, PNG, FITS support
   * VIPS rewrite!

* Fri Aug 12 2011 Adam Goode <adam@spicenitz.org> - 7.24.7-2
- Clean up Requires and BuildRequires

* Wed Aug 10 2011 Adam Goode <adam@spicenitz.org> - 7.24.7-1
- New upstream release

* Mon Feb 14 2011 Adam Goode <adam@spicenitz.org> - 7.24.2-1
- New upstream release
   * Run-time code generation, for 4x speedup in some operations
   * Open via disc mode, saving memory
   * FITS supported
   * Improved TIFF and JPEG load

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.22.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 05 2010 jkeating - 7.22.2-1.2
- Rebuilt for gcc bug 634757

* Wed Sep 29 2010 jkeating - 7.22.2-3
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 7.22.2-2
- rebuild against ImageMagick

* Fri Sep 17 2010 Rex Dieter <rdieter@fedoraproject.org> - 7.22.2-1.1
- rebuild (ImageMagick)

* Fri Aug  6 2010 Adam Goode <adam@spicenitz.org> - 7.22.2-1
- New upstream release (a few minor fixes)

* Tue Jul 27 2010 Adam Goode <adam@spicenitz.org> - 7.22.1-2
- Add COPYING to doc subpackage

* Tue Jul 27 2010 Adam Goode <adam@spicenitz.org> - 7.22.1-1
- New upstream release
   + More revision of VIPS library
   + New threading system
   + New command-line program, vipsthumbnail
   + Improved interpolators
   + German translation
   + PFM (portable float map) image format read and write
   + Much lower VM use with many small images open
   + Rewritten flood-fill

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 7.20.7-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 15 2010 Adam Goode <adam@spicenitz.org> - 7.20.7-3
- Don't require gtk-doc anymore (resolves #604421)

* Sun Mar  7 2010 Adam Goode <adam@spicenitz.org> - 7.20.7-2
- Rebuild for imagemagick soname change
- Remove some old RPM stuff

* Tue Feb  2 2010 Adam Goode <adam@spicenitz.org> - 7.20.7-1
- New upstream release
   + C++ and Python bindings now have support for deprecated functions
   + Bugfixes for YCbCr JPEG TIFF files

* Wed Jan  6 2010 Adam Goode <adam@spicenitz.org> - 7.20.6-1
- New upstream release
   + About half of the VIPS library has been revised
   + Now using gtk-doc
   + Better image file support
   + MATLAB file read supported
   + New interpolation system
   + Support for Radiance files

* Fri Sep  4 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 7.18.2-1
- Update to 7.18.2 to sync with fixed nip2 FTBFS.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.16.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 10 2009 Adam Goode <adam@spicenitz.org> - 7.16.4-3
- Rebuild for ImageMagick soname change

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.16.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 28 2008 Adam Goode <adam@spicenitz.org> - 7.16.4-1
- New release

* Sun Dec 21 2008 Adam Goode <adam@spicenitz.org> - 7.16.3-1
- New release
- Update description

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 7.14.5-2
- Rebuild for Python 2.6

* Sat Aug 30 2008 Adam Goode <adam@spicenitz.org> - 7.14.5-1
- New release

* Fri Jun 20 2008 Adam Goode <adam@spicenitz.org> - 7.14.4-1
- New release

* Sat Mar 15 2008 Adam Goode <adam@spicenitz.org> - 7.14.1-1
- New release

* Mon Mar 10 2008 Adam Goode <adam@spicenitz.org> - 7.14.0-1
- New release
- Remove GCC 4.3 patch (upstream)

* Sat Feb  9 2008 Adam Goode <adam@spicenitz.org> - 7.12.5-5
- Fix GCC 4.3 build

* Sat Feb  9 2008 Adam Goode <adam@spicenitz.org> - 7.12.5-4
- GCC 4.3 mass rebuild

* Tue Oct 23 2007 Adam Goode <adam@spicenitz.org> - 7.12.5-3
- Eliminate build differences in version.h to work on multiarch

* Mon Oct 15 2007 Adam Goode <adam@spicenitz.org> - 7.12.5-2
- Rebuild for OpenEXR update

* Fri Sep 21 2007 Adam Goode <adam@spicenitz.org> - 7.12.5-1
- New upstream release

* Thu Aug 16 2007 Adam Goode <adam@spicenitz.org> - 7.12.4-2
- Add Conflicts for doc
- Update doc package description

* Thu Aug 16 2007 Adam Goode <adam@spicenitz.org> - 7.12.4-1
- New upstream release
- Update License tag

* Tue Jul 24 2007 Adam Goode <adam@spicenitz.org> - 7.12.2-1
- New stable release 7.12

* Sat May  5 2007 Adam Goode <adam@spicenitz.org> - 7.12.0-1
- New upstream release

* Thu Aug 31 2006 Adam Goode <adam@spicenitz.org> - 7.10.21-1
- New upstream release

* Fri Jul 28 2006 Adam Goode <adam@spicenitz.org> - 7.10.20-3
- Include results of running automake in the patch for undefined symbols
- No longer run automake or autoconf (autoconf was never actually necessary)

* Mon Jul 24 2006 Adam Goode <adam@spicenitz.org> - 7.10.20-2
- Eliminate undefined non-weak symbols in libvipsCC.so

* Fri Jul 21 2006 Adam Goode <adam@spicenitz.org> - 7.10.20-1
- New upstream release
- Updated for FC5

* Tue Dec 14 2004 John Cupitt <john.cupitt@ng-london.org.uk> 7.10.8
- updated for 7.10.8
- now updated from configure
- implicit deps and files

* Wed Jul 16 2003 John Cupitt <john.cupitt@ng-london.org.uk> 7.8.10
- updated for 7.8.10
- updated %%files
- copies formatted docs to install area

* Wed Mar 12 2003 John Cupitt <john.cupitt@ng-london.org.uk> 7.8.8
- updated for 7.8.8, adding libdrfftw

* Mon Feb 3 2003 John Cupitt <john.cupitt@ng-london.org.uk> 7.8.7-2
- hack to change default install prefix to /usr/local

* Thu Jan 30 2003 John Cupitt <john.cupitt@ng-london.org.uk> 7.8.7-1
- first stab at an rpm package for vips
