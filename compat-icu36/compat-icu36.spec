Name:           compat-icu36
Version:        3.6
Release:        5.16.1
Summary:        International Components for Unicode

Group:          System Environment/Libraries
License:        X License
URL:            http://www.ibm.com/software/globalization/icu/
Source0:        ftp://ftp.software.ibm.com/software/globalization/icu/icu4c-3_6-src.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

BuildRequires:  doxygen, autoconf
Patch1:  icu-3.4-multiarchdevel.patch
Patch2:  icu-config
Patch3:  icu.icu5365.dependantvowels.patch
Patch4:  icu.icu5418.malayam.patch
Patch5:  icu.icu5431.malayam.patch
Patch6:  icu.icu5433.oriya.patch
Patch7:  icu.icuXXXX.virama.prevnext.patch
Patch8:  icu.icu5465.telegu.patch
Patch9:  icu.icu5488.assamese.patch
Patch10: icu.icu5500.devicetablecrash.patch
Patch11: icu.icu5501.sinhala.biggerexpand.patch
Patch12: icu.icu5557.safety.patch
Patch13: icu.icu5594.gujarati.patch
Patch14: icu.icu5506.multiplevowels.patch
Patch15: icu.icuXXXX.malayalam.bysyllable.patch
Patch16: icu.rh429023.regexp.patch
Patch17: icu.icu5483.backport.patch
Patch18: icu.icu5797.backport.patch
Patch19: icu.icu6001.backport.patch
Patch20: icu.icu6002.backport.patch
Patch21: icu.icu6175.emptysegments.patch
Patch22: icu.icu5691.backport.patch
Patch23: icu.icuXXXX.rollbackabi.patch
Patch24: canonicalize.patch
Conflicts: icu

%description
The International Components for Unicode (ICU) libraries provide
robust and full-featured Unicode services on a wide variety of
platforms. ICU supports the most current version of the Unicode
standard, and they provide support for supplementary Unicode
characters (needed for GB 18030 repertoire support).
As computing environments become more heterogeneous, software
portability becomes more important. ICU lets you produce the same
results across all the various platforms you support, without
sacrificing performance. It offers great flexibility to extend and
customize the supplied services.


%package     -n compat-libicu36
Summary:        International Components for Unicode - libraries
Group:          System Environment/Libraries

%description -n compat-libicu36
%{summary}.

This package provides the ICU libraries for package built
against version %{version}.

%package     -n compat-libicu36-devel
Summary:        Development files for International Components for Unicode
Group:          Development/Libraries
Requires:       compat-libicu36 = %{version}-%{release}
Requires:       pkgconfig
Conflicts:      libicu-devel

%description -n compat-libicu36-devel
%{summary}.

%package     -n compat-libicu36-doc
Summary:        Documentation for International Components for Unicode
Group:          Documentation

%description -n compat-libicu36-doc
%{summary}.


%prep
%setup -q -n icu
%patch1  -p1 -b .multiarchdevel
%patch3  -p1 -b .dependantvowels
%patch4  -p1 -b .icu5418.malayam.patch
%patch5  -p1 -b .icu5431.malayam.patch
%patch6  -p1 -b .icu5433.oriya.patch
%patch7  -p1 -b .icuXXXX.virama.prevnext.patch
%patch8  -p1 -b .icu5465.telegu.patch
%patch9  -p1 -b .icu5488.assamese.patch
%patch10 -p1 -b .icu5500.devicetablecrash.patch
%patch11 -p1 -b .icu5501.sinhala.biggerexpand.patch
%patch12 -p1 -b .icu5557.safety.patch
%patch13 -p1 -b .icu5594.gujarati.patch
%patch14 -p1 -b .icu5506.multiplevowels.patch
%patch15 -p1 -b .icuXXXX.malayalam.bysyllable.patch
%patch16 -p1 -b .rh429023.regexp.patch
%patch17 -p1 -b .icu5483.backport.patch
%patch18 -p1 -b .icu5797.backport.patch
%patch19 -p1 -b .icu6001.backport.patch
%patch20 -p1 -b .icu6002.backport.patch
%patch21 -p1 -b .icu6175.emptysegments.patch
%patch22 -p1 -b .icu5691.backport.patch
%patch23 -p1 -b .icuXXXX.rollbackabi.patch
%patch24 -p0 -b .canonicalize.patch

%build
cd source
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export CXXFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
autoconf
%configure --with-data-packaging=library --disable-samples
#rhbz#654590
sed -i -- "s/-nodefaultlibs -nostdlib//" config/mh-linux
make # %{?_smp_mflags} # -j(X>1) may "break" man pages as of 3.2, b.f.u #2357
make doc

%install
rm -rf $RPM_BUILD_ROOT source/__docs
make -C source install DESTDIR=$RPM_BUILD_ROOT
make -C source install-doc docdir=__docs
chmod +x $RPM_BUILD_ROOT%{_libdir}/*.so.*
cp %{PATCH2} $RPM_BUILD_ROOT%{_bindir}/icu-config
chmod a+x $RPM_BUILD_ROOT%{_bindir}/icu-config
sed -i s/\\\$\(THREADSCXXFLAGS\)// $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/icu.pc
sed -i s/\\\$\(THREADSCPPFLAGS\)/-D_REENTRANT/ $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/icu.pc

%check
make -C source check


%clean
rm -rf $RPM_BUILD_ROOT


%post -n compat-libicu36 -p /sbin/ldconfig

%postun -n compat-libicu36 -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc license.html readme.html
%{_bindir}/derb
%{_bindir}/genbrk
%{_bindir}/gencnval
%{_bindir}/genctd
%{_bindir}/genrb
%{_bindir}/makeconv
%{_bindir}/pkgdata
%{_bindir}/uconv
%{_sbindir}/*
%{_mandir}/man1/derb.1*
%{_mandir}/man1/gencnval.1*
%{_mandir}/man1/genrb.1*
%{_mandir}/man1/genbrk.1*
%{_mandir}/man1/genctd.1*
%{_mandir}/man1/makeconv.1*
%{_mandir}/man1/pkgdata.1*
%{_mandir}/man1/uconv.1*
%{_mandir}/man8/*.8*

%files -n compat-libicu36
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files -n compat-libicu36-devel
%defattr(-,root,root,-)
%{_bindir}/icu-config
%{_mandir}/man1/icu-config.1*
%{_includedir}/layout
%{_includedir}/unicode
%{_libdir}/*.so
%{_libdir}/icu
%{_libdir}/pkgconfig/icu.pc
%dir %{_datadir}/icu
%dir %{_datadir}/icu/3.6
%{_datadir}/icu/3.6/mkinstalldirs
%{_datadir}/icu/3.6/config
%doc %{_datadir}/icu/3.6/license.html

%files -n compat-libicu36-doc
%defattr(-,root,root,-)
%doc source/__docs/icu/html/*


%changelog
* Wed Mar 20 2013 Remi Collet <RPMS@famillecollet.com> - 3.6-5.16.1
- new package from RHEL-5 spec of icu.

