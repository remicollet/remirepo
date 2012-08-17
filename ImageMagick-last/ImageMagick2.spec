%global VER 6.7.8
%global Patchlevel 10

%if 0%{?rhel} >= 6 || 0%{?fedora} >= 5
%define withdjvu 1
%else
%define withdjvu 0
%endif


Name:           ImageMagick-last
Version:        %{VER}.%{Patchlevel}
Release:        1%{?dist}
Summary:        An X application for displaying and manipulating images
Group:          Applications/Multimedia
License:        ImageMagick
Url:            http://www.imagemagick.org/
Source0:        ftp://ftp.ImageMagick.org/pub/ImageMagick/ImageMagick-%{VER}-%{Patchlevel}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  bzip2-devel, freetype-devel, libjpeg-devel, libpng-devel
BuildRequires:  libtiff-devel, giflib-devel, zlib-devel
%if 0%{?fedora} >= 7 || 0%{?rhel} >= 6
BuildRequires:  perl-devel
%else
BuildRequires:  perl
%endif
BuildRequires:  ghostscript-devel
%if %{withdjvu}
BuildRequires:  djvulibre-devel
%endif
BuildRequires:  libwmf-devel, jasper-devel, libtool-ltdl-devel
BuildRequires:  libX11-devel, libXext-devel, libXt-devel
BuildRequires:  lcms-devel, libxml2-devel, librsvg2-devel

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}


%description
ImageMagick is an image display and manipulation tool for the X
Window System. ImageMagick can read and write JPEG, TIFF, PNM, GIF,
and Photo CD image formats. It can resize, rotate, sharpen, color
reduce, or add special effects to an image, and when finished you can
either save the completed work in the original format or a different
one. 

ImageMagick-last includes the command line programs for creating animated or
transparent .gifs, creating composite images, creating thumbnail images,
and more.

ImageMagick-latest conflicts with ImageMagick official RPM and so can not
be installed together.



%package devel
Summary: Library links and header files for ImageMagick app development
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libX11-devel, libXext-devel, libXt-devel
Requires: ghostscript-devel%{?_isa}
Requires: bzip2-devel%{?_isa}
Requires: freetype-devel%{?_isa}
Requires: libtiff-devel%{?_isa}
Requires: libjpeg-devel%{?_isa}
Requires: lcms-devel%{?_isa}
Requires: jasper-devel%{?_isa}
Requires: pkgconfig


%description devel
ImageMagick-last-devel contains the library links and header files you'll
need to develop ImageMagick applications. ImageMagick is an image
manipulation program.

If you want to create applications that will use ImageMagick code or
APIs, you need to install ImageMagick-devel as well as ImageMagick.
You do not need to install it if you just want to use ImageMagick,
however.


%package libs
Summary: Commands for ImageMagick
Group: Applications/Multimedia
Requires: %{name}%{?_isa} = %{version}-%{release}

%description libs
Provides the shared libraries and plugins of ImageMagick-last.

This package could be installed beside official RPM of ImageMagick
for applications requiring this libraries.



%if %{withdjvu}
%package djvu
Summary: DjVu plugin for ImageMagick
Group: Applications/Multimedia
Requires: %{name}%{?_isa} = %{version}-%{release}

%description djvu
This packages contains a plugin for ImageMagick which makes it possible to
save and load DjvU files from ImageMagick and libMagickCore using applications.
%endif


%package doc
Summary: ImageMagick html documentation
Group: Documentation

%description doc
ImageMagick documentation, this package contains usage (for the
commandline tools) and API (for the libraries) documentation in html format.
Note this documentation can also be found on the ImageMagick website:
http://www.imagemagick.org/


%package perl
Summary: ImageMagick perl bindings
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description perl
Perl bindings to ImageMagick.

Install ImageMagick-perl if you want to use any perl scripts that use
ImageMagick.


%package c++
Summary: ImageMagick Magick++ library (C++ bindings)
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description c++
This package contains the Magick++ library, a C++ binding to the ImageMagick
graphics manipulation library.

Install ImageMagick-c++ if you want to use any applications that use Magick++.


%package c++-devel
Summary: C++ bindings for the ImageMagick library
Group: Development/Libraries
Requires: %{name}-c++%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description c++-devel
ImageMagick-devel contains the static libraries and header files you'll
need to develop ImageMagick applications using the Magick++ C++ bindings.
ImageMagick is an image manipulation program.

