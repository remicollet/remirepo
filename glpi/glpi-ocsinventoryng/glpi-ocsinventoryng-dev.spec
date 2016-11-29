# remirepo spec file for glpi-ocsinventoryng
#
# Copyright (c) 2013-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global pluginname   ocsinventoryng
%global lockname     ocsinventoryng.lock

Name:           glpi-ocsinventoryng
Version:        1.3.1
Release:        1%{?dist}
Summary:        Plugin to synchronize GLPI with OCS Inventory NG

Group:          Applications/Internet
License:        GPLv2+
URL:            https://github.com/pluginsGLPI/ocsinventoryng

Source0:        https://github.com/pluginsGLPI/ocsinventoryng/releases/download/%{version}/glpi-ocsinventoryng-%{version}.tar.gz
Source1:        %{name}-httpd.conf

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext

Requires:       glpi >= 9.1.1
Requires:       glpi <  9.2
Requires:       crontabs
Requires:       php-cli
# phpcompatinfo for version 1.0.2
Requires:       php-date
Requires:       php-json
Requires:       php-pcre

# Latest version is 1.6.x for GLPI 0.83.x
Obsoletes:      glpi-mass-ocs-import < 1.7
Provides:       glpi-mass-ocs-import = 1.7.0
Provides:       glpi-massocsimport   = 1.7.0


%description
This plugin allows you to synchronize GLPI inventory with OCS Inventory NG.

It's intended to replace native mode OCS of GLPI and use the massocsimport
plugin features to provide better compatibility and extensibility with OCS.


%prep
%setup -q -c

mv %{pluginname}/docs docs

# dos2unix to avoid rpmlint warnings
for doc in docs/* ; do
    sed -i -e 's/\r//' $doc
    chmod -x $doc
done

# Create link to LICENSE for standard doc folder
ln -s %{_datadir}/glpi/plugins/%{pluginname}/LICENSE LICENSE

# For developer only
rm     %{pluginname}/README.md
rm     %{pluginname}/TOKNOW.txt
rm     %{pluginname}/ocsinventoryng.png

# For Windows only
rm %{pluginname}/scripts/*.bat

# Access retricted in apache config
rm ocsinventoryng/scripts/.htaccess \
   ocsinventoryng/install/mysql/.htaccess

cat <<EOF | tee cron
# GLPI ocsinventoryng plugin
# Synchronization only of OCS servers in "expert" mode
# Must be enabled from the GLPI Control panel
*/5 * * * * apache %{_datadir}/glpi/plugins/%{pluginname}/scripts/ocsng_fullsync.sh
EOF

# fix perms
find %{pluginname} -type f -exec chmod -x {} \;
chmod +x %{pluginname}/scripts/*.sh

# Display compatibility check
grep version_compare %{pluginname}/setup.php


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

# Cron
install -p -D -m 644 cron %{buildroot}%{_sysconfdir}/cron.d/%{name}

# Lock
mkdir -p %{buildroot}%{_localstatedir}/lib/glpi/files/_lock
touch %{buildroot}%{_localstatedir}/lib/glpi/files/_lock/%{lockname}


%clean
rm -rf %{buildroot}


%post
# first install (not upgrade)
if [ "$1" -eq "1" ]; then
    install -o apache -g apache -m 644 /dev/null %{_localstatedir}/lib/glpi/files/_lock/%{lockname}
fi


%postun
# uninstall (not upgrade)
if [ "$1" -eq "0" -a -f %{_localstatedir}/lib/glpi/files/_lock/%{lockname} ]; then
    rm %{_localstatedir}/lib/glpi/files/_lock/%{lockname}
fi


%check
# Check consistency for the name of the lock file in sources
grep %{lockname} %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}/scripts/ocsng_fullsync.sh || exit 1
grep %{lockname} %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}/setup.php || exit 1


%files -f %{name}.lang
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc docs/*
%config(noreplace) %{_sysconfdir}/cron.d/%{name}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%dir %{_datadir}/glpi/plugins/%{pluginname}
%dir %{_datadir}/glpi/plugins/%{pluginname}/locales
%{_datadir}/glpi/plugins/%{pluginname}/*.php
%{_datadir}/glpi/plugins/%{pluginname}/ajax
%{_datadir}/glpi/plugins/%{pluginname}/css
%{_datadir}/glpi/plugins/%{pluginname}/files
%{_datadir}/glpi/plugins/%{pluginname}/front
%{_datadir}/glpi/plugins/%{pluginname}/inc
%{_datadir}/glpi/plugins/%{pluginname}/install
%{_datadir}/glpi/plugins/%{pluginname}/pics
%{_datadir}/glpi/plugins/%{pluginname}/scripts
# Keep here as required from interface
%{_datadir}/glpi/plugins/%{pluginname}/LICENSE
# flag file (empty) used to enable/disable the plugin in the interface (apache)
%ghost %{_localstatedir}/lib/glpi/files/_lock/%{lockname}


%changelog
* Tue Nov 29 2016 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1 for GLPI 9.1.1

* Tue Nov 29 2016 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0 for GLPI 9.1.1
- update script is broken
  open https://github.com/pluginsGLPI/ocsinventoryng/issues/58

* Wed Sep 28 2016 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3 for GLPI 9.1

* Fri Sep 16 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2 for GLPI 0.90 and 9.1
- sources from github

* Fri Nov 27 2015 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1 for GLPI 0.90
  https://forge.glpi-project.org/versions/1181

* Thu Oct  8 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0 for GLPI 0.90
  https://forge.glpi-project.org/versions/1179

* Wed Sep 16 2015 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2 for GLPI 0.85+
  https://forge.glpi-project.org/versions/1131

* Mon Jun  8 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1 for GLPI 0.85+
- add upstream patch for https://forge.indepnet.net/issues/5359

* Sun Mar  1 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0 for GLPI 0.85+
  https://forge.indepnet.net/versions/1116

* Mon Sep  8 2014 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3 for GLPI 0.84+
  https://forge.indepnet.net/versions/957

* Wed Oct  2 2013 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Initial RPM (from glpi-mass-ocs-import.spec)
