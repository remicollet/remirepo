%{!?__pecl: %{expand: %%global __pecl %{_bindir}/pecl}}

%global pecl_name APC

Summary:       APC caches and optimizes PHP intermediate code
Name:          php-pecl-apc
Version:       3.1.13
Release:       1%{?dist}
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/APC
Source:        http://pecl.php.net/get/APC-%{version}.tgz

# Upstream patch from SVN, fixed test suite.
# http://svn.php.net/viewvc?view=revision&revision=327449
# http://svn.php.net/viewvc?view=revision&revision=327450
# http://svn.php.net/viewvc?view=revision&revision=327453
# http://svn.php.net/viewvc?view=revision&revision=327454
Patch0:        apc-svn.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php-devel >= 5.1.0, httpd-devel, php-pear, pcre-devel
# For tests
BuildRequires: php-dom

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

Conflicts:     php-mmcache php-eaccelerator
Provides:      php-pecl(%{pecl_name}) = %{version}
Provides:      php-pecl(%{pecl_name})%{?_isa} = %{version}

# Other third party repo stuff
Obsoletes:     php53-pecl-apc
Obsoletes:     php53u-pecl-apc
%if "%{php_version}" > "5.4"
Obsoletes:     php54-pecl-apc
%endif


# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
APC is a free, open, and robust framework for caching and optimizing PHP
intermediate code.


%package devel
Summary:       APC developer files (header)
Group:         Development/Libraries
Requires:      php-pecl-apc%{?_isa} = %{version}-%{release}
Requires:      php-devel%{?_isa}

%description devel
These are the files needed to compile programs using APC serializer.


%prep
%setup -q -c 

cd APC-%{version}
%patch0 -p3 -b .orig

%if 0%{?__isa_bits}
# port number to allow 32/64 build at same time
port=$(expr %{__isa_bits} + 8900)
sed -e "/PHP_CLI_SERVER_PORT/s/8964/$port/" \
    -i tests/server_test.inc
%endif

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_APC_VERSION/{s/.* "//;s/".*$//;p}' php_apc.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

%if 0%{?__ztsphp:1}
# duplicate for ZTS build
cp -pr APC-%{version} APC-%{version}-zts
%endif

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

%if 0%{?__ztsphp:1}
cd ../APC-%{version}-zts
%{_bindir}/zts-phpize
%configure --enable-apc-mmap --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


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
%if 0%{?__ztsphp:1}
pushd APC-%{version}-zts
make install INSTALL_ROOT=%{buildroot}
popd
install -D -m 644 apc.ini %{buildroot}%{php_ztsinidir}/apc.ini
%endif

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
cd %{pecl_name}-%{version}
ln -sf %{php_extdir}/dom.so modules/

TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=dom.so -d extension=apc.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php

%if 0%{?__ztsphp:1}
cd ../%{pecl_name}-%{version}-zts
ln -sf %{php_ztsextdir}/dom.so modules/

TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=dom.so -d extension=apc.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php
%endif


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

%if 0%{?__ztsphp:1}
%{php_ztsextdir}/apc.so
%config(noreplace) %{php_ztsinidir}/apc.ini
%endif

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/php/ext/apc

%if 0%{?__ztsphp:1}
%{php_ztsincldir}/ext/apc
%endif


%changelog
* Mon Sep  3 2012 Remi Collet <remi@fedoraproject.org> - 3.1.13-1
- Version 3.1.13 (beta) - API 3.1.0 (stable)
- add patches from upstream (fixes some tests)
- change serveur port for tests (allow 32/64 bits build)
- obsoletes php53*, php54*

* Sun Aug 26 2012 Remi Collet <remi@fedoraproject.org> - 3.1.12-2
- add patches from upstream
- delete tests which fail because of missing dom extension

* Thu Aug 16 2012 Remi Collet <remi@fedoraproject.org> - 3.1.12-1
- Version 3.1.12 (beta) - API 3.1.0 (stable)
- spec cleanups

* Fri Jul 20 2012 Remi Collet <remi@fedoraproject.org> - 3.1.11-1
- update to 3.1.11 (beta)

* Fri Jun 22 2012 Remi Collet <remi@fedoraproject.org> - 3.1.10-2.1
- sync with rawhide, rebuild for remi repo

* Fri Jun 22 2012 Remi Collet <remi@fedoraproject.org> - 3.1.10-2
- add patches from upstream

* Wed Apr 11 2012 Remi Collet <remi@fedoraproject.org> - 3.1.10-2
- Update to 3.1.10 (beta) for PHP 5.4

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
