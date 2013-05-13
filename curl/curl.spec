Summary: A utility for getting files from remote servers (FTP, HTTP, and others)
Name: curl
Version: 7.27.0
Release: 10%{?dist}
License: MIT
Group: Applications/Internet
Source: http://curl.haxx.se/download/%{name}-%{version}.tar.bz2
Source2: curlbuild.h
Source3: hide_selinux.c

# eliminate unnecessary inotify events on upload via file protocol (#844385)
Patch1: 0001-curl-7.27.0-1f8518c5.patch

# do not crash if MD5 fingerprint is not provided by libssh2
Patch2: 0002-curl-7.27.0-f05e5136.patch

# fix a syntax error in curl-config (#871317)
Patch3: 0003-curl-7.27.0-382429e7.patch

# do not print misleading NSS error codes
Patch4: 0004-curl-7.27.0-52b6eda4.patch

# update the links to cipher-suites supported by NSS
Patch5: 0005-curl-7.27.0-f208bf5a.patch

# prevent NSS from crashing on client auth hook failure
Patch6: 0006-curl-7.27.0-68d2830e.patch

# clear session cache if a client cert from file is used
Patch7: 0007-curl-7.27.0-b36f1d26.patch

# fix error messages for CURLE_SSL_{CACERT,CRL}_BADFILE
Patch8: 0008-curl-7.27.0-26613d78.patch

# fix buffer overflow when negotiating SASL DIGEST-MD5 auth (CVE-2013-0249)
Patch9: 0009-curl-7.27.0-f206d6c0.patch

# curl_global_init() now accepts the CURL_GLOBAL_ACK_EINTR flag
Patch10: 0010-curl-7.27.0-57ccdfa8.patch

# fix cookie tailmatching to prevent cross-domain leakage (CVE-2013-1944)
Patch11: 0011-curl-7.27.0-2eb8dcf2.patch

# show proper host name on failed resolve (#957173)
Patch12: 0012-curl-7.27.0-25e577b3.patch

# prevent an artificial timeout event due to stale speed-check data (#906031)
Patch13: 0013-curl-7.27.0-b37b5233.patch

# switch SSL socket into non-blocking mode after handshake (#960765)
Patch14: 0014-curl-7.27.0-9d0af301.patch

# patch making libcurl multilib ready
Patch101: 0101-curl-7.27.0-multilib.patch

# prevent configure script from discarding -g in CFLAGS (#496778)
Patch102: 0102-curl-7.27.0-debug.patch

# use localhost6 instead of ip6-localhost in the curl test-suite
Patch104: 0104-curl-7.19.7-localhost6.patch

# disable valgrind for certain test-cases (libssh2 problem)
Patch106: 0106-curl-7.21.0-libssh2-valgrind.patch

# work around valgrind bug (#678518)
Patch107: 0107-curl-7.21.4-libidn-valgrind.patch

# Fix character encoding of docs, which are of mixed encoding originally so
# a simple iconv can't fix them
Patch108: 0108-curl-7.27.0-utf8.patch

Provides: webclient
URL: http://curl.haxx.se/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: groff
BuildRequires: krb5-devel
BuildRequires: libidn-devel
BuildRequires: libssh2-devel >= 1.2.0
BuildRequires: openssl-devel
BuildRequires: openldap-devel >= %{openldap_version}
BuildRequires: openssh-clients
BuildRequires: openssh-server
BuildRequires: pkgconfig
BuildRequires: stunnel
BuildRequires: zlib-devel

# valgrind is not available on s390(x), sparc or arm5
%ifnarch s390 s390x %{sparc} %{arm} ppc
BuildRequires: valgrind
%endif

Requires: libcurl = %{version}-%{release}

# require at least the version of libssh2 that we were built against,
# to ensure that we have the necessary symbols available (#525002, #642796)
%global libssh2_version %(pkg-config --modversion libssh2 2>/dev/null || echo 0)

# older version than 12.el5_6.5 doesn't provides "ldap_init_fd"
%global openldap_version 2.3.43-25.el5_8.1

%description
curl is a command line tool for transferring data with URL syntax, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP.  curl supports SSL certificates, HTTP POST, HTTP PUT, FTP
uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, kerberos...), file transfer
resume, proxy tunneling and a busload of other useful tricks. 

