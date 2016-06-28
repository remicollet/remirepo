%global pluginname   loadentity
#global svnrelease   57

Name:           glpi-loadentity
Version:        1.3.1
%if 0%{?svnrelease}
Release:        0.1.svn%{svnrelease}%{?dist}
%else
Release:        1.1%{?dist}
%endif
Summary:        GLPI Plugin for entity import
Summary(fr):    Extension GLPI d'import d'une entité

Group:          Applications/Internet
License:        GPLv2+
URL:            https://forge.glpi-project.org/projects/loadentity

%if 0%{?svnrelease}
# svn export -r 57 https://forge.glpi-project.org/svn/loadentity/trunk loadentity
# tar czf glpi-loadentity-1.2.0-57.tar.gz loadentity
Source0:        glpi-loadentity-%{version}-%{svnrelease}.tar.gz
%else
Source0:        https://forge.glpi-project.org/attachments/download/1215/glpi-loadentity-1.3.1.tar.gz
%endif


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       glpi >= 0.83.3
Requires:       glpi <  0.84
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

cat >httpd <<EOF
<Directory /usr/share/glpi/plugins/%{pluginname}/scripts>
	<IfModule mod_authz_core.c>
		Require all denied
	</IfModule>
	<IfModule !mod_authz_core.c>
		Order Allow,Deny
		Deny from all
	</IfModule>
</Directory>
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
install --mode 644 cron %{buildroot}%{_sysconfdir}/cron.d/%{name}

# ===== apache =====
rm %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}/scripts/.htaccess
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install --mode 644 httpd %{buildroot}/%{_sysconfdir}/httpd/conf.d/%{name}.conf


%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%doc docs/* %{pluginname}/LICENSE
%config(noreplace) %{_sysconfdir}/cron.d/%{name}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_datadir}/glpi/plugins/%{pluginname}

%changelog
* Tue Jun 28 2016 Johan Cwiklinski <jcwiklinski AT teclib DOT com> - 1.3.1-1.1
- Change URL and Source

* Thu Jul 12 2012 Remi Collet <Fedora@FamilleCollet.com> - 1.3.1-1
- version 1.3.1 for GLPI 0.83.3
  https://forge.indepnet.net/projects/loadentity/versions/788

* Fri Apr 06 2012 Remi Collet <Fedora@FamilleCollet.com> - 1.3.0-1
- version 1.3.0 for GLPI 0.83
  https://forge.indepnet.net/projects/loadentity/versions/653

* Tue Oct 12 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.2.0-1
- version 1.2.0 and GLPI 0.78 released

* Fri Jun 18 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.2.0-0.1.svn57
- update to 1.2.0 for glpi 0.78 RC (svn snapshot)

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

