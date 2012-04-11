%{!?phpname:	%{expand: %%global phpname   php}}
%{!?__pecl:	%{expand: %%global __pecl    %{_bindir}/pecl}}

%global pecl_name APC
#global svnver    324329

Summary:       APC caches and optimizes PHP intermediate code
Name:          %{phpname}-pecl-apc
Version:       3.1.10
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/APC
%if 0%{?svnver}
# svn co -r 324329 https://svn.php.net/repository/pecl/apc/trunk apc-svn324329
# tar czf apc-svn324329.tgz apc-svn324329
Source:        apc-svn%{svnver}.tgz
Release:       8.svn%{svnver}%{?dist}
%else
Release:       1%{?dist}
Source:        http://pecl.php.net/get/APC-%{version}.tgz
%endif


BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
Conflicts:     %{phpname}-mmcache %{phpname}-eaccelerator
BuildRequires: %{phpname}-devel >= 5.1.0, httpd-devel, %{phpname}-pear, pcre-devel
Requires:      %{phpname}(zend-abi) = %{php_zend_api}
Requires:      %{phpname}(api) = %{php_core_api}
Provides:      %{phpname}-pecl(%{pecl_name}) = %{version}

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{_libdir}/.*\\.so$


%description
APC is a free, open, and robust framework for caching and optimizing PHP
intermediate code.


%package devel
Summary:       APC developer files (header)
Group:         Development/Libraries
Requires:      %{phpname}-pecl-apc%{?_isa} = %{version}-%{release}
Requires:      %{phpname}-devel%{?_isa}

%description devel
These are the files needed to compile programs using APC serializer.


%prep
%setup -q -c 

%if 0%{?svnver}
mv apc-svn%{svnver}/package.xml .
mv apc-svn%{svnver} APC-%{version}
%endif

