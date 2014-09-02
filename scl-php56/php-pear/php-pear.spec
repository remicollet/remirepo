%{?scl:%scl_package php-pear}
%{!?scl:%global pkg_name %{name}}
%{!?scl:%global _root_sysconfdir %{_sysconfdir}}

%global peardir %{_datadir}/pear
%global metadir %{_localstatedir}/lib/pear

%global getoptver 1.3.1
%global arctarver 1.3.12
# https://pear.php.net/bugs/bug.php?id=19367
# Structures_Graph 1.0.4 - incorrect FSF address
%global structver 1.0.4
%global xmlutil   1.2.3

%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_root_sysconfdir}/rpm; echo $d)


Summary: PHP Extension and Application Repository framework
Name: %{?scl_prefix}php-pear
Version: 1.9.5
Release: 1%{?dist}
Epoch: 1
# PEAR, Archive_Tar, XML_Util are BSD
# Console_Getopt is PHP
# Structures_Graph is LGPLv2+
License: BSD and PHP and LGPLv2+
Group: Development/Languages
URL: http://pear.php.net/package/PEAR
Source0: http://download.pear.php.net/package/PEAR-%{version}.tgz
# wget https://raw.github.com/pear/pear-core/master/install-pear.php
Source1: install-pear.php
Source3: strip.php
Source10: pear.sh
Source11: pecl.sh
Source12: peardev.sh
Source13: macros.pear
Source21: http://pear.php.net/get/Archive_Tar-%{arctarver}.tgz
Source22: http://pear.php.net/get/Console_Getopt-%{getoptver}.tgz
Source23: http://pear.php.net/get/Structures_Graph-%{structver}.tgz
Source24: http://pear.php.net/get/XML_Util-%{xmlutil}.tgz
# Man pages
# https://github.com/pear/pear-core/pull/14
Source30: pear.1
Source31: pecl.1
Source32: peardev.1
# https://github.com/pear/pear-core/pull/16
Source33: pear.conf.5

# From RHEL: ignore REST cache creation failures as non-root user (#747361)
# TODO See https://github.com/pear/pear-core/commit/dfef86e05211d2abc7870209d69064d448ef53b3#PEAR/REST.php
Patch0: php-pear-1.9.4-restcache.patch
# Relocate Metadata
Patch1: php-pear-metadata.patch

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{?scl_prefix}php-cli >= 5.1.0-1, %{?scl_prefix}php-xml, gnupg

Provides:  %{?scl_prefix}php-pear(Console_Getopt) = %{getoptver}
Provides:  %{?scl_prefix}php-pear(Archive_Tar) = %{arctarver}
Provides:  %{?scl_prefix}php-pear(PEAR) = %{version}
Provides:  %{?scl_prefix}php-pear(Structures_Graph) = %{structver}
Provides:  %{?scl_prefix}php-pear(XML_Util) = %{xmlutil}

Requires:  %{?scl_prefix}php-cli
# phpci detected extension
# PEAR (date, spl always builtin):
Requires:  %{?scl_prefix}php-ftp
Requires:  %{?scl_prefix}php-pcre
Requires:  %{?scl_prefix}php-posix
Requires:  %{?scl_prefix}php-tokenizer
Requires:  %{?scl_prefix}php-xml
Requires:  %{?scl_prefix}php-zlib
# Console_Getopt: pcre
# Archive_Tar: pcre, posix, zlib
Requires:  %{?scl_prefix}php-bz2
# Structures_Graph: none
# XML_Util: pcre
# optional: overload and xdebug


%description
PEAR is a framework and distribution system for reusable PHP
components.  This package contains the basic PEAR components.

%prep
%setup -cT

