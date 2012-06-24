%global rhelrel 15-el5

Summary: A utility for getting files from remote servers (FTP, HTTP, and others).
Name: compat-libcurl3
Version: 7.15.5
Release: 2%{?dist}
License: MIT
Group: Applications/Internet
Source: http://curl.haxx.se/download/curl-%{version}.tar.bz2
Patch0: curl-7.14.1-nousr.patch
Patch1: curl-7.15.0-curl_config-version.patch
Patch2: curl-7.15.3-multilib.patch
Patch3: curl-7.15.5-CVE-2009-0037.patch
Patch4: curl-7.15.5-CVE-2009-2417.patch
Patch5: curl-7.15.5-bz473128.patch
Patch6: curl-7.15.5-bz479967.patch
Patch7: curl-7.15.5-bz517084.patch
Patch8: curl-7.15.5-bz517199.patch
Patch9: curl-7.15.5-bz532069.patch
Patch10: curl-7.15.5-bz563220.patch
Patch11: curl-7.15.5-bz655073.patch
Patch12: curl-7.15.5-CVE-2011-2192.patch
Patch13: curl-7.15.5-bz723643.patch
Patch14: curl-7.15.5-bz652557.patch
Patch15: curl-7.15.5-bz657396.patch
Patch16: curl-7.15.5-bz688871.patch
Patch17: curl-7.15.5-bz746849.patch
URL: http://curl.haxx.se/
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: openssl-devel, libtool, pkgconfig, libidn-devel
Requires: openssl

%description
cURL is a tool for getting files from FTP, HTTP, Gopher, Telnet, and
Dict servers, using any of the supported protocols. cURL is designed
to work without user interaction or any kind of interactivity. cURL
offers many useful capabilities, like proxy support, user
authentication, FTP upload, HTTP post, and file transfer resume.

%{name} is provided for compatibility for package build against old
libcurl (libcurl.so.3 provided by version < 7.16).
In sync with curl-%{version}-%{rhelrel}.


%package devel
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}, openssl-devel, libidn-devel
Summary: Files needed for building applications with libcurl.

%description devel
cURL is a tool for getting files from FTP, HTTP, Gopher, Telnet, and
Dict servers, using any of the supported protocols. The curl-devel
package includes files needed for developing applications which can
use cURL's capabilities internally.

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q -n curl-%{version}

%patch0 -p1 -b .nousr
%patch1 -p1 -b .ver
%patch2 -p1 -b .multilib
%patch3 -p1 -b .CVE-2009-0037
%patch4 -p1 -b .CVE-2009-2417
%patch5 -p1 -b .bz473128
%patch6 -p1 -b .bz479967
%patch7 -p1 -b .bz517084
%patch8 -p1 -b .bz517199
%patch9 -p1 -b .bz532069
%patch10 -p1 -b .bz563220
%patch11 -p1 -b .bz655073
%patch12 -p1 -b .CVE-2011-2192
%patch13 -p1 -b .bz723643
%patch14 -p1 -b .bz652557
%patch15 -p1 -b .bz657396
%patch16 -p1 -b .bz688871
%patch17 -p1 -b .bz746849

%build
aclocal
libtoolize --force
./reconf

if pkg-config openssl ; then
	CPPFLAGS=`pkg-config --cflags openssl`; export CPPFLAGS
	LDFLAGS=`pkg-config --libs openssl`; export LDFLAGS
fi
%configure --with-ssl=/usr --enable-ipv6 \
       --with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt \
       --with-gssapi=/usr/kerberos --with-libidn
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libcurl.la


# don't need curl's copy of the certs; use openssl's
find ${RPM_BUILD_ROOT} -name ca-bundle.crt -exec rm -f '{}' \;

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%doc CHANGES README* COPYING
%doc docs/BUGS docs/FAQ docs/FEATURES
%doc docs/MANUAL docs/RESOURCES
%doc docs/TheArtOfHttpScripting docs/TODO
%exclude %{_bindir}/curl
%exclude %{_mandir}/man1/curl.1*
%{_libdir}/libcurl.so.*
#%{_datadir}/ssl/certs/ca-bundle.crt

