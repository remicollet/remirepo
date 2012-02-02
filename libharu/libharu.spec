Name:           libharu
Version:        2.2.1
Release:        1%{?dist}
Summary:        C library for generating PDF files

Group:          System Environment/Libraries
License:        zlib with acknowledgement
URL:            http://libharu.org
Source0:        http://libharu.org/files/%{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: glibc-headers
BuildRequires: libpng-devel
BuildRequires: zlib-devel


%description
libHaru is a library for generating PDF files. 
It is free, open source, written in ANSI C and cross platform.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static --enable-debug
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


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