If you want to create applications that will use Magick++ code
or APIs, you'll need to install ImageMagick-c++-devel, ImageMagick-devel and
ImageMagick.
You don't need to install it if you just want to use ImageMagick, or if you
want to develop/compile applications using the ImageMagick C interface,
however.


%prep
%setup -q -n ImageMagick-%{VER}-%{Patchlevel}
sed -i 's/libltdl.la/libltdl.so/g' configure
iconv -f ISO-8859-1 -t UTF-8 README.txt > README.txt.tmp
touch -r README.txt README.txt.tmp
mv README.txt.tmp README.txt
# for %doc
mkdir Magick++/examples
cp -p Magick++/demo/*.cpp Magick++/demo/*.miff Magick++/examples


%build
%configure --enable-shared \
           --disable-static \
           --with-modules \
           --with-perl \
           --with-x \
           --with-threads \
           --with-magick_plus_plus \
           --with-gslib \
           --with-wmf \
           --with-lcms \
           --with-rsvg \
           --with-xml \
           --with-perl-options="INSTALLDIRS=vendor %{?perl_prefix} CC='%__cc -L$PWD/magick/.libs' LDDLFLAGS='-shared -L$PWD/magick/.libs'" \
           --without-dps \
           --without-included-ltdl --with-ltdl-include=%{_includedir} \
           --with-ltdl-lib=%{_libdir} \
           --sysconfdir=%{_sysconfdir}/%{name}

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Do *NOT* use %%{?_smp_mflags}, this causes PerlMagick to be silently misbuild
make


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
cp -a www/source $RPM_BUILD_ROOT%{_datadir}/doc/ImageMagick-%{VER}
# Delete *ONLY* _libdir/*.la files! .la files used internally to handle plugins - BUG#185237!!!
rm $RPM_BUILD_ROOT%{_libdir}/*.la

# fix weird perl Magick.so permissions
chmod 755 $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Image/Magick/Magick.so

# perlmagick: fix perl path of demo files
%{__perl} -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)' PerlMagick/demo/*.pl

# perlmagick: cleanup various perl tempfiles from the build which get installed
find $RPM_BUILD_ROOT -name "*.bs" |xargs rm -f
find $RPM_BUILD_ROOT -name ".packlist" |xargs rm -f
find $RPM_BUILD_ROOT -name "perllocal.pod" |xargs rm -f

# perlmagick: build files list
echo "%defattr(-,root,root,-)" > perl-pkg-files
find $RPM_BUILD_ROOT/%{_libdir}/perl* -type f -print \
        | sed "s@^$RPM_BUILD_ROOT@@g" > perl-pkg-files 
find $RPM_BUILD_ROOT%{perl_vendorarch} -type d -print \
        | sed "s@^$RPM_BUILD_ROOT@%dir @g" \
        | grep -v '^%dir %{perl_vendorarch}$' \
        | grep -v '/auto$' >> perl-pkg-files 
if [ -z perl-pkg-files ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi

# fix multilib issues
%ifarch x86_64 s390x ia64 ppc64 alpha sparc64
%define wordsize 64
%else
%define wordsize 32
%endif

mv $RPM_BUILD_ROOT%{_includedir}/ImageMagick/magick/magick-config.h \
   $RPM_BUILD_ROOT%{_includedir}/ImageMagick/magick/magick-config-%{wordsize}.h

cat >$RPM_BUILD_ROOT%{_includedir}/ImageMagick/magick/magick-config.h <<EOF
#ifndef IMAGEMAGICK_MULTILIB
#define IMAGEMAGICK_MULTILIB

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "magick-config-32.h"
#elif __WORDSIZE == 64
# include "magick-config-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF

# Fonts must be packaged separately. It does nothave matter and demos work without it.
rm PerlMagick/demo/Generic.ttf


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%post c++ -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%postun c++ -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/[a-z]*
%{_mandir}/man[145]/[a-z]*
%{_mandir}/man1/ImageMagick.*

%files libs
%defattr(-,root,root,-)
%doc ChangeLog
%doc README.txt LICENSE NOTICE AUTHORS.txt NEWS.txt
%{_libdir}/libMagickCore.so.5*
%{_libdir}/libMagickWand.so.5*
%{_libdir}/ImageMagick-%{VER}
%{_datadir}/ImageMagick-%{VER}
%if %{withdjvu}
%exclude %{_libdir}/ImageMagick-%{VER}/modules-Q16/coders/djvu.*
%endif
%{_sysconfdir}/%{name}


%files devel
%defattr(-,root,root,-)
%{_bindir}/MagickCore-config
%{_bindir}/Magick-config
%{_bindir}/MagickWand-config
%{_bindir}/Wand-config
%{_libdir}/libMagickCore.so
%{_libdir}/libMagickWand.so
%{_libdir}/pkgconfig/MagickCore.pc
%{_libdir}/pkgconfig/ImageMagick.pc
%{_libdir}/pkgconfig/MagickWand.pc
%{_libdir}/pkgconfig/Wand.pc
%dir %{_includedir}/ImageMagick
%{_includedir}/ImageMagick/magick
%{_includedir}/ImageMagick/wand
%{_mandir}/man1/Magick-config.*
%{_mandir}/man1/MagickCore-config.*
%{_mandir}/man1/Wand-config.*
%{_mandir}/man1/MagickWand-config.*

%if %{withdjvu}
%files djvu
%defattr(-,root,root,-)
%{_libdir}/ImageMagick-%{VER}/modules-Q16/coders/djvu.*
%endif

%files doc
%defattr(-,root,root,-)
%doc %{_datadir}/doc/ImageMagick-%{VER}

%files c++
%defattr(-,root,root,-)
%doc Magick++/AUTHORS Magick++/ChangeLog Magick++/NEWS Magick++/README
%doc www/Magick++/COPYING
%{_libdir}/libMagick++.so.5*

%files c++-devel
%defattr(-,root,root,-)
%doc Magick++/examples
%{_bindir}/Magick++-config
%{_includedir}/ImageMagick/Magick++
%{_includedir}/ImageMagick/Magick++.h
%{_libdir}/libMagick++.so
%{_libdir}/pkgconfig/Magick++.pc
%{_libdir}/pkgconfig/ImageMagick++.pc
%{_mandir}/man1/Magick++-config.*

%files perl -f perl-pkg-files
%defattr(-,root,root,-)
%{_mandir}/man3/*
%doc PerlMagick/demo/ PerlMagick/Changelog PerlMagick/README.txt


%changelog
* Wed Aug 15 2012 Remi Collet <RPMS@FamilleCollet.com> - 6.7.8.10-1
- rename to ImageMagick-last
- update to 6.7.8-10 (soname bump to .5)

* Thu Nov 25 2010 Remi Collet <RPMS@FamilleCollet.com> - 6.6.5.10-1
- update to 6.6.5-10 (soname bump to .4)

* Sat Sep 05 2009 Remi Collet <RPMS@FamilleCollet.com> - 6.5.5.6-1
- patch level 6

* Wed Aug 26 2009 Remi Collet <RPMS@FamilleCollet.com> - 6.5.5.2-1
- rename to ImageMagick2 for EL and Fedora <= 10

* Mon Aug 3 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 6.5.4.7-3
- Update to version 6.5.4-7
- Use lzma-compressed source tarball as sugested by Ville Skyttä (BZ#515319)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.5.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 15 2009 Hans de Goede <hdegoede@redhat.com> 6.5.3.7-1
- New upstream release 6.5.3-7

* Mon Apr 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 6.5.1.2-1
- update to 6.5.1-2

* Fri Mar 13 2009 Hans de Goede <hdegoede@redhat.com> 6.4.9.6-2
- Fix undefined warning in magick-type.h (#489453)
- Do not link PerlMagick against system ImageMagick, but against the just
  build one

* Mon Mar  9 2009 Hans de Goede <hdegoede@redhat.com> 6.4.9.6-1
- New upstream release 6.4.9-6

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.4.5.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Hans de Goede <hdegoede@redhat.com> 6.4.5.5-8
- Remove (TM) from description as per new guidelines

* Sat Jan 17 2009 Rakesh Pandit <rakesh@fedoraproject.org> 6.4.5.5-7
- Corrected the wrong release and bumped

* Sat Jan 17 2009 Rakesh Pandit <rakesh@fedoraproject.org> 6.4.5.5-6
- Rebuild with new djvulibre

* Sat Dec 27 2008 Hans de Goede <hdegoede@redhat.com> 6.4.5.5-5
- Remove 2 included copies of the non Free artbrush font (rh 477399)

* Wed Dec 10 2008 Hans de Goede <hdegoede@redhat.com> 6.4.5.5-4
- Do not pass -jX to make when building, this breaks PerlMagick (rh 475554)

* Wed Nov 19 2008 Hans de Goede <hdegoede@redhat.com> 6.4.5.5-3
- Remove --without-windows-font-dir from configure args, specifying it
  makes ImageMagick search for windows fonts in the "no/" dir (rh 472244)

* Fri Nov 14 2008 Hans de Goede <hdegoede@redhat.com> 6.4.5.5-2
- Enable djvu support, put the new djvu plugin into a separate -djvu
  subpackage because of deps (rh 225897)

* Fri Nov 14 2008 Hans de Goede <hdegoede@redhat.com> 6.4.5.5-1
- New upstream release 6.4.5-5
- Various specfile fixes from merge review (rh 225897)
- Fix building with new libtool (rh 471468)

* Thu Nov 13 2008 Hans de Goede <hdegoede@redhat.com> 6.4.0.10-3
- Rebuild for new libtool (rh 471468)

* Sun Jul 27 2008 Hans de Goede <jwrdegoede@fedoraproject.org> 6.4.0.10-2
- Fix ownership of /usr/include/ImageMagick (bz 444647)

* Sat Apr 26 2008 Hans de Goede <jwrdegoede@fedoraproject.org> 6.4.0.10-1
- New upstream release 6.4.0.10
- This fixes conversion of 24 bpp windows icons (bz 440136)
- Don't reuse GError structs, that upsets glib2 (bz 325211)
- Use the system ltdl, not the included copy (bz 237475)
- Fix various multilib conflicts (bz 341561)
- Use xdg-open instead of htmlview (bz 388451)
- Some small specfile cleanups (utf-8 stuff & others) fixing rpmlint warnings

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.3.8.1-3
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 6.3.8.1-2
- Autorebuild for GCC 4.3

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 6.3.8.1-1
- update to 6.3.8.1
- rebuild for new perl
- fix license tag
- fix rpath issues
- add sparc64 to 64bit arch list

* Fri Sep 21 2007 Norm Murray <nmurray@redhat.com> 6.3.5.9-1.fc8
- rebase to 6.3.5.9
- fix build with missing open() arg
- add build require of jasper-devel, remove windows font dir
- update multilib patch

* Thu Apr  5 2007 Norm Murray <nmurray@redhat.com> 6.3.2.9-3.fc7
- heap overflows (#235075, CVE-2007-1797)

* Fri Mar 30 2007 Norm Murray <nmurray@redhat.com> 6.3.2.9-2.fc7
- perlmagick build fix (#231259)

* Fri Mar  2 2007 Norm Murray <nmurray@redhat.com> 6.3.2.9-1.fc7.0
- update to 6.3.2-9

* Wed Aug 23 2006 Matthias Clasen <mclasen@redhat.com> - 6.2.8.0-3.fc6
- fix several integer and buffer overflows (#202193, CVE-2006-3743)
- fix more integer overflows (#202771, CVE-2006-4144)

* Mon Jul 24 2006 Matthias Clasen <mclasen@redhat.com> - 6.2.8.0-2
- Add missing BRs

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.2.8.0-1.1
- rebuild

* Fri Jun  9 2006 Matthias Clasen <mclasen@redhat.com> - 6.2.8-1
- Update to 6.2.8

* Fri Jun  2 2006 Matthias Clasen <mclasen@redhat.com> - 6.2.5.4-7
- Fix multilib issues

* Thu May 25 2006 Matthias Clasen <mclasen@redhat.com> - 6.2.5.4-6
- Fix a heap overflow CVE-2006-2440 (#192279)
- Include required .la files  

* Mon Mar 20 2006 Matthias Clasen <mclasen@redhat.com> - 6.2.5.4-5
- Don't ship .la and .a files (#185237)

* Mon Feb 13 2006 Jesse Keating <jkeating@redhat.com> - 6.2.5.4-4.2.1
- rebump for build order issues during double-long bump

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.2.5.4-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6.2.5.4-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 30 2006 Matthias Clasen <mclasen@redhat.com> 6.2.5.4-4
- Make -devel require lcms-devel (#179200)

* Mon Jan 23 2006 Matthias Clasen <mclasen@redhat.com> 6.2.5.4-3
- Fix linking of DSOs.  (#176695)

* Mon Jan  9 2006 Matthias Clasen <mclasen@redhat.com> 6.2.5.4-2
- fix a format string vulnerability (CVE-2006-0082)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov  1 2005 Matthias Clasen <mclasen@redhat.com> 6.2.5.4-1
- Switch requires to modular X
- Update to 6.2.5

* Tue Sep 20 2005 Matthias Clasen <mclasen@redhat.com> 6.2.4.6-1
- Update to 6.2.4-6
- Drop upstreamed patches
- Disable DPS (#158984)
- Add missing requires (#165931)

* Thu Jun  9 2005 Tim Waugh <twaugh@redhat.com> 6.2.2.0-4
- Rebuilt for fixed ghostscript.

* Mon Jun  6 2005 Tim Waugh <twaugh@redhat.com> 6.2.2.0-3
- Rebuilt for new ghostscript.

* Thu May 26 2005  <mclasen@redhat.com> - 6.2.2.0-2
- fix a denial of service in the xwd coder (#158791, CAN-2005-1739)

* Tue Apr 26 2005 Matthias Clasen <mclasen@redhat.com> - 6.2.2.0-1
- Update to 6.2.2 to fix a heap corruption issue
  in the pnm coder.
 
* Mon Apr 25 2005  Matthias Clasen <mclasen@redhat.com> - 6.2.1.7-4
- .la files for modules are needed, actually

* Mon Apr 25 2005  Matthias Clasen <mclasen@redhat.com> - 6.2.1.7-3
- Really remove .la files for modules

* Mon Apr 25 2005  <mclasen@redhat.com> - 6.2.1.7-1
- Update to 6.2.1
- Include multiple improvements and bugfixes
  by Rex Dieter et al (111961, 145466, 151196, 149970, 
  146518, 113951, 145449, 144977, 144570, 139298)

* Sun Apr 24 2005  <mclasen@redhat.com> - 6.2.0.7-3
- Make zip compression work for tiff (#154045)

* Wed Mar 16 2005  <mclasen@redhat.com> - 6.2.0.7-2
- Update to 6.2.0 to fix a number of security issues:
  #145112 (CAN-2005-05), #151265 (CAN-2005-0397)
- Drop a lot of upstreamed patches

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> 6.0.7.1-7
- rebuild with gcc4
- remove an extraneous vsnprintf prototype which causes
  gcc4 to complain

* Mon Oct 11 2004 Tim Waugh <twaugh@redhat.com> 6.0.7.1-4
- The devel subpackage requires XFree86-devel (bug #126509).
- Fixed build requirements (bug #120776).  From Robert Scheck.

* Tue Sep 14 2004 Karsten Hopp <karsten@redhat.de> 6.0.7.1-3 
- move *.mgk files (#132007, #131708, #132397)

* Sun Sep 12 2004 Karsten Hopp <karsten@redhat.de> 6.0.7.1-1 
- update to 6.0.7 Patchlevel 1, fixes #132106

* Sat Sep 4 2004 Bill Nottingham <notting@redhat.com> 6.0.6.2-2
- move libWand out of -devel, fix requirements (#131767)

* Wed Sep 01 2004 Karsten Hopp <karsten@redhat.de> 6.0.6.2-1 
- update to latest stable version
- get rid of obsolete patches
- fix remaining patches

* Sat Jun 19 2004 Alan Cox <alan@redhat.com>
- Easyfixes (#124791) - fixed missing dependancy between -devel and
  libexif-devel

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 23 2004 Karsten Hopp <karsten@redhat.de> 5.5.7.15-1.3 
- freetype patch to fix convert (#115716)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Jan 25 2004 Nils Philippsen <nphilipp@redhat.com> 5.5.7.15-0.2
- make perl module link against the built library instead of the installed one

* Thu Jan 22 2004 Nils Philippsen <nphilipp@redhat.com> 5.5.7.15-0.1
- version 5.5.7 patchlevel 15

* Mon Oct 13 2003 Nils Philippsen <nphilipp@redhat.com> 5.5.7.10-0.1
- rebuild with release 0.1 to not block an official update package

* Wed Sep 10 2003 Nils Philippsen <nphilipp@redhat.com> 5.5.7.10-2
- hack around libtool stupidity
- disable automake patch as we require automake-1.7 anyway

* Wed Sep 10 2003 Nils Philippsen <nphilipp@redhat.com> 5.5.7.10-1
- version 5.5.7 patchlevel 10

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 29 2003 Tim Powers <timp@redhat.com> 5.5.6-4
- rebuild for RHEL to fix broken deps

* Thu May 15 2003 Tim Powers <timp@redhat.com> 5.5.6-3
- rebuild again to fix broken dep on libMagick.so.5

* Mon May 12 2003 Karsten Hopp <karsten@redhat.de> 5.5.6-2
- rebuild

* Fri May 09 2003 Karsten Hopp <karsten@redhat.de> 5.5.6-1
- update
- specfile fixes
  #63897 (_target instead of _arch)
  #74521 (SRPM doesn't compile)
  #80441 (RFE: a newer version of ImageMagick is available)
  #88450 (-devel package missing dependancy)
  #57396 (convert won't read RAW format images)
- verified that the upstream version fixes the following bugreports:
  #57544 (display cannot handle many xpm's which both ee and rh71 display can)
  #63727 (ImageMagick fails to handle RGBA files)
  #73864 (composite dumps core on certain operations)
  #78242 (Header files for c missing in devel rpms)
  #79783 (magick_config.h is missing from ImageMagick-c++-devel)
  #80117 (Documentation is installed twice by RPM )
  #82762 (Trouble with browsing help files)
  #85760 (Segmentation fault)
  #86120 (eps->ppm convert crashes)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 5.4.7-9
- use internal dep generator.

* Mon Dec 16 2002 Tim Powers <timp@redhat.com> 5.4.7-8
- rebuild

* Sat Dec 14 2002 Tim Powers <timp@redhat.com> 5.4.7-7
- don't use rpms internal dep generator

* Fri Nov 22 2002 Tim Powers <timp@redhat.com>
- fix perl paths in file list

* Thu Nov 21 2002 Tim Powers <timp@redhat.com>
- lib64'ize
- don't throw stuff in /usr/X11R6, that's for X only
- remove files we aren't shipping

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Tue Jul 23 2002 Tim Powers <timp@redhat.com> 5.4.7-4
- build using gcc-3.2-0.1

* Wed Jul 03 2002 Karsten Hopp <karsten@redhat.de> 5.4.7-3
- fix non-cpp headers in -devel package
- fix #62157 (wrong path for include files in ImageMagick-devel)
- fix #63897 (use _target instead of _arch) in libtool workaround
- fix #65860, #65780 (tiff2ps) expands images to >10 MB Postscript files.

* Mon Jul 01 2002 Karsten Hopp <karsten@redhat.de> 5.4.7-1
- update
- fix localdoc patch
- fix %%files section
- disable nonroot patch
- fix #62100,55950,62162,63136 (display doesn't start form gnome menu)
- fix libtool workaround
- moved Magick*-config into -devel package (#64249)

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May  6 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.6-1
- 5.4.6

* Thu Mar 14 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.3.11-1
- Update to pl 11

* Fri Feb 22 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.3.5-1
- Update to 5.4.3 pl5; this fixes #58080

* Thu Jan 17 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.2.3-1
- Patchlevel 3

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jan  4 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.2.2-1
- Update to 5.4.2-2
- Fix #57923, also don't hardcode netscape as html viewer

* Wed Dec  5 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.1-1
- 5.4.1
- Link against new libstdc++

* Fri Nov  9 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.0.5-1
- 5.4.0.5
- Make the error message when trying to display an hpgl file more
  explicit (#55875)

* Mon Nov  5 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.0.3-1
- 5.4.0.3
- Fix names of man pages

* Mon Oct 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.0-1
- 5.4.0
- work around build system breakage causing applications to be named
  %%{_arch}-redhat-linux-foo rather than foo

* Wed Sep 19 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.9-1
- 5.3.9

* Mon Aug 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.8-3
- Add delegates.mgk back, got lost during the update to 5.3.8 (Makefile bug)
  (#52611)

* Mon Aug 20 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.8-2
- Remove Magick++ includes from -devel, they're already in -c++-devel
  (#51590)

* Sun Jul 28 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.8-1
- 5.3.8 (bugfix release)

* Sat Jul 27 2001 Than Ngo <than@redhat.com> 5.3.7-3
- fix to build Perlmagic on s390 s390x

* Thu Jul 26 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.7-2
- Add delegates.mgk to the package (#50725)

* Tue Jul 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.7-1
- 5.3.7
- Fix build without previously installed ImageMagick-devel (#49816)
- Move perl bindings to a separate package.

* Mon Jul  9 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.6-2
- Fix build as non-root again
- Shut up rpmlint

* Tue Jul  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.6-1
- 5.3.6
- Get rid of the ia64 patch, it's no longer needed since glibc was fixed

* Sat Jun 16 2001 Than Ngo <than@redhat.com>
- update to 5.3.5
- cleanup specfile

* Sat May 19 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.3-2
- 5.3.3-respin, fixes #41196

* Tue May  1 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.3-1
- 5.3.3
- Add a desktop file for "display" (RFE#17417)

* Sun Apr 15 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.3.2
- work around bugs in ia64 glibc headers

* Mon Jan 08 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- remove patch for s390, it is not necessary

* Mon Jan  1 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.2.7

* Wed Dec 27 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.2.6

* Mon Dec 18 2000 Than Ngo <than@redhat.com>
- ported to s390

* Mon Sep 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.2.4
- Fix up and package the C++ bindings in the new c++/c++-devel packages.

* Wed Aug  2 2000 Matt Wilson <msw@redhat.com>
- rebuild against new libpng

* Wed Jul 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- include images with docs (#10312)

* Thu Jul 13 2000 Matt Wilson <msw@redhat.com>
- don't build with -ggdb, use -g instead.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul  3 2000 Florian La Roche <laroche@redhat.com>
- update to 5.2.2 beta

* Mon Jul  3 2000 Florian La Roche <laroche@redhat.com>
- update to 5.2.1, redone patches as they failed

* Fri Jun 30 2000 Matt Wilson <msw@redhat.com>
- remove hacks to move perl man pages
- don't include the perl*/man stuff, these files go in /usr/share/man now.

