# This is the apache userid, used for sysvipc semaphores which is the default
# on ppc since spinlock is not detected (not supported?)
# We also use it for the default ownership of the cache directory
%global apache    48
%global gitver    42067ac
%global cache     %{_var}/cache/php-eaccelerator
%global extname   eaccelerator

Summary:   PHP accelerator, optimizer and dynamic content cacher
Name:      php-eaccelerator
Version:   1.0
Release:   0.5.git%{gitver}%{?dist}
Epoch:     1
# The eaccelerator module itself is GPLv2+
# The PHP control panel is under the Zend license (control.php and dasm.php)
License:   GPLv2+ and PHP
Group:     Development/Languages
URL:       http://eaccelerator.net/

# github.com/eaccelerator/eaccelerator/tarvall/42067ac7e2d55caa5d060580489f5043357ffbe2
Source0:   eaccelerator-eaccelerator-%{gitver}.tar.gz
Source1:   %{name}.cron
Source2:   %{name}.httpd

# Fix packaging directory path
Patch0:    %{name}-config.patch
# Try to improves cache management
# https://github.com/eaccelerator/eaccelerator/pull/17
Patch1:    %{name}-cache.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php-devel >= 5.1.0
# Required by phpize
BuildRequires: autoconf, automake, libtool

# ABI check is not enough for this extension (http://eaccelerator.net/ticket/438)
Requires:  php-common%{?_isa} = %{php_version}
# Required by our cleanup cron job
Requires:  tmpwatch

Conflicts: php-pecl-apc, php-xcache

# Other third party repo stuff
Obsoletes: php53-eaccelerator
Obsoletes: php53u-eaccelerator
%if "%{php_version}" > "5.4"
Obsoletes: php54-eaccelerator
%endif

# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
eAccelerator is a free open-source PHP accelerator & optimizer. It increases
the performance of PHP scripts by caching them in their compiled state, so
that the overhead of compiling is almost completely eliminated. It also
optimizes scripts to speed up their execution. eAccelerator typically reduces
server load and increases the speed of your PHP code by 1-10 times.

eAccelerator stores compiled PHP scripts in shared memory and executes code
directly from it. It creates locks only for a short time, while searching for a
compiled PHP script in the cache, so one script can be executed simultaneously
by several engines. Files that can't fit in shared memory are cached on disk
only.

eAccelerator was born in December 2004 as a fork of the Turck MMCache project.
Turck MMCache was created by Dmitry Stogov and much of the eAccelerator code
is still based on his work.

Default configuration provided have disk cache disabled.
Install %{name}-http package for Apache specific configuration files,
which have disk cache and control panel enabled.


%package httpd
Summary:       Configuration file for eAccelerator and Apache
Group:         Development/Languages
Requires(pre): httpd
Requires:      php%{?_isa}
Requires:      %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description httpd
This package provides Apache configuration for eAccelerator:
- enable disk cache
- enable control panel on http://localhost/eaccelerator


%prep
%setup -q -c

cp %{SOURCE1} .
cp %{SOURCE2} .

# prepare duplicated build tree
mv eaccelerator-eaccelerator-%{gitver} nts
cp -r nts zts

cd nts
%patch0 -p0 -b .upstream
# Change extension path in the example config
sed -e 's|@EXTDIR@/|%{php_extdir}/|' \
    -i %{extname}.ini
%patch1 -p0 -b .cache

cd ../zts
%patch0 -p0 -b .upstream
# Change extension path in the example config
sed -e 's|@EXTDIR@/|%{php_ztsextdir}/|' \
    -i %{extname}.ini
%patch1 -p0 -b .cache


%build
cd nts
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config \
%ifnarch %{ix86} x86_64
    --with-eaccelerator-userid="%{apache}"
%endif

make %{?_smp_mflags}

cd ../zts
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config \
%ifnarch %{ix86} x86_64
    --with-eaccelerator-userid="%{apache}"
%endif

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make -C nts install INSTALL_ROOT=%{buildroot}
make -C zts install INSTALL_ROOT=%{buildroot}

# The cache directory where pre-compiled files will reside
mkdir -p %{buildroot}%{cache}/%{apache}

