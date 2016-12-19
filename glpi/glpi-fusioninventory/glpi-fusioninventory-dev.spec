# remirepo spec file for glpi-fusioninventory
#
# Copyright (c) 2010-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global pluginname    fusioninventory
%global glpi_version  9.1
%global glpi_min      9.1.1
%global glpi_max      9.2
%global plug_version  1.1
%global gh_tag        glpi9.1+1.1

Name:           glpi-fusioninventory
# New version schema : 2.4.0 = 0.80+1.0 < 0.80+1.1 < 0.83+1.0
Epoch:          1
Version:        %{glpi_min}.%{plug_version}
Release:        1%{?dist}
Summary:        FusionInventory Server embedded as a GLPI plugin
Summary(fr):    Serveur FusionInventory en extension pour GLPI

Group:          Applications/Internet
License:        AGPLv3+
URL:            http://fusioninventory.org/

Source0:        https://github.com/fusioninventory/fusioninventory-for-glpi/releases/download/%{gh_tag}/fusioninventory-for-glpi_%{glpi_version}.%{plug_version}.tar.gz
Source1:        %{name}-httpd.conf


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext

# phpcompatinfo for version 0.84+3.1
Requires:       php-date
Requires:       php-fileinfo
Requires:       php-hash
Requires:       php-json
Requires:       php-mysqli
Requires:       php-pcre
Requires:       php-session
Requires:       php-simplexml
Requires:       php-spl
Requires:       php-zip
Requires:       php-zlib
Requires:       glpi >= %{glpi_min}
Requires:       glpi <  %{glpi_max}


%description
FusionInventory Server embedded as a plugin into GLPI.


%description -l fr
Serveur FusionInventory embarqué dans une extension GLPI.


%prep
%setup -q -c

mv %{pluginname}/docs docs

