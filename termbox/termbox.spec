# spec file for termbox
#
# Copyright (c) 2014-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    aba34487481da9c7102573f8f5db1be469386a72
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
#global gh_date      20140912
%global gh_owner     nsf
%global gh_project   termbox

Name:          termbox
Version:       1.1.0
Release:       1%{?dist}
Summary:       Minimalist library for text-based user interfaces
Group:         System Environment/Libraries

License:       MIT
URL:           https://github.com/%{gh_owner}/%{gh_project}
Source0:       https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRequires: waf


%description
Termbox is a library that provides minimalist API which allows the
programmer to write text-based user interfaces.


%package devel
Summary:    Header files and development libraries for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

rm waf


%build
export CFLAGS="%{optflags}"

%{_bindir}/waf configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir}

%{_bindir}/waf build %{?_smp_mflags}


%install
%{_bindir}/waf install \
    --targets=termbox_shared \
    --destdir=%{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/lib%{name}.so.*

%files devel
%doc README.rst
%doc src/demo/
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so


%changelog
* Thu Sep  1 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0

* Fri Sep 12 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-0.1.20140912git7cdd648
- initial package
