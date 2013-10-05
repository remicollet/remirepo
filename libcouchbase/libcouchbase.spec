%global gh_owner    couchbase
%global gh_commit   55e4a2d9cb810eac5d58bfbf5c1b1d7397bfce76
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})

# Tests require some need which are downloaded during make
%global with_tests  %{?_with_tests:1}%{!?_with_tests:0}

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 6
%global with_dtrace 1
%else
%global with_dtrace 0
%endif

Name:          libcouchbase
Version:       2.1.3
Release:       1%{?dist}
Summary:       Couchbase client library
Group:         System Environment/Libraries
License:       ASL 2.0
URL:           http://www.couchbase.com/communities/c/getting-started
#Source0:      http://packages.couchbase.com/clients/c/%{name}-%{version}.tar.gz
Source0:       https://github.com/%{gh_owner}/%{name}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz

%if %{with_tests}
Source10:      http://googletest.googlecode.com/files/gtest-1.7.0-rc1.zip
Source11:      http://files.couchbase.com/maven2/org/couchbase/mock/CouchbaseMock/0.6-SNAPSHOT/CouchbaseMock-0.6-20130903.160518-3.jar
%endif

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libtool
BuildRequires: cyrus-sasl-devel
BuildRequires: libevent-devel >= 1.4
BuildRequires: libev-devel
%if %{with_dtrace}
BuildRequires: systemtap-sdt-devel >= 1.8
%endif


%description
The C library provides fast access to documents in Couchbase Server 2.0.
With JSON documents and Couchbase server 2.0 you have new ways to index
and query data stored in the cluster through views. This client library,
libcouchbase, also simplifies requests to Views through its handling of
HTTP transport.

This Couchbase Client Library for C and C++ provides a complete interface
to the functionality of Couchbase Server.


%package       devel
Summary:       Development files for Couchbase client library
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package       tools
Summary:       Couchbase tools
Group:         Applications/System
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description tools
The %{name}-tools package contains some command line tools to manage
a Couchbase Server.


%prep
%setup -qn %{name}-%{gh_commit}

cat <<EOF | tee m4/version.m4
m4_define([VERSION_NUMBER], [%{version}])
m4_define([GIT_CHANGESET],[%{gh_commit}])
EOF

%if %{with_tests}
cp %{SOURCE10} gtest-1.7.0.zip
cp %{SOURCE11} tests/CouchbaseMock.jar
%endif


%build
autoreconf -i --force

# Hack for manpage layout
sed -e '/manpage_layout=/s/=.*/=bsd/' \
    -i configure

%{configure} \
%if ! %{with_tests}
    --disable-tests \
    --disable-couchbasemock \
%endif
    --enable-system-libsasl

make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}

# Remove uneeded files
rm -f %{buildroot}%{_libdir}/*.la


%files
%defattr(-,root,root,-)
%doc LICENSE RELEASE_NOTES.markdown
%{_libdir}/%{name}.so.*
# Backends
%{_libdir}/%{name}_libevent.so
%{_libdir}/%{name}_libev.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_mandir}/man3/libcouch*
%{_mandir}/man3/lcb*
%{_mandir}/man5/lcb*
%{_libdir}/%{name}.so

%files tools
%defattr(-,root,root,-)
%{_bindir}/cbc*
%{_mandir}/man1/cbc*
%{_mandir}/man5/cbc*

%check
%if %{with_tests}
make check
%else
: check disabled, missing '--with tests' option
%endif


%changelog
* Sat Oct  5 2013 Remi Collet <remi@feoraproject.org> - 2.1.3-1
- update to 2.1.3

* Sun Apr 14 2013 Remi Collet <remi@feoraproject.org> - 2.0.5-1
- Initial package
