%global pluginname   massocsimport
%global lockname     massocsimport.lock
#global svnrelease   138

Name:           glpi-mass-ocs-import
Version:        1.6.0
%if 0%{?svnrelease}
Release:        0.1.svn%{svnrelease}%{?dist}
%else
Release:        1.1%{?dist}
%endif
Summary:        GLPI Plugin for OCS Massive import
Summary(fr):    Extension GLPI d'import en masse OCS

Group:          Applications/Internet
License:        GPLv2+
URL:            https://forge.glpi-project.org/projects/massocsimport

%if 0%{?svnrelease}
# svn export -r 138 https://forge.glpi-project.org/svn/massocsimport/trunk massocsimport
# tar czf glpi-massocsimport-1.6.0-138.tar.gz massocsimport
Source0:        glpi-massocsimport-1.6.0-%{svnrelease}.tar.gz
%else
Source0:        https://forge.glpi-project.org/attachments/download/1132/glpi-massocsimport-1.6.0.tar.gz
%endif


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       glpi >= 0.83
Requires:       glpi <  0.84
Requires:       php-cli
Requires:       %{_sysconfdir}/cron.d

# This plugin have been renamed
Provides:       glpi-%{pluginname} = %{version}-%{release}


%description
Plugin which allow OCS continuous synchronization and massive importation.

The extension Config panel is provided to handle the synchronization options.

%description -l fr
Extension permettant de réaliser une importation au fil de l'eau depuis OCS 
et de suivre leur traitement.

Le module de configuration intégré permet de gérer les options de
synchronisation.

%prep
%setup -q -c 

# fix wrong-file-end-of-line-encoding, preserving timestamp
mv %{pluginname}/docs docs
for fic in docs/*; do
  mv $fic $fic.ref
  sed -e 's/\r//' $fic.ref >$fic
  touch -r $fic.ref $fic
  rm $fic.ref
done

cat >README-RPM-POSTINTALL.txt <<EOF
Remember to Install this extension in the Application.
Cron is provided, but disabled. 
EOF

cat >%{name}.httpd <<EOF
<Directory /usr/share/glpi/plugins/%{pluginname}/scripts>
	<IfModule mod_authz_core.c>
		Require all denied
	</IfModule>
	<IfModule !mod_authz_core.c>
		Order Allow,Deny
		Deny from all
	</IfModule>
</Directory>
EOF

cat >cron <<EOF
# GLPI mass_ocs_import extension.
# Must be enabled from the GLPI Control panel.
*/5 * * * * apache %{_datadir}/glpi/plugins/%{pluginname}/scripts/ocsng_fullsync.sh
EOF


%build
# empty build


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_datadir}/glpi/plugins
cp -ar %{pluginname} %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}
rm %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}/scripts/run.bat

chmod +x %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}/scripts/ocsng_fullsync.sh

mkdir -p %{buildroot}%{_sysconfdir}/cron.d
install -m 644 cron %{buildroot}%{_sysconfdir}/cron.d/%{name}

mkdir -p %{buildroot}%{_localstatedir}/lib/glpi/files/_lock
touch %{buildroot}%{_localstatedir}/lib/glpi/files/_lock/%{lockname}

# ===== apache =====
rm %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}/scripts/.htaccess
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install --mode 644 %{name}.httpd %{buildroot}/%{_sysconfdir}/httpd/conf.d/%{name}.conf


%post
# first install (not upgrade)
if [ "$1" -eq "1" ]; then
    %{__install} -o apache -g apache -m 644 /dev/null %{_localstatedir}/lib/glpi/files/_lock/%{lockname}
fi


%postun
# uninstall (not upgrade)
if [ "$1" -eq "0" -a -f %{_localstatedir}/lib/glpi/files/_lock/%{lockname} ]; then
    %{__rm} %{_localstatedir}/lib/glpi/files/_lock/%{lockname}
fi


%check
# Check the name of the lock file in sources
grep %{lockname} %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}/scripts/ocsng_fullsync.sh || exit 1
grep %{lockname} %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}/setup.php || exit 1


%clean
rm -rf %{buildroot} 


%files
%defattr(-,root,root,-)
%doc README-RPM-POSTINTALL.txt docs/* %{pluginname}/LICENSE
%config(noreplace) %{_sysconfdir}/cron.d/%{name}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_datadir}/glpi/plugins/%{pluginname}
# flag file (empty) used to enable/disable the plugin in the interface (apache).
%ghost %{_localstatedir}/lib/glpi/files/_lock/%{lockname}


%changelog
* Tue Jun 28 2016 Johan Cwiklinski <jcwiklinski AT teclib DOT com> - 1.6.0-1.1
- Change URL and Source

* Fri Apr 06 2012 Remi Collet <Fedora@FamilleCollet.com> - 1.6.0-1
- version 1.6.0
  https://forge.indepnet.net/projects/massocsimport/versions/639
- fix config for httpd 2.4

* Sun Feb 26 2012 Remi Collet <Fedora@FamilleCollet.com> - 1.6.0-0.1.svn138
- update to 1.6.0 for glpi 0.83 RC (svn snapshot)

* Tue Sep 27 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.5.2-1
- version 1.5.1 released
  https://forge.indepnet.net/projects/massocsimport/versions/618

* Tue Jul 30 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.5.1-1
- version 1.5.1 released

* Thu Jun 30 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.5.0-1
- version 1.5.0 released

* Tue Jun 28 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.5.0-0.1.svn108
- update to 1.5.0 for glpi 0.80 (svn snapshot)

* Sat Jun 11 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.4.2-1
- version 1.4.2
  https://forge.indepnet.net/projects/massocsimport/versions/534

* Sun Oct 31 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.4.1-1
- version 1.4.1 (minor bugfix)

* Tue Oct 12 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.4.0-1
- version 1.4.0 and GLPI 0.78 released

* Wed Aug 25 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.4.0-0.1.svn60
- new snapshot

* Wed Jul 07 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.4.0-0.1.svn57
- new snapshot

* Fri Jul 02 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.4.0-0.1.svn56
- new snapshot

* Fri Jun 18 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.4.0-0.1.svn54
- update to 1.4.0 for glpi 0.78 RC (svn snapshot)

* Fri May 21 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.3.0-2
- spec cleanup

* Tue Aug 18 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.3.0-1
- update to 1.3.0 finale for glpi 0.72

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 09 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.2.2-1
- update to 1.2.2 (bugfixes)

* Tue Mar 03 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.2.1-1
- update to 1.2.1 (bugfixes)
- rename README.fedora to README-RPM-POSTINTALL.txt
- add some docs

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Sep 28 2008 Remi Collet <Fedora@FamilleCollet.com> - 1.2-1.el4.1
- Fix MySQL 4.1 compatibility issue

* Sat Jul 12 2008 Remi Collet <Fedora@FamilleCollet.com> - 1.2-1
- update to 1.2 for glpi 0.71

* Thu Feb 14 2008 Remi Collet <Fedora@FamilleCollet.com> - 1.1-1
- update to 1.1 (setup bug fixes)

* Sat Dec 22 2007 Remi Collet <Fedora@FamilleCollet.com> - 1.0-1
- update to 1.0 finale

* Fri Jul 06 2007 Remi Collet <RPMS@FamilleCollet.com> - 1.0-0.20070706
- Initial RPM