* Thu Jun 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- disable optimization on Alpha and Sparc

* Wed Jun 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 5.2.0
- update URL
- remove redundant CXXFLAGS=$RPM_OPT_FLAGS

* Thu Jun  1 2000 Matt Wilson <msw@redhat.com>
- bootstrap rebuilt to nuke broken libbz2 deps
- add Prefix: tag such that the FHS macros work properly

* Wed May 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- now compiles with bzip2 1.0
- changed buildroot to include version

* Fri May  5 2000 Bill Nottingham <notting@redhat.com>
- fix compilation with new perl

* Sat Mar 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.1.1

* Thu Feb  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Rebuild to get compressed man pages

* Thu Nov 18 1999 Michael K. Johnson <johnsonm@redhat.com>
- ugly hack to print with lpr instead of lp

* Mon Aug 30 1999 Bill Nottingham <notting@redhat.com>
- update to 4.2.9

* Tue Aug 17 1999 Bill Nottingham <notting@redhat.com>
- update to 4.2.8

* Fri Apr 09 1999 Cristian Gafton <gafton@redhat.com>
- include the perl man pages as well

* Tue Apr 06 1999 Michael K. Johnson <johnsonm@redhat.com>
- remove --enable-16bit because it damages interoperability

* Mon Apr  5 1999 Bill Nottingham <notting@redhat.com>
- update to 4.2.2
- change ChangeLog to refer to actual dates. 
- strip binaries

* Thu Apr  1 1999 Bill Nottingham <notting@redhat.com>
- add more files. Oops.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Wed Mar 10 1999 Bill Nottingham <notting@redhat.com>
- version 4.2.1

* Tue Jan 19 1999 Michael K. Johnson <johnsonm@redhat.com>
- changed group

* Tue Jan 19 1999 Cristian Gafton <gafton@redhat.com>
- hacks to make it work with the new perl
- version 4.1.0 (actually installs the sonames as 4.0.10... doh!)
- make sure the libraries have the x bit on

* Wed Jun 10 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 21 1998 Cristian Gafton <gafton@redhat.com>
- updated to 4.0.5

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- updated to 4.0.4
- added BuildRoot

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- updated from 3.8.3 to 3.9.1
- removed PNG patch (appears to be fixed)

* Wed Oct 15 1997 Erik Troan <ewt@redhat.com>
- build against new libpng

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu Mar 20 1997 Michael Fulbright <msf@redhat.com>
- updated to version 3.8.3.
- updated source and url tags.
