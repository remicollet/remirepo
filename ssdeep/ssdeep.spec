# spec file for ssdeep
#
# Copyright (c) 2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#

Name:      ssdeep
Version:   2.10
Release:   1%{?dist}
Summary:   Compute context triggered piecewise hashes
Group:     Development/Tools

License:   GPLv2+
URL:       http://ssdeep.sourceforge.net/
Source0:   http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:  %{name}-libs%{?_isa} = %{version}-%{release}


%description
ssdeep is a program for computing context triggered piecewise hashes (CTPH).
Also called fuzzy hashes, CTPH can match inputs that have homologies.
Such inputs have sequences of identical bytes in the same order, although bytes
in between these sequences may be different in both content and length.


%package devel
Summary: Development files for libfuzzy
Group:   Development/Libraries
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains library and header files for
developing applications that use libfuzzy.


%package libs
Summary: Runtime libfuzzy library
Group:   System Environment/Libraries

%description libs
The %{name}-libs package contains libraries needed by applications
that use libfuzzy.


%prep
%setup -q


%build
%configure --disable-static

# rpath removal
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

rm %{buildroot}%{_libdir}/libfuzzy.la


%clean
rm -rf %{buildroot}


%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.*

%files devel
%defattr(-,root,root,-)
%doc FILEFORMAT NEWS README TODO
%{_includedir}/fuzzy.h
%{_libdir}/libfuzzy.so

%files libs
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libfuzzy.so.2*


%changelog
* Wed Jan 22 2014 Remi Collet <remi@fedoraproject.org> - 2.10-1
- initial package