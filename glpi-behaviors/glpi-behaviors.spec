%global pluginname   behaviors
#global svnrelease   315

Name:           glpi-behaviors
Version:        0.83.0
%if 0%{?svnrelease}
Release:        0.1.svn%{svnrelease}%{?dist}
%else
Release:        2%{?dist}
%endif
Summary:        Plugin to add optional behaviors to GLPI
Summary(fr):    Extension ajoutant des comportements optionnels à GLPI

Group:          Applications/Internet
License:        AGPLv3+
URL:            https://forge.indepnet.net/projects/behaviors

%if 0%{?svnrelease}
# svn export -r 315 https://forge.indepnet.net/svn/behaviors/trunk behaviors
# tar czf glpi-behaviors-0.83-315.tar.gz behaviors
Source0:        glpi-behaviors-0.83-%{svnrelease}.tar.gz
%else
Source0:        https://forge.indepnet.net/attachments/download/1154/glpi-behaviors-0.83.0.tar.gz
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       glpi >= 0.83
Requires:       glpi <  0.84


%description
This plugin allows you to add optional behaviors to GLPI.

%description -l fr
Cette extension permet d’ajouter des comportements optionnels à GLPI.


%prep
%setup -q -c

# Create link to LICENSE for standard doc folder
ln -s %{_datadir}/glpi/plugins/%{pluginname}/LICENSE LICENSE

chmod -x %{pluginname}/setup.php


%build
# empty build


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
* Thu Apr 19 2012 Remi Collet <Fedora@FamilleCollet.com> - 0.83.0-1
- Initial RPM

