%global pluginname   reports
%global svnrelease   95

Name:           glpi-reports
Version:        1.4.0
%if 0%{?svnrelease}
Release:        0.1.svn%{svnrelease}%{?dist}
%else
Release:        1%{?dist}
%endif
Summary:        GLPI Plugin providing additional reports
Summary(fr):    Extension GLPI fournissant des rapports supplémentaires

Group:          Applications/Internet
License:        GPLv2+
URL:            https://forge.indepnet.net/projects/reports

%if 0%{?svnrelease}
# svn export -r 95 https://forge.indepnet.net/svn/reports/trunk reports
# tar czf glpi-reports-1.4.0-95.tar.gz reports
Source0:        glpi-%{pluginname}-%{version}-%{svnrelease}.tar.gz
%else
Source0:        https://forge.indepnet.net/attachments/download/136/glpi-reports-1.3.0.tar.gz
%endif


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       glpi >= 0.78


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

# dos2unix to avoid rpmlint warnings
for doc in docs/* ; do
    sed -i -e 's/\r//' $doc
done


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
* Sat Sep 04 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.4.0-0.1.svn95
- version 1.4.0 for glpi 0.78 RC (svn snapshot)
- initial RPM

