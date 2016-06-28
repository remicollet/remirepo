# spec file for glpi-appliances
#
# Copyright (c) 2010-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global pluginname   appliances

Name:           glpi-appliances
Version:        1.9.1
Release:        1.1%{?dist}
Summary:        GLPI Plugin to manage appliances
Summary(fr):    Extension GLPI de gestion des applicatifs

Group:          Applications/Internet
License:        GPLv2+
URL:            https://forge.glpi-project.org/projects/appliances

Source0:        https://forge.glpi-project.org/attachments/download/1773/glpi-appliances-1.9.1.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext

Requires:       glpi >= 0.84
Requires:       glpi <  0.85


%description
This plugin add appliances management to GLPI
* Appliances creation (composed by various inventory item)
* Direct management from items
* Integrated with Helpdesk


%description -l fr
Cette extension permet la gestion des applicatifs dans GLPI
* Création d’applicatifs composé de plusieurs items
* Gestion directe à partir de l’item
* Intégration avec l'assistance


%prep
%setup -q -c 

# Create link to LICENSE for standard doc folder
ln -s %{_datadir}/glpi/plugins/%{pluginname}/LICENSE LICENSE

rm -rf %{pluginname}/tools

cat >httpd <<EOF
<Directory /usr/share/glpi/plugins/%{pluginname}/sql>
	<IfModule mod_authz_core.c>
		Require all denied
	</IfModule>
	<IfModule !mod_authz_core.c>
		Order Allow,Deny
		Deny from all
	</IfModule>
</Directory>
EOF


%build
# Regenerate the locales
for po in %{pluginname}/locales/*.po
do
   msgfmt $po -o $(dirname $po)/$(basename $po .po).mo
done


%install
rm -rf %{buildroot} 

mkdir -p %{buildroot}/%{_datadir}/glpi/plugins
cp -ar %{pluginname} %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}

# ===== apache =====
rm -f %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}/sql/.htaccess
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install --mode 644 httpd %{buildroot}/%{_sysconfdir}/httpd/conf.d/%{name}.conf

for i in %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}/locales/*
do
  lang=$(basename $i)
  echo "%lang(${lang:0:2}) %{_datadir}/glpi/plugins/%{pluginname}/locales/${lang}"
done | tee %{name}.lang


%clean
rm -rf %{buildroot} 

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc LICENSE
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%dir %{_datadir}/glpi/plugins/%{pluginname}
%dir %{_datadir}/glpi/plugins/%{pluginname}/locales
%{_datadir}/glpi/plugins/%{pluginname}/*.php
%{_datadir}/glpi/plugins/%{pluginname}/ajax
%{_datadir}/glpi/plugins/%{pluginname}/front
%{_datadir}/glpi/plugins/%{pluginname}/inc
%{_datadir}/glpi/plugins/%{pluginname}/sql
# Keep here as required from interface
%{_datadir}/glpi/plugins/%{pluginname}/LICENSE


%changelog
* Tue Jun 28 2016 Johan Cwiklinski <jcwiklinski AT teclib DOT com> - 1.9.1-1.1
- Change URL and Source

* Sun Jun  8 2014 Remi Collet <remi@fedoraproject.org> - 1.9.1-1
- version 1.9.1
  https://forge.indepnet.net/versions/1002

* Mon Sep 30 2013 Remi Collet <remi@fedoraproject.org> - 1.9.0-1
- version 1.9.0 for GLPI 0.84.2

* Thu Jul 12 2012 Remi Collet <Fedora@FamilleCollet.com> - 1.8.1-1
- version 1.8.1 for GLPI 0.83.3
  https://forge.indepnet.net/projects/appliances/versions/747

* Fri Apr 06 2012 Remi Collet <Fedora@FamilleCollet.com> - 1.8.0-1
- version 1.8.0
  https://forge.indepnet.net/projects/appliances/versions/614
- fix config for httpd 2.4
- add 2 patches from SVN (php 5.4.0 + missing tab)

* Sun Feb 26 2012 Remi Collet <Fedora@FamilleCollet.com> - 1.8.0-0.1.svn184
- version 1.8.0 for glpi 0.83RC (svn snapshot)

* Thu Jun 30 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.7.0-1
- version 1.7.0 released

* Tue Jun 28 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.7.0-0.1.svn136
- version 1.7.0 for glpi 0.80 (svn snapshot)

* Tue Oct 12 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.6.0-1
- version 1.6.0 and GLPI 0.78 released

* Wed Aug 25 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.6.0-0.1.svn114
- new svn snapshot

* Sun Jun 20 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.6.0-0.1.svn110
- version 1.6.0 for glpi 0.78 RC (svn snapshot)
- initial RPM

