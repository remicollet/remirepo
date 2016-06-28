# remirepo spec file for glpi-webservices
#
# Copyright (c) 2010-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global pluginname   webservices
#global svnrelease   322

Name:           glpi-webservices
Version:        1.6.0
%if 0%{?svnrelease}
Release:        0.1.svn%{svnrelease}%{?dist}
%else
Release:        1.1%{?dist}
%endif
Summary:        GLPI Plugin which provides web services
Summary(fr):    Extension GLPI fournissant des services web

Group:          Applications/Internet
License:        GPLv2+
URL:            https://forge.glpi-project.org/projects/webservices

%if 0%{?svnrelease}
# svn export -r 322 https://forge.glpi-project.org/svn/webservices/trunk webservices
# tar czf glpi-webservices-1.3.0-322.tar.gz webservices
Source0:        glpi-%{pluginname}-%{version}-%{svnrelease}.tar.gz
%else
Source0:        https://forge.glpi-project.org/attachments/download/2099/glpi-webservices-1.6.0.tar.gz
%endif


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       glpi >= 0.85.3
Requires:       glpi <  0.91
Requires:       php-xmlrpc
Requires:       php-soap


%description
This plugin provides a server for Web Services which allow
an external application to check and control GLPI.

%description -l fr
Cette extension fournit un serveur de services web permettant
à une application externe d'interroger et de piloter GLPI.


%prep
%setup -q -c 

rm -rf %{pluginname}/.htaccess \
       %{pluginname}/scripts/.htaccess

rm -rf %{pluginname}/tools

# Create link to LICENSE for standard doc folder
ln -s %{_datadir}/glpi/plugins/%{pluginname}/LICENSE LICENSE

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
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install --mode 644 httpd %{buildroot}/%{_sysconfdir}/httpd/conf.d/%{name}.conf


%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_datadir}/glpi/plugins/%{pluginname}


%changelog
* Tue Jun 28 2016 Johan Cwiklinski <jcwiklinski AT teclib DOT com> - 1.6.0-1.1
- Change URL

* Sat Oct  3 2015 Remi Collet <Fedora@FamilleCollet.com> - 1.6.0-1
- version 1.6.0 for GLPI 0.85.3 and 0.90
  https://forge.glpi-project.org/versions/1176

* Tue Jun  2 2015 Remi Collet <Fedora@FamilleCollet.com> - 1.5.0-1
- version 1.5.0 for GLPI 0.85
  https://forge.indepnet.net/versions/1102

* Mon Nov 17 2014 Remi Collet <Fedora@FamilleCollet.com> - 1.4.3-1
- version 1.4.3
  https://forge.indepnet.net/versions/1040

* Mon Apr  7 2014 Remi Collet <Fedora@FamilleCollet.com> - 1.4.2-1
- version 1.4.2
  https://forge.indepnet.net/projects/webservices/versions/1031

* Wed Feb 12 2014 Remi Collet <Fedora@FamilleCollet.com> - 1.4.1-1
- version 1.4.1
  https://forge.indepnet.net/projects/webservices/versions/996

* Wed Nov 13 2013 Remi Collet <Fedora@FamilleCollet.com> - 1.4.0-1
- version 1.4.0 for GLPI 0.84
  https://forge.indepnet.net/projects/webservices/versions/921

* Thu Jul 12 2012 Remi Collet <Fedora@FamilleCollet.com> - 1.3.1-1
- version 1.3.1 for GLPI 0.83.3
  https://forge.indepnet.net/projects/webservices/versions/703

* Fri Apr 06 2012 Remi Collet <Fedora@FamilleCollet.com> - 1.3.0-1
- version 1.3.0
  https://forge.indepnet.net/projects/webservices/versions/635
- fix config for httpd 2.4

* Sun Feb 26 2012 Remi Collet <Fedora@FamilleCollet.com> - 1.3.0-0.1.svn322
- update to 1.3.0 for glpi 0.83 RC (svn snapshot)

* Sun Oct 16 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.2.0-1
- update to 1.2.0 finale version

* Tue Sep 27 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.2.0-0.2.svn290
- new snapshot

* Tue Sep 20 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.2.0-0.2.svn282
- new snapshot

* Sun Jul 17 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.2.0-0.1.svn264
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
