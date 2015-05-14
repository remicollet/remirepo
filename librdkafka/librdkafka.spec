# remirepo/fedora spec file for librdkafka
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global libname      librdkafka
%global gh_commit    25d879180d83f8789291d1a6fdb657ee7b50ec40
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     edenhill
%global gh_project   %{libname}

Name:    %{libname}
Version: 0.8.6
Release: 1%{?dist}
Group:   System Environment/Libraries
Summary: Apache Kafka C/C++ client library

# librdkafka is BSD-2, pycrc is MIT, snappy is BSD-3
License: BSD and MIT
URL:     https://github.com/%{gh_owner}/%{gh_project}
Source0: https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Needed to run the test suite
# find regress/ -type f | /usr/lib/rpm/perl.req
BuildRequires:  zlib-devel
BuildRequires:  libstdc++-devel
BuildRequires:  gcc-c++


%description
librdkafka is a C library implementation of the Apache Kafka protocol,
containing both Producer and Consumer support.

It was designed with message delivery reliability and high performance
in mind, current figures exceed 800000 msgs/second for the producer
and 3 million msgs/second for the consumer.


%package devel
Group:    Development/Libraries
Summary:  Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -qn %{gh_project}-%{gh_commit}

mkdir rpmdocs
cp -pr examples rpmdocs/examples

# See https://github.com/edenhill/librdkafka/issues/277
sed -e 's/-Werror //' -i mklove/modules/configure.good_cflags


%build
%configure

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

rm %{buildroot}%{_libdir}/*.a

# https://github.com/edenhill/librdkafka/issues/275
if test -f %{buildroot}%{_libdir}/pkgconfig/rdkafka.pc
then
  : pkgconfig installed, can clean this test
else
  install -Dpm 0644 rdkafka.pc %{buildroot}%{_libdir}/pkgconfig/rdkafka.pc
fi


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE*
%{_libdir}/%{libname}.so.1
%{_libdir}/%{libname}++.so.1

%files devel
%defattr(-,root,root,-)
%doc *md
%doc rpmdocs/examples
%{_includedir}/%{libname}/
%{_libdir}/%{libname}.so
%{_libdir}/%{libname}++.so
%{_libdir}/pkgconfig/rdkafka.pc


%changelog
* Thu May 14 2015 Remi Collet <remi@fedoraproject.org> - 0.8.6-1
- initial package