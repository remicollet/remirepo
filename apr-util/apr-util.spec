
%define apuver 1

Summary: Apache Portable Runtime Utility library
Name: apr-util
Version: 1.3.9
Release: 3%{?dist}
License: ASL 2.0
Group: System Environment/Libraries
URL: http://apr.apache.org/
Source0: http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2
Patch1: apr-util-1.2.7-pkgconf.patch
Patch2: apr-util-1.3.7-nodbmdso.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: autoconf, apr-devel >= 1.3.0
BuildRequires: db4-devel, expat-devel, libuuid-devel

%description
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines.  This library
contains additional utility interfaces for APR; including support
for XML, LDAP, database interfaces, URI parsing and more.

%package devel
Group: Development/Libraries
Summary: APR utility library development kit
Requires: apr-util = %{version}-%{release}, apr-devel, pkgconfig
Requires: db4-devel, expat-devel, openldap-devel

%description devel
This package provides the support files which can be used to 
build applications using the APR utility library.  The mission 
of the Apache Portable Runtime (APR) is to provide a free 
library of C data structures and routines.

%package pgsql
Group: Development/Libraries
Summary: APR utility library PostgreSQL DBD driver
BuildRequires: postgresql-devel
Requires: apr-util = %{version}-%{release}

%description pgsql
This package provides the PostgreSQL driver for the apr-util
DBD (database abstraction) interface.

%package mysql
Group: Development/Libraries
Summary: APR utility library MySQL DBD driver
BuildRequires: mysql-devel
Requires: apr-util = %{version}-%{release}

%description mysql
This package provides the MySQL driver for the apr-util DBD
(database abstraction) interface.

%package sqlite
Group: Development/Libraries
Summary: APR utility library SQLite DBD driver
BuildRequires: sqlite-devel >= 3.0.0
Requires: apr-util = %{version}-%{release}

%description sqlite
This package provides the SQLite driver for the apr-util DBD
(database abstraction) interface.

%package freetds
Group: Development/Libraries
Summary: APR utility library FreeTDS DBD driver
BuildRequires: freetds-devel
Requires: apr-util = %{version}-%{release}

%description freetds
This package provides the FreeTDS driver for the apr-util DBD
(database abstraction) interface.

%package odbc
Group: Development/Libraries
Summary: APR utility library ODBC DBD driver
BuildRequires: unixODBC-devel
Requires: apr-util = %{version}-%{release}

%description odbc
This package provides the ODBC driver for the apr-util DBD
(database abstraction) interface.

%package ldap
Group: Development/Libraries
Summary: APR utility library LDAP support
BuildRequires: openldap-devel
Requires: apr-util = %{version}-%{release}

%description ldap
This package provides the LDAP support for the apr-util.

%prep
%setup -q
%patch1 -p1 -b .pkgconf
%patch2 -p1 -b .nodbmdso

%build
autoheader && autoconf
%configure --with-apr=%{_prefix} \
        --includedir=%{_includedir}/apr-%{apuver} \
        --with-ldap --without-gdbm \
        --with-sqlite3 --with-pgsql --with-mysql --with-freetds --with-odbc \
        --with-berkeley-db \
        --without-sqlite2
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/aclocal
install -m 644 build/find_apu.m4 $RPM_BUILD_ROOT/%{_datadir}/aclocal

# Unpackaged files; remove the static libaprutil
rm -f $RPM_BUILD_ROOT%{_libdir}/aprutil.exp \
      $RPM_BUILD_ROOT%{_libdir}/libapr*.a

# And remove the reference to the static libaprutil from the .la
# file.
sed -i '/^old_library/s,libapr.*\.a,,' \
      $RPM_BUILD_ROOT%{_libdir}/libapr*.la

# Remove unnecessary exports from dependency_libs
sed -ri '/^dependency_libs/{s,-l(pq|sqlite[0-9]|rt|dl|uuid) ,,g}' \
      $RPM_BUILD_ROOT%{_libdir}/libapr*.la