%files devel
%defattr(-,root,root)
%doc docs/examples/*.c docs/examples/Makefile.example docs/INTERNALS
%{_bindir}/curl-config*
%{_includedir}/curl
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/curl-config.1*
%{_mandir}/man3/*

%changelog
* Sun Jun 24 2012 Remi Collet <RPMS@FamilleCollet.com> - 7.15.5-2
- sync with curl 7.15.5-15

* Thu Oct 27 2011 Kamil Dudka <kdudka@redhat.com> 7.15.5-15
- introduce the --delegation option of curl (#746849)

* Fri Oct 21 2011 Kamil Dudka <kdudka@redhat.com> 7.15.5-14
- fix stack smashing in the FTP implementation (#652557)
- fix proxy kerberos authentication (#657396)
- update running_handles counter properly in curl_multi_remove_handle (#688871)

* Tue Aug 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 7.15.5-1
- build as compat-libcurl3 for remi repository
- sync with 7.15.5-9.el5_6.3

* Wed Aug 03 2011 Kamil Dudka <kdudka@redhat.com> 7.15.5-13
- add a new option CURLOPT_GSSAPI_DELEGATION (#723643)

* Thu Jun 23 2011 Kamil Dudka <kdudka@redhat.com> 7.15.5-12
- do not delegate GSSAPI credentials (CVE-2011-2192)

* Thu Jun 23 2011 Kamil Dudka <kdudka@redhat.com> 7.15.5-9.el5_6.3
- do not delegate GSSAPI credentials (CVE-2011-2192)

* Mon Jan 24 2011 Kamil Dudka <kdudka@redhat.com> - 7.15.5-11
- avoid use of uninitialized variable on failure of a LDAP request (#655073)

* Mon Jan 24 2011 Kamil Dudka <kdudka@redhat.com> - 7.15.5-9.el5_6.2
- avoid use of uninitialized variable on failure of a LDAP request (#670523)

* Tue Jan 18 2011 Kamil Dudka <kdudka@redhat.com> - 7.15.5-10
- proxy tunnel support for LDAP requests (#655073)

* Tue Jan 18 2011 Kamil Dudka <kdudka@redhat.com> - 7.15.5-9.el5_6.1
- proxy tunnel support for LDAP requests (#670523)

* Mon Feb 15 2010 Kamil Dudka <kdudka@redhat.com> - 7.15.5-9
- http://curl.haxx.se/docs/adv_20100209.html (#565408)

* Tue Oct 27 2009 Kamil Dudka <kdudka@redhat.com> - 7.15.5-8
- mention lack of IPv6, FTPS and LDAP support while using a socks proxy
  (#473128)
- avoid tight loop if an upload connection is broken (#479967)
- add options --ftp-account and --ftp-alternative-to-user to program help
  (#517084)
- fix crash when reusing connection after negotiate-auth (#517199)
- support for CRL loading from a PEM file (#532069)

* Tue Aug 11 2009 Jindrich Novy <jnovy@redhat.com> - 7.15.5-7
- sync patch for CVE-2007-0037 with 5.3.Z
Related: #485290

* Mon Aug 10 2009 Kamil Dudka <kdudka@redhat.com> - 7.15.5-6
- fix CVE-2009-2417
Resolves: #516258

* Tue Mar 10 2009 Jindrich Novy <jnovy@redhat.com> - 7.15.5-5
- forwardport one hunk from upstream curl-7.15.1
Related: #485290

* Fri Mar 06 2009 Jindrich Novy <jnovy@redhat.com> - 7.15.5-4
- fix hunk applied to wrong place due to nonzero patch fuzz
Related: #485290

* Tue Mar 03 2009 Jindrich Novy <jnovy@redhat.com> - 7.15.5-3
- fix CVE-2007-0037
Resolves: #485290

* Tue Jan 16 2007 Jindrich Novy <jnovy@redhat.com> - 7.15.5-2
- don't package generated makefiles for docs/examples to avoid
  multiarch conflicts (#222718)

* Thu Aug 24 2006 Jindrich Novy <jnovy@redhat.com> - 7.15.5-1.fc6
- update to curl-7.15.5
- use %%{?dist}

* Fri Jun 30 2006 Ivana Varekova <varekova@redhat.com> - 7.15.4-1
- update to 7.15.4

* Mon Mar 20 2006 Ivana Varekova <varekova@redhat.com> - 7.15.3-1
- fix multilib problem using pkg-config
- update to 7.15.3

* Thu Feb 23 2006 Ivana Varekova <varekova@redhat.com> - 7.15.1-2
- fix multilib problem - #181290 - 
  curl-devel.i386 not installable together with curl-devel.x86-64

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 7.15.1-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 7.15.1-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  8 2005 Ivana Varekova <varekova@redhat.com> 7.15.1-1
- update to 7.15.1 (bug 175191)

* Wed Nov 30 2005 Ivana Varekova <varekova@redhat.com> 7.15.0-3
- fix curl-config bug 174556 - missing vernum value

* Wed Nov  9 2005 Ivana Varekova <varekova@redhat.com> 7.15.0-2
- rebuilt

* Tue Oct 18 2005 Ivana Varekova <varekova@redhat.com> 7.15.0-1
- update to 7.15.0

* Thu Oct 13 2005 Ivana Varekova <varekova@redhat.com> 7.14.1-1
- update to 7.14.1

* Thu Jun 16 2005 Ivana Varekova <varekova@redhat.com> 7.14.0-1
- rebuild new version 

* Tue May 03 2005 Ivana Varekova <varekova@redhat.com> 7.13.1-3
- fix bug 150768 - curl-7.12.3-2 breaks basic authentication
  used Daniel Stenberg patch 

* Mon Apr 25 2005 Joe Orton <jorton@redhat.com> 7.13.1-2
- update to use ca-bundle in /etc/pki
- mark License as MIT not MPL

* Mon Mar  9 2005 Ivana Varekova <varekova@redhat.com> 7.13.1-1
- rebuilt (7.13.1)

* Tue Mar  1 2005 Tomas Mraz <tmraz@redhat.com> 7.13.0-2
- rebuild with openssl-0.9.7e

* Sun Feb 13 2005 Florian La Roche <laroche@redhat.com>
- 7.13.0

* Wed Feb  9 2005 Joe Orton <jorton@redhat.com> 7.12.3-3
- don't pass /usr to --with-libidn to remove "-L/usr/lib" from
  'curl-config --libs' output on x86_64.

* Fri Jan 28 2005 Adrian Havill <havill@redhat.com> 7.12.3-1
- Upgrade to 7.12.3, which uses poll() for FDSETSIZE limit (#134794)
- require libidn-devel for devel subpkg (#141341)
- remove proftpd kludge; included upstream

* Wed Oct 06 2004 Adrian Havill <havill@redhat.com> 7.12.1-1
- upgrade to 7.12.1
- enable GSSAPI auth (#129353)
- enable I18N domain names (#134595)
- workaround for broken ProFTPD SSL auth (#134133). Thanks to
  Aleksandar Milivojevic

* Wed Sep 29 2004 Adrian Havill <havill@redhat.com> 7.12.0-4
- move new docs position so defattr gets applied

* Mon Sep 27 2004 Warren Togami <wtogami@redhat.com> 7.12.0-3
- remove INSTALL, move libcurl docs to -devel

* Fri Jul 26 2004 Jindrich Novy <jnovy@redhat.com>
- updated to 7.12.0
- updated nousr patch

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 07 2004 Adrian Havill <havill@redhat.com> 7.11.1-1
- upgraded; updated nousr patch
- added COPYING (#115956)
- 

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Jan 31 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 7.10.8
- remove patch2, already upstream

* Wed Oct 15 2003 Adrian Havill <havill@redhat.com> 7.10.6-7
- aclocal before libtoolize
- move OpenLDAP license so it's present as a doc file, present in
  both the source and binary as per conditions

* Mon Oct 13 2003 Adrian Havill <havill@redhat.com> 7.10.6-6
- add OpenLDAP copyright notice for usage of code, add OpenLDAP
  license for this code

* Tue Oct 07 2003 Adrian Havill <havill@redhat.com> 7.10.6-5
- match serverAltName certs with SSL (#106168)

* Mon Sep 16 2003 Adrian Havill <havill@redhat.com> 7.10.6-4.1
- bump n-v-r for RHEL

* Mon Sep 16 2003 Adrian Havill <havill@redhat.com> 7.10.6-4
- restore ca cert bundle (#104400)
- require openssl, we want to use its ca-cert bundle

* Sun Sep  7 2003 Joe Orton <jorton@redhat.com> 7.10.6-3
- rebuild

* Fri Sep  5 2003 Joe Orton <jorton@redhat.com> 7.10.6-2.2
- fix to include libcurl.so

* Mon Aug 25 2003 Adrian Havill <havill@redhat.com> 7.10.6-2.1
- bump n-v-r for RHEL

* Mon Aug 25 2003 Adrian Havill <havill@redhat.com> 7.10.6-2
- devel subpkg needs openssl-devel as a Require (#102963)

* Tue Jul 28 2003 Adrian Havill <havill@redhat.com> 7.10.6-1
- bumped version

* Tue Jul 01 2003 Adrian Havill <havill@redhat.com> 7.10.5-1
- bumped version

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Apr 12 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 7.10.4
- adapt nousr patch

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Joe Orton <jorton@redhat.com> 7.9.8-4
- don't add -L/usr/lib to 'curl-config --libs' output

* Mon Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 7.9.8-3
- rebuild

* Wed Nov  6 2002 Joe Orton <jorton@redhat.com> 7.9.8-2
- fix `curl-config --libs` output for libdir!=/usr/lib
- remove docs/LIBCURL from docs list; remove unpackaged libcurl.la
- libtoolize and reconf

* Mon Jul 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.8-1
- 7.9.8 (# 69473)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 16 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.7-1
- 7.9.7

* Wed Apr 24 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.6-1
- 7.9.6

* Thu Mar 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.5-2
- Stop the curl-config script from printing -I/usr/include 
  and -L/usr/lib (#59497)

* Fri Mar  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.5-1
- 7.9.5

* Tue Feb 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.3-2
- Rebuild

* Wed Jan 23 2002 Nalin Dahyabhai <nalin@redhat.com> 7.9.3-1
- update to 7.9.3

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 7.9.2-2
- automated rebuild

* Wed Jan  9 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.2-1
- 7.9.2

* Fri Aug 17 2001 Nalin Dahyabhai <nalin@redhat.com>
- include curl-config in curl-devel
- update to 7.8 to fix memory leak and strlcat() symbol pollution from libcurl

* Wed Jul 18 2001 Crutcher Dunnavant <crutcher@redhat.com>
- added openssl-devel build req

* Mon May 21 2001 Tim Powers <timp@redhat.com>
- built for the distro

* Tue Apr 24 2001 Jeff Johnson <jbj@redhat.com>
- upgrade to curl-7.7.2.
- enable IPv6.

* Fri Mar  2 2001 Tim Powers <timp@redhat.com>
- rebuilt against openssl-0.9.6-1

* Thu Jan  4 2001 Tim Powers <timp@redhat.com>
- fixed mising ldconfigs
- updated to 7.5.2, bug fixes

* Mon Dec 11 2000 Tim Powers <timp@redhat.com>
- updated to 7.5.1

* Mon Nov  6 2000 Tim Powers <timp@redhat.com>
- update to 7.4.1 to fix bug #20337, problems with curl -c
- not using patch anymore, it's included in the new source. Keeping
  for reference

* Fri Oct 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix bogus req in -devel package

* Fri Oct 20 2000 Tim Powers <timp@redhat.com> 
- devel package needed defattr so that root owns the files

* Mon Oct 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 7.3
- apply vsprintf/vsnprintf patch from Colin Phipps via Debian

* Mon Aug 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- enable SSL support
- fix packager tag
- move buildroot to %%{_tmppath}

* Tue Aug 1 2000 Tim Powers <timp@redhat.com>
- fixed vendor tag for bug #15028

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Tue Jul 11 2000 Tim Powers <timp@redhat.com>
- workaround alpha build problems with optimizations

* Mon Jul 10 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jun 5 2000 Tim Powers <timp@redhat.com>
- put man pages in correct place
- use %%makeinstall

* Mon Apr 24 2000 Tim Powers <timp@redhat.com>
- updated to 6.5.2

* Wed Nov 3 1999 Tim Powers <timp@redhat.com>
- updated sources to 6.2
- gzip man page

* Mon Aug 30 1999 Tim Powers <timp@redhat.com>
- changed group

* Thu Aug 26 1999 Tim Powers <timp@redhat.com>
- changelog started
- general cleanups, changed prefix to /usr, added manpage to files section
- including in Powertools
