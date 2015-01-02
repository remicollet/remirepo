# spec file for termbox
#
# Copyright (c) 2014-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    7cdd648ab890764fda6a3ce5da08f60e4392aa8e
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_date      20140912
%global gh_owner     nsf
%global gh_project   termbox

Name:          termbox
Version:       1.1.0
Release:       0.1.%{gh_date}git%{gh_short}%{?dist}
Summary:       Minimalist library for text-based user interfaces
Group:         System Environment/Libraries

License:       MIT
URL:           https://github.com/%{gh_owner}/%{gh_project}
Source0:       https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?gh_date:-%{gh_short}}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
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
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/lib%{name}.so.*

%files devel
%defattr(-,root,root,-)
%doc README
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so


%changelog
* Fri Sep 12 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-0.1.20140912git7cdd648
- initial package