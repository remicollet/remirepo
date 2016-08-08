# remirepo spec file for libbson, from
#
# Fedora spec file for libbson
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#

%global prever beta1
Name:       libbson
Version:    1.4.0
Release:    0.1.%{prever}%{?dist}
Summary:    Building, parsing, and iterating BSON documents
Group:      System Environment/Libraries
## Installed:
# COPYING:                          ASL 2.0
# src/bson/b64_ntop.h:              ISC and MIT
# src/bson/b64_pton.h:              ISC and MIT
# src/bson/bson-md5.h:              zlib
# src/yajl/yajl_alloc.h:            ISC
# doc/man/bson_iter_symbol.3:       GFDL
## Not installed:
# configure:                        FSFUL
# aclocal.m4:                       FSFULLR
# Makefile.in:                      FSFULLR
# build/autotools/depcomp:          GPLv2+ with exceptions
# build/autotools/ltmain.sh:        GPLv2+ with exceptions
# build/autotools/m4/ax_pthread.m4  GPLv3+ with exception
# build/autotools/install-sh:       MIT and Public Domain
# doc/html/jquery.js:               (MIT or GPLv2) and (MIT, BSD GPL)
# doc/html/jquery.syntax.js:        MIT
# doc/mallard2man.py:               GPLv3+
# src/bson/bson-stdint-win32.h:     BSD
License:    ASL 2.0 and ISC and MIT and zlib
URL:        https://github.com/mongodb/%{name}
Source0:    %{url}/releases/download/%{version}%{?prever:-%{prever}}/%{name}-%{version}%{?prever:-%{prever}}.tar.gz
# Do not install COPYING, install ChangeLog, distribution specific
Patch0:     %{name}-1.3.1-Install-documentation-according-to-guidelines.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  python
# Modified yajl-2.0.4 is bundled, waiting on yajl upstream to merge libbson's
# changes, <https://github.com/lloyd/yajl/issues/161>,
# <https://jira.mongodb.org/browse/CDRIVER-601>, bug #1215182
Provides:       bundled(yajl) = 2.0.4

%description
This is a library providing useful routines related to building, parsing,
and iterating BSON documents <http://bsonspec.org/>.

%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
License:    ASL 2.0 and GFDL
Requires:   %{name}%{?_isa} = %{version}-%{release}
# gcc for standard library header files
Requires:   gcc%{?_isa}
Requires:   pkgconfig

%description devel
This package contains libraries and header files needed for developing
applications that use %{name}.

%prep
%setup -q -n %{name}-%{version}%{?prever:-%{prever}}

# Generate build scripts from sources
%if 0%{?fedora} >= 20 || 0%{?rhel} >= 7
%patch0 -p1
autoreconf --force --install
%endif


%build
%configure \
    --disable-coverage \
    --disable-debug \
    --disable-debug-symbols \
    --enable-extra-align \
    --disable-hardening \
    --disable-html-docs \
    --enable-ld-version-script \
    --disable-lto \
    --disable-maintainer-flags \
    --enable-man-pages \
    --disable-optimizations \
    --enable-shared \
    --disable-silent-rules \
    --disable-static \
    --disable-yelp
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f '{}' +
# Move ambiguously named manual pages into package-specific directory
# <https://jira.mongodb.org/browse/CDRIVER-1039>
#install -d -m 0755 %{buildroot}%{_docdir}/%{name}-devel
#for P in clock creating endianness errors index installing json memory \
#        oid parsing performance threading utf8 version; do
#    mv %{buildroot}%{_mandir}/man3/"$P".3 %{buildroot}%{_docdir}/%{name}-devel
#done
# Install examples here because it's forbidden to use relative %%doc with
# installing into %%_pkgdocdir
install -d -m 0755 %{buildroot}%{_docdir}/%{name}-devel/examples
install -m 0644 -t %{buildroot}%{_docdir}/%{name}-devel/examples examples/*.c

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
rm -f %{buildroot}%{_docdir}/%{name}/COPYING
install -d Changelog %{buildroot}%{_docdir}/%{name}/Changelog
%endif


%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
# AUTHORS is empty, README etc. are installed by "make install"
%{_docdir}/%{name}
%{_libdir}/*.so.*

%files devel
%{_docdir}/%{name}-devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*


%changelog
* Mon Aug  8 2016 Remi Collet <remi@fedoraproject.org> - 1.4.0-0.1.beta1
- update to 1.4.0-beta1

* Thu Mar 31 2016 Petr Pisar <ppisar@redhat.com> - 1.3.5-1
- 1.3.5 bump

* Tue Mar 15 2016 Remi Collet <remi@fedoraproject.org> - 1.3.4-1
- switch to Fedora spec file
- tweak install for EL-6 (don't run autoconf)

* Tue Mar 15 2016 Petr Pisar <ppisar@redhat.com> - 1.3.4-1
- 1.3.4 bump

* Sun Feb  7 2016 Remi Collet <remi@fedoraproject.org> - 1.3.3-1
- Update to 1.3.3

* Tue Feb  2 2016 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- Update to 1.3.2

* Thu Jan 21 2016 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1
- workaround for man pages are no more generated / installed
  https://jira.mongodb.org/browse/CDRIVER-1069
- workaround for man pages installation broken
  https://jira.mongodb.org/browse/CDRIVER-1068

* Wed Dec 16 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0

* Tue Dec  8 2015 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3 (1.3.0 not compatible with pecl/mongodb)

* Tue Dec  8 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0
- open https://jira.mongodb.org/browse/CDRIVER-1039
  libbson 1.3.0 man pages broken installation

* Wed Oct 14 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Sun Oct  4 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.2.rc0
- Update to 1.2.0-rc0

* Wed Apr 22 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.1.beta
- Initial package
- https://jira.mongodb.org/browse/CDRIVER-621 - typo in man pages
- https://jira.mongodb.org/browse/CDRIVER-623 - bundled jayl
