%global pluginname   behaviors

Name:           glpi-behaviors
Version:        0.84.1
Release:        1%{?dist}
Summary:        Plugin to add optional behaviors to GLPI
Summary(fr):    Extension ajoutant des comportements optionnels à GLPI

Group:          Applications/Internet
License:        AGPLv3+
URL:            https://forge.indepnet.net/projects/behaviors

Source0:        https://forge.indepnet.net/attachments/download/1570/glpi-behaviors-0.84.1.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext

Requires:       glpi >= 0.84
Requires:       glpi <  0.85


%description
This plugin allows you to add optional behaviors to GLPI.

%description -l fr
Cette extension permet d’ajouter des comportements optionnels à GLPI.


%prep
%setup -q -c

# Create link to LICENSE for standard doc folder
ln -s %{_datadir}/glpi/plugins/%{pluginname}/LICENSE LICENSE

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
%doc LICENSE
%dir %{_datadir}/glpi/plugins/%{pluginname}
%dir %{_datadir}/glpi/plugins/%{pluginname}/locales
%{_datadir}/glpi/plugins/%{pluginname}/*.php
%{_datadir}/glpi/plugins/%{pluginname}/front
%{_datadir}/glpi/plugins/%{pluginname}/inc
# Keep here as required from interface
%{_datadir}/glpi/plugins/%{pluginname}/LICENSE


%changelog
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

