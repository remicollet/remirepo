%global pluginname   fusioninventory

Name:           glpi-%{pluginname}
Version:        2.2.2
Release:        1%{?dist}
Summary:        GLPI Plugin for FusionInventory project
Summary(fr):    Extension GLPI pour FusionInventory

Group:          Applications/Internet
License:        GPLv2+
URL:            http://forge.fusioninventory.org/projects/fusioninventory-for-glpi

Source0:        http://forge.fusioninventory.org/attachments/download/120/fusioninventory-for-glpi-2.2.2-release.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

# php-mysql + php-xml already required by GLPI.
Requires:       glpi >= 0.72.1

%description
FusionInventory Server embedded as a plugin into GLPI.


%description -l fr
Serveur FusionInventory embarqué dans une extension GLPI.


%prep
%setup -q -c

# dos2unix to avoid rpmlint warnings
for doc in %{pluginname}/docs/* ; do
    sed -i -e 's/\r//' $doc
done
mv %{pluginname}/docs docs


%build
# empty build


%install
rm -rf %{buildroot} 

mkdir -p %{buildroot}/%{_datadir}/glpi/plugins
cp -ar %{pluginname} %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}


%clean
rm -rf %{buildroot} 


%files
%defattr(-,root,root,-)
%doc docs/*
%{_datadir}/glpi/plugins/%{pluginname}


%changelog
* Wed Aug 25 2010 Remi Collet <RPMS@FamilleCollet.com> - 2.2.2-1
- update to 2.2.2
  Changes : http://forge.fusioninventory.org/news/11

* Fri May 21 2010 Remi Collet <RPMS@FamilleCollet.com> - 2.2.1-1
- update to 2.2.1

* Tue May 18 2010 Remi Collet <RPMS@FamilleCollet.com> - 2.2.0-1
- Initial RPM

