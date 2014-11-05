%global gh_owner    couchbase
%global gh_commit   bd3a20f9e18a69dca199134956fd4ad3e1b80ca8
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})

# Tests require some need which are downloaded during make
%global with_tests  %{?_with_tests:1}%{!?_with_tests:0}

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 6
%global with_dtrace 1
%else
%global with_dtrace 0
%endif

Name:          libcouchbase
Version:       2.4.3
Release:       1%{?dist}
Summary:       Couchbase client library
Group:         System Environment/Libraries
License:       ASL 2.0
URL:           http://www.couchbase.com/communities/c/getting-started
Source0:       http://packages.couchbase.com/clients/c/%{name}-%{version}.tar.gz
#Source0:      https://github.com/%{gh_owner}/%{name}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz

%if %{with_tests}
# grep DOWNLOAD Makefile.am
Source10:      http://googletest.googlecode.com/files/gtest-1.7.0-rc1.zip
Source11:      http://files.couchbase.com/maven2/org/couchbase/mock/CouchbaseMock/0.8-SNAPSHOT/CouchbaseMock-0.8-20140621.030439-1.jar
%endif

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libtool
BuildRequires: openssl-devel
BuildRequires: cyrus-sasl-devel
%if "%{?vendor}" == "Remi Collet"
# ensure we use latest version (libevent-last)
BuildRequires: libevent-devel >= 2.0.20
%else
BuildRequires: libevent-devel >= 1.4
%endif
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
#%setup -qn %{name}-%{gh_commit}
%setup -q

#config/gensrclist.pl
#cat <<EOF | tee m4/version.m4
#m4_define([VERSION_NUMBER], [%{version}])
#m4_define([GIT_CHANGESET],[%{gh_commit}])
#EOF

%if %{with_tests}
cp %{SOURCE10} gtest-1.7.0.zip
cp %{SOURCE11} tests/CouchbaseMock.jar
%endif


%build
autoreconf -i --force

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
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/%{name}.so.*
# Backends
%{_libdir}/%{name}_libevent.so
%{_libdir}/%{name}_libev.so

%files devel
%defattr(-,root,root,-)
%doc RELEASE_NOTES.markdown
%{_includedir}/%{name}
#{_mandir}/man3/libcouch*
#{_mandir}/man3/lcb*
#{_mandir}/man5/lcb*
%{_libdir}/%{name}.so

%files tools
%defattr(-,root,root,-)
%{_bindir}/cbc*
%{_mandir}/man1/cbc*
%{_mandir}/man4/cbc*

%check
%if %{with_tests}
make check
%else
: check disabled, missing '--with tests' option
%endif


%changelog
* Wed Nov  5 2014 Remi Collet <remi@feoraproject.org> - 2.4.3-1
- update to 2.4.3

* Sat Sep 20 2014 Remi Collet <remi@feoraproject.org> - 2.4.1-1
- update to 2.4.1

* Mon May 12 2014 Remi Collet <remi@feoraproject.org> - 2.3.1-1
- update to 2.3.1
- always use libevent 2

* Sat Oct  5 2013 Remi Collet <remi@feoraproject.org> - 2.1.3-1
- update to 2.1.3

* Sun Apr 14 2013 Remi Collet <remi@feoraproject.org> - 2.0.5-1
- Initial package
