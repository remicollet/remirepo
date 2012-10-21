%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_include:  %global python_include  %(%{__python} -c "from distutils.sysconfig import get_python_inc; print get_python_inc(0)")}

Summary:        Portable C library for dynamically generating PDF files
Name:           pdflib-lite
# Remenber to check the URL after changing this...
Version:        7.0.5
Release:        3%{?dist}
License:        Distributable
Group:          System Environment/Libraries
URL:            http://www.pdflib.com/

Source:         http://www.pdflib.com/binaries/PDFlib/705/PDFlib-Lite-%{version}.tar.gz

Patch0:         pdflib-lite-7.0.4-gcc43.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
PDFlib is a development tool for PDF-enabling your software, 
or generating PDF on your server. PDFlib offers a simple-to-use API
for programmatically creating PDF files from within your own server- 
or client-side software. PDFlib doesn't make use of third-party software
for generating PDF, nor does it require any other tools.

%package devel
Summary:        Development files for pdflib
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
PDFlib is a development tool for PDF-enabling your software, 
or generating PDF on your server. PDFlib offers a simple-to-use API
for programmatically creating PDF files from within your own server- 
or client-side software. PDFlib doesn't make use of third-party software
for generating PDF, nor does it require any other tools.

This package contains the files needed for compiling programs that will use
the PDFlib library.

%package python
Summary:        Python shared library for pdflib
Group:          System Environment/Libraries
BuildRequires:  python-devel
Requires:       %{name} = %{version}-%{release}
Provides:       python-pdflib = %{version}-%{release}

%description python
PDFlib is a development tool for PDF-enabling your software, 
or generating PDF on your server. PDFlib offers a simple-to-use API
for programmatically creating PDF files from within your own server- 
or client-side software. PDFlib doesn't make use of third-party software
for generating PDF, nor does it require any other tools.

This package contains the library needed for python programs 
that will use the PDFlib library.

%package perl
Summary:        Perl shared library for pdflib
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Provides:       perl-pdflib = %{version}-%{release}
%if 0%{?fedora} >= 7 || 0%{?rhel} >= 6
BuildRequires:  perl-devel
%endif

%description perl
PDFlib is a development tool for PDF-enabling your software, 
or generating PDF on your server. PDFlib offers a simple-to-use API
for programmatically creating PDF files from within your own server- 
or client-side software. PDFlib doesn't make use of third-party software
for generating PDF, nor does it require any other tools.

This package contains the library needed for perl programs 
that will use the PDFlib library.


%prep
%setup -q -n PDFlib-Lite-%{version}
%patch0 -p0 -b .gcc43

sed -i -e 's,^PYTHONLIBDIR.*,PYTHONLIBDIR = %{python_sitearch},' \
       -e 's,^PERLLIBDIR.*,PERLLIBDIR = %{perl_vendorarch},' \
       config/mkcommon.inc.in

%build
# C, CPP, perl and python bindings enabled
# java, ruby and tcl disabled
# File a bug with RFE and patch if you need it
%configure \
    --with-pyincl=%{python_include} \
    --with-java=no \
    --with-ruby=no \
    --with-tcl=no \
    --enable-large_files --enable-tiffwrite

# for x86_64 build
sed -i -e s@/usr/lib@%{_libdir}@ libtool

%{__make} %{?_smp_mflags}
for lang in perl python
do
  %{__make} -C bind/pdflib/$lang
done

%install
rm -rf %{buildroot} examples
mkdir -p %{buildroot}%{python_sitearch}
mkdir -p %{buildroot}%{perl_vendorarch}

make install DESTDIR=%{buildroot}
for lang in perl python
do
  make -C bind/pdflib/$lang install DESTDIR=%{buildroot}
done

install -p -m 0644 bind/pdflib/cpp/pdflib.hpp %{buildroot}%{_includedir}/pdflib.hpp

