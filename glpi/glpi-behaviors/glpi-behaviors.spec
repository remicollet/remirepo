# remirepo spec file for glpi-behaviors
#
# Copyright (c) 2012-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global pluginname   behaviors

Name:           glpi-behaviors
Version:        1.1
Release:        1%{?dist}
Summary:        Plugin to add optional behaviors to GLPI
Summary(fr):    Extension ajoutant des comportements optionnels à GLPI

Group:          Applications/Internet
License:        AGPLv3+
URL:            https://forge.glpi-project.org/projects/behaviors

Source0:        https://forge.glpi-project.org/attachments/download/2157/glpi-behaviors.1.1.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext

Requires:       glpi >= 0.90
Requires:       glpi <  0.91


%description
This plugin allows you to add optional behaviors to GLPI.

%description -l fr
Cette extension permet d’ajouter des comportements optionnels à GLPI.


%prep
%setup -q -c

# Create link to LICENSE for standard doc folder
ln -s %{_datadir}/glpi/plugins/%{pluginname}/LICENSE LICENSE

# For developer only
rm -rf %{pluginname}/tools


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
%{!?_licensedir:%global license %%doc}
%license LICENSE
%dir %{_datadir}/glpi/plugins/%{pluginname}
%dir %{_datadir}/glpi/plugins/%{pluginname}/locales
%{_datadir}/glpi/plugins/%{pluginname}/*.php
%{_datadir}/glpi/plugins/%{pluginname}/front
%{_datadir}/glpi/plugins/%{pluginname}/inc
# Keep here as required from interface
%{_datadir}/glpi/plugins/%{pluginname}/LICENSE


%changelog
* Tue Nov  8 2016 Remi Collet <remi@fedoraproject.org> - 1.1-1
- version 1.1
  https://forge.glpi-project.org/versions/1209

* Thu Feb 25 2016 Remi Collet <remi@fedoraproject.org> - 1.0-1
- version 1.0
  https://forge.glpi-project.org/versions/1182

* Tue Oct  6 2015 Remi Collet <remi@fedoraproject.org> - 0.90-1
- version 0.90
  https://forge.glpi-project.org/versions/1101

* Wed Dec 17 2014 Remi Collet <remi@fedoraproject.org> - 0.85-1
- version 0.85
  https://forge.indepnet.net/versions/922

* Mon Nov 17 2014 Remi Collet <remi@fedoraproject.org> - 0.84.3-1
- version 0.84.3
  https://forge.indepnet.net/versions/1100

* Mon Sep  8 2014 Remi Collet <remi@fedoraproject.org> - 0.84.2-1
- version 0.84.2 for GLPI 0.84
  https://forge.indepnet.net/versions/1021

* Mon Sep 30 2013 Remi Collet <remi@fedoraproject.org> - 0.84.1-1
- version 0.84.1 for GLPI 0.84

* Fri Jan 11 2013 Remi Collet <Fedora@FamilleCollet.com> - 0.83.4-1
- version 0.83.4 for GLPI >= 0.83.4
  https://forge.indepnet.net/projects/behaviors/versions/787

* Thu Jul 12 2012 Remi Collet <Fedora@FamilleCollet.com> - 0.83.3-1
- version 0.83.3 for GLPI 0.83.3
  https://forge.indepnet.net/projects/behaviors/versions/752

* Thu Apr 19 2012 Remi Collet <Fedora@FamilleCollet.com> - 0.83.0-1
- Initial RPM

