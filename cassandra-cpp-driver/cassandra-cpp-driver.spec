# remirepo/fedora spec file for cassandra-cpp-driver
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit   8e4f51422ea71c6ec2e9b8eb20b2bb3051a3d63a
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    datastax
%global gh_project  cpp-driver
%global libname     libcassandra
%global soname      2

Name:          cassandra-cpp-driver
Summary:       DataStax C/C++ Driver for Apache Cassandra
Version:       2.6.0
Release:       1%{?dist}
License:       ASL 2.0
Group:         System Environment/Libraries

URL:           http://datastax.github.io/cpp-driver/
Source0:       https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRequires: cmake >= 2.6.4
BuildRequires: libuv-devel
BuildRequires: openssl-devel


%description
%{summary}.

A modern, feature-rich, and highly tunable C/C++ client library for
Apache Cassandra (1.2+) and DataStax Enterprise (3.1+) using exclusively
Cassandra's native protocol and Cassandra Query Language v3.


%package devel
Summary:    Header files and development libraries for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

find examples -name .gitignore -exec rm {} \; -print


%build
%if 0%{?fedora} >= 26
export CXXFLAGS="$RPM_OPT_FLAGS -Wno-implicit-fallthrough"
%endif
%cmake

make %{_smp_mflags}


%install
make install DESTDIR="%{buildroot}"

rm %{buildroot}%{_libdir}/%{libname}_static.a
rm %{buildroot}%{_libdir}//pkgconfig/cassandra_static.pc


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%{_libdir}/%{libname}.so.%{soname}*


%files devel
%doc *.md
%doc examples
%{_libdir}/%{libname}.so
%{_includedir}/cassandra.h
%{_libdir}/pkgconfig/cassandra.pc


%changelog
* Fri Mar 10 2017 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0
- open https://datastax-oss.atlassian.net/browse/CPP-442
  Broken build on EL-6 64-bit

* Mon Mar  6 2017 Remi Collet <remi@fedoraproject.org> - 2.5.0-2
- use -Wno-implicit-fallthrough, workaround for GCC 7
- open https://datastax-oss.atlassian.net/browse/CPP-438
  Broken build with GCC 7 and OpenSSL 1.1

* Fri Oct 21 2016 Remi Collet <remi@fedoraproject.org> - 2.5.0-1
- update to 2.5.0

* Sat Sep  3 2016 Remi Collet <remi@fedoraproject.org> - 2.4.3-1
- update to 2.4.3

* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 2.4.2-1
- update to 2.4.2

* Fri Jun 10 2016 Remi Collet <remi@fedoraproject.org> - 2.4.1-1
- update to 2.4.1

* Tue Jun  7 2016 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- update to 2.4.0

* Fri Feb 12 2016 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- update to 2.2.2

* Thu Nov 26 2015 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- update to 2.2.1

* Thu Aug 13 2015 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- initial package