# Trim libtool DSO cruft
rm -f $RPM_BUILD_ROOT%{_libdir}/apr-util-%{apuver}/*.*a

%check
# Run the less verbose test suites
export MALLOC_CHECK_=2 MALLOC_PERTURB_=$(($RANDOM % 255 + 1))
cd test
make %{?_smp_mflags} testall
# testall breaks with DBD DSO; ignore
export LD_LIBRARY_PATH="`echo "../dbm/.libs:../dbd/.libs:../ldap/.libs:$LD_LIBRARY_PATH" | sed -e 's/::*$//'`"
./testall -v -q || true
./testall testrmm
./testall testdbm

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE NOTICE
%{_libdir}/libaprutil-%{apuver}.so.*
%dir %{_libdir}/apr-util-%{apuver}

%files pgsql
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_dbd_pgsql*

%files mysql
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_dbd_mysql*

%files sqlite
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_dbd_sqlite*

%files freetds
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_dbd_freetds*

%files odbc
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_dbd_odbc*

%files ldap
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_ldap*

%files devel
%defattr(-,root,root,-)
%{_bindir}/apu-%{apuver}-config
%{_libdir}/libaprutil-%{apuver}.*a
%{_libdir}/libaprutil-%{apuver}.so
%{_includedir}/apr-%{apuver}/*.h
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4

%changelog
* Fri Oct 01 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.3.9-3
- rebuild against apr 1.4.2

* Wed Nov 25 2009 Joe Orton <jorton@redhat.com> - 1.3.9-3
- rebuild for new BDB

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.3.9-2
- rebuilt with new openssl

* Thu Aug  6 2009 Bojan Smojver <bojan@rexursive.com> - 1.3.9-1
- bump up to 1.3.9
- CVE-2009-2412
- allocator alignment fixes

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Bojan Smojver <bojan@rexursive.com> 1.3.8-2
- adjust apr-util-1.3.7-nodbmdso.patch

* Wed Jul 15 2009 Bojan Smojver <bojan@rexursive.com> 1.3.8-1
- bump up to 1.3.8

* Wed Jul 15 2009 Bojan Smojver <bojan@rexursive.com> 1.3.7-5
- BR: +libuuid-devel, -e2fsprogs-devel

* Tue Jun  9 2009 Joe Orton <jorton@redhat.com> 1.3.7-4
- disable DBM-drivers-as-DSO support
- backport r783046 from upstream

* Mon Jun  8 2009 Bojan Smojver <bojan@rexursive.com> - 1.3.7-3
- make export of LD_LIBRARY_PATH simpler

* Mon Jun  8 2009 Bojan Smojver <bojan@rexursive.com> - 1.3.7-2
- revert tests

* Mon Jun  8 2009 Bojan Smojver <bojan@rexursive.com> - 1.3.7-1
- bump up to 1.3.7
- CVE-2009-0023
- "billion laughs" fix of apr_xml_* interface

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 23 2009 Joe Orton <jorton@redhat.com> 1.3.4-2
- rebuild for new MySQL

* Wed Aug 16 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.4-1
- bump up to 1.3.4
- drop PostgreSQL patch, fixed upstream

* Wed Jul 16 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.2-8
- beat the fuzz, rework apr-util-1.2.7-pkgconf.patch

* Wed Jul 16 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.2-7
- ship find_apu.m4, fix bug #455189

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.2-6
- rebuild for new db4-4.7

* Tue Jul  8 2008 Joe Orton <jorton@redhat.com> 1.3.2-5
- restore requires for openldap-devel from -devel

* Wed Jul  2 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.2-4
- properly fix PostgreSQL detection

* Wed Jul  2 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.2-3
- revert build dependencies, change from -2 didn't help
- add apr-util-1.3.2-pgsql.patch (remove pgsql_LIBS during detection)

* Wed Jul  2 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.2-2
- try adding postgresql-server to build dependencies to pull some libs in

* Thu Jun 19 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.2-1
- bump up to 1.3.2

* Sun Jun  1 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.0-1
- bump up to 1.3.0

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.12-5
- Autorebuild for GCC 4.3

* Tue Dec  4 2007 Joe Orton <jorton@redhat.com> 1.2.12-4
- rebuild for OpenLDAP soname bump

* Mon Dec  3 2007 Bojan Smojver <bojan@rexursive.com> - 1.2.12-3
- remove all instances of MySQL flags being added to APRUTIL_LDFLAGS

* Tue Nov 27 2007 Bojan Smojver <bojan@rexursive.com> - 1.2.12-1
- bump up to 1.2.12
- drop MySQL DBD driver, shipped upstream
- adjust various patches to apply
- rework tests in %%check (1.2.x got tests from trunk)

* Mon Sep 24 2007 Jesse Keating <jkeating@redhat.com> - 1.2.10-2
- Rebuild for upgrade path (add dist since that's now on F-7 branch)

* Sun Sep  9 2007 Bojan Smojver <bojan@rexursive.com> 1.2.10-1
- bump up to 1.2.10
- pick up newly checked in MySQL DBD driver directly from ASF
- remove dbdopen patch (fixed upstream)
- remove xmlns patch (fixed upstream)
- remove autoexpat patch (fixed upstream)

* Sun Sep  2 2007 Joe Orton <jorton@redhat.com> 1.2.8-12
- rebuild for fixed APR 32-bit ABI
- remove sqlite driver from main package (#274521)

* Wed Aug 22 2007 Joe Orton <jorton@redhat.com> 1.2.8-11
- rebuild for expat soname bump

* Tue Aug 21 2007 Joe Orton <jorton@redhat.com> 1.2.8-10
- fix License

* Wed Aug  8 2007 Joe Orton <jorton@redhat.com> 1.2.8-9
- add rewrite of expat autoconf code (upstream r493791)
- fix build for new glibc open()-as-macro
- split out sqlite subpackage

* Tue Jul  3 2007 Joe Orton <jorton@redhat.com> 1.2.8-8
- add fix for attribute namespace handling in apr_xml (PR 41908)

* Thu Apr  5 2007 Joe Orton <jorton@redhat.com> 1.2.8-7
- remove old Conflicts, doxygen BR (#225254)

* Fri Mar 23 2007 Joe Orton <jorton@redhat.com> 1.2.8-6
- add DBD DSO lifetime fix (r521327)

* Thu Mar 22 2007 Joe Orton <jorton@redhat.com> 1.2.8-5
- drop doxygen documentation (which caused multilib conflicts)

* Wed Feb 28 2007 Joe Orton <jorton@redhat.com> 1.2.8-4
- add mysql driver in -mysql subpackage (Bojan Smojver, #222237)

* Tue Feb 27 2007 Joe Orton <jorton@redhat.com> 1.2.8-3
- build DBD drivers as DSOs (w/Bojan Smojver, #192922)
- split out pgsql driver into -pgsql subpackage

* Tue Dec  5 2006 Joe Orton <jorton@redhat.com> 1.2.8-2
- update to 1.2.8, pick up new libpq soname

* Fri Dec  1 2006 Joe Orton <jorton@redhat.com> 1.2.7-5
- really rebuild for db45

* Sat Nov 11 2006 Joe Orton <jorton@redhat.com> 1.2.7-4
- add support for BDB 4.5 from upstream, rebuild

* Wed Jul 19 2006 Joe Orton <jorton@redhat.com> 1.2.7-3
- fix buildconf with autoconf 2.60

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.7-2.1
- rebuild

* Tue May  2 2006 Joe Orton <jorton@redhat.com> 1.2.7-2
- update to 1.2.7
- use pkg-config in apu-1-config to make it libdir-agnostic

* Thu Apr  6 2006 Joe Orton <jorton@redhat.com> 1.2.6-2
- update to 1.2.6
- define LDAP_DEPRECATED in apr_ldap.h (r391985, #188073)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.2-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.2-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 30 2006 Joe Orton <jorton@redhat.com> 1.2.2-4
- rebuild to drop reference to libexpat.la

* Wed Jan 18 2006 Joe Orton <jorton@redhat.com> 1.2.2-3
- disable sqlite2 support
- BuildRequire e2fsprogs-devel
- enable malloc paranoia in %%check

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.com> 1.2.2-2.2
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Dec  6 2005 Joe Orton <jorton@redhat.com> 1.2.2-2
- trim exports from .la file/--libs output (#174924)

* Fri Nov 25 2005 Joe Orton <jorton@redhat.com> 1.2.2-1
- update to 1.2.2

* Thu Oct 20 2005 Joe Orton <jorton@redhat.com> 0.9.7-3
- fix epoch again

* Thu Oct 20 2005 Joe Orton <jorton@redhat.com> 0.9.7-2
- update to 0.9.7
- drop static libs (#170051)

* Tue Jul 26 2005 Joe Orton <jorton@redhat.com> 0.9.6-3
- add FILE bucket fix for truncated files (#159191)
- add epoch to dependencies

* Fri Mar  4 2005 Joe Orton <jorton@redhat.com> 0.9.6-2
- rebuild

* Wed Feb  9 2005 Joe Orton <jorton@redhat.com> 0.9.6-1
- update to 0.9.6

* Wed Jan 19 2005 Joe Orton <jorton@redhat.com> 0.9.5-3
- restore db-4.3 detection lost in 0.9.5 upgrade

* Wed Jan 19 2005 Joe Orton <jorton@redhat.com> 0.9.5-2
- rebuild

* Mon Nov 22 2004 Joe Orton <jorton@redhat.com> 0.9.5-1
- update to 0.9.5

* Thu Nov 11 2004 Jeff Johnson <jbj@jbj.org> 0.9.4-19
- actually explicitly check for and detect db-4.3.

* Thu Nov 11 2004 Jeff Johnson <jbj@jbj.org> 0.9.4-18
- rebuild against db-4.3.21.

* Fri Sep 17 2004 Joe Orton <jorton@redhat.com> 0.9.4-17
- add security fix for CAN-2004-0786

* Sat Jun 19 2004 Joe Orton <jorton@redhat.com> 0.9.4-16
- have -devel require matching release of apr-util

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Apr  1 2004 Joe Orton <jorton@redhat.com> 0.9.4-14
- fix use of SHA1 passwords (#119651)

* Tue Mar 30 2004 Joe Orton <jorton@redhat.com> 0.9.4-13
- remove fundamentally broken check_sbcs() from xlate code

* Fri Mar 19 2004 Joe Orton <jorton@redhat.com> 0.9.4-12
- tweak xlate fix

* Fri Mar 19 2004 Joe Orton <jorton@redhat.com> 0.9.4-11
- rebuild with xlate fixes and tests enabled

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> 0.9.4-10.1
- rebuilt

* Tue Mar  2 2004 Joe Orton <jorton@redhat.com> 0.9.4-10
- rename sdbm_* symbols to apu__sdbm_*

* Mon Feb 16 2004 Joe Orton <jorton@redhat.com> 0.9.4-9
- fix sdbm apr_dbm_exists() on s390x/ppc64

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 0.9.4-8
- rebuilt

* Thu Feb  5 2004 Joe Orton <jorton@redhat.com> 0.9.4-7
- fix warnings from use of apr_optional*.h with gcc 3.4

* Thu Jan 29 2004 Joe Orton <jorton@redhat.com> 0.9.4-6
- drop gdbm support

* Thu Jan  8 2004 Joe Orton <jorton@redhat.com> 0.9.4-5
- fix DB library detection

* Sat Dec 13 2003 Jeff Johnson <jbj@jbj.org> 0.9.4-4
- rebuild against db-4.2.52.

* Mon Oct 13 2003 Jeff Johnson <jbj@jbj.org> 0.9.4-3
- rebuild against db-4.2.42.

* Mon Oct  6 2003 Joe Orton <jorton@redhat.com> 0.9.4-2
- fix 'apu-config --apu-la-file' output

* Mon Oct  6 2003 Joe Orton <jorton@redhat.com> 0.9.4-1
- update to 0.9.4.

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.3-10
- rebuild

* Mon Jul  7 2003 Joe Orton <jorton@redhat.com> 0.9.3-9
- rebuild
- don't run testuuid test because of #98677

* Thu Jul  3 2003 Joe Orton <jorton@redhat.com> 0.9.3-8
- rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 20 2003 Joe Orton <jorton@redhat.com> 0.9.3-6
- fix to detect crypt_r correctly (CAN-2003-0195)

* Thu May 15 2003 Joe Orton <jorton@redhat.com> 0.9.3-5
- fix to try linking against -ldb first (#90917)
- depend on openldap, gdbm, db4, expat appropriately.

* Tue May 13 2003 Joe Orton <jorton@redhat.com> 0.9.3-4
- rebuild

* Wed May  7 2003 Joe Orton <jorton@redhat.com> 0.9.3-3
- make devel package conflict with old subversion-devel
- run the less crufty parts of the test suite

* Tue Apr 29 2003 Joe Orton <jorton@redhat.com> 0.9.3-2
- run ldconfig in post/postun

* Mon Apr 28 2003 Joe Orton <jorton@redhat.com> 0.9.3-1
- initial build