# Create a usable PEAR directory (used by install-pear.php)
for archive in %{SOURCE0} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24}
do
    tar xzf  $archive --strip-components 1 || tar xzf  $archive --strip-path 1
    file=${archive##*/}
    [ -f LICENSE ] && mv LICENSE LICENSE-${file%%-*}
    [ -f README ]  && mv README  README-${file%%-*}

    tar xzf $archive 'package*xml'
    [ -f package2.xml ] && mv package2.xml ${file%%-*}.xml \
                        || mv package.xml  ${file%%-*}.xml
done
cp %{SOURCE1} %{SOURCE30} %{SOURCE31} %{SOURCE32} %{SOURCE33} .

# apply patches on used PEAR during install
%patch1 -p0 -b .metadata

sed -e 's/@SCL@/%{?scl:%{scl}_}/' \
    -e 's:@VARDIR@:%{_localstatedir}:' \
    -e 's:@BINDIR@:%{_bindir}:' \
    %{SOURCE13} | tee macros.pear


%build
# This is an empty build section.

%install
rm -rf $RPM_BUILD_ROOT

export PHP_PEAR_SYSCONF_DIR=%{_sysconfdir}
export PHP_PEAR_SIG_KEYDIR=%{_sysconfdir}/pearkeys
export PHP_PEAR_SIG_BIN=%{_root_bindir}/gpg
export PHP_PEAR_INSTALL_DIR=%{peardir}

# 1.4.11 tries to write to the cache directory during installation
# so it's not possible to set a sane default via the environment.
# The ${PWD} bit will be stripped via relocate.php later.
export PHP_PEAR_CACHE_DIR=${PWD}%{_localstatedir}/cache/php-pear
export PHP_PEAR_TEMP_DIR=/var/tmp

install -d $RPM_BUILD_ROOT%{peardir} \
           $RPM_BUILD_ROOT%{_localstatedir}/cache/php-pear \
           $RPM_BUILD_ROOT%{_localstatedir}/www/html \
           $RPM_BUILD_ROOT%{_localstatedir}/lib/pear/pkgxml \
           $RPM_BUILD_ROOT%{_docdir}/pecl \
           $RPM_BUILD_ROOT%{_datadir}/tests/pecl \
           $RPM_BUILD_ROOT%{_sysconfdir}/pear

export INSTALL_ROOT=$RPM_BUILD_ROOT

%{_bindir}/php --version

%{_bindir}/php -dmemory_limit=64M -dshort_open_tag=0 -dsafe_mode=0 \
         -d 'error_reporting=E_ALL&~E_DEPRECATED' -ddetect_unicode=0 \
         install-pear.php --force \
                 --dir      %{peardir} \
                 --cache    %{_localstatedir}/cache/php-pear \
                 --config   %{_sysconfdir}/pear \
                 --bin      %{_bindir} \
                 --www      %{_localstatedir}/www/html \
                 --doc      %{_docdir}/pear \
                 --test     %{_datadir}/tests/pear \
                 --data     %{_datadir}/pear-data \
                 --metadata %{metadir} \
                 %{SOURCE0} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24}

# Replace /usr/bin/* with simple scripts:
install -m 755 %{SOURCE10} $RPM_BUILD_ROOT%{_bindir}/pear
install -m 755 %{SOURCE11} $RPM_BUILD_ROOT%{_bindir}/pecl
install -m 755 %{SOURCE12} $RPM_BUILD_ROOT%{_bindir}/peardev
for exe in pear pecl peardev; do
    sed -e 's:/usr:%{_prefix}:' \
        -i $RPM_BUILD_ROOT%{_bindir}/$exe
done

# Sanitize the pear.conf
%{_bindir}/php %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf ext_dir >new-pear.conf
%{_bindir}/php %{SOURCE3} new-pear.conf http_proxy > $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf

%{_bindir}/php -r "print_r(unserialize(substr(file_get_contents('$RPM_BUILD_ROOT%{_sysconfdir}/pear.conf'),17)));"

install -m 644 -D macros.pear \
           $RPM_BUILD_ROOT%{macrosdir}/macros.%{name}

# apply patches on installed PEAR tree
pushd $RPM_BUILD_ROOT%{peardir} 
 pushd PEAR
  %__patch -s --no-backup --fuzz 0 -p0 < %{PATCH0}
 popd
  %__patch -s --no-backup --fuzz 0 -p0 < %{PATCH1}
popd

# Why this file here ?
rm -rf $RPM_BUILD_ROOT/.depdb* $RPM_BUILD_ROOT/.lock $RPM_BUILD_ROOT/.channels $RPM_BUILD_ROOT/.filemap

# Need for re-registrying XML_Util
install -m 644 *.xml $RPM_BUILD_ROOT%{_localstatedir}/lib/pear/pkgxml

# The man pages
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m 644 pear.1 pecl.1 peardev.1 $RPM_BUILD_ROOT%{_mandir}/man1/
install -d $RPM_BUILD_ROOT%{_mandir}/man5
install -p -m 644 pear.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5/

# make the cli commands available in standard root for SCL build
%if 0%{?scl:1}
install -m 755 -d $RPM_BUILD_ROOT%{_root_bindir}
ln -s %{_bindir}/pear      $RPM_BUILD_ROOT%{_root_bindir}/%{scl_prefix}pear
%endif


%check
# Check that no bogus paths are left in the configuration, or in
# the generated registry files.
grep $RPM_BUILD_ROOT $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1
grep %{_libdir} $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1
grep '"/tmp"' $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1
grep /usr/local $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1
grep -rl $RPM_BUILD_ROOT $RPM_BUILD_ROOT && exit 1


