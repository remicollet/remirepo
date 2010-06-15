%define pluginname   loadentity

Name:           glpi-loadentity
Version:        1.0.0
Release:        1%{?dist}
Summary:        GLPI Plugin for entity import
Summary(fr):    Extension GLPI d'import d'une entité

Group:          Applications/Internet
License:        GPLv2+
URL:            http://www.glpi-project.org/

Source0:        http://www.glpi-project.org/IMG/gz/glpi-%{pluginname}-%{version}.tar.gz
Source1:        %{name}.conf


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       glpi >= 0.72
Requires:       %{_sysconfdir}/cron.d

%description
Plugin which allow to export data from a entity to CSV.

Designed to work with serveur using dumpentity.

%description -l fr
Extension permettant de réaliser une importation des données 
d'une entité en CSV.

Conçue pour fonctionner avec un serveur utilisant dumpentity.

%prep
%setup -q -c 

cat >cron <<EOF
# GLPI loadentity extension.
# Change time to avoid bottleneck on server
# and uncomment to enable
# 0 6 * * * apache php -q -f %{_datadir}/glpi/plugins/%{pluginname}/scripts/run.php
EOF

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

mkdir -p %{buildroot}%{_sysconfdir}/cron.d
install -m 644 cron %{buildroot}%{_sysconfdir}/cron.d/%{name}

# ===== apache =====
rm %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}/scripts/.htaccess
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install --mode 644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/httpd/conf.d/%{name}.conf


%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%doc docs/*
%config(noreplace) %{_sysconfdir}/cron.d/%{name}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_datadir}/glpi/plugins/%{pluginname}

%changelog
* Mon Jul 20 2009 Remi Collet <RPMS@FamilleCollet.com> - 1.0.0-1
- update to 1.0.0 for glpi 0.72

* Sat Jul 12 2008 Remi Collet <RPMS@FamilleCollet.com> - 0.2-1
- update to 0.2 for glpi 0.71

* Sun Nov 11 2007 Remi Collet <RPMS@FamilleCollet.com> - 0.1-0.20071111
- new SVN snapshot

* Wed Oct 24 2007 Remi Collet <RPMS@FamilleCollet.com> - 0.1-0.20071024
- new SVN snapshot

* Sun Oct 21 2007 Remi Collet <RPMS@FamilleCollet.com> - 0.1-0.20071021
- update from SVN
- add apache conf

* Sat Oct 20 2007 Remi Collet <RPMS@FamilleCollet.com> - 0.1-0.20071020
- Initial RPM

