# remirepo spec file for gnupg1
# renamed for parallel installation, from:
#
# Fedora spec file for gnupg
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
Summary: A GNU utility for secure communication and data storage
Name: gnupg1
Version: 1.4.20
Release: 1%{?dist}
License: GPLv3+ with exceptions
Group: Applications/System
Source0: ftp://ftp.gnupg.org/gcrypt/gnupg/gnupg-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/gnupg/gnupg-%{version}.tar.bz2.sig
Source2: gnupg-shm-coprocessing.expect
Patch0: gnupg-1.4.1-gcc.patch

URL: http://www.gnupg.org/
%if 0%{?rhel} < 7
BuildRequires: autoconf268
%else
# Requires autoconf >= 2.60 because earlier autoconf didn't define $localedir.
BuildRequires: autoconf >= 2.60
%endif
BuildRequires: git
BuildRequires: automake, bzip2-devel, expect, ncurses-devel
BuildRequires: openldap-devel, readline-devel, zlib-devel, gettext-devel
BuildRequires: curl-devel
%ifnarch s390 s390x
BuildRequires: libusb-devel
%endif
# pgp-tools, perl-GnuPG-Interface include 'Requires: gpg' -- Rex
Provides: gpg = %{version}-%{release}
Provides: gnupg = %{version}-%{release}
Requires(post): /sbin/install-info
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
GnuPG (GNU Privacy Guard) is a GNU utility for encrypting data and
creating digital signatures. GnuPG has advanced key management
capabilities and is compliant with the proposed OpenPGP Internet
standard described in RFC2440. Since GnuPG doesn't use any patented
algorithm, it is not compatible with any version of PGP2 (PGP2.x uses
only IDEA for symmetric-key encryption, which is patented worldwide).

%prep
%setup -q -n gnupg-%{version}

git init
git config user.email "gnupg-owner@fedoraproject.org"
git config user.name "Fedora Ninjas"
git add .
git commit -a -q -m "%{version} baseline."
git am %{patches}

# Convert these files to UTF-8, per rpmlint.
iconv -f iso-8859-15 -t utf-8 THANKS > THANKS.utf8
mv THANKS.utf8 THANKS
git commit -a -m "run iconv"

# Hack
sed -e 's/serial-tests //' \
%if 0%{?rhel} < 7
    -e '/AM_GNU_GETTEXT_VERSION/s/0.19.3/0.17/' \
%else
    -e '/AM_GNU_GETTEXT_VERSION/s/0.19.3/0.18.2/' \
%endif
    -i configure.ac

git commit -a -m "configure hack"
git tag -a %{name}-%{version} -m "baseline"

%if 0%{?rhel} < 7
autoreconf268 -vif
%else
autoreconf -vif
%endif


%build
configure_flags=

%ifarch ppc64 sparc64
configure_flags=--disable-asm
%endif
CFLAGS="$RPM_OPT_FLAGS -fPIE -DPIC" ; export CFLAGS
LDFLAGS="$RPM_OPT_FLAGS -pie -Wl,-z,relro,-z,now" ; export LDFLAGS
%configure \
    --disable-rpath \
    --with-zlib --enable-noexecstack \
    $configure_flags
make %{?_smp_mflags}
env LANG=C expect -f %{SOURCE2}


%check
make check


%clean
rm -rf %{buildroot}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -m644 doc/gnupg1.info %{buildroot}/%{_infodir}
sed 's^\.\./g[0-9\.]*/^^g' tools/lspgpot > lspgpot
install -m755 lspgpot %{buildroot}%{_bindir}/lspgpot
rm -f %{buildroot}/%{_infodir}/dir
%find_lang gnupg

: Rename or drop binaries to avoid conflict with link from gnupg2
rm %{buildroot}%{_bindir}/gpgsplit

rm %{buildroot}%{_bindir}/gpg-zip
rm %{buildroot}%{_mandir}/man1/gpg-zip.1

mv %{buildroot}%{_bindir}/gpg         %{buildroot}%{_bindir}/gpg1
mv %{buildroot}%{_mandir}/man1/gpg.1  %{buildroot}%{_mandir}/man1/gpg1.1

mv %{buildroot}%{_bindir}/gpgv %{buildroot}%{_bindir}/gpgv1
mv %{buildroot}%{_mandir}/man1/gpgv.1 %{buildroot}%{_mandir}/man1/gpgv1.1


%post
if test -s %{_infodir}/gnupg1.info.gz ; then
    /sbin/install-info %{_infodir}/gnupg1.info.gz %{_infodir}/dir 2> /dev/null
fi
exit 0

