# remirepo spec file for hdrhistogram
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit   4c4112a19e5359bb6c74ea5c393e0a59dd012532
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    HdrHistogram
%global gh_project  HdrHistogram_c
%global libname     libhdr_histogram
%global soname      1

Name:          hdrhistogram
Summary:       A High Dynamic Range (HDR) Histogram
Version:       0.9.5
Release:       1%{?dist}
License:       CC0 or BSD
Group:         System Environment/Libraries

URL:           https://github.com/%{gh_owner}/%{gh_project}
Source0:       https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# build with fPIC
Patch0:        %{name}-fpic.patch

BuildRequires: cmake > 2.8
BuildRequires: zlib-devel

Requires:   %{name}-libs%{?_isa} = %{version}-%{release}


%description
HdrHistogram: A High Dynamic Range (HDR) Histogram.

This port contains a subset of the functionality supported
by the Java implementation. The current supported features are:

- Standard histogram with 64 bit counts (32/16 bit counts not supported)
- All iterator types (all values, recorded, percentiles, linear, logarithmic)
- Histogram serialisation (encoding version 1.2, decoding 1.0-1.2)
- Reader/writer phaser and interval recorder


%package devel
Summary:    Header files and development libraries for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}.


%package libs
Summary:    A High Dynamic Range (HDR) Histogram C library
Group:      System Environment/Libraries

%description libs
This package contains the %{libname} library.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mkdir docs
cp -pr examples docs/examples

%patch0 -p1 -b .fpic

grep CMAKE_C_FLAGS CMakeLists.txt


%build
export CFLAGS="%{optflags} -Wno-unknown-pragmas -std=gnu99"

%if 0%{?rhel} == 5
%cmake28 .
%else
%cmake .
%endif

make %{_smp_mflags}


%install
make install DESTDIR="%{buildroot}"

# https://github.com/HdrHistogram/HdrHistogram_c/issues/32
install -p src/hdr_thread.h %{buildroot}%{_includedir}/hdr/hdr_thread.h

rm %{buildroot}/%{_libdir}/%{libname}_static.a
rm %{buildroot}/%{_bindir}/*test


%check
make test


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%doc *.md
%{_bindir}/hiccup
%{_bindir}/hdr_decoder

%files libs
%{!?_licensedir:%global license %%doc}
%license COPYING.txt
%license LICENSE.txt
%{_libdir}/%{libname}.so.%{soname}*

%files devel
%doc *.md
%doc docs/examples
%{_libdir}/%{libname}.so
%{_includedir}/hdr


%changelog
* Sun Sep  4 2016 Remi Collet <remi@fedoraproject.org> - 0.9.5-1
- update to 0.9.5

* Mon Jul 18 2016 Remi Collet <remi@fedoraproject.org> - 0.9.4-1
- update to 0.9.4

* Wed Apr  6 2016 Remi Collet <remi@fedoraproject.org> - 0.9.3-1
- update to 0.9.3

* Fri Jan  1 2016 Remi Collet <remi@fedoraproject.org> - 0.9.1-1
- initial package
