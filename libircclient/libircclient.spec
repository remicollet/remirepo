%define major	0

Name:		libircclient
Summary:	C library to create IRC clients
Version:	1.7
Release:	1%{?dist}
License:	LGPLv3+
Group:		Development/Libraries
URL:		http://www.ulduzsoft.com/libircclient/
Source0:	http://downloads.sourceforge.net/libircclient/%{name}-%{version}.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	openssl-devel
# Correct install target to use includedir and libdir
Patch0:		libircclient-1.7-install.patch
# Add rfc include to main header to avoid build failures of packages using it
# example: error: 'LIBIRC_RFC_RPL_ENDOFNAMES' was not declared in this scope
Patch1:		libircclient-1.7-rfc.patch
# According to http://upstream-tracker.org/versions/libircclient.html
# no ABI change between 1.6 and 1.7
# so keep APIVERSION=0 as in our previous build of 1.6
Patch2:		libircclient-1.7-soname.patch

%description
libircclient is a small but extremely powerful library which implements
the IRC protocol. It is designed to be small, fast, portable and compatible
with the RFC standards as well as non-standard but popular features.
It is perfect for building the IRC clients and bots.

%package	devel
Summary:	Development files for libircclient
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
This package contains development files for libircclient.

%prep
%setup -q
rm -rvf cocoa
%patch0 -p1 -b .inst
%patch1 -p1 -b .rfc
%patch2 -p1 -b .shared

%build
%configure --enable-shared --enable-openssl --enable-ipv6
make %{?_smp_mflags}

# TODO make documentation and man page


%install
rm -rf ${RPM_BUILD_ROOT}

make install DESTDIR=${RPM_BUILD_ROOT}

# this header is not supposed to be installed
# but it is used by pecl/ircclient
install -pm 644 src/params.h ${RPM_BUILD_ROOT}%{_includedir}/libirc_params.h

# Man page
install -Dpm 644 man/%{name}.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/%{name}.1


%clean
rm -rf ${RPM_BUILD_ROOT}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc Changelog
%doc LICENSE
%doc THANKS
%{_libdir}/%{name}.so.%{major}

%files		devel
%defattr(-,root,root,-)
%{_libdir}/%{name}.so
%{_includedir}/libirc*.h
%{_mandir}/man1/%{name}.*

%changelog
* Fri Jan 10 2014 Remi Collet <remi.fedoraproject.org> - 1.7-1
- update to 1.7, no ABI change

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat May  5 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.6-3
- Add Changelog, LICENSE, and THANKS files to main package.

* Fri May  4 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.6-2
- Add patch to create a shared library.
- Add documentation to devel package.

* Sat Apr 28 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.6-1
- Initial libircclient spec.