# https://bugs.php.net/61696
sed -i -e 's/"3.1.9"/"%{version}"/' APC-%{version}/php_apc.h

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_APC_VERSION/{s/.* "//;s/".*$//;p}' APC-%{version}/php_apc.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi

cp -pr APC-%{version} APC-%{version}-zts

# Drop in the bit of configuration
cat > apc.ini << 'EOF'
; Enable apc extension module
extension = apc.so

; Options for the APC module version >= 3.1.3
; See http://www.php.net/manual/en/apc.configuration.php

; This can be set to 0 to disable APC. 
apc.enabled=1
; The number of shared memory segments to allocate for the compiler cache. 
apc.shm_segments=1
; The size of each shared memory segment, with M/G suffixe
apc.shm_size=64M
; A "hint" about the number of distinct source files that will be included or 
; requested on your web server. Set to zero or omit if you are not sure;
apc.num_files_hint=1024
; Just like num_files_hint, a "hint" about the number of distinct user cache
; variables to store.  Set to zero or omit if you are not sure;
apc.user_entries_hint=4096
; The number of seconds a cache entry is allowed to idle in a slot in case this
; cache entry slot is needed by another entry.
apc.ttl=7200
; use the SAPI request start time for TTL
apc.use_request_time=1
; The number of seconds a user cache entry is allowed to idle in a slot in case
; this cache entry slot is needed by another entry.
apc.user_ttl=7200
; The number of seconds that a cache entry may remain on the garbage-collection list. 
apc.gc_ttl=3600
; On by default, but can be set to off and used in conjunction with positive
; apc.filters so that files are only cached if matched by a positive filter.
apc.cache_by_default=1
; A comma-separated list of POSIX extended regular expressions.
apc.filters
; The mktemp-style file_mask to pass to the mmap module 
apc.mmap_file_mask=/tmp/apc.XXXXXX
; This file_update_protection setting puts a delay on caching brand new files.
apc.file_update_protection=2
; Setting this enables APC for the CLI version of PHP (Mostly for testing and debugging).
apc.enable_cli=0
; Prevents large files from being cached
apc.max_file_size=1M
; Whether to stat the main script file and the fullpath includes.
apc.stat=1
; Vertification with ctime will avoid problems caused by programs such as svn or rsync by making 
; sure inodes have not changed since the last stat. APC will normally only check mtime.
apc.stat_ctime=0
; Whether to canonicalize paths in stat=0 mode or fall back to stat behaviour
apc.canonicalize=0
; With write_lock enabled, only one process at a time will try to compile an 
; uncached script while the other processes will run uncached
apc.write_lock=1
; Logs any scripts that were automatically excluded from being cached due to early/late binding issues.
apc.report_autofilter=0
; RFC1867 File Upload Progress hook handler
apc.rfc1867=0
apc.rfc1867_prefix =upload_
apc.rfc1867_name=APC_UPLOAD_PROGRESS
apc.rfc1867_freq=0
apc.rfc1867_ttl=3600
; Optimize include_once and require_once calls and avoid the expensive system calls used.
apc.include_once_override=0
apc.lazy_classes=0
apc.lazy_functions=0
; Enables APC handling of signals, such as SIGSEGV, that write core files when signaled. 
; APC will attempt to unmap the shared memory segment in order to exclude it from the core file
apc.coredump_unmap=0
; Records a md5 hash of files. 
apc.file_md5=0
; not documented
apc.preload_path
EOF


%build
cd APC-%{version}
%{_bindir}/phpize
%configure --enable-apc-mmap --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../APC-%{version}-zts
%{_bindir}/zts-phpize
%configure --enable-apc-mmap --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
# Install the NTS stuff
pushd APC-%{version}
make install INSTALL_ROOT=%{buildroot}

# Fix the charset of NOTICE
iconv -f iso-8859-1 -t utf8 NOTICE >NOTICE.utf8
mv NOTICE.utf8 NOTICE
popd
install -D -m 644 apc.ini %{buildroot}%{_sysconfdir}/php.d/apc.ini

# Install the ZTS stuff
pushd APC-%{version}-zts
make install INSTALL_ROOT=%{buildroot}
popd
install -D -m 644 apc.ini %{buildroot}%{php_ztsinidir}/apc.ini

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
cd %{pecl_name}-%{version}
TEST_PHP_EXECUTABLE=%{_bindir}/php %{_bindir}/php run-tests.php \
    -n -q -d extension_dir=modules \
    -d extension=apc.so

cd ../%{pecl_name}-%{version}-zts
TEST_PHP_EXECUTABLE=%{__ztsphp} %{__ztsphp} run-tests.php \
    -n -q -d extension_dir=modules \
    -d extension=apc.so


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc APC-%{version}/TECHNOTES.txt APC-%{version}/CHANGELOG APC-%{version}/LICENSE
%doc APC-%{version}/NOTICE        APC-%{version}/TODO      APC-%{version}/apc.php
%doc APC-%{version}/INSTALL
%config(noreplace) %{_sysconfdir}/php.d/apc.ini
%{php_extdir}/apc.so
%{pecl_xmldir}/%{name}.xml
%{php_ztsextdir}/apc.so
%config(noreplace) %{php_ztsinidir}/apc.ini


%files devel
%{_includedir}/php/ext/apc
%{php_ztsincldir}/ext/apc


%changelog
* Wed Apr 11 2012 Remi Collet <remi@fedoraproject.org> - 3.1.10-1
- Update to 3.1.10 (beta) for PHP 5.3
- fix reported version, https://bugs.php.net/61696

* Sun Mar 18 2012 Remi Collet <remi@fedoraproject.org> - 3.1.9-8.svn324329
- pull changes from SVN revision 324329

* Mon Mar 12 2012 Remi Collet <remi@fedoraproject.org> - 3.1.9-7.svn324146
- pull changes from SVN revision 324146, fix https://bugs.php.net/60658

* Sun Mar 11 2012 Remi Collet <remi@fedoraproject.org> - 3.1.9-7.svn324037
- pull changes from SVN revision 324037
- add patch from https://bugs.php.net/61238

* Mon Feb 27 2012 Remi Collet <remi@fedoraproject.org> - 3.1.9-6.svn323587
- pull changes from SVN revision 323587

* Sun Nov 13 2011 Remi Collet <remi@fedoraproject.org> - 3.1.9-5.svn322617
- pull changes from SVN revision 322617

* Sun Nov 13 2011 Remi Collet <remi@fedoraproject.org> - 3.1.9-4.svn316786
- pull changes from SVN revision 316786
- build against php 5.4

* Sat Sep 16 2011 Remi Collet <Fedora@FamilleCollet.com> - 3.1.9-3
- rebuild using latest php version and macro

* Tue Aug 24 2011 Remi Collet <Fedora@FamilleCollet.com> - 3.1.9-2
- build zts extension

* Sun May 15 2011 Remi Collet <Fedora@FamilleCollet.com> - 3.1.9-1
- update to 3.1.9 (bugfix, stable)

* Sat May 14 2011 Remi Collet <Fedora@FamilleCollet.com> - 3.1.8-2
- fix for http://pecl.php.net/bugs/22687

* Tue May  3 2011 Remi Collet <Fedora@FamilleCollet.com> - 3.1.8-1
- update to 3.1.8 (bugfix, stable)

* Thu Feb 17 2011 Remi Collet <Fedora@FamilleCollet.com> - 3.1.7-1.1
- test rebuild with new Arch specific ABI macro

* Wed Jan 12 2011 Remi Collet <Fedora@FamilleCollet.com> - 3.1.7-1
- update to 3.1.7 (bugfix)
- add devel subpackage (for serializer)

* Mon Dec 27 2010 Remi Collet <rpms@famillecollet.com> 3.1.6-2
- relocate using phpname macro

* Tue Nov 30 2010 Remi Collet <Fedora@FamilleCollet.com> - 3.1.6-1
- update to 3.1.6 (bugfix)

* Wed Nov 03 2010 Remi Collet <Fedora@FamilleCollet.com> - 3.1.5-2
- fix reported version, see http://pecl.php.net/bugs/19590

* Wed Nov 03 2010 Remi Collet <Fedora@FamilleCollet.com> - 3.1.5-1
- update to 3.1.5 (bugfix)

* Sat Oct 23 2010 Remi Collet <Fedora@FamilleCollet.com> - 3.1.4-3
- add filter_provides to avoid private-shared-object-provides apc.so

* Sun Aug 08 2010 Remi Collet <Fedora@FamilleCollet.com> - 3.1.4-2
- fix default value for apc.shm_size (need M suffixes)

* Thu Aug 05 2010 Remi Collet <Fedora@FamilleCollet.com> - 3.1.4-1
- update to Version 3.1.4 (beta) - API 3.1.0 (beta)

* Fri Aug 14 2009 Remi Collet <Fedora@FamilleCollet.com> - 3.1.3p1-1
- update to 3.1.3 patch1 (beta, for PHP 5.3 support)
- add test suite (disabled for http://pecl.php.net/bugs/bug.php?id=16793)
- add use_request_time, lazy_classes, lazy_functions options (apc.ini)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> - 3.1.2-1
- update to 3.1.2 (beta) - PHP 5.3 support
- use setup -q -c

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jun 25 2008 Tim Jackson <rpm@timj.co.uk> - 3.0.19-1
- Update to 3.0.19
- Fix PHP Zend API/ABI dependencies to work on EL-4/5
- Fix "License" tag
- Fix encoding of "NOTICE" file
- Add registration via PECL

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.0.14-3
- Autorebuild for GCC 4.3

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 3.0.14-2
- Rebuild for selinux ppc32 issue.

* Thu Jun 28 2007 Chris Chabot <chabotc@xs4all.nl> - 3.0.14-1
- Updated to 3.0.14
- Included new php api snipplets

* Fri Sep 15 2006 Chris Chabot <chabotc@xs4all.nl> - 3.0.12-5
- Updated to new upstream version

* Mon Sep 11 2006 Chris Chabot <chabotc@xs4all.nl> - 3.0.10-5
- FC6 rebuild 

* Sun Aug 13 2006 Chris Chabot <chabotc@xs4all.nl> - 3.0.10-4
- FC6T2 rebuild

* Mon Jun 19 2006 - Chris Chabot <chabotc@xs4all.nl> - 3.0.10-3
- Renamed to php-pecl-apc and added provides php-apc
- Removed php version string from the package version

* Mon Jun 19 2006 - Chris Chabot <chabotc@xs4all.nl> - 3.0.10-2
- Trimmed down BuildRequires
- Added Provices php-pecl(apc)

* Sun Jun 18 2006 - Chris Chabot <chabotc@xs4all.nl> - 3.0.10-1
- Initial package, templated on already existing php-json 
  and php-eaccelerator packages
