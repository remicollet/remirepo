# remirepo spec file for mongo-c-driver
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_owner     mongodb
%global gh_project   mongo-c-driver
#global gh_commit    495cd3ffa9beade31c2b410eb5e9555c7db240e1
#global gh_short     %%(c=%%{gh_commit}; echo ${c:0:7})
#global gh_date      20151001
%global with_tests   0%{!?_without_tests:1}
%global libname      libmongoc
%global libver       1.0
#global prever       rc0

Name:      mongo-c-driver
Summary:   Client library written in C for MongoDB
Version:   1.3.0
%if 0%{?gh_date}
Release:   0.6.%{gh_date}git%{gh_short}%{?dist}
Source0:   https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?prever}-%{gh_short}.tar.gz
BuildRequires: libtool autoconf
%else
Release:   1%{?dist}
Source0:   https://github.com/%{gh_owner}/%{gh_project}/releases/download/%{version}%{?prever:-%{prever}}/%{gh_project}-%{version}%{?prever:-%{prever}}.tar.gz
# https://jira.mongodb.org/browse/CDRIVER-1039
Source1:   https://raw.githubusercontent.com/mongodb/mongo-c-driver/master/doc/mallard2man.py
%endif
License:   ASL 2.0
Group:     System Environment/Libraries
URL:       https://github.com/%{gh_owner}/%{gh_project}

BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(libbson-1.0)
%if 0%{?fedora} > 21 || 0%{?rhel} > 6
BuildRequires: pkgconfig(libsasl2)
%else
BuildRequires: cyrus-sasl-devel
%endif
%if %{with_tests}
BuildRequires: mongodb-server
BuildRequires: openssl
BuildRequires: perl
%endif
# From man pages
BuildRequires: python


%description
%{name} is a client library written in C for MongoDB.


%package devel
Summary:    Header files and development libraries for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   pkgconfig
# Sub package removed
Obsoletes:  %{name}-tools < 1.3.0


%description devel
This package contains the header files and development libraries
for %{name}.

Documentation: http://api.mongodb.org/c/%{version}/


%prep
%if 0%{?gh_date}
%setup -q -n %{gh_project}-%{gh_commit}
autoreconf -fvi -I build/autotools
%else
%setup -q -n %{gh_project}-%{version}%{?prever:-%{prever}}
install -m 0755 %{SOURCE1} doc/
#mkdir doc/man
%endif

# Ensure we are using system library
# Done after autoreconf because of m4_include
rm -r src/libbson


%build
export LIBS=-lpthread

%configure \
  --enable-sasl \
  --enable-ssl \
  --with-libbson=system \
  --enable-man-pages

make %{_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}

rm    %{buildroot}%{_libdir}/*la
rm -r %{buildroot}%{_datadir}/doc/
# drop "generic" man pages, avoid conflicts
# https://jira.mongodb.org/browse/CDRIVER-1039
rm    %{buildroot}/%{_mandir}/man3/[a-l]*
rm    %{buildroot}/%{_mandir}/man3/ma*
rm    %{buildroot}/%{_mandir}/man3/[t-u]*


%check
%if %{with_tests}
: Run a server
mkdir dbtest
mongod \
  --journal \
  --logpath     $PWD/server.log \
  --pidfilepath $PWD/server.pid \
  --dbpath      $PWD/dbtest \
  --fork

: Run the test suite
ret=0
make check || ret=1

: Cleanup
[ -s server.pid ] && kill $(cat server.pid)

%if 0%{?gh_date}
exit 0
%else
exit $ret
%endif
%else
: check disabled, missing '--with tests' option
%endif


%post   -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/%{libname}-%{libver}.so.*
%{_libdir}/%{libname}-priv.so.*

%files devel
%doc NEWS README*
%{_includedir}/%{libname}-%{libver}
%{_libdir}/%{libname}-%{libver}.so
%{_libdir}/%{libname}-priv.so
%{_libdir}/pkgconfig/%{libname}-*.pc
%{_mandir}/man3/mongoc*
%{_bindir}/mongoc-stat


%changelog
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