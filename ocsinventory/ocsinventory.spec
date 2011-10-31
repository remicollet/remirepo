%if %{?fedora}%{?rhel} >= 5
%global useselinux 1
%else
%global useselinux 0
%endif

# Remember to change this and Source0 for each release. thanks to launchpad :(
%global tarname OCSNG_UNIX_SERVER


Name:        ocsinventory
Summary:     Open Computer and Software Inventory Next Generation

Version:     2.0.2
Release:     1%{?dist}.3

Group:       Applications/Internet
License:     GPLv2
URL:         http://www.ocsinventory-ng.org/

# This change for each version... thanks launchpad :(
Source0:     http://launchpad.net/ocsinventory-server/stable-2.0/%{version}/+download/%{tarname}-%{version}.tar.gz
Source1:     ocsinventory-reports.conf

# Manage upgrade from 1.3.x
# http://bazaar.launchpad.net/~ocsinventory-core/ocsinventory-ocsreports/stable-2.0/revision/794
Patch0:      %{name}-upgrade.patch
# Use CONF_MYSQL everywhere
# http://bazaar.launchpad.net/~ocsinventory-core/ocsinventory-ocsreports/stable-2.0/revision/796
Patch1:      %{name}-dbconf.patch

BuildArch:   noarch
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Apache::DBI)
BuildRequires: perl(DBD::mysql)
BuildRequires: perl(Net::IP)
BuildRequires: perl(XML::Simple)

# Main package is a dummy package
Requires:    ocsinventory-server  = %{version}-%{release}
Requires:    ocsinventory-reports = %{version}-%{release}
Requires:    mysql-server


%description
Open Computer and Software Inventory Next Generation is an application
designed to help a network or system administrator keep track of the
computers configuration and software that are installed on the network.

OCS Inventory is also able to detect all active devices on your network,
such as switch, router, network printer and unattended devices.

OCS Inventory NG includes package deployment feature on client computers.

ocsinventory is a meta-package that will install the communication server,
the administration console and the database server (MySQL).

%description -l fr
Open Computer and Software Inventory Next Generation est une application 
destinée à aider l'administrateur système ou réseau à surveiller la
configuration des machines du réseau et les logiciels qui y sont installés.

OCS Inventory est aussi capable de détecter tout périphérique actif sur
le réseau, comme les commutateurs, routeurs, imprimantes et autres matériels
autonomes.

OCS Inventory NG intègre des fonctionnalités de télédiffusion de paquets
sur les machines clients.

ocsinventory est un méta-paquet qui installera le serveur de communication, 
la console d'administration et le serveur de base de données (MySQL).


%package server
Group:    Applications/Internet
Summary:  OCS Inventory NG - Communication server
Requires: mod_perl
%if 0%{?rhel} != 4
# when use with mod_perl2
Requires: perl(SOAP::Transport::HTTP2)
%endif
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# Required by the original setup script, but not detected automatically :
# Apache::DBI drags in DBI
Requires: perl(Apache::DBI)
Requires: perl(Net::IP)
Requires: perl(DBD::mysql)
# Optional, not detected automatically :
Requires: perl(SOAP::Lite)
Requires: perl(XML::Entities)
%if %{useselinux}
Requires: policycoreutils
%endif

%description server
This package provides the Communication server, which will handle HTTP
communications between database server and agents.

%description -l fr server
Ce paquet fournit le serveur de communication (Communication server), 
qui gère les communications HTTP entre les agents et le serveur de base
de données.


%package reports
Group:    Applications/Internet
Summary:  OCS Inventory NG - Communication server
# From PHP_Compat : date, mysql, ereg, pcre, zip, hash, xml, gd, zlib 
Requires: php
Requires: php-mysql php-gd php-domxml
%if 0%{?fedora} < 16
Requires: php-zip
%endif
# Required by the original setup script, but not detected automatically :
Requires: perl(DBD::mysql)
# Required by ipdiscover-util.pl (nmap and nmblookup)
Requires: nmap
# nmblookup is provided by samba or samba3x (EL-5)
Requires: %{_bindir}/nmblookup
%if %{useselinux}
Requires: policycoreutils
%endif

%description reports
This package provides the Administration console, which will allow 
administrators to query the database server through their favorite browser.

%description -l fr reports
Ce paquet fournit la console d'administration (Administration console), 
qui autorise les administrateurs à interroger la base de données via leur
navigateur favori.


%prep
%setup -q -n %{tarname}-%{version}

%patch0 -p0
%patch1 -p0

chmod -x binutils/ocs-errors

