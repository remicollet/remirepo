Name:           glpi-fusioninventory
Version:        2.3.6
Release:        1%{?dist}
Summary:        FusionInventory Server embedded as a GLPI plugin
Summary(fr):    Serveur FusionInventory en extension pour GLPI

Group:          Applications/Internet
License:        GPLv2+
URL:            http://forge.fusioninventory.org/projects/fusioninventory-for-glpi

Source0:        http://forge.fusioninventory.org/attachments/download/410/fusioninventory-for-glpi-metapackage_2.3.6.tar.gz
Source1:        %{name}-httpd.conf

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       glpi >= 0.78
Requires:       glpi <  0.80
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
rm -f fusinvsnmp/install/mysql/.htaccess


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
%{_sysconfdir}/httpd/conf.d/%{name}.conf
# fusioninventory
%doc fusioninventory-docs/*
%dir %{_datadir}/glpi/plugins/fusioninventory
%dir %{_datadir}/glpi/plugins/fusioninventory/locales
%{_datadir}/glpi/plugins/fusioninventory/*.php
%{_datadir}/glpi/plugins/fusioninventory/*.js
%{_datadir}/glpi/plugins/fusioninventory/ajax
%{_datadir}/glpi/plugins/fusioninventory/front
%{_datadir}/glpi/plugins/fusioninventory/inc
%{_datadir}/glpi/plugins/fusioninventory/install
%{_datadir}/glpi/plugins/fusioninventory/pics
# fusinvinventory
%dir %{_datadir}/glpi/plugins/fusinvinventory
%dir %{_datadir}/glpi/plugins/fusinvinventory/locales
%{_datadir}/glpi/plugins/fusinvinventory/*.php
%{_datadir}/glpi/plugins/fusinvinventory/ajax
%{_datadir}/glpi/plugins/fusinvinventory/front
%{_datadir}/glpi/plugins/fusinvinventory/inc
%{_datadir}/glpi/plugins/fusinvinventory/install
%{_datadir}/glpi/plugins/fusinvinventory/pics
# fusinvsnmp
%doc fusinvsnmp-docs
%dir %{_datadir}/glpi/plugins/fusinvsnmp
%dir %{_datadir}/glpi/plugins/fusinvsnmp/locales
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


%changelog
* Mon Jul 04 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.3.6-1
- update to 2.3.6
  http://fusioninventory.org/wordpress/2011/07/04/1122/

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