rm %{buildroot}%{_libdir}/*.{la,a}
rm %{buildroot}%{python_sitearch}/*.{la,a}
rm %{buildroot}%{perl_vendorarch}/*.{la,a}

# require to extract debuginfo
chmod +x %{buildroot}%{_libdir}/libpdf*
chmod +x %{buildroot}%{python_sitearch}/pdflib_py.so*
chmod +x %{buildroot}%{perl_vendorarch}/pdflib_pl.so*

# Only sources
mkdir -p examples/{c,cpp,perl,php,python}
cp -r bind/pdflib/data examples/data
cp bind/pdflib/c/*.c \
   bind/pdflib/c/Makefile \
   bind/pdflib/c/readme.txt \
   examples/c
cp bind/pdflib/cpp/*.cpp \
   bind/pdflib/cpp/Makefile \
   bind/pdflib/cpp/readme.txt \
   examples/cpp
cp bind/pdflib/perl/*.pl \
   bind/pdflib/perl/Makefile \
   bind/pdflib/perl/readme.txt \
   examples/perl
cp bind/pdflib/python/*.py \
   bind/pdflib/python/Makefile \
   bind/pdflib/python/readme.txt \
   examples/python
cp bind/pdflib/php/*.php \
   bind/pdflib/php/readme.txt \
   examples/php
# overwrite the default php4 one
cp bind/pdflib/php/examples.php5/*.php \
   examples/php


%clean
rm -rf %{buildroot}


%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-, root, root, -)
%doc readme.txt doc/pdflib/PDFlib-Lite-license.pdf
%{_bindir}/pdfimage
%{_bindir}/text2pdf
%{_libdir}/*.so.*


%files devel
%defattr(-, root, root, -)
%doc doc/pdflib/PDFlib-Lite-license.pdf
%doc doc/pdflib/changes.txt doc/pdflib/compatibility.txt examples
%doc doc/pdflib/PDFlib-API-reference.pdf doc/pdflib/PDFlib-tutorial.pdf doc/pdflib/readme-source-unix.txt
%{_bindir}/pdflib-config
%{_includedir}/*
%{_libdir}/*.so


%files python
%defattr(-, root, root, -)
%doc doc/pdflib/PDFlib-Lite-license.pdf
%{python_sitearch}/pdflib_py.so*


%files perl
%defattr(-, root, root, -)
%doc doc/pdflib/PDFlib-Lite-license.pdf
%{perl_vendorarch}/pdflib_pl.*


%changelog
* Sun Oct 21 2012 Remi Collet <Fedora@FamilleCollet.com> 7.0.5-3
- rebuild

* Wed Oct 10 2012 Nicolas Chauvet <kwizart@gmail.com> - 7.0.5-3
- Rebuilt for perl

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 7.0.5-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Jul 23 2011 Remi Collet <Fedora@FamilleCollet.com> 7.0.5-1.1
- BR perl-devel on EL-6

* Thu May 06 2010 Remi Collet <Fedora@FamilleCollet.com> 7.0.5-1
- update to 7.0.5

* Sat Jun 13 2009 Remi Collet <Fedora@FamilleCollet.com> 7.0.4p4-1
- update to 7.0.4p4

* Thu Mar 19 2009 Remi Collet <Fedora@FamilleCollet.com> 7.0.4p1-1
- update to 7.0.4p1

* Thu Mar 19 2009 Remi Collet <Fedora@FamilleCollet.com> 7.0.4-1
- update to 7.0.4

* Sat Dec 20 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 7.0.3-3
- rebuild for python 2.6

* Sun Sep 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 7.0.3-2
- rebuild

* Fri Mar 28 2008 Remi Collet <Fedora@FamilleCollet.com> 7.0.3-1
- update to 7.0.3
- fix CVE-2007-6561: PDFlib stack-based buffer overflows

* Sat Mar 15 2008 Thorsten Leemhuis <fedora at leemhuis.info> 7.0.2p8-2
- rebuild for new perl

* Fri Feb 29 2008 Remi Collet <Fedora@FamilleCollet.com> 7.0.2p8-1
- update to 7.0.2p8
- del destdir.patch ("make install DESTDIR" is now ok)
- add gcc43.patch for Fedora 9

* Thu Aug 16 2007 Remi Collet <Fedora@FamilleCollet.com> 7.0.2-1
- Add BR perl-devel for fedora >= 7

* Thu Aug 16 2007 Remi Collet <Fedora@FamilleCollet.com> 7.0.2-1
- update to 7.0.2

* Thu Mar 15 2007 Remi Collet <Fedora@FamilleCollet.com> 7.0.1-1
- update to 7.0.1

* Mon Dec 18 2006 Remi Collet <Fedora@FamilleCollet.com> 7.0.0p3-3
- review for Livna
- Requires/BuildRequires cleanup
- Change License = Distributable, include PDFlib-Lite-license.pdf in sub-packages
- add --with-pyinc, python2.5 not defined in configure
- add some comments

* Sun Dec 10 2006 Remi Collet <Fedora@FamilleCollet.com> 7.0.0p3-2
- add python subpackage
- add perl subpackage

* Sat Dec 09 2006 Remi Collet <Fedora@FamilleCollet.com> 7.0.0p3-1
- initial release for Extras
