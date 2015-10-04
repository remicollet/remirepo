# spec file for libbson
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    7afe7e98969889c442f780eda45172d33a1d9e8e
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     mongodb
%global gh_project   libbson
%global libver       1.0
%global prever       rc0
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

# TODO bundled yajl version 2.0.4
# See https://jira.mongodb.org/browse/CDRIVER-623

Name:      libbson
Summary:   Library to build, parse, and iterate BSON documents
Version:   1.2.0
Release:   0.2.%{prever}%{?dist}
License:   ASL 2.0
Group:     System Environment/Libraries
URL:       https://github.com/%{gh_owner}/%{gh_project}
Source0:   https://github.com/%{gh_owner}/%{gh_project}/releases/download/%{version}%{?prever:-%{prever}}/%{gh_project}-%{version}%{?prever:-%{prever}}.tar.gz
BuildRequires: python


%description
%{name} is a library providing useful routines related to building,
parsing, and iterating BSON documents. It is a useful base for those
wanting to write high-performance C extensions to higher level
languages such as python, ruby, or perl.


%package devel
Summary:    Header files and development libraries for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   pkgconfig


%description devel
This package contains the header files and development libraries
for %{name}.



%prep
%setup -q -n %{gh_project}-%{version}%{?prever:-%{prever}}


%build
%configure \
  --enable-man-pages

make %{_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}

rm    %{buildroot}%{_libdir}/*la
rm -r %{buildroot}%{_datadir}/doc


%check
: Run test suite
make check


%post   -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/%{name}-%{libver}.so.*


%files devel
%doc NEWS README
%{_includedir}/%{name}-%{libver}
%{_libdir}/%{name}-%{libver}.so
%{_libdir}/pkgconfig/%{name}-%{libver}.pc
%{_mandir}/man3/bson*


%changelog
* Sun Oct  4 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.2.rc0
- Update to 1.2.0-rc0

* Wed Apr 22 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.1.beta
- Initial package
- https://jira.mongodb.org/browse/CDRIVER-621 - typo in man pages
- https://jira.mongodb.org/browse/CDRIVER-623 - bundled jayl