# remirepo/fedora spec file for libui
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit   f56411fde197481c00ad950e1a545452d47efa55
%global gh_date     20161102
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    andlabs
%global gh_project  libui
%global libname     libui
%global soname      0

Name:          %{libname}
Summary:       Simple and portable GUI library 
Version:       0
Release:       0.3.%{gh_date}git%{gh_short}%{?dist}
License:       MIT
Group:         System Environment/Libraries

URL:           https://github.com/andlabs/libui
Source0:       https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

%if 0%{?rhel}
BuildRequires: cmake3 >= 3.1.0
%else
BuildRequires: cmake  >= 3.1.0
%endif
BuildRequires: gtk3-devel


%description
Simple and portable (but not inflexible) GUI library in C that uses the native
GUI technologies of each platform it supports. 


%package devel
Summary:    Header files and development libraries for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%if 0%{?rhel}
sed -e 's/NOT APPLE/0/' -i CMakeLists.txt
%endif


%build
%if 0%{?rhel}
%cmake3
%else
%cmake
%endif

make %{_smp_mflags}


%install
: Library
install -Dm 755 out/%{libname}.so.%{soname} %{buildroot}%{_libdir}/%{libname}.so.%{soname}
ln -s %{libname}.so.%{soname} %{buildroot}%{_libdir}/%{libname}.so

: Headers
for header in ui.h ui_unix.h uitable.h; do
  install -Dpm 644 $header %{buildroot}%{_includedir}/$header
done


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license LICENSE
%{_libdir}/%{libname}.so.%{soname}*


%files devel
%doc *.md
%doc examples
%{_libdir}/%{libname}.so
%{_includedir}/ui*.h


%changelog
* Thu Nov  3 2016 Remi Collet <remi@fedoraproject.org> - 0-0.3.20161102gitf56411f
- refresh

* Fri Oct 28 2016 Remi Collet <remi@fedoraproject.org> - 0-0.3.20161026git5de62d0
- refresh

* Tue Oct 25 2016 Remi Collet <remi@fedoraproject.org> - 0-0.2.20161023git0870a30
- update to latest upstream snapshot for pecl/ui

* Tue Oct 25 2016 Remi Collet <remi@fedoraproject.org> - 0-0.1.alpha3.1
- initial package

