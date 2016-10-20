# remirepo/fedora spec file for mongo-c-driver
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_owner     mongodb
%global gh_project   mongo-c-driver
%global libname      libmongoc
%global libver       1.0
%global prever       rc3
%global bsonver      1.5

%ifarch x86_64
%global with_tests   0%{!?_without_tests:1}
%else
# See https://jira.mongodb.org/browse/CDRIVER-1186
# 32-bit MongoDB support was officially deprecated
# in MongoDB 3.2, and support is being removed in 3.4.
%global with_tests   0%{?_with_tests:1}
%endif

Name:      mongo-c-driver
Summary:   Client library written in C for MongoDB
Version:   1.5.0
Release:   0.3.%{prever}%{?dist}
License:   ASL 2.0
Group:     System Environment/Libraries
URL:       https://github.com/%{gh_owner}/%{gh_project}

Source0:   https://github.com/%{gh_owner}/%{gh_project}/releases/download/%{version}%{?prever:-%{prever}}/%{gh_project}-%{version}%{?prever:-%{prever}}.tar.gz

BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(libbson-1.0) > %{bsonver}
%if 0%{?fedora} > 21 || 0%{?rhel} > 6
BuildRequires: pkgconfig(libsasl2)
%else
BuildRequires: cyrus-sasl-devel
%endif
%if %{with_tests}
BuildRequires: mongodb-server
BuildRequires: openssl
%endif
BuildRequires: perl
# From man pages
BuildRequires: python

Requires:   %{name}-libs%{?_isa} = %{version}-%{release}
# Sub package removed
Obsoletes:  %{name}-tools         < 1.3.0
Provides:   %{name}-tools         = %{version}
Provides:   %{name}-tools%{?_isa} = %{version}


%description
%{name} is a client library written in C for MongoDB.


%package libs
Summary:    Shared libraries for %{name}
Group:      Development/Libraries

%description libs
This package contains the shared libraries for %{name}.


%package devel
Summary:    Header files and development libraries for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   pkgconfig

%description devel
This package contains the header files and development libraries
for %{name}.

Documentation: http://api.mongodb.org/c/%{version}/


%prep
%setup -q -n %{gh_project}-%{version}%{?prever:-%{prever}}

rm -r src/libbson

# Ignore check for libbson version = libmongoc version
sed -e 's/libbson-1.0 >= \$MONGOC_RELEASED_VERSION/libbson-1.0 >= %{bsonver}/' \
    -i configure


%build
export LIBS=-lpthread

%configure \
  --enable-debug-symbols \
  --enable-shm-counters \
  --disable-automatic-init-and-cleanup \
  --enable-crypto-system-profile \
%if %{with_tests}
  --enable-tests \
%else
  --disable-tests \
%endif
  --enable-sasl \
  --enable-ssl \
  --with-libbson=system \
  --disable-html-docs \
  --enable-man-pages

make %{_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}

rm    %{buildroot}%{_libdir}/*la
rm -r %{buildroot}%{_datadir}/doc/


%check
%if %{with_tests}
: Run a server
mkdir dbtest
mongod \
  --journal \
  --bind_ip     127.0.0.1 \
  --unixSocketPrefix /tmp \
  --logpath     $PWD/server.log \
  --pidfilepath $PWD/server.pid \
  --dbpath      $PWD/dbtest \
  --fork

: Run the test suite
ret=0
export MONGOC_TEST_OFFLINE=on
make check || ret=1

: Cleanup
[ -s server.pid ] && kill $(cat server.pid)

exit $ret
%endif


%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig


%files
%{_bindir}/mongoc-stat

%files libs
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/%{libname}-%{libver}.so.*

%files devel
%doc NEWS README*
%{_includedir}/%{libname}-%{libver}
%{_libdir}/%{libname}-%{libver}.so
%{_libdir}/pkgconfig/%{libname}-*.pc
%{_mandir}/man3/mongoc*


%changelog
* Thu Oct 20 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.3.rc3
- update to 1.5.0-rc3
- drop patches merged upstream

* Fri Oct 14 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.2.rc2
- open https://jira.mongodb.org/browse/CDRIVER-1703 missing files
- open https://jira.mongodb.org/browse/CDRIVER-1702 broken test
- enable test suite

* Fri Oct 14 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.1.rc2
- update to 1.5.0-rc2
- disable test suite

* Thu Aug 11 2016 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- update to 1.4.0
- drop API patch merged upstream

* Mon Aug  8 2016 Remi Collet <remi@fedoraproject.org> - 1.4.0-0.1.beta1
- update to 1.4.0-beta1
- build with --enable-system-crypto-profile option
- open https://jira.mongodb.org/browse/CDRIVER-1457 (symbols)
- open https://github.com/mongodb/mongo-c-driver/pull/385
- drop crypto patch merged upstream

* Mon May 16 2016 Remi Collet <remi@fedoraproject.org> - 1.3.5-2
- add patch to enforce system crypto policies

* Thu Mar 31 2016 Remi Collet <remi@fedoraproject.org> - 1.3.5-1
- update to 1.3.5
- use --disable-automatic-init-and-cleanup build option
- ignore check for libbson version = libmongoc version

* Sat Mar 19 2016 Remi Collet <remi@fedoraproject.org> - 1.3.4-2
- build with MONGOC_NO_AUTOMATIC_GLOBALS

* Tue Mar 15 2016 Remi Collet <remi@fedoraproject.org> - 1.3.4-1
- update to 1.3.4
- drop patch merged upstream

* Mon Feb 29 2016 Remi Collet <remi@fedoraproject.org> - 1.3.3-2
- cleanup for review
- move libraries in "libs" sub-package
- add patch to skip online tests
  open https://github.com/mongodb/mongo-c-driver/pull/314
- temporarily disable test suite on arm  (#1303864)
- temporarily disable test suite on i686/F24+ (#1313018)

* Sun Feb  7 2016 Remi Collet <remi@fedoraproject.org> - 1.3.3-1
- Update to 1.3.3

* Tue Feb  2 2016 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- Update to 1.3.2

* Thu Jan 21 2016 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1

* Wed Dec 16 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0
- move tools in devel package

* Tue Dec  8 2015 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3

* Tue Dec  8 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0
- open https://jira.mongodb.org/browse/CDRIVER-1040 - ABI breaks

* Wed Oct 14 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Sun Oct  4 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.6.rc0
- Update to 1.2.0-rc0

* Fri Sep 11 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.5.20150903git3eaf73e
- add patch to export library verson in the API
  open https://github.com/mongodb/mongo-c-driver/pull/265

* Fri Sep  4 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.4.20150903git3eaf73e
- update to version 1.2.0beta1 from git snapshot
- https://jira.mongodb.org/browse/CDRIVER-828 missing tests/json

* Mon Aug 31 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.3.beta
- more upstream patch (for EL-6)

* Mon Aug 31 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.2.beta
- Upstream version 1.2.0beta

* Wed May 20 2015 Remi Collet <remi@fedoraproject.org> - 1.1.6-1
- Upstream version 1.1.6

* Mon May 18 2015 Remi Collet <remi@fedoraproject.org> - 1.1.5-1
- Upstream version 1.1.5

* Sat Apr 25 2015 Remi Collet <remi@fedoraproject.org> - 1.1.4-3
- test build for upstream patch

* Thu Apr 23 2015 Remi Collet <remi@fedoraproject.org> - 1.1.4-2
- cleanup build dependencies and options

* Wed Apr 22 2015 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- Initial package
- open https://jira.mongodb.org/browse/CDRIVER-624 - gcc 5
