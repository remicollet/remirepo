# spec file for glpi
#
# Copyright (c) 2007-2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global useselinux 1

Name:           glpi
Version:        0.84.3
Release:        1%{?dist}
Summary:        Free IT asset management software
Summary(fr):    Gestion Libre de Parc Informatique

Group:          Applications/Internet
License:        GPLv2+ and GPLv3+
URL:            http://www.glpi-project.org/
Source0:        https://forge.indepnet.net/attachments/download/1615/glpi-0.84.3.tar.gz

Source1:        glpi-httpd.conf
Source2:        glpi-config_path.php
Source3:        glpi-logrotate

# Switch all internal cron tasks to system
Patch0:         glpi-0.84-cron.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext

Requires:       httpd, mod_php
Requires:       php(language) >= 5.3
Requires:       php-date
Requires:       php-gd
Requires:       php-fileinfo
Requires:       php-imap
Requires:       php-json
Requires:       php-ldap
Requires:       php-mbstring
Requires:       php-mysqli
Requires:       php-pcre
Requires:       php-session
Requires:       php-xml
Requires:       php-pear(Cache_Lite) >= 1.7.4
Requires:       php-PHPMailer
Requires:       php-pear-CAS >= 1.2.0
Requires:       php-htmLawed
Requires:       php-simplepie
Requires:       php-ZendFramework2-Cache
Requires:       php-ZendFramework2-Cache-apc
Requires:       php-ZendFramework2-I18n
Requires:       php-ZendFramework2-Loader
Requires:       php-ZendFramework2-ServiceManager
Requires:       php-ZendFramework2-Stdlib
Requires:       php-ZendFramework2-Version

%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
Requires:       php-pear(components.ez.no/Graph) >= 1.5
Requires:       gnu-free-sans-fonts
%else
Requires:       freefont
%endif
Requires:         %{_sysconfdir}/logrotate.d
Requires(postun): /sbin/service
Requires(post):   /sbin/service
%if %{useselinux}
Requires(post):   /sbin/restorecon
Requires(post):   /usr/sbin/semanage
Requires(postun): /usr/sbin/semanage
%endif
Requires:         crontabs


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

%patch0 -p0

find . -name \*.orig -exec rm {} \; -print

# Drop bundled Flash files
find lib -name \*.swf -exec rm {} \; -print

# Use system lib
rm -rf lib/cache_lite
rm -rf lib/phpmailer
rm -rf lib/phpcas
rm -rf lib/htmlawed
rm -rf lib/Zend
rm -rf lib/simplepie
rm -rf lib/ezcomponents

%if 0%{?fedora} < 9 && 0%{?rhel} < 6
# fix font path on old version
sed -e '/GLPI_FONT_FREESANS/s/gnu-free/freefont/' \
    %{SOURCE2} >config/config_path.php
%else
cp  %{SOURCE2}  config/config_path.php
%endif

mv lib/tiny_mce/license.txt LICENSE.tiny_mce
mv lib/extjs/gpl-3.0.txt    LICENSE.extjs
mv lib/icalcreator/lgpl.txt LICENSE.icalcreator
rm scripts/glpi_cron_*.sh

sed -i -e 's/\r//' LICENSE.tiny_mce
for fic in LISEZMOI.txt README.txt
do
   iconv -f ISO-8859-15 -t UTF-8 $fic >a && mv a $fic
done

cat >cron <<EOF
# GLPI core
# Run cron from to execute task even when no user connected
*/3 * * * * apache %{_bindir}/php %{_datadir}/%{name}/front/cron.php
EOF


