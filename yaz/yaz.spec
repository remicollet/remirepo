# remirepo spec file for yaz, from:
#
# Fedora spec file for redis
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

Name:           yaz
Version:        5.14.11
Release:        1%{?dist}
Summary:        Z39.50/SRW/SRU toolkit
License:        BSD
URL:            http://www.indexdata.com/yaz/
Source0:        http://ftp.indexdata.com/pub/yaz/yaz-%{version}.tar.gz
BuildRequires:  bison
BuildRequires:  chrpath
BuildRequires:  gnutls-devel
BuildRequires:  hiredis-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libgpg-error-devel
BuildRequires:  libicu-devel
BuildRequires:  libmemcached-devel
BuildRequires:  libpcap-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  readline-devel
BuildRequires:  tcl
BuildRequires:  tcp_wrappers-devel

%description
YAZ is a programmers toolkit supporting the development of Z39.50/SRW/SRU 
clients and servers. Z39.50-2003 (version 3) as well as SRW/SRU version 1.1 
are supported in both the client and server roles. The SOLR webservice is 
supported in the client role through the ZOOM API.

The current version of YAZ includes support for the industry standard ZOOM 
API for Z39.50. This API vastly simplifies the process of writing new clients 
using YAZ, and it reduces your dependency on any single toolkit. YAZ can be 
used by itself to build Z39.50 applications in C.For programmers preferring 
another language, YAZ has three language bindings to commonly used application
development languages.

This package contains both a test-server and clients (normal & ssl).

%package -n     lib%{name}
Summary:        Shared libraries for %{name}

%description -n lib%{name}
This packages contains shared libraries for %{name}.

%package -n     lib%{name}-devel
Summary:        Development files for %{name}
Requires:       gnutls-devel%{?_isa}
Requires:       lib%{name}%{?_isa} = %{version}-%{release}
Requires:       libmemcached-devel%{?_isa}
Requires:       libxml2-devel%{?_isa}
Requires:       readline-devel%{?_isa}

%description -n lib%{name}-devel
This package contains libraries and header files for
developing applications that use lib%{name}.

%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description    doc
This package contains documentation for %{name}, a Z39.50 protocol
server and client.

%prep
%setup -q

%build
%configure \
        --enable-tcpd \
        --enable-shared \
        --with-memcached \
        --with-redis \
        --disable-static \
        --disable-rpath

%make_build

%install
%make_install

# Remove cruft
find %{buildroot} -name '*.*a' -delete -print

# Delete rpath
chrpath --delete %{buildroot}%{_bindir}/yaz-icu
chrpath --delete %{buildroot}%{_bindir}/yaz-url
chrpath --delete %{buildroot}%{_bindir}/yaz-json-parse
chrpath --delete %{buildroot}%{_bindir}/yaz-illclient
chrpath --delete %{buildroot}%{_bindir}/yaz-client
chrpath --delete %{buildroot}%{_bindir}/yaz-marcdump
chrpath --delete %{buildroot}%{_bindir}/zoomsh
chrpath --delete %{buildroot}%{_bindir}/yaz-iconv
chrpath --delete %{buildroot}%{_bindir}/yaz-ztest

%check
make check

%post -n lib%{name} -p /sbin/ldconfig

%postun -n lib%{name} -p /sbin/ldconfig

%files
%doc NEWS README
%license LICENSE
%{_bindir}/yaz-client
%{_bindir}/yaz-ztest
%{_bindir}/yaz-marcdump
%{_bindir}/yaz-iconv
%{_bindir}/yaz-illclient
%{_bindir}/yaz-icu
%{_bindir}/yaz-json-parse
%{_bindir}/yaz-url
%{_bindir}/zoomsh
%{_mandir}/man1/yaz-client.*
%{_mandir}/man1/yaz-illclient.*
%{_mandir}/man8/yaz-ztest.*
%{_mandir}/man1/zoomsh.*
%{_mandir}/man1/yaz-marcdump.*
%{_mandir}/man1/yaz-iconv.*
%{_mandir}/man1/yaz-icu.*
%{_mandir}/man7/yaz-log.*
%{_mandir}/man1/yaz-json-parse.*
%{_mandir}/man1/yaz-url.*

