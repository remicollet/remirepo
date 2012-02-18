%{!?phpname:		%{expand: %%global phpname     php}}

%global php_zendabiver %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP Extension => //p') | tail -1)
%global php_version %((echo 0; php-config --version 2>/dev/null) | tail -1)
%global pecl_name APC

%global svnver 322617

Summary:       APC caches and optimizes PHP intermediate code
Name:          %{phpname}-pecl-apc
Version:       3.1.9
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/APC
%if 0%{?svnver}
# svn co -r 322617 https://svn.php.net/repository/pecl/apc/trunk apc-svn322617
# tar czf apc-svn322617.tgz apc-svn322617
Source:        apc-svn%{svnver}.tgz
Release:       5.svn%{svnver}%{?dist}
%else
Release:       3%{?dist}
Source:        http://pecl.php.net/get/APC-%{version}.tgz
%endif

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
Conflicts:     %{phpname}-mmcache %{phpname}-eaccelerator
BuildRequires: %{phpname}-devel >= 5.1.0, httpd-devel, %{phpname}-pear, pcre-devel
%if 0%{?php_zend_api:1}
# Require clean ABI/API versions if available (Fedora)
Requires:      %{phpname}(zend-abi) = %{php_zend_api}
Requires:      %{phpname}(api) = %{php_core_api}
%else
%if "%{rhel}" == "5"
# RHEL5 where we have php-common providing the Zend ABI the "old way"
Requires:      php-zend-abi = %{php_zendabiver}
%else
# RHEL4 where we have no php-common and nothing providing the Zend ABI...
Requires:      php = %{php_version}
%endif
%endif
Provides:      %{phpname}-pecl(%{pecl_name}) = %{version}

%if 0%{?pecl_install:1}
Requires(post): %{__pecl}
Requires(postun): %{__pecl}
%endif

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{php_ztsextdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$
%global __provides_exclude_from %__provides_exclude_from|%{php_ztsextdir}/.*\\.so$


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

# Check than upstream version is correct, http://pecl.php.net/bugs/19590
grep '"%{version}"' APC-%{version}/php_apc.h || exit 1

cp -pr APC-%{version} APC-%{version}-zts


%build
cd APC-%{version}-zts
%{_bindir}/zts-phpize
%configure --enable-apc-mmap --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}

cd ../APC-%{version}
%{_bindir}/phpize
%configure --enable-apc-mmap --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
pushd APC-%{version}-zts
make install INSTALL_ROOT=%{buildroot}
popd

pushd APC-%{version}
make install INSTALL_ROOT=%{buildroot}

# Fix the charset of NOTICE
iconv -f iso-8859-1 -t utf8 NOTICE >NOTICE.utf8
mv NOTICE.utf8 NOTICE
popd

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

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
; requested on your web server. Set to zero or omit if you're not sure;
apc.num_files_hint=1024
; Just like num_files_hint, a "hint" about the number of distinct user cache
; variables to store.  Set to zero or omit if you're not sure;
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
; sure inodes havn't changed since the last stat. APC will normally only check mtime.
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
install -D -m 644 apc.ini %{buildroot}%{php_ztsinidir}/apc.ini
install -D -m 644 apc.ini %{buildroot}%{php_inidir}/apc.ini


%check
cd %{pecl_name}-%{version}
TEST_PHP_EXECUTABLE=%{__php} %{__php} run-tests.php \
    -n -q -d extension_dir=modules \
    -d extension=apc.so

cd ../%{pecl_name}-%{version}-zts
TEST_PHP_EXECUTABLE=%{__ztsphp} %{__ztsphp} run-tests.php \
    -n -q -d extension_dir=modules \
    -d extension=apc.so


%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc APC-%{version}/TECHNOTES.txt APC-%{version}/CHANGELOG APC-%{version}/LICENSE
%doc APC-%{version}/NOTICE        APC-%{version}/TODO      APC-%{version}/apc.php
%doc APC-%{version}/INSTALL
%config(noreplace) %{php_inidir}/apc.ini
%config(noreplace) %{php_ztsinidir}/apc.ini
%{php_extdir}/apc.so
%{php_ztsextdir}/apc.so
%{pecl_xmldir}/%{name}.xml


%files devel
%{php_incldir}/ext/apc
%{php_ztsincldir}/ext/apc


%changelog
* Sun Nov 13 2011 Remi Collet <remi@fedoraproject.org> - 3.0.6-5.svn322617
- pull changes from SVN revision 322617

* Sun Nov 13 2011 Remi Collet <remi@fedoraproject.org> - 3.0.6-4.svn316786
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
