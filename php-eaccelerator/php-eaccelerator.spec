%{!?phpname:		%{expand: %%global phpname     php}}

%if %{phpname} == php
%global phpbindir      %{_bindir}
%global phpconfdir     %{_sysconfdir}
%global phpincldir     %{_includedir}
%else
%global phpbindir      %{_bindir}/%{phpname}
%global phpconfdir     %{_sysconfdir}/%{phpname}
%global phpincldir     %{_includedir}/%{phpname}
%endif

%global php_extdir %(%{phpbindir}/php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %((echo 0; %{phpbindir}/php-config --version 2>/dev/null) | tail -1)

# This is the apache userid, used for sysvipc semaphores which is the default
# on ppc since spinlock is not detected (not supported?)
# We also use it for the default ownership of the cache directory
%global apache 48
#global svn   358

Summary: PHP accelerator, optimizer, encoder and dynamic content cacher
Name: %{phpname}-eaccelerator
Version: 0.9.6.1
#Release: 0.2%{?svn:.svn%{svn}}%{?dist}
Release: 5%{?dist}
Epoch: 1
# The eaccelerator module itself is GPLv2+
# The PHP control panel is under the Zend license (control.php and dasm.php)
License: GPLv2+ and Zend
Group: Development/Languages
URL: http://eaccelerator.net/
%if 0%{?svn}
Source0: http://snapshots.eaccelerator.net/eaccelerator-svn%{svn}.tar.gz
%else
Source0: http://bart.eaccelerator.net/source/%{version}/eaccelerator-%{version}.tar.bz2
%endif
Source1: php-eaccelerator.cron

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
# ABI check is not enough for this extension (http://eaccelerator.net/ticket/438)
Requires: %{phpname}-common%{?_isa} = %{php_version}
Provides: %{phpname}-zend_extension
Conflicts: %{phpname}-mmcache %{phpname}-pecl-apc
BuildRequires: %{phpname}-devel >= 5.1.0
# Required by phpize
BuildRequires: autoconf, automake, libtool


%if 0%{?fedora}%{?rhel} > 4
%{?filter_setup:
%filter_provides_in %{php_extdir}/.*\.so$
%filter_setup
}
%endif


%description
eAccelerator is a further development of the MMCache PHP Accelerator & Encoder.
It increases performance of PHP scripts by caching them in compiled state, so
that the overhead of compiling is almost completely eliminated.


%prep
%if 0%{?svn}
%setup -q -n eaccelerator-svn%{svn}
%else
%setup -q -n eaccelerator-%{version}
%endif


# Change paths in the example config, other values are changed by a patch
%{__sed} -i 's|/usr/lib/php4/|%{php_extdir}/|g;
             s|/tmp/eaccelerator|%{_var}/cache/%{phpname}-eaccelerator|g' \
    eaccelerator.ini

%{__sed} -e 's|php-eaccelerator|%{phpname}-eaccelerator|g' \
    %{SOURCE1} >%{phpname}-eaccelerator


%build
%{phpbindir}/phpize
%configure \
    --with-php-config=%{phpbindir}/php-config \
%ifnarch %{ix86} x86_64
    --with-eaccelerator-userid="%{apache}"
%endif

%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# The cache directory where pre-compiled files will reside
%{__mkdir_p} %{buildroot}%{_var}/cache/%{phpname}-eaccelerator

# Drop in the bit of configuration
%{__install} -D -m 0644 eaccelerator.ini \
    %{buildroot}%{phpconfdir}/php.d/eaccelerator.ini

# Cache removal cron job
%{__install} -D -m 0755 -p %{phpname}-eaccelerator \
    %{buildroot}%{_sysconfdir}/cron.daily/%{phpname}-eaccelerator


%clean
%{__rm} -rf %{buildroot}


%preun
# Upon last removal (not update), clean all cache files
if [ $1 -eq 0 ]; then
    %{__rm} -rf %{_var}/cache/%{phpname}-eaccelerator/* &>/dev/null || :
fi

%post
# We don't want to require "httpd" in case PHP is used with some other web
# server or without any, but we do want the owner of this directory to default
# to apache for a working "out of the box" experience on the most common setup.
#
# We can't store numeric ownerships in %%files and have it work, so "fix" here,
# but only change the ownership if it's the current user (which is root), which
# allows users to manually change ownership and not have it change back.

# Create the ghost'ed directory with default ownership and mode
if [ ! -d %{_var}/cache/%{phpname}-eaccelerator ]; then
    %{__mkdir_p} %{_var}/cache/%{phpname}-eaccelerator
    %{__chown} %{apache}:%{apache} %{_var}/cache/%{phpname}-eaccelerator
    %{__chmod} 0750 %{_var}/cache/%{phpname}-eaccelerator
fi


%check
# only check if build extension can be loaded
%{phpbindir}/php \
    -n -q -d extension_dir=modules \
    -d extension=eaccelerator.so \
    --modules | grep eAccelerator


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README*
%doc eaccelerator.ini *.php
%{_sysconfdir}/cron.daily/%{phpname}-eaccelerator
%config(noreplace) %{phpconfdir}/php.d/eaccelerator.ini
%{php_extdir}/eaccelerator.so
# We need this hack, as otherwise rpm resets ownership upon package upgrade
#attr(0750,apache,apache) %{_var}/cache/php-eaccelerator/
#attr(0750,root,root) %verify(not user group) %{_var}/cache/php-eaccelerator/
%ghost %{_var}/cache/%{phpname}-eaccelerator/


%changelog
* Thu Mar 17 2011 Remi Collet <Fedora@FamilleCollet.com> - 1:0.9.6.1-5
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

* Wed May 16 2007 Matthias Saou <http://freshrpms.net/> 5.2.2_0.9.5-2
- Include ppc64 %%ifarch, since it's now a Fedora target.
- Include patch to fix trac bug #187.

* Wed May 16 2007 Matthias Saou <http://freshrpms.net/> 5.2.2_0.9.5-1
- Rebuild against PHP 5.2.2.

* Mon Feb 19 2007 Matthias Saou <http://freshrpms.net/> 5.2.1_0.9.5-1
- Rebuild against PHP 5.2.1.

* Mon Dec  4 2006 Matthias Saou <http://freshrpms.net/> 5.2.0_0.9.5-2
- Include patch to fix use of PHP 5.2 (ea #204, rh #218166).

* Wed Nov 29 2006 Matthias Saou <http://freshrpms.net/> 5.2.0_0.9.5-1
- Rebuild against PHP 5.2.0.

* Wed Nov  8 2006 Matthias Saou <http://freshrpms.net/> 5.1.6_0.9.5-2
- Change to require php-common instead of php, for fastcgi without apache.

* Mon Oct 16 2006 Matthias Saou <http://freshrpms.net/> 5.1.6_0.9.5-1
- Update to 0.9.5 final.
- Add cleanup of the cache directory upon package removal.

* Thu Sep  7 2006 Matthias Saou <http://freshrpms.net/> 5.1.6_0.9.5-0.4.rc1
- Rebuild for PHP 5.1.6, eA still checks the exact PHP version it seems :-(
- Put "Requires: php = %%{php_version}" back to avoid broken setups if/when
  PHP gets updated.

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 5.1.4_0.9.5-0.4.rc1
- FC6 rebuild.

* Tue Aug 22 2006 Matthias Saou <http://freshrpms.net/> 5.1.4_0.9.5-0.3.rc1
- Update to 0.9.5-rc1.
- Enable shared-memory, sessions and content-caching (#201319).
- Remove both patches of fixes, merged upstream.
- Change from creating a full eaccelerator.ini to using the included one with
  path substitutions and a patch to change default values.

* Tue May 23 2006 Matthias Saou <http://freshrpms.net/> 5.1.x_0.9.5-0.2.beta2
- Rebuild against PHP 5.1.4.

* Fri May  5 2006 Matthias Saou <http://freshrpms.net/> 5.1.x_0.9.5-0.2.beta2
- Rework heavily the API version requirement detection, should work with
  chroots builds where PHP isn't installed outside.
- Replace the CC way of getting the API version with php -i output.

* Tue Apr 11 2006 Matthias Saou <http://freshrpms.net/> 5.1.x_0.9.5-0.1.beta2
- Update to 0.9.5-beta2.

* Tue Mar 14 2006 Matthias Saou <http://freshrpms.net/> 5.1.x_0.9.3-0.3
- Pass userid 48 to configure script on PPC for sysvipc semaphores.

* Tue Mar 14 2006 Matthias Saou <http://freshrpms.net/> 5.1.x_0.9.3-0.2
- Update to latest eaccelerator-svn200603090012 snapshot.

* Thu Feb  9 2006 Matthias Saou <http://freshrpms.net/> 5.1.x_0.9.3-0.1
- Update to 5.1.x compatible snapshot.
- Will try to make re2c available in Extras in order to build require it.

* Mon Oct 17 2005 Matthias Saou <http://freshrpms.net/> 4.x.x_0.9.3-4
- Re-add %%{?_smp_mflags}, as this was a false alarm.
- Force SEM to FCNTL as the IPC version is buggy on x86_64 SMP at least.

* Mon Jun 27 2005 Matthias Saou <http://freshrpms.net/> 4.x.x_0.9.3-3
- Include buffer overflow patch from zoeloelip, this should fix the real
  problem that wasn't in fact solved with the removal of _smp_mflags.
- Add explicit shm_and_disk defaults to the ini file.

* Mon Jun 27 2005 Matthias Saou <http://freshrpms.net/> 4.x.x_0.9.3-2
- Remove %%{?_smp_mflags}, since the module crashes otherwise (#161189).

* Tue Jun 21 2005 Matthias Saou <http://freshrpms.net/> 4.x.x_0.9.3-1
- Update to 0.9.3, bugfix release.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue Jan 11 2005 Matthias Saou <http://freshrpms.net/> 4.x.x_0.9.2a-0
- Initial RPM release based on the php-mmcache spec file.

