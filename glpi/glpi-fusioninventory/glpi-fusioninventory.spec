# spec file for glpi-fusioninventory
#
# Copyright (c) 2010-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global pluginname    fusioninventory
%global glpi_version  0.84.0
%global plug_version  1.2

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

Source0:        http://forge.fusioninventory.org/attachments/download/1084/fusioninventory-for-glpi_0.84+1.2.tar.gz
Source1:        %{name}-httpd.conf

# http://forge.fusioninventory.org/issues/2259
Patch0:         %{pluginname}-install.patch

# To be followed
# http://forge.fusioninventory.org/issues/2271 mysql_real_escape_string


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext

# phpcompatinfo
Requires:       php-curl
Requires:       php-date
Requires:       php-fileinfo
Requires:       php-hash
Requires:       php-json
Requires:       php-libxml
Requires:       php-mcrypt
Requires:       php-mysqli
Requires:       php-pcre
Requires:       php-session
Requires:       php-simplexml
Requires:       php-spl
Requires:       php-zip
Requires:       php-zlib
Requires:       glpi >= %{glpi_version}
Requires:       glpi <  0.85
Requires:       glpi-reports


%description
FusionInventory Server embedded as a plugin into GLPI.


%description -l fr
Serveur FusionInventory embarqué dans une extension GLPI.


%prep
%setup -q -c

%patch0 -p0

mv %{pluginname}/docs docs

# dos2unix to avoid rpmlint warnings
for doc in docs/* ; do
    sed -i -e 's/\r//' $doc
done

# Create link to LICENSE for standard doc folder
ln -s %{_datadir}/glpi/plugins/%{pluginname}/LICENSE docs/LICENSE
mv %{pluginname}/README.asciidoc docs/

# .htaccess replaced by a httpd config file
rm %{pluginname}/install/mysql/.htaccess \
   %{pluginname}/scripts/.htaccess \
   %{pluginname}/tools/.htaccess


%build
# Regenerate the locales
for po in %{pluginname}/locales/*.po
do
   msgfmt $po -o $(dirname $po)/$(basename $po .po).mo
done


%install
rm -rf %{buildroot} 

# Plugin
mkdir -p %{buildroot}/%{_datadir}/glpi/plugins
cp -ar %{pluginname} %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}

# Apache
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Locales
for i in %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}/locales/*
do
  lang=$(basename $i)
  echo "%lang(${lang:0:2}) %{_datadir}/glpi/plugins/%{pluginname}/locales/${lang}"
done | tee %{name}.lang


%clean
rm -rf %{buildroot} 


%files -f %{name}.lang
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
# fusioninventory
%doc docs/*
%dir %{_datadir}/glpi/plugins/%{pluginname}
%dir %{_datadir}/glpi/plugins/%{pluginname}/locales
# LICENSE file required by installation process
%{_datadir}/glpi/plugins/%{pluginname}/LICENSE
%{_datadir}/glpi/plugins/%{pluginname}/*.php
%{_datadir}/glpi/plugins/%{pluginname}/*.js
%{_datadir}/glpi/plugins/%{pluginname}/ajax
%{_datadir}/glpi/plugins/%{pluginname}/b
%{_datadir}/glpi/plugins/%{pluginname}/css
%{_datadir}/glpi/plugins/%{pluginname}/front
%{_datadir}/glpi/plugins/%{pluginname}/inc
%{_datadir}/glpi/plugins/%{pluginname}/lib
%{_datadir}/glpi/plugins/%{pluginname}/install
%{_datadir}/glpi/plugins/%{pluginname}/pics
%{_datadir}/glpi/plugins/%{pluginname}/report
%{_datadir}/glpi/plugins/%{pluginname}/scripts
%{_datadir}/glpi/plugins/%{pluginname}/tools
%{_datadir}/glpi/plugins/%{pluginname}/snmpmodels


%changelog
* Fri Aug 03 2012 Remi Collet <remi@fedoraproject.org> - 1:0.84.0.1.2-1
- update to 0.84+1.2 for GLPI 0.84
- add explicit dependency on required extensions

* Fri Aug 03 2012 Remi Collet <RPMS@FamilleCollet.com> - 1:0.83.3.1.0-1
- update to 0.83+1.0 (finale)
  http://forge.fusioninventory.org/versions/67

* Fri Jul 27 2012 Remi Collet <RPMS@FamilleCollet.com> - 1:0.83.3.1.0-0.2.RC3
- update to 0.83+1.0-RC3

* Thu Jul 12 2012 Remi Collet <RPMS@FamilleCollet.com> - 1:0.83.3.1.0-0.1.RC2
- update to 0.83+1.0-RC2

* Fri Jun 08 2012 Remi Collet <RPMS@FamilleCollet.com> - 1:0.83.0.1.0-0.4.beta4
- update to 0.83+1.0-beta4

* Thu May 03 2012 Remi Collet <RPMS@FamilleCollet.com> - 1:0.83.0.1.0-0.4.beta3
- spec cleanups

* Thu May 03 2012 Remi Collet <RPMS@FamilleCollet.com> - 1:0.83.0.1.0-0.3.beta3
- add missing fusinvdeploy

* Mon Apr 23 2012 Remi Collet <RPMS@FamilleCollet.com> - 1:0.83.0.1.0-0.2.beta3
- update to 0.83+1.0-beta3

* Sun Feb 26 2012 Remi Collet <RPMS@FamilleCollet.com> - 1:0.83.0.1.0-0.1.beta2
- update to 0.83+1.0-beta2 for glpi 0.83 RC

* Tue Jan 10 2012 Remi Collet <RPMS@FamilleCollet.com> - 1:0.80.0.1.1
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

