Name:          cmph
Version:       2.0
Release:       1%{?dist}
Summary:       Minimal hash C library
Group:         System Environment/Libraries
License:       MPLv1.1 or LGPLv2
URL:           http://cmph.sourceforge.net/
Source0:       http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libtool
BuildRequires: check-devel


%description
Cmph is a free minimal perfect hash C library, providing several algorithms
in the literature in a consistent, ease to use, API.


%package       devel
Summary:       Development files for Cmph library
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

# Fix sources permission
chmod -x src/*.{c,h}

# Honour RPM build flags
sed -e 's/-Wall/$CFLAGS/' -i configure.ac


%build
%if 0%{?rhel} == 5
: Use provided configure in EL5
%else
autoreconf -i --force
%endif

# --enable-cxxmph not used, build broken

%{configure} \
    --enable-check

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/lib%{name}.{a,la}


%check
make check


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING LGPL-2 MPL-1.1 README
%{_libdir}/lib%{name}.so.*
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}*
%{_includedir}/chd_ph.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Wed Oct  9 2013 Remi Collet <remi@feoraproject.org> - 2.0-1
- Initial package
