%define major	0

Name:		libircclient
Summary:	C library to create IRC clients
Version:	1.6
Release:	6%{?dist}
License:	LGPLv3+
Group:		Development/Libraries
URL:		http://www.ulduzsoft.com/libircclient/
Source0:	http://downloads.sourceforge.net/libircclient/%{name}-%{version}.tar.gz
BuildRequires:	openssl-devel
# Correct install target to use includedir and libdir
Patch0:		libircclient-1.6-install.patch
# Add rfc include to main header to avoid build failures of packages using it
# example: error: 'LIBIRC_RFC_RPL_ENDOFNAMES' was not declared in this scope
Patch1:		libircclient-1.6-rfc.patch
# Create a dynamic library by default. Upstream report about patches:
# https://sourceforge.net/tracker/?func=detail&aid=3522604&group_id=118640&atid=681658
Patch2:		libircclient-1.6-shared.patch

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
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure --enable-shared --enable-openssl --enable-ipv6
make %{?_smp_mflags}

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc Changelog
%doc LICENSE
%doc THANKS
%{_libdir}/*.so.%{major}

%files		devel
%defattr(-,root,root,-)
%doc doc/html/*
%doc doc/rfc1459.txt
%{_libdir}/libircclient.so
%{_includedir}/libirc*.h

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 5 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.6-3
- Add Changelog, LICENSE, and THANKS files to main package.

* Fri May 4 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.6-2
- Add patch to create a shared library.
- Add documentation to devel package.

* Sat Apr 28 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.6-1
- Initial libircclient spec.
