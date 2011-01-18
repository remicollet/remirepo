%if %{?fedora}%{?rhel} >= 5
%global useselinux 1
%else
%global useselinux 0
%endif

#global svnrelease 12930

Name:           glpi
Version:        0.78.2
%if 0%{?svnrelease}
Release:        2.svn%{svnrelease}%{?dist}
%else
Release:        1%{?dist}
%endif
Summary:        Free IT asset management software
Summary(fr):    Gestion Libre de Parc Informatique

Group:          Applications/Internet
License:        GPLv2+ and GPLv3+
URL:            http://www.glpi-project.org/
%if 0%{?svnrelease}
# launch mktar %{svnrelease} to create
Source0:        glpi-0.78-%{svnrelease}.tar.gz
Source99:       mktar.sh
%else
Source0:        https://forge.indepnet.net/attachments/download/772/glpi-0.78.2.tar.gz
%endif

Source1:        glpi-httpd.conf
Source2:        glpi-config_path.php
Source3:        glpi-logrotate

# Switch all internal cron tasks to system
Patch0:         glpi-cron.patch


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       php >= 5.0.0, php-mysql, httpd, php-gd, php-ldap, php-imap, php-mbstring, php-xml, php-json
Requires:       php-pear(Cache_Lite) >= 1.7.4
Requires:       php-PHPMailer
Requires:       php-pear-CAS >= 1.1.0
Requires:       php-pear(components.ez.no/Graph) >= 1.5
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6 
Requires:       gnu-free-sans-fonts
%else
Requires:       freefont
%endif
Requires:       %{_sysconfdir}/logrotate.d
Requires(postun): /sbin/service
Requires(post): /sbin/service
BuildRequires:  dos2unix
%if %{useselinux}
Requires:       policycoreutils
%endif
Requires:       %{_sysconfdir}/cron.d


%description
GLPI is the Information Resource-Manager with an additional Administration-
Interface. You can use it to build up a database with an inventory for your 
company (computer, software, printers...). It has enhanced functions to make
the daily life for the administrators easier, like a job-tracking-system with
mail-notification and methods to build a database with basic information 
about your network-topology.


%description -l fr
GLPI est une application libre, distribuée sous licence GPL destinée à la
gestion de parc informatique et de helpdesk.

GLPI est composé d’un ensemble de services web écrits en PHP qui permettent
de recenser et de gérer l’intégralité des composantes matérielles ou 
logicielles d’un parc informatique, et ainsi d’optimiser le travail des
techniciens grâce à une maintenance plus cohérente.


%prep
%setup -q -n glpi

%patch0

# Use system lib
rm -rf lib/cache_lite
rm -rf lib/phpmailer
rm -rf lib/phpcas
rm -rf lib/ezcomponents

%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6 
cp %{SOURCE2} config/config_path.php 
%else
# fix font path on old version
sed -e /GLPI_FONT_FREESANS/s/gnu-free/freefont/ %{SOURCE2} >config/config_path.php 
%endif

mv lib/tiny_mce/license.txt LICENSE.tiny_mce
mv lib/extjs/gpl-3.0.txt    LICENSE.extjs
mv lib/icalcreator/lgpl.txt LICENSE.icalcreator
rm scripts/glpi_cron_*.sh

dos2unix -o LICENSE.tiny_mce
for fic in LISEZMOI.txt README.txt
do
   iconv -f ISO-8859-15 -t UTF-8 $fic >a && mv a $fic
done

cat >cron <<EOF
# GLPI core
# Run cron from to execute task even when no user connected
*/4 * * * * apache %{_bindir}/php %{_datadir}/%{name}/front/cron.php
EOF


%build
# empty build


%install
rm -rf %{buildroot} 

# ===== application =====
mkdir -p %{buildroot}/%{_datadir}/%{name}
cp -a COPYING.txt *.php *.js %{buildroot}/%{_datadir}/%{name}/

for i in ajax css front inc install lib locales pics plugins scripts
do   cp -ar $i %{buildroot}/%{_datadir}/%{name}/$i
done

find %{buildroot}/%{_datadir}/%{name} -type f -exec chmod 644 {} \; 
# chmod 755 %{buildroot}/%{_datadir}/%{name}/scripts/*.sh

# ===== apache =====
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install --mode 644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/httpd/conf.d/glpi.conf

# ===== config =====
cp -ar config %{buildroot}/%{_datadir}/%{name}/config

mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
touch %{buildroot}%{_sysconfdir}/%{name}/config_db.php

# ===== files =====
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}
cp -ar files %{buildroot}/%{_localstatedir}/lib/%{name}/files

# ===== log =====
mkdir -p %{buildroot}%{_localstatedir}/log
mv %{buildroot}/%{_localstatedir}/lib/%{name}/files/_log %{buildroot}%{_localstatedir}/log/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# ====== Cron =====
mkdir -p %{buildroot}%{_sysconfdir}/cron.d
install -m 644 cron %{buildroot}%{_sysconfdir}/cron.d/%{name}

# cleanup
find %{buildroot} -name remove.txt -exec rm -f {} \; -print

