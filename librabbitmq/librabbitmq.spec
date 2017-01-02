# remirepo spec file for librabbitmq-last
# renamed to allow parallel installation
#
# Fedora spec file for librabbitmq
#
# Copyright (c) 2012-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit   caad0ef1533783729c7644a226c989c79b4c497b
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    alanxz
%global gh_project  rabbitmq-c
%global libname     librabbitmq
# soname 4 since 0.6.0 (Fedora 23) 0.7.0/4.1, 0.8.0/4.2
# soname 1 up to 0.5.2
%global soname      4

%if 0%{?fedora} < 23
Name:      %{libname}-last
%else
Name:      %{libname}
%endif
Summary:   Client library for AMQP
Version:   0.8.0
Release:   1%{?dist}
License:   MIT
Group:     System Environment/Libraries
URL:       https://github.com/alanxz/rabbitmq-c

Source0:   https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if 0%{?rhel} == 5
BuildRequires: cmake28
BuildRequires: popt
%else
BuildRequires: cmake > 2.8
BuildRequires: popt-devel
%endif
BuildRequires: openssl-devel
# For man page
BuildRequires: xmlto

%if "%{name}" == "%{libname}"
Obsoletes:      %{libname}-last <= %{version}
%endif


%description
This is a C-language AMQP client library for use with AMQP servers
speaking protocol versions 0-9-1.
%if "%{name}" != %{libname}
This package is designed to be installed beside system %{libname}.
%endif


%package devel
Summary:    Header files and development libraries for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}
%if "%{name}" != %{libname}
Conflicts:  %{libname}-devel < %{version}
Provides:   %{libname}-devel = %{version}-%{release}
%else
Obsoletes:  %{libname}-last-devel <= %{version}
%endif

%description devel
This package contains the header files and development libraries
for %{name}.


%package tools
Summary:    Example tools built using the librabbitmq package
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}
%if "%{name}" != %{libname}
Conflicts:  %{libname}-tools < %{version}
Provides:   %{libname}-tools = %{version}-%{release}
%else
Obsoletes:  %{libname}-last-tools <= %{version}
%endif

%description tools
This package contains example tools built using %{name}.

It provides:
amqp-consume        Consume messages from a queue on an AMQP server
amqp-declare-queue  Declare a queue on an AMQP server
amqp-delete-queue   Delete a queue from an AMQP server
amqp-get            Get a message from a queue on an AMQP server
amqp-publish        Publish a message on an AMQP server


%prep
%setup -q -n %{gh_project}-%{gh_commit}

# Copy sources to be included in -devel docs.
cp -pr examples Examples


%build
# static lib required for tests
%if 0%{?rhel} == 5
%cmake28 \
%else
%cmake \
%endif
  -DBUILD_TOOLS_DOCS:BOOL=ON \
  -DBUILD_STATIC_LIBS:BOOL=ON

make %{_smp_mflags}


%install
make install  DESTDIR="%{buildroot}"

rm %{buildroot}%{_libdir}/%{libname}.a


%check
: check .pc is usable
grep @ %{buildroot}%{_libdir}/pkgconfig/librabbitmq.pc && exit 1

: upstream tests
make test


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr (-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE-MIT
%{_libdir}/%{libname}.so.%{soname}*


%files devel
%defattr (-,root,root,-)
%doc AUTHORS THANKS TODO *.md
%doc Examples
%{_libdir}/%{libname}.so
%{_includedir}/amqp*
%{_libdir}/pkgconfig/%{libname}.pc

%files tools
%defattr (-,root,root,-)
%{_bindir}/amqp-*
%doc %{_mandir}/man1/amqp-*.1*
%doc %{_mandir}/man7/librabbitmq-tools.7*


%changelog
* Tue Apr 12 2016 Remi Collet <remi@fedoraproject.org> - 0.8.0-1
- update to 0.8.0

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 0.7.1-1
- update to 0.7.1

* Fri Jul  3 2015 Remi Collet <remi@fedoraproject.org> - 0.7.0-1
- update to 0.7.0
- swicth to cmake
- switch from upstream tarball to github sources

* Mon Apr 20 2015 Remi Collet <remi@fedoraproject.org> - 0.6.0-1
- update to 0.6.0
- soname changed to .4
- rename to librabbitmq-last (except F23+)

* Mon Sep 15 2014 Remi Collet <remi@fedoraproject.org> - 0.5.2-1
- update to 0.5.2

* Wed Aug 13 2014 Remi Collet <remi@fedoraproject.org> - 0.5.1-1
- update to 0.5.1
- fix license handling
- move all documentation in devel subpackage

* Mon Feb 17 2014 Remi Collet <remi@fedoraproject.org> - 0.5.0-1
- update to 0.5.0
- open https://github.com/alanxz/rabbitmq-c/issues/169 (version is 0.5.1-pre)
- open https://github.com/alanxz/rabbitmq-c/issues/170 (amqp_get_server_properties)

* Mon Jan 13 2014 Remi Collet <remi@fedoraproject.org> - 0.4.1-4
- drop BR python-simplejson

* Tue Jan  7 2014 Remi Collet <remi@fedoraproject.org> - 0.4.1-3
- fix broken librabbitmq.pc, #1039555
- add check for usable librabbitmq.pc

* Thu Jan  2 2014 Remi Collet <remi@fedoraproject.org> - 0.4.1-2
- fix Source0 URL

* Sat Sep 28 2013 Remi Collet <remi@fedoraproject.org> - 0.4.1-1
- update to 0.4.1
- add ssl support

* Thu Aug  1 2013 Remi Collet <remi@fedoraproject.org> - 0.3.0-3
- cleanups

* Wed Mar 13 2013 Remi Collet <remi@fedoraproject.org> - 0.3.0-2
- remove tools from main package

* Wed Mar 13 2013 Remi Collet <remi@fedoraproject.org> - 0.3.0-1
- update to 0.3.0
- create sub-package for tools

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-0.2.git2059570
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 01 2012 Remi Collet <remi@fedoraproject.org> - 0.2-0.1.git2059570
- update to latest snapshot (version 0.2, moved to github)
- License is now MIT

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.3.hgfb6fca832fd2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 11 2012 Remi Collet <remi@fedoraproject.org> - 0.1-0.2.hgfb6fca832fd2
- add %%check (per review comment)

* Sat Mar 10 2012 Remi Collet <remi@fedoraproject.org> - 0.1-0.1.hgfb6fca832fd2
- Initial RPM

