%global pluginname   appliances
%global svnrelease   114

Name:           glpi-appliances
Version:        1.6.0
%if 0%{?svnrelease}
Release:        0.1.svn%{svnrelease}%{?dist}
%else
Release:        1%{?dist}
%endif
Summary:        GLPI Plugin to manage appliances
Summary(fr):    Extension GLPI de gestion des applicatifs

Group:          Applications/Internet
License:        GPLv2+
URL:            https://forge.indepnet.net/projects/appliances

%if 0%{?svnrelease}
# svn export -r 114 https://forge.indepnet.net/svn/appliances/trunk appliances
# tar czf glpi-appliances-1.6.0-114.tar.gz appliances
Source0:        glpi-%{pluginname}-%{version}-%{svnrelease}.tar.gz
%else
Source0:        https://forge.indepnet.net/attachments/download/459/glpi-applicatifs-1.5.2.tar.gz
%endif


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       glpi >= 0.78
Requires:       php-xmlrpc php-soap

%description
This plugin add appliances management to GLPI
* Appliances creation (composed by various inventory item)
* Direct management from items
* Integrated with Helpdesk


%description -l fr
Cette extension permet la gestion des applicatifs dans GLPI
* Création d’applicatifs composé de plusieurs items
* Gestion directe à partir de l’item
* Intégration avec l'assistance


%prep
%setup -q -c 

cat >httpd <<EOF
<Directory /usr/share/glpi/plugins/%{pluginname}/sql>
    Order Allow,Deny
    Deny from all
</Directory>
EOF


%build
# empty build

%install
rm -rf %{buildroot} 

mkdir -p %{buildroot}/%{_datadir}/glpi/plugins
cp -ar %{pluginname} %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}

# ===== apache =====
rm -f %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}/sql/.htaccess
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install --mode 644 httpd %{buildroot}/%{_sysconfdir}/httpd/conf.d/%{name}.conf


%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_datadir}/glpi/plugins/%{pluginname}


%changelog
* Wed Aug 25 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.6.0-0.1.svn114
- new svn snapshot

* Sun Jun 20 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.6.0-0.1.svn110
- version 1.6.0 for glpi 0.78 RC (svn snapshot)
- initial RPM