%preun
if [ $1 = 0 ]; then
    if test -s %{_infodir}/gnupg1.info.gz ; then
        /sbin/install-info --delete %{_infodir}/gnupg1.info.gz %{_infodir}/dir 2> /dev/null
    fi
fi
exit 0

%files -f gnupg.lang
%defattr(-,root,root)
%doc AUTHORS BUGS COPYING NEWS PROJECTS README THANKS TODO
%doc doc/DETAILS doc/HACKING doc/OpenPGP doc/samplekeys.asc
%{_bindir}/gpg1
%{_bindir}/gpgv1
%{_bindir}/lspgpot
%dir %{_datadir}/gnupg
%dir %{_libexecdir}/gnupg
%{_datadir}/gnupg/FAQ
%{_datadir}/gnupg/options.skel
%{_libexecdir}/gnupg/gpgkeys_curl
%{_libexecdir}/gnupg/gpgkeys_finger
%{_libexecdir}/gnupg/gpgkeys_hkp
%{_libexecdir}/gnupg/gpgkeys_ldap
%{_infodir}/gnupg1.info.gz
%{_mandir}/man1/gpg1.1.gz
%{_mandir}/man1/gpgv1.1.gz

%changelog
* Thu Jun 16 2016 Remi Collet <remi@remirepo.net> - 1.4.20-1
- adapt for EL to install beside gnupg2

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 21 2015 Brian C. Lane <bcl@redhat.com> 1.4.20-1
- New upstream v1.4.20 (#1293112)
- Reject signatures made using the MD5 hash algorithm unless the new option --allow-weak-digest-algos or --pgp2 are given.
- New option --weak-digest to specify hash algorithms which should be considered weak.
- Changed default cipher for symmetric-only encryption to AES-128.
- Fix for DoS when importing certain garbled secret keys.
- Improved error reporting for secret subkey w/o corresponding public subkey.
- Improved error reporting in decryption due to wrong algorithm.
- Fix cluttering of stdout with trustdb info in double verbose mode.
- Pass a DBUS envvar to gpg-agent for use by gnome-keyring.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Brian C. Lane <bcl@redhat.com> 1.4.19-2
- Bump release so f20 version doesn't break upgrade path (#1231428)

* Fri Feb 27 2015 Brian C. Lane <bcl@redhat.com> 1.4.19-1
- New upstream v1.4.19
- Use ciphertext blinding for Elgamal decryption [CVE-2014-3591]
- Fixed data-dependent timing variations in modular exponentiation [related to CVE-2015-0837]
- Drop patches now included upstream

* Fri Oct 17 2014 Brian C. Lane <bcl@redhat.com> 1.4.18-4
- Add kbnode_t needed for import filter patch

* Thu Oct 16 2014 Brian C. Lane <bcl@redhat.com> 1.4.18-3
- Adding patch for rhbz#1127013 / issue1680 - import filter too strict

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 30 2014 Brian C. Lane <bcl@redhat.com> 1.4.18-1
- New upstream v1.4.18
- Fix a regression in 1.4.17 if more than one keyid is given to --recv-keys et al.
- Cap RSA and Elgamal keysize at 4096 bit also for unattended key generation.

* Mon Jun 23 2014 Brian C. Lane <bcl@redhat.com> 1.4.17-1
- New upstream v1.4.17
- Avoid DoS due to garbled compressed data packets.
- Screen keyserver reponses to avoid import of unwanted keys by rogue servers.
- Add hash algorithms to the "sig" records of the colon output.
- More specific reason codes for INV_RECP status.
- Drop gpg.ru.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 27 2014 Brian C. Lane <bcl@redhat.com> 1.4.16-4
- Cleanup some autoreconf complaints

* Sat Dec 21 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.4.16-3
- Drop INSTALL from docs.
- Fix bogus dates in %%changelog.

* Wed Dec 18 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.16-2
- New upstream v1.4.16
  fixes for CVE-2013-4576

* Mon Oct 07 2013 Brian C. Lane <bcl@redhat.com> 1.4.15-1
- New upstream v1.4.15
  fixes for CVE-2013-4402 (#1015967)
  fixes for CVE-2013-4351 (#1010140)

* Mon Jul 29 2013 Brian C. Lane <bcl@redhat.com> 1.4.14-1
- New upstream v1.4.14
  fixes for CVE-2013-4242 (#988592)
  includes fix for build on big-endian arches

* Sat Jan 26 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.13-3
- Add -vif to autoreconf to fix build failure

* Mon Jan 07 2013 Dan Horák <dan[at]danny.cz> 1.4.13-2
- fix build on big-endian arches (gnupg bug #1461)

* Wed Jan 02 2013 Brian C. Lane <bcl@redhat.com> 1.4.13-1
- New upstream v1.4.13
  fixes for CVE-2012-6085 (#891142)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 30 2012 Brian C. Lane <bcl@redhat.com> - 1.4.12-1
- New upstream v1.4.12

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 20 2010 Brian C. Lane <bcl@redhat.com> 1.4.11-2
- Added ownership of %dir %{_libexecdir}/gnupg (#644576)

* Mon Oct 18 2010 Brian C. Lane <bcl@redhat.com> 1.4.11-1
- New upstream v1.4.11
- Dropped patch gnupg-1.4.6-dir.patch, now in upstream

* Wed Jul 21 2010 Brian C. Lane <bcl@redhat.com> 1.4.10-2
- Reviving gnupg 1.x series for F-13, F-14 and rawhide

* Wed Sep  2 2009 Nalin Dahyabhai <nalin@redhat.com> 1.4.10-1
- update to 1.4.10

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Nalin Dahyabhai <nalin@redhat.com>
- switch from %%{_libdir}/%%{name} as libexecdir to regular old %%{_libexecdir}
  (part of #225847)
- remove explicit configure arguments to use bzip2 and readline, which are
  the default and trigger errors when not present, but continue to explicitly
  request zlib so that we don't fall back to the internal one if something
  ever looks "off" about the system copy (part of #225847)
- convert the ru manual and doc files to UTF-8 (the ones which aren't already,
  rpmlint)

* Tue Jul 22 2008 Nalin Dahyabhai <nalin@redhat.com> - 1.4.9-4
- describe license as actually GPLv3+ with exceptions rather than just GPLv3+
  (Todd Zullinger, #447772)
- drop unneeded patch to use gpgkeys_ldap for ldaps: URLs (#447772)

* Tue May 27 2008 Nalin Dahyabhai <nalin@redhat.com> - 1.4.9-3
- note license is actually GPLv3+ rather than just GPLv3 (Todd Zullinger,
  #447772)

* Sat May 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.4.9-2
- fix build failure with curl-7.18.1+ and gcc-4.3+ (#447772)

* Mon May 19 2008 Dennis Gilmore <dennis@ausil.us> - 1.4.9-1.1
- rebuild for sparc

* Wed Mar 26 2008 Nalin Dahyabhai <nalin@redhat.com> - 1.4.9-1
- update to 1.4.9 to fix a possible vulnerability in 1.4.8
- add a disttag
- drop patch to let us specify a dependent library for readline, as the
  readline package now links with its dependency

* Wed Mar 26 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.4.8-5
- drop Provides: openpgp
- versioned Provides: gpg

* Wed Mar 26 2008 Dennis Gilmore <dennis@ausil.us> - 1.4.8-4
- disable asm on sparc64 

* Mon Feb 25 2008 Nalin Dahyabhai <nalin@redhat.com> - 1.4.8-3
- rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.8-2
- Autorebuild for GCC 4.3

* Thu Dec 20 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.4.8-1
- update to 1.4.8, noting license change to GPLv3

* Tue Dec 04 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.4.7-8
- respin for openldap

* Thu Aug 16 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.4.7-7
- clarify license

* Fri Mar  9 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.4.7-6
- require autoconf >= 2.60, noting that we need it to define $localedir, to
  avoid cases where using older versions causes gnupg to not be able to find
  locale data (#231595)

* Mon Mar  5 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.4.7-3
- update to 1.4.7, changing the default to not allow multiple plaintexts in
  a single stream

* Tue Feb 27 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.4.6-4
- flip the switch on libtermcap/ncurses (#230187)
- rpmlint fixups

* Wed Dec  6 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.6-3
- rebuild

* Wed Dec  6 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.6-2
- rebuild

* Wed Dec  6 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.6-1
- update to 1.4.6, incorporating fixes for CVE-2006-6169 and CVE-2006-6235

* Tue Dec  5 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.5-13
- apply the termlib patch again

* Tue Dec  5 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.5-12
- don't apply the non-security termlib patch

* Tue Dec  5 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.5-11
- rebuild

* Tue Dec  5 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.5-10
- incorporate patch from Werner to fix use of stack variable after it goes
  out of scope (CVE-2006-6235, #218483)

* Fri Dec  1 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.5-9
- rebuild
- give configure a --with-termlib option which can be used to force the
  selection of libtermcap or libncurses, but don't flip the switch yet

* Fri Dec  1 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.5-8
- rebuild

* Fri Dec  1 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.5-7
- rebuild

* Fri Dec  1 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.5-6
- add patch for overflow in openfile.c from Werner's mail
  (CVE-2006-6169, #218506)

* Tue Oct 31 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.5-5
- rebuild against current libcurl

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 1.4.5-4
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)

* Tue Aug  1 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.5-3
- rebuild

* Tue Aug  1 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.5-2
- rebuild
- reenable curl support

* Tue Aug  1 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.5-1
- update to 1.4.5, fixing additional size overflows in packet parsing (#200904,
  CVE-2006-3746)
- temporarily disable curl support again

* Fri Jul 28 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.4.90-1
- update to 1.4.5rc1 to check for build problems, but mark it as 1.4.4.90
  to avoid looking "newer" than the eventual 1.4.5
- because we call aclocal, buildrequire gettext-devel to get AM_GNU_GETTEXT

* Thu Jul 20 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.4-7
- add BuildPrereq on curl-devel to get curl's ipv6 support (#198375)

* Wed Jul 12 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.4-6
- fix a cast in gpgkeys_hkp to avoid tripping stack smashing or buffer overflow
  detection (#198612)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.4.4-5.1
- rebuild

* Wed Jul  5 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.4-5
- try again using per-platform buildprereq (jkeating)

* Wed Jul  5 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.4-4
- buildprereq libusb-devel, so that we get CCID support back (#197450)

* Mon Jun 26 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.4-3
- rebuild

* Mon Jun 26 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.4-2
- rebuild

* Mon Jun 26 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.4-1
- update to 1.4.4

* Tue Jun 20 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.3-5
- rebuild

* Tue Jun 20 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.3-4
- add patch from upstream to fix CVE-2006-3082 (#195946)

* Tue Apr 11 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.3-3
- rebuild

* Tue Apr 11 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.3-2
- apply patch from David Shaw to try multiple defaults if the the photo-viewer
  option isn't set (fixes #187880)

* Fri Mar 10 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.3-1
- update to 1.4.3

* Fri Mar 10 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.2.2-2
- rebuild

* Fri Mar 10 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.2.2-1
- update to 1.4.2.2 to fix detection of unsigned data (CVE-2006-0049, #185111)

* Mon Feb 20 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.2.1-4
- rebuild

* Mon Feb 20 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.2.1-3
- add patch from David Shaw to fix error reading keyrings created with older
  versions of GnuPG (Enrico Scholz, #182163)

* Wed Feb 15 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.2.1-2
- rebuild

* Wed Feb 15 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.4.2.1-1
- update to 1.4.2.1 (fixes CVE-2006-0455)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.4.2-3.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.4.2-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Aug  9 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.2-3
- don't override libexecdir any more; we don't need to (#165462)

* Thu Aug  4 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.2-2
- pull in David Shaw's fix for key generation in batch mode

* Fri Jul 29 2005 Nalin Dahyabhai <nalin@redhat.com>
- change %%post to check if the info files are there before attempting to
  add or remove them from the info index (#91641)

* Wed Jul 27 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.2-1
- update to 1.4.2

* Thu May  5 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.1-3
- fix the execstack problem correctly this time (arjanv)

* Thu Apr 28 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.1-2
- add -Wa,--noexecstack back to CFLAGS when invoking configure, the
  --enable-noexecstack flag only seems to affect asm modules

* Wed Mar 16 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.1-1
- update to 1.4.1

* Tue Mar  8 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.0-2
- build asm modules with -Wa,--noexecstack

* Mon Jan 24 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.0-1
- comment out libusb-devel req for now so that we can build
- build the mpi asm modules with gcc, not a cpp/as setup so that we don't end
  up with text relocations in the resulting binaries (#145836)

* Wed Dec 22 2004 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.4.0

* Mon Nov  1 2004 Nalin Dahyabhai <nalin@redhat.com>
- add a pile of buildprereq

* Mon Nov  1 2004 Robert Scheck <redhat@linuxnetz.de> 1.2.6-2
- set LANG=C before running shm coprocessing build-time check (#129873)

* Thu Aug 26 2004 Nalin Dahyabhai <nalin@redhat.com> 1.2.6-1
- update to 1.2.6

* Tue Jul 27 2004 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.5
- reenable optimization on ppc64

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb  6 2004 Nalin Dahyabhai <nalin@redhat.com> 1.2.4-1
- update to 1.2.4, dropping separate ElGamal disabling patch

* Fri Dec 12 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.3-3
- rebuild

* Mon Dec  1 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.3-2
- incorporate patch from gnupg-announce which removes the ability to create
  ElGamal encrypt+sign keys or to sign messages with such keys

* Mon Oct 27 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.3-1
- use -fPIE instead of -fpie because some arches need it

* Mon Oct 27 2003 Nalin Dahyabhai <nalin@redhat.com>
- build gnupg as a position-independent executable (Arjan van de Ven)

* Mon Aug 25 2003 Nalin Dahyabhai <nalin@redhat.com>
- add Werner's key as a source file

* Fri Aug 22 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.3

* Thu Jun 19 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.2-3
- disable asm and optimization on ppc64

* Fri Jun 13 2003 Nalin Dahyabhai <nalin@redhat.com>
- add a build-time check to ensure that shm coprocessing was enabled

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May  5 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.2-1
- update to 1.2.2, fixing CAN-2003-0255

* Thu May  1 2003 Elliot Lee <sopwith@redhat.com> 1.2.1-5
- Add ppc64 patch to fix up global symbol names in assembly

* Fri Feb 28 2003 Kevin Sonney <ksonney@redhat.com> 1.2.1-4
- remove autoconf call on sparc

* Fri Feb  7 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.1-3
- modify g10defs to look for helpers in libexecdir, because that's where they
  get installed, per gnupg-users
- actually drop updates for 1.0.7 which are no longer needed for 1.2.1
  
* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Oct 28 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.1-1
- update to 1.2.1

* Tue Sep 24 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.0-1
- update to 1.2.0
- stop stripping files manually, let the buildroot policies handle it
- add translations updates ca and fr

* Tue Aug 27 2002 Nalin Dahyabhai <nalin@redhat.com> 1.0.7-6
- rebuild

* Wed Jul 24 2002 Nalin Dahyabhai <nalin@redhat.com> 1.0.7-5
- specify a menu entry when installing info pages

* Wed Jul 24 2002 Nalin Dahyabhai <nalin@redhat.com> 1.0.7-4
- add and install info pages (#67931)
- don't include two copies of the faq, add new doc files (#67931)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr 30 2002 Nalin Dahyabhai <nalin@redhat.com> 1.0.7-1
- update to 1.0.7

* Fri Feb 22 2002 Nalin Dahyabhai <nalin@redhat.com> 1.0.6-5
- rebuild

* Wed Jan 23 2002 Nalin Dahyabhai <nalin@redhat.com> 1.0.6-4
- make the codeset patch unconditional

* Thu Aug  9 2001 Nalin Dahyabhai <nalin@redhat.com> 1.0.6-3
- set message output encoding to match the message encoding, based on a
  patch by goeran@uddeborg.pp.se (#49182)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com> 1.0.6-2
- Bump release + rebuild.

* Wed May 30 2001 Nalin Dahyabhai <nalin@redhat.com> 1.0.6-1
- update to 1.0.6, fixes format string exploit

* Mon Apr 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.0.5, dropping various patches

* Tue Feb 27 2001 Trond Eivind Glomsrød <teg@redhat.com>
- langify
- strip binaries in /usr/lib/gnupg

* Tue Feb 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix the group

* Mon Dec 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- go with this version -- 1.0.4c includes a lot of changes beyond just the
  two security fixes

* Thu Dec 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- add the --allow-secret-key-import patch from CVS in case we don't get a 1.0.5

* Fri Dec  8 2000 Nalin Dahyabhai <nalin@redhat.com>
- build as an errata for 7

* Fri Dec  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- add a security patch for a problem with detached signature verification...
  might hold off for an impending 1.0.5, though

* Thu Oct 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix a bug preventing creation of .gnupg directories

* Wed Oct 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- add patch to recognize AES signatures properly (#19312)
- add gpgv to the package

* Tue Oct 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.0.4 to get security fix

* Tue Oct 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix man page typos (#18797)

* Thu Sep 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.0.3
- switch to bundled copy of the man page

* Wed Aug 30 2000 Matt Wilson <msw@redhat.com>
- rebuild to cope with glibc locale binary incompatibility, again

* Wed Aug 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- revert locale patch (#16222)

* Tue Aug 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- set all locale data instead of LC_MESSAGES and LC_TIME (#16222)

* Sun Jul 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.0.2

* Wed Jul 19 2000 Jakub Jelinek <jakub@redhat.com>
- rebuild to cope with glibc locale binary incompatibility

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jul 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- include lspgpot (#13772)

* Mon Jun  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new build environment

* Fri Feb 18 2000 Bill Nottingham <notting@redhat.com>
- build of 1.0.1

* Fri Sep 10 1999 Cristian Gafton <gafton@redhat.com>
- version 1.0.0 build for 6.1us