# dos2unix to avoid rpmlint warnings
for doc in docs/* ; do
    sed -i -e 's/\r//' $doc
done

# Create link to LICENSE for standard doc folder
ln -s %{_datadir}/glpi/plugins/%{pluginname}/LICENSE LICENSE
mv %{pluginname}/README.asciidoc docs/
mv %{pluginname}/PICTURES .

# .htaccess replaced by a httpd config file
rm %{pluginname}/install/mysql/.htaccess \
   %{pluginname}/scripts/.htaccess

#Fix rpmlint warnings
chmod +x %{pluginname}/scripts/createSNMPWalks.php
find %{pluginname}/lib \(\
    -name .travis.yml \
    -o -name .npmignore \
    -o -name .gitignore \
    -o -name .gitmodules \
    -o -name .jshintrc \
    \) -exec rm -f {} \;
iconv -f ISO-8859-1 -t UTF-8 docs/CHANGES >a && mv a docs/CHANGES


%build
# Regenerate the locales
for po in %{pluginname}/locales/*.po
do
   msgfmt $po -o $(dirname $po)/$(basename $po .po).mo
done


%install
rm -rf %{buildroot} 

# Plugin
mkdir -p %{buildroot}%{_localstatedir}/lib/glpi/files/_plugins/%{pluginname}

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
%{!?_licensedir:%global license %%doc}
%license LICENSE PICTURES
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
%{_datadir}/glpi/plugins/%{pluginname}/js
%{_datadir}/glpi/plugins/%{pluginname}/lib
%{_datadir}/glpi/plugins/%{pluginname}/install
%{_datadir}/glpi/plugins/%{pluginname}/pics
%{_datadir}/glpi/plugins/%{pluginname}/report
%{_datadir}/glpi/plugins/%{pluginname}/scripts
# Data
%attr(750,apache,root) %{_localstatedir}/lib/glpi/files/_plugins/%{pluginname}


%changelog
* Mon Dec 19 2016 Remi Collet <remi@fedoraproject.org> - 1:9.1.0.1.1-1
- update to 9.1+1.1

* Tue Nov 22 2016 Remi Collet <remi@fedoraproject.org> - 1:9.1.0.1.0-1
- update to 9.1+1.0

* Thu Jul 28 2016 Remi Collet <remi@fedoraproject.org> - 1:0.90.0.1.4-1
- update to 0.90+1.4

* Fri Jul 08 2016 Johan Cwiklinski <jcwiklinski AT teclib DOT com> - 1:0.90.0.1.3-2
- Add plugin data dir

* Wed May 18 2016 Remi Collet <remi@fedoraproject.org> - 1:0.90.0.1.3-1
- update to 0.90+1.3

* Fri Mar 25 2016 Remi Collet <remi@fedoraproject.org> - 1:0.90.0.1.2-1
- update to 0.90+1.2

* Wed Feb 24 2016 Remi Collet <remi@fedoraproject.org> - 1:0.90.0.1.1-1
- update to 0.90+1.1

* Thu Oct  8 2015 Remi Collet <remi@fedoraproject.org> - 1:0.90.0.1.0-1
- update to 0.90+1.0 for GLPI 0.90

* Tue Oct  6 2015 Remi Collet <remi@fedoraproject.org> - 1:0.85.0.1.3-1
- update to 0.85+1.3 for GLPI 0.85
  http://forge.fusioninventory.org/versions/217

* Sat Jul 25 2015 Remi Collet <remi@fedoraproject.org> - 1:0.85.0.1.2-1
- update to 0.85+1.2 for GLPI 0.85
  http://forge.fusioninventory.org/versions/213

* Sun Mar  1 2015 Remi Collet <remi@fedoraproject.org> - 1:0.85.0.1.1-1
- update to 0.85+1.1 for GLPI 0.85
  http://forge.fusioninventory.org/versions/208

* Tue Dec 23 2014 Remi Collet <remi@fedoraproject.org> - 1:0.85.0.1.0-1
- update to 0.85+1.0 for GLPI 0.85
  http://forge.fusioninventory.org/versions/97

* Wed Dec 17 2014 Remi Collet <remi@fedoraproject.org> - 1:0.85.0.1.0-0.1.BETA1
- update to 0.85+1.0-BETA1 for GLPI 0.85
  http://forge.fusioninventory.org/versions/97

* Mon Oct 27 2014 Remi Collet <remi@fedoraproject.org> - 1:0.84.0.3.5-1
- update to 0.84+3.5 for GLPI 0.84
  http://forge.fusioninventory.org/versions/204

* Fri Oct 17 2014 Remi Collet <remi@fedoraproject.org> - 1:0.84.0.3.4-1
- update to 0.84+3.4 for GLPI 0.84
  http://forge.fusioninventory.org/versions/198

* Thu Sep 11 2014 Remi Collet <remi@fedoraproject.org> - 1:0.84.0.3.3-1
- update to 0.84+3.3 for GLPI 0.84
  http://forge.fusioninventory.org/versions/196

* Wed Aug 20 2014 Remi Collet <remi@fedoraproject.org> - 1:0.84.0.3.2-1
- update to 0.84+3.2 for GLPI 0.84
  0.84+3.2: http://forge.fusioninventory.org/versions/191

* Mon Aug 18 2014 Remi Collet <remi@fedoraproject.org> - 1:0.84.0.3.1-1
- update to 0.84+3.1 for GLPI 0.84
  0.84+3.1: http://forge.fusioninventory.org/versions/189
  0.84+3.1: http://forge.fusioninventory.org/versions/181

* Tue Mar 25 2014 Remi Collet <remi@fedoraproject.org> - 1:0.84.0.2.2-1
- update to 0.84+2.2 for GLPI 0.84
  0.84+2.1: http://forge.fusioninventory.org/versions/172
  0.84+2.2: http://forge.fusioninventory.org/versions/178

* Wed Jan 15 2014 Remi Collet <remi@fedoraproject.org> - 1:0.84.0.2.0-1
- update to 0.84+2.0 for GLPI 0.84
- set allow_url_fopen=On in config

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