# Directories not in apache space
rm -f %{buildroot}%{_localstatedir}/lib/%{name}/files/.htaccess
# Proctection in /etc/httpd/conf.d/glpi.conf
rm -f %{buildroot}%{_datadir}/%{name}/install/mysql/.htaccess
rm -f %{buildroot}%{_datadir}/%{name}/locales/.htaccess
rm -f %{buildroot}%{_datadir}/%{name}/config/.htaccess
rm -f %{buildroot}%{_datadir}/%{name}/scripts/.htaccess


# Lang
for i in %{buildroot}%{_datadir}/%{name}/locales/*
do
  lang=$(basename $i)
  echo "%lang(${lang:0:2}) %{_datadir}/%{name}/locales/${lang}"
done >%{name}.lang


%clean
rm -rf %{buildroot} 


%post
%if %{useselinux}
(
# New File context
semanage fcontext -a -s system_u -t httpd_sys_script_rw_t -r s0 "%{_sysconfdir}/glpi(/.*)?" 
semanage fcontext -a -s system_u -t httpd_log_t           -r s0 "%{_localstatedir}/log/glpi(/.*)?"
# keep httpd_sys_script_rw_t (httpd_var_lib_t prevent dir creation)
semanage fcontext -a -s system_u -t httpd_sys_script_rw_t -r s0 "%{_localstatedir}/lib/glpi(/.*)?"
# files created by app
restorecon -R %{_sysconfdir}/%{name}
restorecon -R %{_localstatedir}/lib/%{name}
restorecon -R %{_localstatedir}/log/%{name}
) &>/dev/null
%endif
/sbin/service httpd condrestart > /dev/null 2>&1 || :


%postun
%if %{useselinux}
if [ "$1" -eq "0" ]; then
    # Remove the File Context
    (
    semanage fcontext -d "%{_sysconfdir}/glpi(/.*)?"
    semanage fcontext -d "%{_localstatedir}/log/glpi(/.*)?"
    semanage fcontext -d "%{_localstatedir}/lib/glpi(/.*)?"
    ) &>/dev/null
fi
%endif
/sbin/service httpd condrestart > /dev/null 2>&1 || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc *.txt LICENSE.*

%attr(750,apache,root) %dir %{_sysconfdir}/%{name}
%ghost %config(noreplace,missingok) %{_sysconfdir}/%{name}/config_db.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/glpi.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/cron.d/%{name}

# This folder can contain private information (sessions, docs, ...)
%dir %_localstatedir/lib/%{name}
%attr(750,apache,root) %{_localstatedir}/lib/%{name}/files

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.php
%{_datadir}/%{name}/*.js
# License file required by installation process
%{_datadir}/%{name}/COPYING.txt
%{_datadir}/%{name}/ajax
%{_datadir}/%{name}/config
%{_datadir}/%{name}/css
%{_datadir}/%{name}/front
%{_datadir}/%{name}/inc
%{_datadir}/%{name}/install
%{_datadir}/%{name}/lib
%{_datadir}/%{name}/pics
%{_datadir}/%{name}/plugins
%{_datadir}/%{name}/scripts
%attr(750,apache,root) %dir %{_localstatedir}/log/%{name}
%dir %{_datadir}/%{name}/locales


%changelog
* Tue Jan 18 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.78.2-1
- version 0.78.2 released

* Mon Nov 15 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.78.1-1
- version 0.78.1 released

* Sun Oct 31 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.78-2.svn12930
- Patches from SVN (12691-12930) for know 0.78 issues
  https://forge.indepnet.net/issues/2374
  https://forge.indepnet.net/issues/2378
  https://forge.indepnet.net/issues/2380
  https://forge.indepnet.net/issues/2382

* Tue Oct 12 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.78-2.svn12852
- Patches from SVN (12691-12852) for know 0.78 issues
  https://forge.indepnet.net/issues/2313
  https://forge.indepnet.net/issues/2314
  https://forge.indepnet.net/issues/2315
  https://forge.indepnet.net/issues/2317
  https://forge.indepnet.net/issues/2326
  https://forge.indepnet.net/issues/2329
  https://forge.indepnet.net/issues/2330
  https://forge.indepnet.net/issues/2332
  https://forge.indepnet.net/issues/2333
  https://forge.indepnet.net/issues/2334
  https://forge.indepnet.net/issues/2335
  https://forge.indepnet.net/issues/2337

* Tue Oct 12 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.78-1
- version 0.78 released

* Sat Sep 18 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.78-0.1.svn12452
- new svn snapshot (which is > RC3)

* Sat Sep 04 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.78-0.1.svn12271
- new svn snapshot

* Wed Aug 25 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.78-0.1.svn12190
- new svn snapshot

* Tue Aug 10 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.78-0.1.svn12085
- new svn snapshot

* Sun Jul 25 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.78-0.1.svn11932
- new svn snapshot

* Wed Jul 07 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.78-0.1.svn11874
- new svn snapshot (which is RC2)

* Fri Jul 02 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.78-0.1.svn11854
- new svn snapshot

* Sat Jun 19 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.78-0.1.svn11771
- new svn snapshot
- switch from gnu-free-sans-fonts to freefont on fedora <= 10 and EL <= 5

* Sat Jun 19 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.78-0.1.svn11763
- new svn snapshot

* Tue Jun 15 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.78-0.1.svn11723
- update to 0.78 RC (svn snapshot)
- use system ezComponents
- use system font

* Thu May 20 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.72.4-3.svn11497
- use system phpCAS instead of bundled copy
- minor bug fixes from SVN

* Mon Mar 22 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.72.4-2.svn11035
- update embedded phpCAS to 1.1.0RC7 (security fix - #575906)

* Tue Mar  2 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.72.4-1
- update to 0.72.4

* Tue Oct 27 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.72.3-1
- update to 0.72.3

* Wed Sep 09 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.72.2.1-1
- update to 0.72.21

* Tue Aug 18 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.72.1-1.svn8743
- update to 0.72.1 svn revision 8743
- use system PHPMailer
- now requires php > 5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.71.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 02 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.71.6-1
- update to 0.71.6 (Bugfix Release)

* Fri May 22 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.71.5-4
- post 0.71.5 patches (7910=>8321)

* Sun Apr 26 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.71.5-3
- post 0.71.5 patches (7910=>8236)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.71.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.71.5-1
- update to 0.71.5 (Fix regression in 0.71.4)

* Mon Jan 26 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.71.4-1
- update to 0.71.4 (Security Release)

* Sun Nov 30 2008 Remi Collet <Fedora@FamilleCollet.com> - 0.71.3-1
- update to 0.71.3 (bugfix release)

* Sun Sep 28 2008 Remi Collet <Fedora@FamilleCollet.com> - 0.71.2-1.el4.1
- Fix MySQL 4.1 compatibility issue

* Mon Sep 15 2008 Remi Collet <Fedora@FamilleCollet.com> - 0.71.2-1
- update to 0.71.2 bugfix

* Sat Aug 09 2008 Remi Collet <Fedora@FamilleCollet.com> - 0.71.1-2
- fix SElinux bug on install test (glpi-check.patch)
- add create option on logrotate conf

* Fri Aug 01 2008 Remi Collet <Fedora@FamilleCollet.com> - 0.71.1-1
- update to 0.71.1 bugfix
- use system cron
- increase memory_limit / max_execution_time for upgrade

* Fri Jul 11 2008 Remi Collet <Fedora@FamilleCollet.com> - 0.71-1
- update to 0.71 stable
- fix bug #452353 (selinux)

* Fri Apr 25 2008 Remi Collet <Fedora@FamilleCollet.com> - 0.70.2-3
- remplace module policy by simple semanage (#442706)

* Mon Jan 28 2008 Remi Collet <Fedora@FamilleCollet.com> - 0.70.2-2
- rebuild (fix sources tarball)

* Sun Jan 27 2008 Remi Collet <Fedora@FamilleCollet.com> - 0.70.2-1
- bugfixes update 

* Mon Jan 15 2008 Remi Collet <Fedora@FamilleCollet.com> - 0.70.1a-1
- update 

* Sun Jan 13 2008 Remi Collet <Fedora@FamilleCollet.com> - 0.70.1-2
- fix typo in lang files

* Sun Jan 13 2008 Remi Collet <Fedora@FamilleCollet.com> - 0.70.1-1
- update to 0.70.1 (0.70 + bugfixes)

* Thu Jan 03 2008 Remi Collet <Fedora@FamilleCollet.com> - 0.70-4
- Changeset 6226 + 6228
- disable SELinux in EL-5

* Sat Dec 29 2007 Remi Collet <Fedora@FamilleCollet.com> - 0.70-3
- Changeset 6191 + 6194 + 6196

* Fri Dec 28 2007 Remi Collet <Fedora@FamilleCollet.com> - 0.70-2
- Changeset 6190

* Fri Dec 21 2007 Remi Collet <Fedora@FamilleCollet.com> - 0.70-1
- 0.70 final

* Fri Nov 16 2007 Remi Collet <Fedora@FamilleCollet.com> - 0.70-0.4.rc3
- Release Candidate 3

* Thu Nov 01 2007 Remi Collet <Fedora@FamilleCollet.com> - 0.70-0.3.rc2
- correct source

* Thu Nov 01 2007 Remi Collet <Fedora@FamilleCollet.com> - 0.70-0.2.rc2
- Release Candidate 2

* Mon Oct 08 2007 Remi Collet <Fedora@FamilleCollet.com> - 0.70-0.2.rc1
- From review #322781 : fix Source0 and macros
- Requires php-domxml for EL4

* Sun Sep 30 2007 Remi Collet <Fedora@FamilleCollet.com> - 0.70-0.1.rc1
- GLPI Version 0.7-RC1
- initial SPEC for Fedora Review

* Thu May 03 2007 Remi Collet <RPMS@FamilleCollet.com> - 0.70-0.beta.20070503
- initial RPM

