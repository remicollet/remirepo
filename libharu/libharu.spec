Name:           libharu
Version:        2.2.1
Release:        2%{?dist}
Summary:        C library for generating PDF files

Group:          System Environment/Libraries
License:        zlib with acknowledgement
URL:            http://libharu.org
Source0:        http://libharu.org/files/%{name}-%{version}.tar.gz
Patch0:         libharu-2.2.1-png15.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  glibc-headers
BuildRequires:  libpng-devel
BuildRequires:  zlib-devel


%description
libHaru is a library for generating PDF files. 
It is free, open source, written in ANSI C and cross platform.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -b .png15

# honours flag
sed -e '/CFLAGS/s/-O0/-O2/' \
    -e '/CFLAGS/s/-g3/-g/' \
    -i configure


%build
%configure --disable-static --enable-debug
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README 
%{_libdir}/libhpdf-%{version}.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/libhpdf.so



%changelog
* Tue Aug 26 2014 Remi Collet <remi@fedoraproject.org> - 2.2.1-2
- add libpng15 patch from rawhide
- honour compilation options

* Thu Feb 02 2012 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- update to 2.2.1 for remi repo

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Mar 23 2010 Alex71 <nyrk71@gmail.com> 2.1.0-2
- put libhpdf.so in the devel package and libhpdf-2.1.0.so in the main one
- removed duplicated README and CHANGES from devel package
- fixed "E: empty-debuginfo-package" with --enable-debug flag in configure
- removed INSTALL file
- added demo/ directory in doc (devel only) as doc 
* Sat Mar 20 2010 Alex71 <nyrk71@gmail.com> 2.1.0-1
- First release for Fedora