%files -n lib%{name}
%license LICENSE
%{_libdir}/*.so.*
%{_mandir}/man7/yaz.*
%{_mandir}/man7/bib1-attr.*

%files -n lib%{name}-devel
%doc NEWS README
%{_bindir}/yaz-config
%{_bindir}/yaz-asncomp
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_includedir}/%{name}/
%{_datadir}/yaz/
%{_datadir}/aclocal/*
%{_mandir}/man1/yaz-asncomp.*
%{_mandir}/man1/yaz-config.*

%files -n %{name}-doc
%{_datadir}/doc/yaz/


%changelog
* Mon Dec  5 2016 Remi Collet <remi@remirepo.net> - 5.14.11-1
- rebuild for remi repo waiting #1366650

* Sat Oct 24 2015 Christopher Meng <rpm@cicku.me> - 5.14.11-1
- Update to 5.14.11

* Tue Sep 15 2015 Christopher Meng <rpm@cicku.me> - 5.14.9-1
- Update to 5.14.9

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 07 2015 Christopher Meng <rpm@cicku.me> - 5.13.0-1
- Update to 5.13.0

* Thu Feb 26 2015 Christopher Meng <rpm@cicku.me> - 5.9.1-2
- Drop openssl-devel from libyaz-devel as yaz is linked with gnutls already

* Thu Feb 26 2015 Guido Grazioli <guido.grazioli@gmail.com> - 5.9.1-1
- Update to 5.9.1
- Remove rpaths with chrpath

* Wed Feb 04 2015 Petr Machata <pmachata@redhat.com> - 5.8.1-2
- Bump for rebuild.

* Mon Feb 02 2015 Christopher Meng <rpm@cicku.me> - 5.8.1-1
- Update to 5.8.1

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 5.6.0-2
- rebuild for ICU 54.1

* Tue Nov 18 2014 Christopher Meng <rpm@cicku.me> - 5.6.0-1
- Update to 5.6.0

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 5.4.1-2
- rebuild for ICU 53.1

* Fri Aug 22 2014 Christopher Meng <rpm@cicku.me> - 5.4.1-1
- Update to 5.4.1

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Christopher Meng <rpm@cicku.me> - 5.3.0-2
- Enable GnuTLS support.

* Thu Jul 17 2014 Christopher Meng <rpm@cicku.me> - 5.3.0-1
- Update to 5.3.0

* Mon Jun 30 2014 Christopher Meng <rpm@cicku.me> - 5.2.1-1
- Update to 5.2.1

* Sun Jun 15 2014 Christopher Meng <rpm@cicku.me> - 5.2.0-1
- Update to 5.2.0

* Mon Jun 09 2014 Christopher Meng <rpm@cicku.me> - 5.1.3-1
- Update to 5.1.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 05 2014 Christopher Meng <rpm@cicku.me> - 5.1.1-1
- Update to 5.1.1

* Sun Apr 20 2014 Christopher Meng <rpm@cicku.me> - 5.1.0-1
- Update to 5.1.0

* Tue Mar 25 2014 Christopher Meng <rpm@cicku.me> - 5.0.21-1
- Update to 5.0.21
- Build with memcached support for ZOOM caching.
- SPEC cleanup, dependencies cleanup, redundant files cleanup.

* Fri Feb 14 2014 David Tardon <dtardon@redhat.com> - 4.2.56-4
- rebuild for new ICU

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.56-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 30 2013 Dan Horák <dan[at]danny.cz> 4.2.56-2
- add upstream fix for platforms where the char type is unsigned by default

* Mon Apr 29 2013 Peter Robinson <pbrobinson@fedoraproject.org> 4.2.56-1
- Update to 4.2.56

* Tue Apr 02 2013 Guido Grazioli <guido.grazioli@gmail.com> - 4.2.51-1
- Update to 4.2.51
- Remove unneeded patch

* Fri Feb 01 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 4.2.33-3
- Rebuild for icu 50

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 14 2012 Guido Grazioli <guido.grazioli@gmail.com> - 4.2.33-1
- Update to 4.2.33

* Mon Apr 23 2012 Guido Grazioli <guido.grazioli@gmail.com> - 4.2.29-2
- Rebuilt for icu soname bump

* Mon Apr 09 2012 Guido Grazioli <guido.grazioli@gmail.com> - 4.2.29-1
- Update to 4.2.29

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 30 2011 Guido Grazioli <guido.grazioli@gmail.com> - 4.2.17-1
- Update to 4.2.17 (minor bugfixes)

* Mon Sep 12 2011 Guido Grazioli <guido.grazioli@gmail.com> - 4.2.14-1
- Upstream 4.2.14

* Mon Sep 12 2011 Guido Grazioli <guido.grazioli@gmail.com> - 4.2.4-2
- Rebuild against icu 4.8.1

* Tue Jul 19 2011 Guido Grazioli <guido.grazioli@gmail.com> - 4.2.4-1
- Upstream 4.2.4

* Mon May 09 2011 Guido Grazioli <guido.grazioli@gmail.com> - 4.1.7-1
- Upstream 4.1.7 
- Improved description

* Mon Mar 07 2011 Caolán McNamara <caolanm@redhat.com> - 4.0.12-3
- Rebuild against icu 4.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 06 2010 Guido Grazioli <guido.grazioli@gmail.com> - 4.0.12-1
- Upstream 4.0.12 (various bugfixes)
- Remove unused patch, fixed upstream

* Sun Apr 04 2010 Guido Grazioli <guido.grazioli@gmail.com> - 4.0.2-1
- Upstream 4.0.2 (major version release)
- Add patch for explicit DSO linking
- Split documentation to -doc subpackage

* Fri Apr 02 2010 Caolán McNamara <caolanm@redhat.com> - 3.0.49-2
- Rebuild against icu 4.4

* Thu Oct 01 2009 Guido Grazioli <guido.grazioli@gmail.com> - 3.0.49-1
- Upstream 3.0.49 (bugfixes and feature enhancements)
- Require pkgconfig for libyaz-devel (guidelines MUST)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 27 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 3.0.46-1
- Update to 3.0.46 (miscellaneous bugfixes)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 3.0.41-1
- Upstream 3.0.41
- Always use system libtool
- Remove TODO from docs
- Package bib1-attr.7 with libyaz

* Mon Jun 30 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 3.0.34-1
- Upstream 3.0.34

* Sat May 10 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 3.0.26-1
- Upstream 3.0.26

* Sat Feb 02 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 3.0.24-1
- Upstream 3.0.24
- Remove ziffy, as it's no longer part of this package
- Build with icu, available since 3.0.10

* Fri Aug 17 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 3.0.8-1
- New upstream 3.0.8

* Fri Jun 15 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 3.0.6-1
- New major upstream version 3.0.6

* Sun Apr 01 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.1.54-1
- Upstream 2.1.54

* Sat Jan 27 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.1.48-1
- Upstream 2.1.48

* Sun Dec 17 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.1.40-1
- Upstream 2.1.40

* Sat Oct 28 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.1.36-1
- Upstream 2.1.36

* Sun Sep 03 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.1.26-1.1
- Mass rebuild for FC6

* Tue Aug 15 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.1.26-1
- Version 2.1.26
- Kill all tabs

* Tue Jun 20 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.1.22-1
- Version 2.1.22
- Libtoolize correctly
- BuildRequire libxslt
- BuildRequire tcp_wrappers
- Enable pth in configure
- Add %%check routine

* Mon Dec 12 2005 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.1.10-1
- Initial packaging