cat >external-agents.conf <<EOF
# allowed external useragents list
# WARNING may not be supported by OCS NG Community !
# 1 line per agent, with full name (including version)

# Ex, to allow fusioninventory_agent, uncomment next line
#FusionInventory-Agent_v2.1.9
EOF


%build
cd Apache
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

# --- ocsinventory-server --- communication server
cd Apache
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'

chmod -R u+rwX,go+rX,go-w %{buildroot}/*
find %{buildroot}%{perl_vendorlib}/Apache -name \*.pm -exec chmod -x {} \;

%if 0%{?rhel} == 4
# To avoid bad dependency on perl(mod_perl2)
rm -f %{buildroot}%{perl_vendorlib}/Apache/Ocsinventory/Server/Modperl2.pm
%else
# To avoid bad dependency on perl(mod_perl) : RHEL >= 5 && Fedora >= 4
rm -f %{buildroot}%{perl_vendorlib}/Apache/Ocsinventory/Server/Modperl1.pm
%endif

cd ..

mkdir -p %{buildroot}%{_localstatedir}/log/ocsinventory-server

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
sed -e 's;PATH_TO_LOG_DIRECTORY;%{_localstatedir}/log/ocsinventory-server;' \
   ./etc/logrotate.d/ocsinventory-server >%{buildroot}%{_sysconfdir}/logrotate.d/ocsinventory-server

# default configuration (localhost) should work on "simple" installation
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
%{__sed} -e "s;DATABASE_SERVER;localhost;g" \
    -e "s;DATABASE_PORT;3306;g" \
%if 0%{?rhel} == 4
    -e "s;VERSION_MP;1;g" \
%else
    -e "s;VERSION_MP;2;g" \
%endif
    -e "s;PATH_TO_LOG_DIRECTORY;%{_localstatedir}/log/ocsinventory-server;g" \
    -e '/OCS_OPT_EXT_USERAGENTS_FILE_PATH/s;^.*$;  PerlSetEnv OCS_OPT_EXT_USERAGENTS_FILE_PATH %{_sysconfdir}/ocsinventory/ocsinventory-server/external-agents.conf;' \
    etc/ocsinventory/ocsinventory-server.conf | \
    grep -v IfModule >%{buildroot}%{_sysconfdir}/httpd/conf.d/ocsinventory-server.conf

install -Dm 644 external-agents.conf \
        %{buildroot}%{_sysconfdir}/ocsinventory/ocsinventory-server/external-agents.conf

# --- ocsinventory-reports --- administration console

mkdir -p %{buildroot}%{_datadir}/ocsinventory-reports
cp -ar ocsreports %{buildroot}%{_datadir}/ocsinventory-reports
find %{buildroot}%{_datadir}/ocsinventory-reports \
     -type f -exec chmod -x {} \;

mkdir -p %{buildroot}%{_sysconfdir}/ocsinventory/ocsinventory-reports

mv %{buildroot}%{_datadir}/ocsinventory-reports/ocsreports/dbconfig.inc.php \
   %{buildroot}%{_sysconfdir}/ocsinventory/ocsinventory-reports/dbconfig.inc.php

# Not usefull for now (path is harcoded)
sed -i -e '/CONF_MYSQL/s;dbconfig.inc.php;%{_sysconfdir}/ocsinventory/ocsinventory-reports/dbconfig.inc.php;' \
    %{buildroot}%{_datadir}/ocsinventory-reports/ocsreports/var.php

mkdir -p %{buildroot}%{_localstatedir}/lib/ocsinventory-reports/{download,ipd,snmp}
mkdir -p %{buildroot}%{_bindir}

install -pm 644 etc/ocsinventory/snmp_com.txt     %{buildroot}%{_localstatedir}/lib/ocsinventory-reports/snmp/snmp_com.txt
install -pm 755 binutils/ipdiscover-util.pl       %{buildroot}%{_datadir}/ocsinventory-reports/ocsreports/ipdiscover-util.pl
install -pm 755 binutils/ocsinventory-injector.pl %{buildroot}%{_bindir}/ocsinventory-injector
install -pm 755 binutils/ocsinventory-log.pl      %{buildroot}%{_bindir}/ocsinventory-log


mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
sed -e "s;OCSREPORTS_ALIAS;/ocsreports;g" \
    -e "s;PATH_TO_OCSREPORTS_DIR;%{_datadir}/ocsinventory-reports/ocsreports;g" \
    -e "s;PACKAGES_ALIAS;/download;g" \
    -e "s;PATH_TO_PACKAGES_DIR;%{_localstatedir}/lib/ocsinventory-reports/download;g" \
    -e "s;SNMP_ALIAS;/snmp;g" \
    -e "s;PATH_TO_SNMP_DIR;%{_localstatedir}/lib/ocsinventory-reports/snmp;g" \
    %{SOURCE1} >%{buildroot}%{_sysconfdir}/httpd/conf.d/ocsinventory-reports.conf


%clean
rm -rf %{buildroot}


%post server
%if %{useselinux}
(
# New File context
semanage fcontext -a -s system_u -t httpd_log_t -r s0 "%{_localstatedir}/log/ocsinventory-server(/.*)?" 
# files created by app
restorecon -R %{_localstatedir}/log/ocsinventory-server
) &>/dev/null ||:
%endif
/sbin/service httpd condrestart > /dev/null 2>&1 || :


%post reports
%if %{useselinux}
(
# New File context
semanage fcontext -a -s system_u -t httpd_sys_script_rw_t -r s0 "%{_sysconfdir}/ocsinventory/ocsinventory-reports(/.*)?"
semanage fcontext -a -s system_u -t httpd_sys_script_rw_t -r s0 "%{_localstatedir}/lib/ocsinventory-reports(/.*)?"
# files created by app
restorecon -R %{_sysconfdir}/ocsinventory/ocsinventory-reports
restorecon -R %{_localstatedir}/lib/ocsinventory-reports
) &>/dev/null ||:
%endif


%postun server
if [ "$1" -eq "0" ]; then
%if %{useselinux}
    # Remove the File Context
    semanage fcontext -d "%{_localstatedir}/log/ocsinventory-server(/.*)?" &>/dev/null || :
%endif
    /sbin/service httpd condrestart > /dev/null 2>&1 || :
fi


%postun reports
%if %{useselinux}
if [ "$1" -eq "0" ]; then
    # Remove the File Context
    semanage fcontext -d "%{_sysconfdir}/ocsinventory/ocsinventory-reports(/.*)?" &>/dev/null ||:
    semanage fcontext -d "%{_localstatedir}/lib/ocsinventory-reports(/.*)?" &>/dev/null ||:
fi
%endif


%files
%defattr(-, root, root, -)


%files server
%defattr(-, root, root, -)
%doc LICENSE.txt README Apache/Changes
%doc binutils/*.README
%doc binutils/{ocs-errors,soap-client.pl}
%dir %{_sysconfdir}/ocsinventory/ocsinventory-server
%config(noreplace) %{_sysconfdir}/ocsinventory/ocsinventory-server/external-agents.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/ocsinventory-server
%config(noreplace) %{_sysconfdir}/httpd/conf.d/ocsinventory-server.conf
%attr(755,apache,root) %{_localstatedir}/log/ocsinventory-server
%{_bindir}/ocsinventory-injector
%{_bindir}/ocsinventory-log
%{perl_vendorlib}/Apache


%files reports
%defattr(-, root, root, -)
%doc LICENSE.txt README
%dir %{_sysconfdir}/ocsinventory
%attr(750,apache,root) %dir %{_sysconfdir}/ocsinventory/ocsinventory-reports
%attr(640,apache,root) %config(noreplace) %{_sysconfdir}/ocsinventory/ocsinventory-reports/dbconfig.inc.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/ocsinventory-reports.conf
%{_datadir}/ocsinventory-reports
%attr(755,apache,root) %dir %{_localstatedir}/lib/ocsinventory-reports
%attr(755,apache,root) %dir %{_localstatedir}/lib/ocsinventory-reports/ipd
%attr(755,apache,root) %dir %{_localstatedir}/lib/ocsinventory-reports/download
%attr(755,apache,root) %dir %{_localstatedir}/lib/ocsinventory-reports/snmp
%attr(644,apache,root) %config(noreplace) %{_localstatedir}/lib/ocsinventory-reports/snmp/snmp_com.txt


%changelog
* Mon Oct 31 2011 Remi Collet <Fedora@famillecollet.com> - 2.0.2-1.3
- provides external-agents.conf (OCS_OPT_EXT_USERAGENTS_FILE_PATH)

* Mon Oct 31 2011 Remi Collet <Fedora@famillecollet.com> - 2.0.2-1.2
- add patch to use CONF_MYSQL (and avoid link to dbconfig)
- comment /snmp alias for security
- give apache right to create dbconfig.php

* Thu Oct 27 2011 Remi Collet <Fedora@famillecollet.com> - 2.0.2-1.1
- add patch for upgrade from 1.3.x
- restart apache

* Sun Oct 23 2011 Remi Collet <Fedora@famillecollet.com> - 2.0.2-1
- update to 2.0.2

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.3.3-4
- Perl mass rebuild

* Sat Apr 09 2011 Xavier Bachelot <xavier@bachelot.org> 1.3.3-3
- Don't require php-zip for F16 and up.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 24 2010 Remi Collet <Fedora@famillecollet.com> - 1.3.3-1
- update to 1.3.3 (bugfix)
- clean applied patches
- requires nbmlookup instead of samba-client, fix #654252

* Sat Jun 19 2010 Remi Collet <Fedora@famillecollet.com> - 1.3.2-4
- upstream patch to set XML default parser
  (workaround XML::SAX issue on EL5, see #641735)

* Sat Jun 19 2010 Remi Collet <Fedora@famillecollet.com> - 1.3.2-3
- upstream patches

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.3.2-2
- Mass rebuild with perl-5.12.0

* Thu May 13 2010 Remi Collet <Fedora@famillecollet.com> 1.3.2-1
- update to new version
- remove schema patch (upstream)
- remove shorttag option

* Thu Feb 18 2010 Remi Collet <Fedora@famillecollet.com> 1.3.1-1
- update to new version
- improved patch for schema

* Sun Feb 07 2010 Remi Collet <Fedora@famillecollet.com> 1.3-1
- update to new version
- add a patch to improve schema check (when install / upgrade needed)

* Fri Feb 05 2010 Remi Collet <Fedora@famillecollet.com> 1.02.3-1
- Security Fixes - Bug #560737

* Mon Aug 17 2009 Remi Collet <Fedora@famillecollet.com> 1.02.1-3
- add ChangeLog
- Security Fixes (internal version 5003) Bug #517837

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 30 2009 Remi Collet <Fedora@famillecollet.com> 1.02.1-1
- update to OCS Inventory NG 1.02.1 - Security Fixes (internal version 5003)

* Mon Apr 20 2009 Remi Collet <Fedora@famillecollet.com> 1.02-1
- update to OCS Inventory NG 1.02 final release (internal version 5003)

* Sun Jan 18 2009 Remi Collet <Fedora@famillecollet.com> 1.02-0.10.rc3.el4.1
- fix php-xml > php-domxml in EL-4

* Sun Jan 11 2009 Remi Collet <Fedora@famillecollet.com> 1.02-0.10.rc3
- add r1447 and r1462 patch
- change log selinux context (httpd_log_t)

* Fri Oct 17 2008 Remi Collet <Fedora@famillecollet.com> 1.02-0.9.rc3
- upstream r1423 patch - migration script

* Sat Oct 11 2008 Remi Collet <Fedora@famillecollet.com> 1.02-0.8.rc3
- upstream r1413 patch - database schema

* Sat Oct 11 2008 Remi Collet <Fedora@famillecollet.com> 1.02-0.7.rc3
- update to RC3

* Tue Jul 22 2008 Remi Collet <Fedora@famillecollet.com> 1.02-0.6.rc2
- add missing requires perl(SOAP::Transport::HTTP2) (with mod_perl2)
- AddDefaultCharset ISO-8859-1 in httpd config
- fix SElinux path

* Sat Jun 14 2008 Remi Collet <Fedora@famillecollet.com> 1.02-0.5.rc2
- change dir from /var/lib/ocsinventory-server to /var/lib/ocsinventory-reports
- add Requires nmap and samba-client (nmblookup)

* Sun May 18 2008 Remi Collet <Fedora@famillecollet.com> 1.02-0.4.rc2
- remove <IfModule> from ocsinventory-server.conf
- change perm to 755 on /var/lib/ocsinventory-server
- metapackage description closer to upstream components name
- add BR perl(DBD::mysql) to avoid build warning

* Fri May 16 2008 Xavier Bachelot <xavier@bachelot.org> 1.02-0.3.rc2.1
- Fix BuildRequires and Requires.
- Fix %%description french translations and a few typos.
- Rename apache confs.

* Sat May 10 2008 Remi Collet <Fedora@famillecollet.com> 1.02-0.3.rc2
- add missing requires for php extensions (from PHP_Compat result)
- add selinux stuff

* Thu May 08 2008 Remi Collet <Fedora@famillecollet.com> 1.02-0.2.rc2
- update to RC2

* Sun Mar 15 2008 Remi Collet <Fedora@famillecollet.com> 1.02-0.2.rc1
- fix download dir

* Sat Mar  8 2008 Remi Collet <Fedora@famillecollet.com> 1.02-0.1.rc1
- Initial RPM