%package -n libcurl
Summary: A library for getting files from web servers
Group: Development/Libraries
Requires: libssh2%{?_isa} >= %{libssh2_version}
Requires: openldap >= %{openldap_version}

%description -n libcurl
libcurl is a free and easy-to-use client-side URL transfer library, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP. libcurl supports SSL certificates, HTTP POST, HTTP PUT,
FTP uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, Kerberos4), file transfer
resume, http proxy tunneling and more.

%package -n libcurl-devel
Summary: Files needed for building applications with libcurl
Group: Development/Libraries
Requires: libcurl = %{version}-%{release}

# From Fedora 14, %%{_datadir}/aclocal is included in the filesystem package
%if 0%{?fedora} < 14
Requires: %{_datadir}/aclocal
%endif

# From Fedora 11, RHEL-6, pkgconfig dependency is auto-detected
%if 0%{?fedora} < 11 && 0%{?rhel} < 6
Requires: pkgconfig
%endif

Provides: curl-devel = %{version}-%{release}
Obsoletes: curl-devel < %{version}-%{release}

%description -n libcurl-devel
The libcurl-devel package includes header files and libraries necessary for
developing programs which use the libcurl library. It contains the API
documentation of the library, too.

%prep
%setup -q

# upstream patches
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1

# Fedora patches
%patch101 -p1
%patch102 -p1
%patch104 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1

# replace hard wired port numbers in the test suite
%ifarch x86_64
sed -i s/899\\\([0-9]\\\)/649\\1/ tests/data/test*
%else
sed -i s/899\\\([0-9]\\\)/329\\1/ tests/data/test*
%endif

# disable test 1112 (#565305)
printf "1112\n" >> tests/data/DISABLED

# disable test 1319 on ppc64 (server times out)
%ifarch ppc64
echo "1319" >> tests/data/DISABLED
%endif


%build
[ -x /usr/kerberos/bin/krb5-config ] && KRB5_PREFIX="=/usr/kerberos"
%configure --disable-static \
    --enable-hidden-symbols \
    --enable-ipv6 \
    --enable-ldaps \
    --enable-manual \
    --enable-threaded-resolver \
    --with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt \
    --with-gssapi${KRB5_PREFIX} \
    --with-libidn \
    --with-libssh2 \
    --with-ssl --without-nss
#    --enable-debug
# use ^^^ to turn off optimizations, etc.

# Remove bogus rpath
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%check
LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}
export LD_LIBRARY_PATH

# uncomment to use the non-stripped library in tests
# LD_PRELOAD=`find -name \*.so`
# LD_PRELOAD=`readlink -f $LD_PRELOAD`

cd tests
make %{?_smp_mflags}

# make it possible to start a testing OpenSSH server with SELinux
# in the enforcing mode (#521087)
gcc -o hide_selinux.so -fPIC -shared %{SOURCE3}
LD_PRELOAD="`readlink -f ./hide_selinux.so`:$LD_PRELOAD"
export LD_PRELOAD

# Ignore this tests for now (use !xxx)
DISABLED=

# use different port range for 32bit and 64bit build, thus make it possible
# to run both in parallel on the same machine
%ifarch x86_64
./runtests.pl -a -b6490 -p -v $DISABLED
%else
./runtests.pl -a -b3290 -p -v $DISABLED
%endif


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" install

rm -f ${RPM_BUILD_ROOT}%{_libdir}/libcurl.la

install -d $RPM_BUILD_ROOT%{_datadir}/aclocal
install -m 644 docs/libcurl/libcurl.m4 $RPM_BUILD_ROOT%{_datadir}/aclocal

# drop man page for a script we do not distribute
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/mk-ca-bundle.1

# Make libcurl-devel multilib-ready (bug #488922)
%ifarch x86_64
%define _curlbuild_h curlbuild-64.h
%else
%define _curlbuild_h curlbuild-32.h
%endif
mv $RPM_BUILD_ROOT%{_includedir}/curl/curlbuild.h \
   $RPM_BUILD_ROOT%{_includedir}/curl/%{_curlbuild_h}

install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_includedir}/curl/curlbuild.h

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libcurl -p /sbin/ldconfig