# Drop in the bit of configuration
install -D -m 0644 nts/%{extname}.ini \
        %{buildroot}%{php_inidir}/%{extname}.ini
install -D -m 0644 zts/%{extname}.ini \
        %{buildroot}%{php_ztsinidir}/%{extname}.ini

# Cache removal cron job
install -D -m 0755 -p %{name}.cron \
        %{buildroot}%{_sysconfdir}/cron.daily/%{name}

# Apache configuration file
install -D -m 0644 -p %{name}.httpd \
        %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Control panel
install -d -m 0755 %{buildroot}/%{_datadir}/%{extname}
install -p -m 0644 nts/control.php %{buildroot}/%{_datadir}/%{extname}/index.php

%clean
rm -rf %{buildroot}


%preun
# Upon last removal (not update), clean all cache files
if [ $1 -eq 0 ]; then
    rm -rf %{cache}/* &>/dev/null || :
fi

%post httpd
# Please remember to empty your eAccelerator disk cache
# when upgrading, otherwise things will break!
rm -rf %{cache}/%{apache}/* &>/dev/null || :


%check
# Check if the built extensions can be loaded
%{__php} -n \
    -d zend_extension=%{buildroot}%{php_extdir}/%{extname}.so \
    -m | grep -i %{extname}

%{__ztsphp} -n \
    -d zend_extension=%{buildroot}%{php_ztsextdir}/%{extname}.so \
    -m | grep -i %{extname}


%files
%defattr(-,root,root,-)
%doc nts/{AUTHORS,ChangeLog,COPYING,NEWS,README}
%doc nts/*.php
%{_sysconfdir}/cron.daily/%{name}
%config(noreplace) %{php_inidir}/%{extname}.ini
%config(noreplace) %{php_ztsinidir}/%{extname}.ini
%{php_extdir}/%{extname}.so
%{php_ztsextdir}/%{extname}.so
%dir %{cache}
%{_datadir}/%{extname}

%files httpd
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%attr(750,apache,apache) %dir %{cache}/%{apache}


%changelog
* Thu Oct 18 2012 Remi Collet <remi@fedoraproject.org> - 1:1.0-0.5.git42067ac
- rebuild for php 5.4.8

* Thu Sep 13 2012 Remi Collet <remi@fedoraproject.org> - 1:1.0-0.4.git42067ac
- rebuild for php 5.4.7

* Sun Sep  9 2012 Remi Collet <remi@fedoraproject.org> - 1:1.0-0.3.git42067ac
- create httpd subpackage

* Sun Sep  9 2012 Remi Collet <remi@fedoraproject.org> - 1:1.0-0.2.git42067ac
- try to improve cache management

* Sat Sep  8 2012 Remi Collet <remi@fedoraproject.org> - 1:1.0-0.1.git42067ac
- update to 1.0-dev for php 5.4

* Thu Aug 16 2012 Remi Collet <remi@fedoraproject.org> - 1:0.9.6.1-17
- rebuild against PHP 5.3.16

* Fri Jul 20 2012 Remi Collet <remi@fedoraproject.org> - 1:0.9.6.1-16
- rebuild against PHP 5.3.15

* Thu Jun 14 2012 Remi Collet <remi@fedoraproject.org> - 1:0.9.6.1-15
- rebuild against PHP 5.3.14

* Wed May 09 2012 Remi Collet <remi@fedoraproject.org> - 1:0.9.6.1-14
- rebuild against PHP 5.3.13

* Thu May 03 2012 Remi Collet <remi@fedoraproject.org> - 1:0.9.6.1-13
- rebuild against PHP 5.3.12

* Fri Apr 27 2012 Remi Collet <remi@fedoraproject.org> - 1:0.9.6.1-12
- rebuild against PHP 5.3.11

* Fri Feb 03 2012 Remi Collet <remi@fedoraproject.org> - 1:0.9.6.1-11
- rebuild against PHP 5.3.10

* Tue Jan 10 2012 Remi Collet <remi@fedoraproject.org> - 1:0.9.6.1-10
- rebuild against PHP 5.3.9
- add ZTS build

* Tue Aug 23 2011 Remi Collet <remi@fedoraproject.org> - 1:0.9.6.1-9
- rebuild against PHP 5.3.8

* Thu Aug 18 2011 Remi Collet <remi@fedoraproject.org> - 1:0.9.6.1-8
- rebuild against PHP 5.3.7
- add filter (to avoid private-shared-object-provides)

* Wed Jul 13 2011 Matthias Saou <http://freshrpms.net/> 1:0.9.6.1-7
- Add missing tmpwatch requirement (#711236).
- Stop using macros for simple commands, following recent guidelines changes.

* Thu Mar 17 2011 Remi Collet <Fedora@FamilleCollet.com> - 1:0.9.6.1-6
- rebuild against PHP 5.3.6

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 08 2011 Remi Collet <Fedora@FamilleCollet.com> - 1:0.9.6.1-4
- allow relocation with %%{phpname} macro

* Sat Jan 08 2011 Remi Collet <Fedora@FamilleCollet.com> - 1:0.9.6.1-4
- rebuild against PHP 5.3.5

* Sun Aug 08 2010 Remi Collet <Fedora@FamilleCollet.com> - 1:0.9.6.1-3
- rebuild against PHP 5.3.4

* Sun Aug 08 2010 Remi Collet <Fedora@FamilleCollet.com> - 1:0.9.6.1-2
- strong requires PHP version
- rebuild against php 5.3.3

* Sat Jul 03 2010 Remi Collet <Fedora@FamilleCollet.com> - 1:0.9.6.1-1
- update to 0.9.6.1

* Sat Feb 06 2010 Remi Collet <Fedora@FamilleCollet.com> - 1:0.9.6-1
- add missing %%dist tag

* Sat Feb 06 2010 Remi Collet <Fedora@FamilleCollet.com> - 1:0.9.6-1
- update to 0.9.6
- add minimal %%check (extension loadable)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.6-0.2.svn358
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Remi Collet <Fedora@FamilleCollet.com> - 1:0.9.6-0.1.svn358
- rebuild for new PHP 5.3.0 ABI (20090626)
- update to latest SVN snapshot
- remove shared-memory, sessions and content-caching options

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 24 2008 Matthias Saou <http://freshrpms.net/> 1:0.9.5.3-2
- Update default cache dir to be ghosted and take care of creating it and
  changing default ownership in the %%post scriplet (fixes #443407).

* Mon Dec 22 2008 Matthias Saou <http://freshrpms.net/> 1:0.9.5.3-1
- Update to 0.9.5.3.
- Include daily cleanup cron job (#470460).

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org>
- Autorebuild for GCC 4.3

* Mon Nov 26 2007 Matthias Saou <http://freshrpms.net/> 1:0.9.5.2-1
- Update to 0.9.5.2.

* Wed Aug 22 2007 Matthias Saou <http://freshrpms.net/> 1:0.9.5.1-7
- Rebuild for new BuildID feature.

* Sun Aug 12 2007 Matthias Saou <http://freshrpms.net/> 1:0.9.5.1-6
- Change the ifarch ppc* to ifnarch x86(_64) since alpha also needs to be
  excluded (#251302).

* Mon Aug  6 2007 Matthias Saou <http://freshrpms.net/> 1:0.9.5.1-5
- Update License field.

* Wed Jul 25 2007 Jeremy Katz <katzj@redhat.com> - 1:0.9.5.1-4
- rebuild for toolchain bug

* Tue Jul 24 2007 Matthias Saou <http://freshrpms.net/> 1:0.9.5.1-3
- Include patch to skip the exact PHP version check, we'll rely on our
  package's php_zend_api version requirement to "get it right".

* Thu Jul 19 2007 Jesse Keating <jkeating@redhat.com> 1:0.9.5.1-2
- Rebuild for new php

* Fri Jun 22 2007 Matthias Saou <http://freshrpms.net/> 1:0.9.5.1-1
- Update to 0.9.5.1.
- Major spec file cleanup, based on current PHP packaging guidelines.
- Set Epoch to 1, since the proper versionning is lower than previously :-(
- Remove two upstreamed patches (php52fix and trac187).
- Use sed instead of perl for the config file changes.
- No longer use dist because we want to use the same package on F-n and n+1.

