# spec file for glpi-reports
#
# Copyright (c) 2010-2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global pluginname   reports

Name:           glpi-reports
Version:        1.7.0
Release:        1%{?dist}
Summary:        GLPI Plugin providing additional reports
Summary(fr):    Extension GLPI fournissant des rapports supplémentaires

Group:          Applications/Internet
License:        GPLv2+
URL:            https://forge.indepnet.net/projects/reports

Source0:        https://forge.indepnet.net/attachments/download/1563/glpi_reports-1.7.0.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext

Requires:       glpi >= 0.84
Requires:       glpi <  0.85


%description
This plugin enables additional reports.

Main features :
* It also plugin allow you to add new reports in a simply way
  (one PHP script for the report and one for the translation).
* It handle the right for each new report
* It provides some new reports (as sample)


%description -l fr
Ce plugin fournit des rapports supplémentaires.

Fonctionnalités principales :
* Il permet d’ajouter très facilement de nouveaux rapports (via l’ajout d’un 
  fichier PHP pour le rapport et un fichier de langue associé).
* Il prend en charge la gestion de droits de tout nouveau rapport ajouté.
* Il fournit quelques rapports (pour exemple)


%prep
%setup -q -c 

mv %{pluginname}/docs docs

# Create link to LICENSE for standard doc folder
ln -s %{_datadir}/glpi/plugins/%{pluginname}/LICENSE LICENSE

rm -r %{pluginname}/tools
rm    docs/HEADER
mv %{pluginname}/AUTHORS.txt docs/

# dos2unix to avoid rpmlint warnings
for doc in docs/* ; do
    sed -i -e 's/\r//' $doc
done


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

for i in %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}/locales/*
do
  lang=$(basename $i)
  echo "%lang(${lang:0:2}) %{_datadir}/glpi/plugins/%{pluginname}/locales/${lang}"
done | tee %{name}.lang


%clean
rm -rf %{buildroot} 


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc docs/* LICENSE
%dir %{_datadir}/glpi/plugins/%{pluginname}
%dir %{_datadir}/glpi/plugins/%{pluginname}/locales
%{_datadir}/glpi/plugins/%{pluginname}/*.php
%{_datadir}/glpi/plugins/%{pluginname}/front
%{_datadir}/glpi/plugins/%{pluginname}/inc
%{_datadir}/glpi/plugins/%{pluginname}/report
# Keep here as required from interface
%{_datadir}/glpi/plugins/%{pluginname}/LICENSE


%changelog
* Mon Sep 30 2013 Remi Collet <remi@fedoraproject.org> - 1.7.0-1
- version 1.7.0 for GLPI 0.84

* Thu Jul 12 2012 Remi Collet <Fedora@FamilleCollet.com> - 1.6.1-1
- version 1.6.1 for GLPI 0.83.3
  https://forge.indepnet.net/projects/reports/versions/701

* Fri Apr 06 2012 Remi Collet <Fedora@FamilleCollet.com> - 1.6.0-1
- version 1.6.0
  https://forge.indepnet.net/projects/reports/versions/636

* Sun Feb 26 2012 Remi Collet <Fedora@FamilleCollet.com> - 1.6.0-0.1.svn215
- version 1.6.0 for glpi 0.83RC (svn snapshot)

* Thu Jun 30 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.5.0-1
- version 1.5.0 released

* Tue Jun 28 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.5.0-0.1.svn158
- version 1.5.0 for glpi 0.80 (svn snapshot)

* Tue Oct 12 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.4.0-1
- version 1.4.0 and GLPI 0.78 released

* Sat Sep 18 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.4.0-0.1.svn100
- new snapshot

* Sat Sep 04 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.4.0-0.1.svn95
- version 1.4.0 for glpi 0.78 RC (svn snapshot)
- initial RPM