%postun -n libcurl -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc CHANGES README* COPYING
%doc docs/BUGS docs/FAQ docs/FEATURES
%doc docs/MANUAL docs/RESOURCES
%doc docs/TheArtOfHttpScripting docs/TODO
%{_bindir}/curl
%{_mandir}/man1/curl.1*

%files -n libcurl
%defattr(-,root,root,-)
%{_libdir}/libcurl.so.4*

%files -n libcurl-devel
%defattr(-,root,root,-)
%doc docs/examples/*.c docs/examples/Makefile.example docs/INTERNALS
%doc docs/CONTRIBUTE docs/libcurl/ABI
%{_bindir}/curl-config*
%{_includedir}/curl
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/curl-config.1*
%{_mandir}/man3/*
%{_datadir}/aclocal/libcurl.m4

%changelog
* Mon May 13 2013 Remi Collet <RPMS@FamilleCollet.com> - 7.27.0-10
- sync with 7.27.0-10 from F18

* Thu May 09 2013 Kamil Dudka <kdudka@redhat.com> 7.27.0-10
- switch SSL socket into non-blocking mode after handshake (#960765)

* Fri Apr 26 2013 Kamil Dudka <kdudka@redhat.com> 7.27.0-9
- prevent an artificial timeout event due to stale speed-check data (#906031)
- show proper host name on failed resolve (#957173)

* Fri Apr 12 2013 Kamil Dudka <kdudka@redhat.com> 7.27.0-8
- fix cookie tailmatching to prevent cross-domain leakage (CVE-2013-1944)

* Mon Oct 17 2011 Remi Collet <RPMS@FamilleCollet.com> - 7.27.0-7
- sync with 7.27.0-7 from F18

* Mon Oct 17 2011 Remi Collet <RPMS@FamilleCollet.com> - 7.21.7-5.2
- dump release and build against libssh2 1.2.7

* Mon Oct 17 2011 Remi Collet <RPMS@FamilleCollet.com> - 7.21.7-5.1
- use openssl instead of nss (unusable on EL-5)

* Sun Sep 25 2011 Remi Collet <RPMS@FamilleCollet.com> - 7.21.7-5
- sync with fedora 16

* Mon Sep 19 2011 Kamil Dudka <kdudka@redhat.com> 7.21.7-5
- curl-config now provides dummy --static-libs option (#733956)
- break busy loops in tests 502, 555, and 573

* Tue Sep 13 2011 Remi Collet <RPMS@FamilleCollet.com> - 7.21.7-4.1
- raise openldap dependency

* Thu Aug 25 2011 Remi Collet <RPMS@FamilleCollet.com> - 7.21.7-4
- sync with rawhide

* Sun Aug 21 2011 Paul Howarth <paul@city-fan.org> 7.21.7-4
- actually fix SIGSEGV of curl -O -J given more than one URL (#723075)

* Tue Aug 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 7.21.7-3.14
- keep "libcurl" name (and provides compat-libcurl3 as another package)

* Tue Aug 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 7.21.7-3
- sync with rawhide
- disable tests which requires libnsspem.so (not available in EL-5)

* Mon Aug 15 2011 Kamil Dudka <kdudka@redhat.com> 7.21.7-3
- fix SIGSEGV of curl -O -J given more than one URL (#723075)
- introduce the --delegation option of curl (#730444)
- initialize NSS with no database if the selected database is broken (#728562)

* Wed Aug 03 2011 Kamil Dudka <kdudka@redhat.com> 7.21.7-2
- add a new option CURLOPT_GSSAPI_DELEGATION (#719939)

* Sun Jul 24 2011 Remi Collet <RPMS@FamilleCollet.com> - 7.21.7-1
- rebuild for remi repo with libcurl4 sub-packages

* Thu Jun 23 2011 Kamil Dudka <kdudka@redhat.com> 7.21.7-1
- new upstream release (fixes CVE-2011-2192)

* Wed Jun 08 2011 Kamil Dudka <kdudka@redhat.com> 7.21.6-2
- avoid an invalid timeout event on a reused handle (#679709)

* Sat Apr 23 2011 Paul Howarth <paul@city-fan.org> 7.21.6-1
- new upstream release

* Mon Apr 18 2011 Kamil Dudka <kdudka@redhat.com> 7.21.5-2
- fix the output of curl-config --version (upstream commit 82ecc85)

* Mon Apr 18 2011 Kamil Dudka <kdudka@redhat.com> 7.21.5-1
- new upstream release

* Sat Apr 16 2011 Peter Robinson <pbrobinson@gmail.com> 7.21.4-4
- no valgrind on ARMv5 arches

* Sat Mar 05 2011 Dennis Gilmore <dennis@ausil.us> 7.21.4-3
- no valgrind on sparc arches

* Tue Feb 22 2011 Kamil Dudka <kdudka@redhat.com> 7.21.4-2
- do not ignore failure of SSL handshake (upstream commit 7aa2d10)

* Fri Feb 18 2011 Kamil Dudka <kdudka@redhat.com> 7.21.4-1
- new upstream release
- avoid memory leak on SSL connection failure (upstream commit a40f58d)
- work around valgrind bug (#678518)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.21.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Kamil Dudka <kdudka@redhat.com> 7.21.3-2
- build libcurl with --enable-hidden-symbols

* Thu Dec 16 2010 Paul Howarth <paul@city-fan.org> 7.21.3-1
- update to 7.21.3:
  - added --noconfigure switch to testcurl.pl
  - added --xattr option
  - added CURLOPT_RESOLVE and --resolve
  - added CURLAUTH_ONLY
  - added version-check.pl to the examples dir
  - check for libcurl features for some command line options
  - Curl_setopt: disallow CURLOPT_USE_SSL without SSL support
  - http_chunks: remove debug output
  - URL-parsing: consider ? a divider
  - SSH: avoid using the libssh2_ prefix
  - SSH: use libssh2_session_handshake() to work on win64
  - ftp: prevent server from hanging on closed data connection when stopping
    a transfer before the end of the full transfer (ranges)
  - LDAP: detect non-binary attributes properly
  - ftp: treat server's response 421 as CURLE_OPERATION_TIMEDOUT
  - gnutls->handshake: improved timeout handling
  - security: pass the right parameter to init
  - krb5: use GSS_ERROR to check for error
  - TFTP: resend the correct data
  - configure: fix autoconf 2.68 warning: no AC_LANG_SOURCE call detected
  - GnuTLS: now detects socket errors on Windows
  - symbols-in-versions: updated en masse
  - added a couple of examples that were missing from the tarball
  - Curl_send/recv_plain: return errno on failure
  - Curl_wait_for_resolv (for c-ares): correct timeout
  - ossl_connect_common: detect connection re-use
  - configure: prevent link errors with --librtmp
  - openldap: use remote port in URL passed to ldap_init_fd()
  - url: provide dead_connection flag in Curl_handler::disconnect
  - lots of compiler warning fixes
  - ssh: fix a download resume point calculation
  - fix getinfo CURLINFO_LOCAL* for reused connections
  - multi: the returned running handles counter could turn negative
  - multi: only ever consider pipelining for connections doing HTTP(S)
- drop upstream patches now in tarball
- update bz650255 and disable-test1112 patches to apply against new codebase
- add workaround for false-positive glibc-detected buffer overflow in tftpd
  test server with FORTIFY_SOURCE (similar to #515361)

* Fri Nov 12 2010 Kamil Dudka <kdudka@redhat.com> 7.21.2-5
- do not send QUIT to a dead FTP control connection (#650255)
- pull back glibc's implementation of str[n]casecmp(), #626470 appears fixed

* Tue Nov 09 2010 Kamil Dudka <kdudka@redhat.com> 7.21.2-4
- prevent FTP client from hanging on unrecognized ABOR response (#649347)
- return more appropriate error code in case FTP server session idle
  timeout has exceeded (#650255)

* Fri Oct 29 2010 Kamil Dudka <kdudka@redhat.com> 7.21.2-3
- prevent FTP server from hanging on closed data connection (#643656)

* Thu Oct 14 2010 Paul Howarth <paul@city-fan.org> 7.21.2-2
- enforce versioned libssh2 dependency for libcurl (#642796)

* Wed Oct 13 2010 Kamil Dudka <kdudka@redhat.com> 7.21.2-1
- new upstream release, drop applied patches
- make 0102-curl-7.21.2-debug.patch less intrusive

* Wed Sep 29 2010 jkeating - 7.21.1-6
- Rebuilt for gcc bug 634757

* Sat Sep 11 2010 Kamil Dudka <kdudka@redhat.com> 7.21.1-5
- make it possible to run SCP/SFTP tests on x86_64 (#632914)

* Tue Sep 07 2010 Kamil Dudka <kdudka@redhat.com> 7.21.1-4
- work around glibc/valgrind problem on x86_64 (#631449)

* Tue Aug 24 2010 Paul Howarth <paul@city-fan.org> 7.21.1-3
- fix up patches so there's no need to run autotools in the rpm build
- drop buildreq automake
- drop dependency on automake for devel package from F-14, where
  %%{_datadir}/aclocal is included in the filesystem package
- drop dependency on pkgconfig for devel package from F-11, where
  pkgconfig dependencies are auto-generated

* Mon Aug 23 2010 Kamil Dudka <kdudka@redhat.com> 7.21.1-2
- re-enable test575 on s390(x), already fixed (upstream commit d63bdba)
- modify system headers to work around gcc bug (#617757)
- curl -T now ignores file size of special files (#622520)
- fix kerberos proxy authentication for https (#625676)
- work around glibc/valgrind problem on x86_64 (#626470)

* Thu Aug 12 2010 Kamil Dudka <kdudka@redhat.com> 7.21.1-1
- new upstream release

* Mon Jul 12 2010 Dan Horák <dan[at]danny.cz> 7.21.0-3
- disable test 575 on s390(x)

* Mon Jun 28 2010 Kamil Dudka <kdudka@redhat.com> 7.21.0-2
- add support for NTLM authentication (#603783)

* Wed Jun 16 2010 Kamil Dudka <kdudka@redhat.com> 7.21.0-1
- new upstream release, drop applied patches
- update of %%description
- disable valgrind for certain test-cases (libssh2 problem)

* Tue May 25 2010 Kamil Dudka <kdudka@redhat.com> 7.20.1-6
- fix -J/--remote-header-name to strip CR-LF (upstream patch)

* Wed Apr 28 2010 Kamil Dudka <kdudka@redhat.com> 7.20.1-5
- CRL support now works again (#581926)
- make it possible to start a testing OpenSSH server when building with SELinux
  in the enforcing mode (#521087)

* Sat Apr 24 2010 Kamil Dudka <kdudka@redhat.com> 7.20.1-4
- upstream patch preventing failure of test536 with threaded DNS resolver
- upstream patch preventing SSL handshake timeout underflow

* Thu Apr 22 2010 Paul Howarth <paul@city-fan.org> 7.20.1-3
- replace Rawhide s390-sleep patch with a more targeted patch adding a
  delay after tests 513 and 514 rather than after all tests

* Wed Apr 21 2010 Kamil Dudka <kdudka@redhat.com> 7.20.1-2
- experimentally enabled threaded DNS lookup
- make curl-config multilib ready again (#584107)

* Mon Apr 19 2010 Kamil Dudka <kdudka@redhat.com> 7.20.1-1
- new upstream release

* Tue Mar 23 2010 Kamil Dudka <kdudka@redhat.com> 7.20.0-4
- add missing quote in libcurl.m4 (#576252)

* Fri Mar 19 2010 Kamil Dudka <kdudka@redhat.com> 7.20.0-3
- throw CURLE_SSL_CERTPROBLEM in case peer rejects a certificate (#565972)
- valgrind temporarily disabled (#574889)
- kerberos installation prefix has been changed

* Wed Feb 24 2010 Kamil Dudka <kdudka@redhat.com> 7.20.0-2
- exclude test1112 from the test suite (#565305)

* Thu Feb 11 2010 Kamil Dudka <kdudka@redhat.com> 7.20.0-1
- new upstream release - added support for IMAP(S), POP3(S), SMTP(S) and RTSP
- dropped patches applied upstream
- dropped curl-7.16.0-privlibs.patch no longer useful
- a new patch forcing -lrt when linking the curl tool and test-cases

* Fri Jan 29 2010 Kamil Dudka <kdudka@redhat.com> 7.19.7-11
- upstream patch adding a new option -J/--remote-header-name
- dropped temporary workaround for #545779

* Thu Jan 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 7.19.7-10
- bump for libssh2 rebuild

* Sun Dec 20 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-9
- temporary workaround for #548269
  (restored behavior of 7.19.7-4)

* Wed Dec 09 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-8
- replace hard wired port numbers in the test suite

* Wed Dec 09 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-7
- use different port numbers for 32bit and 64bit builds
- temporary workaround for #545779

* Tue Dec 08 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-6
- make it possible to run test241
- re-enable SCP/SFTP tests (#539444)

* Sat Dec 05 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-5
- avoid use of uninitialized value in lib/nss.c
- suppress failure of test513 on s390

* Tue Dec 01 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-4
- do not require valgrind on s390 and s390x
- temporarily disabled SCP/SFTP test-suite (#539444)

* Thu Nov 12 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-3
- fix crash on doubly closed NSPR descriptor, patch contributed
  by Kevin Baughman (#534176)
- new version of patch for broken TLS servers (#525496, #527771)

* Wed Nov 04 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-2
- increased release number (CVS problem)

* Wed Nov 04 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-1
- new upstream release, dropped applied patches
- workaround for broken TLS servers (#525496, #527771)

* Wed Oct 14 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-13
- fix timeout issues and gcc warnings within lib/nss.c

* Tue Oct 06 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-12
- upstream patch for NSS support written by Guenter Knauf

* Wed Sep 30 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-11
- build libcurl with c-ares support (#514771)

* Sun Sep 27 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-10
- require libssh2>=1.2 properly (#525002)

* Sat Sep 26 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-9
- let curl test-suite use valgrind
- require libssh2>=1.2 (#525002)

* Mon Sep 21 2009 Chris Weyl <cweyl@alumni.drew.edu> - 7.19.6-8
- rebuild for libssh2 1.2

* Thu Sep 17 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-7
- make curl test-suite more verbose

* Wed Sep 16 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-6
- update polling patch to the latest upstream version

* Thu Sep 03 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-5
- cover ssh and stunnel support by the test-suite

* Wed Sep 02 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-4
- use pkg-config to find nss and libssh2 if possible
- better patch (not only) for SCP/SFTP polling
- improve error message for not matching common name (#516056)

* Fri Aug 21 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-3
- avoid tight loop during a sftp upload
- http://permalink.gmane.org/gmane.comp.web.curl.library/24744

* Tue Aug 18 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-2
- let curl package depend on the same version of libcurl

* Fri Aug 14 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-1
- new upstream release, dropped applied patches
- changed NSS code to not ignore the value of ssl.verifyhost and produce more
  verbose error messages (#516056)

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 7.19.5-10
- Use lzma compressed upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-8
- do not pre-login to all PKCS11 slots, it causes problems with HW tokens
- try to select client certificate automatically when not specified, thanks
  to Claes Jakobsson

* Fri Jul 10 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-7
- fix SIGSEGV when using NSS client certificates, thanks to Claes Jakobsson

* Sun Jul 05 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-6
- force test suite to use the just built libcurl, thanks to Paul Howarth

* Thu Jul 02 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-5
- run test suite after build
- enable built-in manual

* Wed Jun 24 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-4
- fix bug introduced by the last build (#504857)

* Wed Jun 24 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-3
- exclude curlbuild.h content from spec (#504857)

* Wed Jun 10 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-2
- avoid unguarded comparison in the spec file, thanks to R P Herrold (#504857)

* Tue May 19 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-1
- update to 7.19.5, dropped applied patches

* Mon May 11 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-11
- fix infinite loop while loading a private key, thanks to Michael Cronenworth
  (#453612)

* Mon Apr 27 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-10
- fix curl/nss memory leaks while using client certificate (#453612, accepted
  by upstream)

* Wed Apr 22 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-9
- add missing BuildRequire for autoconf

* Wed Apr 22 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-8
- fix configure.ac to not discard -g in CFLAGS (#496778)

* Tue Apr 21 2009 Debarshi Ray <rishi@fedoraproject.org> 7.19.4-7
- Fixed configure to respect the environment's CFLAGS and CPPFLAGS settings.

* Tue Apr 14 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-6
- upstream patch fixing memory leak in lib/nss.c (#453612)
- remove redundant dependency of libcurl-devel on libssh2-devel

* Wed Mar 18 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-5
- enable 6 additional crypto algorithms by default (#436781,
  accepted by upstream)

* Thu Mar 12 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-4
- fix memory leak in src/main.c (accepted by upstream)
- avoid using %%ifarch

* Wed Mar 11 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-3
- make libcurl-devel multilib-ready (bug #488922)

* Fri Mar 06 2009 Jindrich Novy <jnovy@redhat.com> 7.19.4-2
- drop .easy-leak patch, causes problems in pycurl (#488791)
- fix libcurl-devel dependencies (#488895)

* Tue Mar 03 2009 Jindrich Novy <jnovy@redhat.com> 7.19.4-1
- update to 7.19.4 (fixes CVE-2009-0037)
- fix leak in curl_easy* functions, thanks to Kamil Dudka
- drop nss-fix patch, applied upstream

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Kamil Dudka <kdudka@redhat.com> 7.19.3-1
- update to 7.19.3, dropped applied nss patches
- add patch fixing 7.19.3 curl/nss bugs

* Mon Dec 15 2008 Jindrich Novy <jnovy@redhat.com> 7.18.2-9
- rebuild for f10/rawhide cvs tag clashes

* Sat Dec 06 2008 Jindrich Novy <jnovy@redhat.com> 7.18.2-8
- use improved NSS patch, thanks to Rob Crittenden (#472489)

* Tue Sep 09 2008 Jindrich Novy <jnovy@redhat.com> 7.18.2-7
- update the thread safety patch, thanks to Rob Crittenden (#462217)

* Wed Sep 03 2008 Warren Togami <wtogami@redhat.com> 7.18.2-6
- add thread safety to libcurl NSS cleanup() functions (#459297)

* Fri Aug 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 7.18.2-5
- undo mini libcurl.so.3

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 7.18.2-4
- make miniature library for libcurl.so.3

* Wed Jul  4 2008 Jindrich Novy <jnovy@redhat.com> 7.18.2-3
- enable support for libssh2 (#453958)

* Wed Jun 18 2008 Jindrich Novy <jnovy@redhat.com> 7.18.2-2
- fix curl_multi_perform() over a proxy (#450140), thanks to
  Rob Crittenden

* Wed Jun  4 2008 Jindrich Novy <jnovy@redhat.com> 7.18.2-1
- update to 7.18.2

* Wed May  7 2008 Jindrich Novy <jnovy@redhat.com> 7.18.1-2
- spec cleanup, thanks to Paul Howarth (#225671)
  - drop BR: libtool
  - convert CHANGES and README to UTF-8
  - _GNU_SOURCE in CFLAGS is no more needed
  - remove bogus rpath

* Mon Mar 31 2008 Jindrich Novy <jnovy@redhat.com> 7.18.1-1
- update to curl 7.18.1 (fixes #397911)
- add ABI docs for libcurl
- remove --static-libs from curl-config
- drop curl-config patch, obsoleted by @SSL_ENABLED@ autoconf
  substitution (#432667)

* Fri Feb 15 2008 Jindrich Novy <jnovy@redhat.com> 7.18.0-2
- define _GNU_SOURCE so that NI_MAXHOST gets defined from glibc

* Mon Jan 28 2008 Jindrich Novy <jnovy@redhat.com> 7.18.0-1
- update to curl-7.18.0
- drop sslgen patch -> applied upstream
- fix typo in description

* Tue Jan 22 2008 Jindrich Novy <jnovy@redhat.com> 7.17.1-6
- fix curl-devel obsoletes so that we don't break F8->F9 upgrade
  path (#429612)

* Tue Jan  8 2008 Jindrich Novy <jnovy@redhat.com> 7.17.1-5
- do not attempt to close a bad socket (#427966),
  thanks to Caolan McNamara

* Tue Dec  4 2007 Jindrich Novy <jnovy@redhat.com> 7.17.1-4
- rebuild because of the openldap soname bump
- remove old nsspem patch

* Fri Nov 30 2007 Jindrich Novy <jnovy@redhat.com> 7.17.1-3
- drop useless ldap library detection since curl doesn't
  dlopen()s it but links to it -> BR: openldap-devel
- enable LDAPS support (#225671), thanks to Paul Howarth
- BR: krb5-devel to reenable GSSAPI support
- simplify build process
- update description

* Wed Nov 21 2007 Jindrich Novy <jnovy@redhat.com> 7.17.1-2
- update description to contain complete supported servers list (#393861)

* Sat Nov 17 2007 Jindrich Novy <jnovy@redhat.com> 7.17.1-1
- update to curl 7.17.1
- include patch to enable SSL usage in NSS when a socket is opened
  nonblocking, thanks to Rob Crittenden (rcritten@redhat.com)

* Wed Oct 24 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-10
- correctly provide/obsolete curl-devel (#130251)

* Wed Oct 24 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-9
- create libcurl and libcurl-devel subpackages (#130251)

* Thu Oct 11 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-8
- list features correctly when curl is compiled against NSS (#316191)

* Mon Sep 17 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-7
- add zlib-devel BR to enable gzip compressed transfers in curl (#292211)

* Mon Sep 10 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-6
- provide webclient (#225671)

* Thu Sep  6 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-5
- add support for the NSS PKCS#11 pem reader so the command-line is the
  same for both OpenSSL and NSS by Rob Crittenden (rcritten@redhat.com)
- switch to NSS again

* Mon Sep  3 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-4
- revert back to use OpenSSL (#266021)

* Mon Aug 27 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-3
- don't use openssl, use nss instead

* Fri Aug 10 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-2
- fix anonymous ftp login (#251570), thanks to David Cantrell

* Wed Jul 11 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-1
- update to 7.16.4

* Mon Jun 25 2007 Jindrich Novy <jnovy@redhat.com> 7.16.3-1
- update to 7.16.3
- drop .print patch, applied upstream
- next series of merge review fixes by Paul Howarth
- remove aclocal stuff, no more needed
- simplify makefile arguments
- don't reference standard library paths in libcurl.pc
- include docs/CONTRIBUTE

* Mon Jun 18 2007 Jindrich Novy <jnovy@redhat.com> 7.16.2-5
- don't print like crazy (#236981), backported from upstream CVS

* Fri Jun 15 2007 Jindrich Novy <jnovy@redhat.com> 7.16.2-4
- another series of review fixes (#225671),
  thanks to Paul Howarth
- check version of ldap library automatically
- don't use %%makeinstall and preserve timestamps
- drop useless patches

* Fri May 11 2007 Jindrich Novy <jnovy@redhat.com> 7.16.2-3
- add automake BR to curl-devel to fix aclocal dir. ownership,
  thanks to Patrice Dumas

* Thu May 10 2007 Jindrich Novy <jnovy@redhat.com> 7.16.2-2
- package libcurl.m4 in curl-devel (#239664), thanks to Quy Tonthat

* Wed Apr 11 2007 Jindrich Novy <jnovy@redhat.com> 7.16.2-1
- update to 7.16.2

* Mon Feb 19 2007 Jindrich Novy <jnovy@redhat.com> 7.16.1-3
- don't create/ship static libraries (#225671)

* Mon Feb  5 2007 Jindrich Novy <jnovy@redhat.com> 7.16.1-2
- merge review related spec fixes (#225671)

* Mon Jan 29 2007 Jindrich Novy <jnovy@redhat.com> 7.16.1-1
- update to 7.16.1

* Tue Jan 16 2007 Jindrich Novy <jnovy@redhat.com> 7.16.0-5
- don't package generated makefiles for docs/examples to avoid
  multilib conflicts

* Mon Dec 18 2006 Jindrich Novy <jnovy@redhat.com> 7.16.0-4
- convert spec to UTF-8
- don't delete BuildRoot in %%prep phase
- rpmlint fixes

* Thu Nov 16 2006 Jindrich Novy <jnovy@redhat.com> -7.16.0-3
- prevent curl from dlopen()ing missing ldap libraries so that
  ldap:// requests work (#215928)

* Tue Oct 31 2006 Jindrich Novy <jnovy@redhat.com> - 7.16.0-2
- fix BuildRoot
- add Requires: pkgconfig for curl-devel
- move LDFLAGS and LIBS to Libs.private in libcurl.pc.in (#213278)

* Mon Oct 30 2006 Jindrich Novy <jnovy@redhat.com> - 7.16.0-1
- update to curl-7.16.0

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
