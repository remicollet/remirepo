# remirepo spec file for libsodium-last
# renamed for parallel installation, from:
#
# Fedora spec file for libsodium
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global libname libsodium
%global soname  18

# soname 13 since 1.0.0
# soname 17 since 1.0.6
# soname 18 since 1.0.7

%if 0%{?fedora} >= 24
# Standard build
Name:           %{libname}
%else
# Build for parallel install
Name:           %{libname}-last
%endif
Version:        1.0.11
Release:        2%{?dist}
Summary:        The Sodium crypto library
Group:          System Environment/Libraries
License:        ISC
URL:            http://libsodium.org/
Source0:        http://download.libsodium.org/libsodium/releases/%{libname}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if "%{libname}" != "%{name}"
Provides:       %{libname}         = %{version}-%{release}
Provides:       %{libname}%{?_isa} = %{version}-%{release}
%else
Obsoletes:      %{libname}-last   <= %{version}
%endif


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

%package        static
Summary:        Static library for %{name}
Group:          Development/Libraries
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
%if "%{libname}" != "%{name}"
Conflicts:      %{libname}-static         < %{version}
Provides:       %{libname}-static         = %{version}-%{release}
Provides:       %{libname}-static%{?_isa} = %{version}-%{release}
%else
Obsoletes:      %{libname}-last-static   <= %{version}
%endif

%description    static
This package contains the static library for statically
linking applications to use %{name}.
%if "%{libname}" != "%{name}"
This package can't be installed with system %{libname}-static.
%endif


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa}          = %{version}-%{release}
%if "%{libname}" != "%{name}"
Conflicts:      %{libname}-devel         < %{version}
Provides:       %{libname}-devel         = %{version}-%{release}
Provides:       %{libname}-devel%{?_isa} = %{version}-%{release}
%else
Obsoletes:      %{libname}-last-devel   <= %{version}
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
%configure \
  --disable-silent-rules \
  --disable-opt

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
%{_libdir}/%{libname}.so.%{soname}*

%files devel
%defattr (-,root,root,-)
%doc AUTHORS ChangeLog README.markdown THANKS
%doc test/default/*.{c,exp,h}
%doc test/quirks/quirks.h
%{_includedir}/sodium.h
%{_includedir}/sodium/
%{_libdir}/%{libname}.so
%{_libdir}/pkgconfig/%{libname}.pc

%files static
%defattr (-,root,root,-)
%{_libdir}/libsodium.a

%changelog
* Mon Dec 12 2016 Neal Gompa <ngompa13@gmail.com> - 1.0.11-2
- Add static library subpackage

* Mon Aug  1 2016 Remi Collet <remi@fedoraproject.org> - 1.0.11-1
- update to 1.0.11

* Tue Apr  5 2016 Remi Collet <remi@fedoraproject.org> - 1.0.10-1
- update to 1.0.10

* Sat Apr  2 2016 Remi Collet <remi@fedoraproject.org> - 1.0.9-1
- update to 1.0.9

* Mon Mar  7 2016 Remi Collet <remi@fedoraproject.org> - 1.0.8-2
- obsolete libsodium-last in fedora

* Sat Dec 26 2015 Remi Collet <remi@fedoraproject.org> - 1.0.8-1
- update to 1.0.8

* Wed Dec  9 2015 Remi Collet <remi@fedoraproject.org> - 1.0.7-1
- update to 1.0.7
- soname bump to 18

* Wed Nov  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.6-1
- update to 1.0.6
- soname bump to 17

* Tue Oct 27 2015 Remi Collet <remi@fedoraproject.org> - 1.0.5-2
- update to 1.0.5
- provide libsodium

* Tue Oct 27 2015 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- update to 1.0.5

* Tue Oct 20 2015 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- update to 1.0.4
- add upstream patch for segfault on RHEL-6 i386
  https://github.com/jedisct1/libsodium/issues/307

* Sat May 16 2015 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- update to 1.0.3

* Tue Jan 20 2015 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2

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
