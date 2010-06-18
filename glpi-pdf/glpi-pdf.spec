%global pluginname   pdf
%global svnrelease   188

Name:           glpi-pdf
Version:        0.7.0
%if 0%{?svnrelease}
Release:        0.1.svn%{svnrelease}%{?dist}
%else
Release:        1%{?dist}
%endif
Summary:        GLPI Plugin to print PDF of equipment
Summary(fr):    Extension GLPI pour créer des PDF des matériels

Group:          Applications/Internet
License:        GPLv2+
URL:            https://forge.indepnet.net/wiki/pdf/

%if 0%{?svnrelease}
# svn export -r 188 https://forge.indepnet.net/svn/pdf/trunk pdf
# tar czf glpi-pdf-0.7.0-188.tar.gz pdf
Source0:        glpi-pdf-0.7.0-%{svnrelease}.tar.gz
%else
Source0:        https://forge.indepnet.net/attachments/download/171/glpi-pdf-0.6.1.tar.gz
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       glpi >= 0.78

%description
This GLPI plugin enables you to print, in pdf format, the information 
sheet of an equipment or a software of the inventory. 


%description -l fr
Cette extension GLPI vous permet de créer un PDF contenant toutes les
informations sur un équipement ou un logiciel de l'inventaire.


%prep
%setup -q -c

# dos2unix to avoid rpmlint warnings
mv %{pluginname}/docs docs
for doc in docs/* ; do
    sed -i -e 's/\r//' $doc
done

cd %{pluginname}


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
%doc docs/*
%dir %{_datadir}/glpi/plugins/%{pluginname}
%dir %{_datadir}/glpi/plugins/%{pluginname}/locales
%{_datadir}/glpi/plugins/%{pluginname}/*.php
%{_datadir}/glpi/plugins/%{pluginname}/fonts
%{_datadir}/glpi/plugins/%{pluginname}/front
%{_datadir}/glpi/plugins/%{pluginname}/inc
%{_datadir}/glpi/plugins/%{pluginname}/pics


%changelog
* Tue Jun 15 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.7.0-0.1.svn188
- update to 0.7.0 for glpi 0.78 RC (svn snapshot)

* Fri May 21 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.6.1-2
- spec cleanup

* Tue Aug 18 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.6.1-1
- update to 0.6.1 finale for glpi 0.72

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jul 12 2008 Remi Collet <Fedora@FamilleCollet.com> - 0.5-1
- update to 0.5 finale for glpi 0.71

* Thu Dec 27 2007 Remi Collet <Fedora@FamilleCollet.com> - 0.4-1
- update to 0.4 finale
- Initial RPM for Fedora review

* Sun Nov 11 2007 Remi Collet <RPMS@FamilleCollet.com> - 0.4-0.20071111
- update from SVN

* Sat Sep 23 2007 Remi Collet <RPMS@FamilleCollet.com> - 0.3-0.20070922
- new SVN snapshot

* Mon Aug 13 2007 Remi Collet <RPMS@FamilleCollet.com> - 0.2-0.20070813
- Initial RPM

