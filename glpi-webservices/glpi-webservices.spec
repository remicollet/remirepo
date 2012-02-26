%global pluginname   webservices
#global svnrelease   290

Name:           glpi-webservices
Version:        1.2.0
%if 0%{?svnrelease}
Release:        0.2.svn%{svnrelease}%{?dist}
%else
Release:        1%{?dist}
%endif
Summary:        GLPI Plugin which provides web services
Summary(fr):    Extension GLPI fournissant des services web

Group:          Applications/Internet
License:        GPLv2+
URL:            https://forge.indepnet.net/projects/webservices

%if 0%{?svnrelease}
# svn export -r 290 https://forge.indepnet.net/svn/webservices/branches/1.2-bugfixes webservices
# tar czf glpi-webservices-1.2.0-290.tar.gz webservices
Source0:        glpi-%{pluginname}-%{version}-%{svnrelease}.tar.gz
%else
Source0:        https://forge.indepnet.net/attachments/download/980/glpi-webservices-1.2.0.tar.gz
%endif


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       glpi >= 0.80
Requires:       glpi <  0.81
Requires:       php-xmlrpc php-soap

%description
This plugin provides a server for Web Services which allow
an external application to check and control GLPI.

%description -l fr
Cette extension fournit un serveur de services web permettant
à une application externe d'interroger et de piloter GLPI.


%prep
%setup -q -c 

cat >httpd <<EOF
<Directory /usr/share/glpi/plugins/%{pluginname}/scripts>
    Order Allow,Deny
    Deny from all
</Directory>

<Directory /usr/share/glpi/plugins/%{pluginname}>
    <Files xmlrpc.php>
    # Uncomment next line to enable compression and reduce network load
    #php_value zlib.output_compression 4096
    </Files>
</Directory>
EOF


%build
# empty build

%install
rm -rf %{buildroot} 

mkdir -p %{buildroot}/%{_datadir}/glpi/plugins
cp -ar %{pluginname} %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}

# ===== apache =====
rm -f %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}/.htaccess
rm -f %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}/scripts/.htaccess
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install --mode 644 httpd %{buildroot}/%{_sysconfdir}/httpd/conf.d/%{name}.conf


%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_datadir}/glpi/plugins/%{pluginname}


%changelog
* Sun Oct 16 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.2.0-1
- update to 1.2.0 finale version

* Tue Sep 27 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.2.0-0.2.svn290
- new snapshot

* Tue Sep 20 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.2.0-0.2.svn282
- new snapshot

* Tue Jul 17 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.2.0-0.1.svn264
- update to 1.2.0 for glpi 0.80 RC (svn snapshot)

* Tue Oct 12 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-1
- version 1.0.0 and GLPI 0.78 released

* Wed Aug 25 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-0.1.svn176
- new snapshot

* Tue Aug 10 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-0.1.svn174
- new snapshot

* Wed Jul 07 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-0.1.svn173
- new snapshot

* Fri Jul 02 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-0.1.svn172
- new snapshot

* Sun Jun 20 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-0.1.svn170
- new snapshot

* Fri Jun 18 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-0.1.svn168
- version 1.0.0 for glpi 0.78 RC (svn snapshot)
- initial RPM

