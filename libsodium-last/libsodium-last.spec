%global libname libsodium

%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7
# Standard build
Name:           %{libname}
%else
# Build for parallel install
Name:           %{libname}-last
%endif
Version:        1.0.2
Release:        1%{?dist}
Summary:        The Sodium crypto library
Group:          System Environment/Libraries
License:        ISC
URL:            http://libsodium.org/
Source0:        http://download.libsodium.org/libsodium/releases/%{libname}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
Sodium is a new, easy-to-use software library for encryption, decryption, 
signatures, password hashing and more. It is a portable, cross-compilable, 
installable, packageable fork of NaCl, with a compatible API, and an extended 
API to improve usability even further. Its goal is to provide all of the core 
operations needed to build higher-level cryptographic tools. The design 
choices emphasize security, and "magic constants" have clear rationales.

The same cannot be said of NIST curves, where the specific origins of certain 
constants are not described by the standards. And despite the emphasis on 
higher security, primitives are faster across-the-board than most 
implementations of the NIST standards.
%if "%{libname}" != "%{name}"
This package can be installed beside system %{libname}.
%endif


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa}          = %{version}-%{release}
%if "%{libname}" != "%{name}"
Conflicts:      %{libname}-devel         < %{version}
Provides:       %{libname}-devel         = %{version}-%{release}
Provides:       %{libname}-devel%{?_isa} = %{version}-%{release}
%endif

%description    devel
This package contains libraries and header files for
developing applications that use %{name} libraries.
%if "%{libname}" != "%{name}"
This package can't be installed with system %{libname}-devel.
%endif


%prep
%setup -q -n %{libname}-%{version}

%build
%configure --disable-static --disable-silent-rules
make %{_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/%{libname}.la


%check
make check


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr (-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/%{libname}.so.13*

%files devel
%defattr (-,root,root,-)
%doc AUTHORS ChangeLog README.markdown THANKS
%doc test/default/*.{c,h}
%{_includedir}/sodium.h
%{_includedir}/sodium/
%{_libdir}/%{libname}.so
%{_libdir}/pkgconfig/%{libname}.pc


%changelog
* Tue Jan 20 2015 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.1

* Sat Nov 22 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1

* Sun Sep 28 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- rename to libsodium-last (fedora <= 20, el <= 6)
- update to 1.0.0 (abi is now stable)
- fix license handling

* Sun Aug 24 2014 Christopher Meng <rpm@cicku.me> - 0.7.0-1
- Update to 0.7.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Christopher Meng <rpm@cicku.me> - 0.6.1-1
- Update to 0.6.1

* Thu Jul 03 2014 Christopher Meng <rpm@cicku.me> - 0.6.0-1
- Update to 0.6.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Christopher Meng <rpm@cicku.me> - 0.5.0-1
- Update to 0.5.0

* Mon Dec 09 2013 Christopher Meng <rpm@cicku.me> - 0.4.5-3
- Disable silent build rules.
- Preserve the timestamp.

* Wed Nov 20 2013 Christopher Meng <rpm@cicku.me> - 0.4.5-2
- Add doc for devel package.
- Add support for EPEL6.

* Wed Nov 20 2013 Christopher Meng <rpm@cicku.me> - 0.4.5-1
- Update to 0.4.5

* Wed Jul 10 2013 Christopher Meng <rpm@cicku.me> - 0.4.2-2
- Drop useless files.
- Improve the description.

* Wed Jul 10 2013 Christopher Meng <rpm@cicku.me> - 0.4.2-1
- Initial Package.