%clean
rm -rf $RPM_BUILD_ROOT
rm new-pear.conf


%pre
# Manage relocation of metadata, before update to pear
if [ -d %{peardir}/.registry -a ! -d %{metadir}/.registry ]; then
  mkdir -p %{metadir}
  mv -f %{peardir}/.??* %{metadir}
fi


%post
# force new value as pear.conf is (noreplace)
current=$(%{_bindir}/pear config-get test_dir system)
if [ "$current" != "%{_datadir}/tests/pear" ]; then
%{_bindir}/pear config-set \
    test_dir %{_datadir}/tests/pear \
    system >/dev/null || :
fi

current=$(%{_bindir}/pear config-get data_dir system)
if [ "$current" != "%{_datadir}/pear-data" ]; then
%{_bindir}/pear config-set \
    data_dir %{_datadir}/pear-data \
    system >/dev/null || :
fi

current=$(%{_bindir}/pear config-get metadata_dir system)
if [ "$current" != "%{metadir}" ]; then
%{_bindir}/pear config-set \
    metadata_dir %{metadir} \
    system >/dev/null || :
fi

current=$(%{_bindir}/pear config-get -c pecl doc_dir system)
if [ "$current" != "%{_docdir}/pecl" ]; then
%{_bindir}/pear config-set \
    -c pecl \
    doc_dir %{_docdir}/pecl \
    system >/dev/null || :
fi

current=$(%{_bindir}/pear config-get -c pecl test_dir system)
if [ "$current" != "%{_datadir}/tests/pecl" ]; then
%{_bindir}/pear config-set \
    -c pecl \
    test_dir %{_datadir}/tests/pecl \
    system >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{peardir}
