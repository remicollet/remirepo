%define pluginname   datainjection
#global svnrelease   596

Name:           glpi-data-injection
Version:        2.1.4
%if 0%{?svnrelease}
Release:        0.2.svn%{svnrelease}%{?dist}
%else
Release:        1%{?dist}
%endif
Summary:        Plugin for importing data into GLPI
Summary(fr):    Extension pour importer des données dans GLPI

Group:          Applications/Internet
License:        GPLv2+

URL:            https://forge.indepnet.net/projects/datainjection
%if 0%{?svnrelease}
# svn export -r 596 https://forge.indepnet.net/svn/datainjection/trunk datainjection
# tar czf glpi-datainjection-2.1.0-596.tar.gz datainjection
Source0:        glpi-datainjection-2.1.0-%{svnrelease}.tar.gz
%else
# This change for each new version
Source0:        https://forge.indepnet.net/attachments/download/1038/glpi-datainjection-2.1.4.tar.gz
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       glpi >= 0.80
Requires:       glpi <  0.81
Requires:       glpi-pdf

# This plugin is renamed (for 0.72)
Provides:       glpi-datainjection = %{version}-%{release}


%description
Plugin for importing data into GLPI

It'll can serve, for example, to :
- import machines at the delivery (electronic delivery order in CSV)
- import additional data
- import equipment not managed by OCS
- transmit from an other tool of asset management

%description -l fr
Extension pour importer des données dans GLPI

Elle pourra servir, par exemple, à :
- importer des machines à la livraison (bon de livraison électronique en CSV)
- importer des données complémentaires
- importer des matériels non gérés par OCS
- migrer depuis un autre outil de gestion de parc


%prep
%setup -q -c

mv %{pluginname}/docs docs

# dos2unix to avoid rpmlint warnings
for fic in docs/*; do
  mv $fic $fic.ref
  sed -e 's/\r//' $fic.ref >$fic
  touch -r $fic.ref $fic
  rm $fic.ref
done

# don't need this
rm -f testwebservice.php

# fix in SVN...
chmod -x datainjection/ajax/model.tabs.php


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
%{_datadir}/glpi/plugins/%{pluginname}/*.php
%dir %{_datadir}/glpi/plugins/%{pluginname}/locales
%{_datadir}/glpi/plugins/%{pluginname}/ajax
%{_datadir}/glpi/plugins/%{pluginname}/css
%{_datadir}/glpi/plugins/%{pluginname}/front
%{_datadir}/glpi/plugins/%{pluginname}/inc
%{_datadir}/glpi/plugins/%{pluginname}/javascript
%{_datadir}/glpi/plugins/%{pluginname}/pics


%changelog
* Tue Jan 10 2012 Remi Collet <Fedora@FamilleCollet.com> - 2.1.4-1
- update to 2.1.4
  https://forge.indepnet.net/projects/datainjection/versions/671

* Sun Dec 11 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.1.3-1
- update to 2.1.3
  https://forge.indepnet.net/projects/datainjection/versions/663

* Sat Nov 26 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.1.2-1
- update to 2.1.2
  https://forge.indepnet.net/projects/datainjection/versions/661

* Sat Nov 12 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.1.1-1
- update to 2.1.1

* Sun Oct 16 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.1.0-1
- update to 2.1.0 finale version

* Tue Sep 20 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.1.0-0.2.svn596
- new snapshot

* Sun Jul 24 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.1.0-0.1.svn593
- update to 2.1.0 for glpi 0.80 (svn snapshot)

* Sat Jun 11 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.2-1
- update to 2.0.2
  https://forge.indepnet.net/projects/datainjection/versions/544

* Tue Mar  8 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.1-1.beta
- update to 2.0.1-beta

* Wed Jan 19 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.0-0.1.beta
- update to 2.0.0-beta

* Sun Dec 10 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.7.2-1
- update to 1.7.2
- fix URL + Source (link to new forge)

* Wed Sep 09 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.7.0-1
- update to 1.7.0

* Tue Aug 18 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.6.0-1
- update to 1.6.0 finale for glpi 0.72

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 21 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.5.1-1
- update to 1.5.1

* Fri Mar 13 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.4.0-1
- update to 1.4.0
- spec cleanup

* Sat Jul 12 2008 Remi Collet <Fedora@FamilleCollet.com> - 1.2-1
- update to 1.2 for glpi 0.71

* Sun Jan 13 2008 Remi Collet <Fedora@FamilleCollet.com> - 1.1-1
- update to 1.1
- tag lang files

* Tue Dec 25 2007 Remi Collet <Fedora@FamilleCollet.com> - 1.0-1
- update to 1.0 finale
- add patch 5653 (lang fix)

* Sat Aug 25 2007 Remi Collet <RPMS@FamilleCollet.com> - 1.0-0.20070825
- Initial RPM