%build
# Regenerate the locales
for po in locales/*.po
do
   msgfmt $po -o $(dirname $po)/$(basename $po .po).mo
done


%install
rm -rf %{buildroot} 

# ===== application =====
mkdir -p %{buildroot}/%{_datadir}/%{name}
cp -a COPYING.txt *.php *.js %{buildroot}/%{_datadir}/%{name}/

for i in ajax css front inc install lib locales pics plugins scripts
do   cp -ar $i %{buildroot}/%{_datadir}/%{name}/$i
done

find %{buildroot}/%{_datadir}/%{name} -type f -exec chmod 644 {} \; 

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
* Sun Nov  3 2013 Remi Collet <remi@fedoraproject.org> - 0.84.3-1
- update to 0.84.3
  https://forge.indepnet.net/projects/glpi/versions/973

* Wed Oct  2 2013 Remi Collet <remi@fedoraproject.org> - 0.84.2-1
- update to 0.84.2
- add upstream patch for Zend autoload
- use system ZendFramework2 and SimplePie

* Thu Sep 12 2013 Remi Collet <remi@fedoraproject.org> - 0.83.9.1-4
- restrict access for install to local for security

* Fri Aug 23 2013 Remi Collet <remi@fedoraproject.org> - 0.83.9.1-3
- drop bundled Flash files files, #1000251

* Sat Jul 27 2013 Jóhann B. Guðmundsson <johannbg@fedoraproject.org> - 0.83.9.1-2
- Add a missing requirement on crontabs to spec file

* Tue Jun 25 2013 Remi Collet <remi@fedoraproject.org> - 0.83.9.1-1
- version 0.83.91 released (security)
  https://forge.indepnet.net/versions/show/928

* Thu Jun 20 2013 Remi Collet <remi@fedoraproject.org> - 0.83.9-1
- version 0.83.9 released (security and bugfix)
  https://forge.indepnet.net/projects/glpi/versions/915

* Tue Apr  2 2013 Remi Collet <remi@fedoraproject.org> - 0.83.8-1
- version 0.83.8 released (bugfix)
  https://forge.indepnet.net/projects/glpi/versions/866

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec  4 2012 Remi Collet <remi@fedoraproject.org> - 0.83.7-1
- version 0.83.7 released (bugfix)
  https://forge.indepnet.net/projects/glpi/versions/843

* Tue Oct 16 2012 Remi Collet <remi@fedoraproject.org> - 0.83.6-1
- version 0.83.6 released (bugfix)
  https://forge.indepnet.net/projects/glpi/versions/841

* Tue Oct  9 2012 Remi Collet <remi@fedoraproject.org> - 0.83.5-1
- version 0.83.5 released (bugfix)
  https://forge.indepnet.net/projects/glpi/versions/800

* Fri Jul 27 2012 Remi Collet <remi@fedoraproject.org> - 0.83.4-1
- version 0.83.4 released (bugfix)
  https://forge.indepnet.net/projects/glpi/versions/777

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.3.1-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Remi Collet <remi@fedoraproject.org> - 0.83.3.1-1
- version 0.83.3 released (bugfix + security)
  https://forge.indepnet.net/projects/glpi/versions/771
- new dependency on htmLawed

* Thu May 31 2012 Remi Collet <remi@fedoraproject.org> - 0.83.2-1
- version 0.83.2 released
  https://forge.indepnet.net/projects/glpi/versions/750

* Thu Apr 19 2012 Remi Collet <remi@fedoraproject.org> - 0.83.1-2
- fix cron patch

* Wed Apr 18 2012 Remi Collet <remi@fedoraproject.org> - 0.83.1-1
- version 0.83.1 released
  0.83.1 https://forge.indepnet.net/projects/glpi/versions/696
  0.83   https://forge.indepnet.net/projects/glpi/versions/538
- adapt config for httpd 2.4

* Thu Feb 09 2012 Remi Collet <remi@fedoraproject.org> - 0.80.7-1
- version 0.80.7 released (security)
  https://forge.indepnet.net/projects/glpi/versions/685

* Thu Jan 05 2012 Remi Collet <remi@fedoraproject.org> - 0.80.6.1-1
- version 0.80.61 released (bugfix)
  https://forge.indepnet.net/projects/glpi/versions/677

* Thu Jan 05 2012 Remi Collet <remi@fedoraproject.org> - 0.80.6-1
- version 0.80.6 released (bugfix)
  https://forge.indepnet.net/projects/glpi/versions/657
- add patch for https://forge.indepnet.net/issues/3299

* Wed Nov 30 2011 Remi Collet <remi@fedoraproject.org> - 0.80.5-1
- version 0.80.5 released (bugfix)
  0.80.5 https://forge.indepnet.net/projects/glpi/versions/643
  0.80.4 https://forge.indepnet.net/projects/glpi/versions/632
  0.80.3 https://forge.indepnet.net/projects/glpi/versions/621
  0.80.2 https://forge.indepnet.net/projects/glpi/versions/605
  0.80.1 https://forge.indepnet.net/projects/glpi/versions/575
  0.80   https://forge.indepnet.net/projects/glpi/versions/466
- increase cron run frequency (3 tasks each 3 minutes)

* Sun Jul 24 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.78.5-3.svn14966
- use system EZC only if available (not in EL-5)

* Fri Jul 22 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.78.5-2.svn14966
- bug and security fix from SVN.

* Sat Jun 11 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.78.5-1
- version 0.78.5 released

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.72.4-4.svn11497
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

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

* Tue Jun 02 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.71.6-1
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

* Tue Jan 15 2008 Remi Collet <Fedora@FamilleCollet.com> - 0.70.1a-1
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