%dir %{metadir}
%{metadir}/.channels
%verify(not mtime size md5) %{metadir}/.depdb
%verify(not mtime)          %{metadir}/.depdblock
%verify(not mtime size md5) %{metadir}/.filemap
%verify(not mtime)          %{metadir}/.lock
%{metadir}/.registry
%{metadir}/pkgxml
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/pear.conf
%{macrosdir}/macros.%{name}
%dir %{_localstatedir}/cache/php-pear
%dir %{_localstatedir}/www/html
%dir %{_sysconfdir}/pear
%doc README* LICENSE*
%dir %{_docdir}/pear
%doc %{_docdir}/pear/*
%dir %{_docdir}/pecl
%dir %{_datadir}/tests
%dir %{_datadir}/tests/pecl
%{_datadir}/tests/pear
%{_datadir}/pear-data
%if 0%{?scl:1}
%dir %{_localstatedir}/www
%{_root_bindir}/%{scl_prefix}pear
%endif
%{_mandir}/man1/pear.1*
%{_mandir}/man1/pecl.1*
%{_mandir}/man1/peardev.1*
%{_mandir}/man5/pear.conf.5*


%changelog
* Sun Aug 24 2014 Remi Collet <rcollet@redhat.com> 1:1.9.5-1
- update PEAR to 1.9.5
- update Archive_Tar to 1.3.12
- update XML_Util to 1.2.3
- add man pages
- pecl doc in /usr/share/doc/pecl
- pecl tests in /usr/share/tests/pecl

* Tue Feb  4 2014 Remi Collet <rcollet@redhat.com> 1:1.9.4-10
- expand all macros #1058639

* Tue Sep 24 2013 Remi Collet <rcollet@redhat.com> 1:1.9.4-8
- relocate RPM macro #1008846

* Thu May 23 2013 Remi Collet <rcollet@redhat.com> 1:1.9.4-7
- remove wrappers in /usr/bin (#966509)

* Mon May  6 2013 Remi Collet <rcollet@redhat.com> 1:1.9.4-6
- don't verify metadata file content (#959425)

* Thu Apr 25 2013 Remi Collet <rcollet@redhat.com> 1:1.9.4-5
- update Archive_Tar to 1.3.11
- add explicit requires on all needed extensions (phpci)
- fix pecl launcher (need ini to be parsed for some
  extensions going to be build as shared, mainly simplexml)
- move metadata to /var/lib/pear
- own %%{_localstatedir}/www (#956529)
- update config only if needed in %%post
- remove %%config flag for macros.pear

* Tue Oct 23 2012 Remi Collet <rcollet@redhat.com> 1:1.9.4-3
- provides pear command in standard root (scl)

* Wed Oct  3 2012 Remi Collet <rcollet@redhat.com> 1:1.9.4-2
- rename, but don't relocate macros.pear

* Wed Oct  3 2012 Remi Collet <rcollet@redhat.com> 1:1.9.4-1
- initial spec rewrite for scl build

* Wed Sep 26 2012 Remi Collet <remi@fedoraproject.org> 1:1.9.4-12
- drop relocate stuff, no more needed

* Sun Aug 19 2012 Remi Collet <remi@fedoraproject.org> 1:1.9.4-11
- move data to /usr/share/pear-data
- provides all package.xml

* Wed Aug 15 2012 Remi Collet <remi@fedoraproject.org> 1:1.9.4-10
- enforce test_dir on update

* Mon Aug 13 2012 Remi Collet <remi@fedoraproject.org> 1:1.9.4-9
- move tests to /usr/share/tests/pear
- move pkgxml to /var/lib/pear
- remove XML_RPC
- refresh installer

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.9.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 11 2012 Remi Collet <remi@fedoraproject.org> 1:1.9.4-7
- Update Archive_Tar to 1.3.10

* Wed Apr 04 2012 Remi Collet <remi@fedoraproject.org> 1:1.9.4-6
- fix Obsoletes version for XML_Util (#226295)
- add link to upstream bug - please Provides LICENSE file
  https://pear.php.net/bugs/bug.php?id=19368
- add link to upstream bug - Incorrect FSF address
  https://pear.php.net/bugs/bug.php?id=19367

* Mon Feb 27 2012 Remi Collet <remi@fedoraproject.org> 1:1.9.4-5
- Update Archive_Tar to 1.3.9
- add patch from RHEL (Joe Orton)
- fix install-pear.php URL (with our patch for doc_dir applied)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 15 2011 Remi Collet <remi@fedoraproject.org> 1:1.9.4-3
- update Archive_Tar to 1.3.8
- allow to build with "tests" option

* Sat Aug 27 2011 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.4-2
- update to XML_RPC-1.5.5

* Thu Jul 07 2011 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.4-1
- update to 1.9.4

* Fri Jun 10 2011 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.3-2
- fix pecl launcher

* Fri Jun 10 2011 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.3-1
- update to 1.9.3
- sync options in launcher (pecl, pear, peardev) with upstream

* Wed Mar 16 2011 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.2-3
- move %%{pear_docdir} to %%{_docdir}/pear
  https://fedorahosted.org/fpc/ticket/69

* Tue Mar  8 2011 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.2-2
- update Console_Getopt to 1.3.1 (no change)

* Mon Feb 28 2011 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.2-1
- update to 1.9.2 (bug + security fix)
  http://pear.php.net/advisory-20110228.txt

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.9.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 12 2010 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.1-6
- update Console_Getopt to 1.3.0
- don't require php-devel (#657812)
- update install-pear.php

* Tue Oct 26 2010 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.1-5
- update Structures_Graph to 1.0.4

* Fri Sep 10 2010 Joe Orton <jorton@redhat.com> - 1:1.9.1-4
- ship LICENSE file for XML_RPC

* Fri Sep 10 2010 Joe Orton <jorton@redhat.com> - 1:1.9.1-3
- require php-devel (without which pecl doesn't work)

* Mon Jul 05 2010 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.1-2
- update to XML_RPC-1.5.4

* Thu May 27 2010 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.1-1
- update to 1.9.1

* Thu Apr 29 2010 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.0-5
- update to Archive_Tar-1.3.7 (only metadata fix)

* Tue Mar 09 2010 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.0-4
- update to Archive_Tar-1.3.6

* Sat Jan 16 2010 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.0-3
- update to XML_RPC-1.5.3
- fix licenses (multiple)
- provide bundled LICENSE files

* Fri Jan 01 2010 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.0-2
- update to Archive_Tar-1.3.5, Structures_Graph-1.0.3

* Sat Sep 05 2009 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.0-1
- update to PEAR 1.9.0, XML_RPC 1.5.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 30 2009 Remi Collet <Fedora@FamilleCollet.com> 1:1.8.1-1
- update to 1.8.1
- Update install-pear.php script (1.39)
- add XML_Util

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun May 18 2008 Remi Collet <Fedora@FamilleCollet.com> 1:1.7.2-2
- revert to install-pear.php script 1.31 (for cfg_dir)

* Sun May 18 2008 Remi Collet <Fedora@FamilleCollet.com> 1:1.7.2-1
- update to 1.7.2
- Update install-pear.php script (1.32)

* Tue Mar 11 2008 Tim Jackson <rpm@timj.co.uk> 1:1.7.1-2
- Set cfg_dir to be %%{_sysconfdir}/pear (and own it)
- Update install-pear.php script
- Add %%pear_cfgdir and %%pear_wwwdir macros

* Sun Feb  3 2008 Remi Collet <Fedora@FamilleCollet.com> 1:1.7.1-1
- update to 1.7.1

* Fri Feb  1 2008 Remi Collet <Fedora@FamilleCollet.com> 1:1.7.0-1
- update to 1.7.0

* Thu Oct  4 2007 Joe Orton <jorton@redhat.com> 1:1.6.2-2
- require php-cli not php

* Sun Sep  9 2007 Remi Collet <Fedora@FamilleCollet.com> 1:1.6.2-1
- update to 1.6.2
- remove patches merged upstream
- Fix : "pear install" hangs on non default channel (#283401)

* Tue Aug 21 2007 Joe Orton <jorton@redhat.com> 1:1.6.1-2
- fix License

* Thu Jul 19 2007 Remi Collet <Fedora@FamilleCollet.com> 1:1.6.1-1
- update to PEAR-1.6.1 and Console_Getopt-1.2.3

* Thu Jul 19 2007 Remi Collet <Fedora@FamilleCollet.com> 1:1.5.4-5
- new SPEC using install-pear.php instead of install-pear-nozlib-1.5.4.phar

* Mon Jul 16 2007 Remi Collet <Fedora@FamilleCollet.com> 1:1.5.4-4
- update macros.pear (without define)

* Mon Jul 16 2007 Joe Orton <jorton@redhat.com> 1:1.5.4-3
- add pecl_{un,}install macros to macros.pear (from Remi)

* Fri May 11 2007 Joe Orton <jorton@redhat.com> 1:1.5.4-2
- update to 1.5.4

* Tue Mar  6 2007 Joe Orton <jorton@redhat.com> 1:1.5.0-3
- add redundant build section (#226295)
- BR php-cli not php (#226295)

* Mon Feb 19 2007 Joe Orton <jorton@redhat.com> 1:1.5.0-2
- update builtin module provides (Remi Collet, #226295)
- drop patch 0

* Thu Feb 15 2007 Joe Orton <jorton@redhat.com> 1:1.5.0-1
- update to 1.5.0

* Mon Feb  5 2007 Joe Orton <jorton@redhat.com> 1:1.4.11-4
- fix Group, mark pear.conf noreplace (#226295)

* Mon Feb  5 2007 Joe Orton <jorton@redhat.com> 1:1.4.11-3
- use BuildArch not BuildArchitectures (#226925)
- fix to use preferred BuildRoot (#226925)
- strip more buildroot-relative paths from *.reg
- force correct gpg path in default pear.conf

* Thu Jan  4 2007 Joe Orton <jorton@redhat.com> 1:1.4.11-2
- update to 1.4.11

* Fri Jul 14 2006 Joe Orton <jorton@redhat.com> 1:1.4.9-4
- update to XML_RPC-1.5.0
- really package macros.pear

* Thu Jul 13 2006 Joe Orton <jorton@redhat.com> 1:1.4.9-3
- require php-cli
- add /etc/rpm/macros.pear (Christopher Stone)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.4.9-2.1
- rebuild

* Mon May  8 2006 Joe Orton <jorton@redhat.com> 1:1.4.9-2
- update to 1.4.9 (thanks to Remi Collet, #183359)
- package /usr/share/pear/.pkgxml (#190252)
- update to XML_RPC-1.4.8
- bundle the v3.0 LICENSE file

* Tue Feb 28 2006 Joe Orton <jorton@redhat.com> 1:1.4.6-2
- set cache_dir directory, own /var/cache/php-pear

* Mon Jan 30 2006 Joe Orton <jorton@redhat.com> 1:1.4.6-1
- update to 1.4.6
- require php >= 5.1.0 (#178821)

* Fri Dec 30 2005 Tim Jackson <tim@timj.co.uk> 1:1.4.5-6
- Patches to fix "pear makerpm"

* Wed Dec 14 2005 Joe Orton <jorton@redhat.com> 1:1.4.5-5
- set default sig_keydir to /etc/pearkeys
- remove ext_dir setting from /etc/pear.conf (#175673)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Dec  6 2005 Joe Orton <jorton@redhat.com> 1:1.4.5-4
- fix virtual provide for PEAR package (#175074)

* Sun Dec  4 2005 Joe Orton <jorton@redhat.com> 1:1.4.5-3
- fix /usr/bin/{pecl,peardev} (#174882)

* Thu Dec  1 2005 Joe Orton <jorton@redhat.com> 1:1.4.5-2
- add virtual provides (#173806) 

* Wed Nov 23 2005 Joe Orton <jorton@redhat.com> 1.4.5-1
- initial build (Epoch: 1 to allow upgrade from php-pear-5.x)
