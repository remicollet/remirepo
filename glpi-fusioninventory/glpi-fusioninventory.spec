%global  glpi_version  0.80.0
%global  plug_version  1.3

Name:           glpi-fusioninventory
# New version schema : 2.4.0 = 0.80+1.0 < 0.80+1.1 < 0.83+1.0
Epoch:          1
Version:        %{glpi_version}.%{plug_version}
Release:        1%{?dist}
Summary:        FusionInventory Server embedded as a GLPI plugin
Summary(fr):    Serveur FusionInventory en extension pour GLPI

Group:          Applications/Internet
License:        AGPLv3+
URL:            http://forge.fusioninventory.org/projects/fusioninventory-for-glpi

Source0:        http://forge.fusioninventory.org/attachments/download/626/fusioninventory-for-glpi-metapackage_0.80+1.3.tar.gz
Source1:        %{name}-httpd.conf

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       glpi >= %{glpi_version}
Requires:       glpi <  0.81
Requires:       glpi-reports


%description
FusionInventory Server embedded as a plugin into GLPI.


%description -l fr
Serveur FusionInventory embarqué dans une extension GLPI.


%prep
%setup -q -c

# dos2unix to avoid rpmlint warnings
for doc in */docs/* ; do
    sed -i -e 's/\r//' $doc
done
mv fusinvsnmp/docs      fusinvsnmp-docs  
mv fusioninventory/docs fusioninventory-docs

# .htaccess replaced by a httpd config file
rm -f fusioninventory/install/mysql/.htaccess
rm -f fusioninventory/tools/.htaccess
rm -f fusinvsnmp/install/mysql/.htaccess
rm -f fusinvsnmp/scripts/.htaccess


%build
# empty build


%install
rm -rf %{buildroot} 

mkdir -p %{buildroot}/%{_datadir}/glpi/plugins
cp -ar fusinvinventory %{buildroot}/%{_datadir}/glpi/plugins/fusinvinventory
cp -ar fusinvsnmp      %{buildroot}/%{_datadir}/glpi/plugins/fusinvsnmp
cp -ar fusioninventory %{buildroot}/%{_datadir}/glpi/plugins/fusioninventory

install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Lang
for i in %{buildroot}%{_datadir}/glpi/plugins/fus*/locales/*
do
  lang=$(basename $i)
  plug=$(basename $(dirname $(dirname $i)))
  echo "%lang(${lang:0:2}) %{_datadir}/glpi/plugins/$plug/locales/${lang}"
done | tee %{name}.lang


%clean
rm -rf %{buildroot} 


%files -f %{name}.lang
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
# fusioninventory
%doc fusioninventory-docs/*
%doc fusinvinventory/LICENSE
%dir %{_datadir}/glpi/plugins/fusioninventory
%dir %{_datadir}/glpi/plugins/fusioninventory/locales
# LICENSE file required by installation process
%{_datadir}/glpi/plugins/fusioninventory/LICENSE
%{_datadir}/glpi/plugins/fusioninventory/*.php
%{_datadir}/glpi/plugins/fusioninventory/*.js
%{_datadir}/glpi/plugins/fusioninventory/ajax
%{_datadir}/glpi/plugins/fusioninventory/front
%{_datadir}/glpi/plugins/fusioninventory/inc
%{_datadir}/glpi/plugins/fusioninventory/install
%{_datadir}/glpi/plugins/fusioninventory/pics
%{_datadir}/glpi/plugins/fusioninventory/tools
# fusinvinventory
%dir %{_datadir}/glpi/plugins/fusinvinventory
%dir %{_datadir}/glpi/plugins/fusinvinventory/locales
%{_datadir}/glpi/plugins/fusinvinventory/LICENSE
%{_datadir}/glpi/plugins/fusinvinventory/*.php
%{_datadir}/glpi/plugins/fusinvinventory/ajax
%{_datadir}/glpi/plugins/fusinvinventory/b
%{_datadir}/glpi/plugins/fusinvinventory/front
%{_datadir}/glpi/plugins/fusinvinventory/inc
%{_datadir}/glpi/plugins/fusinvinventory/install
%{_datadir}/glpi/plugins/fusinvinventory/pics
# fusinvsnmp
%doc fusinvsnmp-docs
%dir %{_datadir}/glpi/plugins/fusinvsnmp
%dir %{_datadir}/glpi/plugins/fusinvsnmp/locales
%{_datadir}/glpi/plugins/fusinvsnmp/LICENSE
%{_datadir}/glpi/plugins/fusinvsnmp/*.php
%{_datadir}/glpi/plugins/fusinvsnmp/*.js
%{_datadir}/glpi/plugins/fusinvsnmp/ajax
%{_datadir}/glpi/plugins/fusinvsnmp/front
%{_datadir}/glpi/plugins/fusinvsnmp/inc
%{_datadir}/glpi/plugins/fusinvsnmp/install
%{_datadir}/glpi/plugins/fusinvsnmp/models
%{_datadir}/glpi/plugins/fusinvsnmp/pics
%{_datadir}/glpi/plugins/fusinvsnmp/report
%{_datadir}/glpi/plugins/fusinvsnmp/tool
%{_datadir}/glpi/plugins/fusinvsnmp/scripts


%changelog
* Thu May 03 2012 Remi Collet <RPMS@FamilleCollet.com> - 1:0.80.0.1.3-1
- update to 0.80+1.3
  http://forge.fusioninventory.org/versions/122

* Sat Apr 14 2012 Remi Collet <RPMS@FamilleCollet.com> - 1:0.80.0.1.2-1
- update to 0.80+1.2
  http://forge.fusioninventory.org/versions/110

* Tue Jan 10 2012 Remi Collet <RPMS@FamilleCollet.com> - 1:0.80.0.1.1-1
- update to 0.80+1.1 (new version scheme)
  http://forge.fusioninventory.org/projects/fusioninventory-for-glpi/versions/105
- switch from GPLv2+ to AGPLv3+

* Sun Sep 18 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.4.0-1
- update to 2.4.0 finale

* Mon Aug 29 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.4.0-0.4.RC3
- update to 2.4.0RC3

* Tue Aug 09 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.4.0-0.3.RC2
- update to 2.4.0RC2

* Tue Jul 26 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.4.0-0.2.RC1
- update to 2.4.0RC1

* Tue Jun 28 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.4.0-0.1.beta2
- update to 2.4.0 Beta2 for GLPI 0.80

* Sun Jun 26 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.3.5-1
- update to 2.3.5
  http://fusioninventory.org/wordpress/2011/06/26/fusioninventory-for-glpi-2-3-5-is-available/

* Sat Jun 11 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.3.4-1
- update to 2.3.4 for GLPI 0.78

* Wed Aug 25 2010 Remi Collet <RPMS@FamilleCollet.com> - 2.2.2-1
- update to 2.2.2
  Changes : http://forge.fusioninventory.org/news/11

* Fri May 21 2010 Remi Collet <RPMS@FamilleCollet.com> - 2.2.1-1
- update to 2.2.1

* Tue May 18 2010 Remi Collet <RPMS@FamilleCollet.com> - 2.2.0-1
- Initial RPM

