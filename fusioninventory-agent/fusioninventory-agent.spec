#global gitver f7c5492

Name:        fusioninventory-agent
Summary:     FusionInventory agent
Summary(fr): Agent FusionInventory

Version:   2.0.6

%if 0%{?gitver:1}
Release:   5.git%{gitver}%{?dist}
Source0:   fusinv-fusioninventory-agent-2.0.4-20-gf7c5492.tar.gz
%else
Release:   1%{?dist}
Source0:   http://forge.fusioninventory.org/attachments/download/66/FusionInventory-Agent-2.0.6.tar.gz
%endif

Source1:   %{name}.cron
Source2:   %{name}.init

Group:     Applications/System
License:   GPLv2+
URL:       http://fusioninventory.org/

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: perl(Module::Install)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:  perl(LWP) perl(Net::IP) perl(HTTP::Status) perl(Net::SSLeay) perl(Crypt::SSLeay)
Requires:  perl(Proc::Daemon) perl(Proc::PID::File)
# Not yet available in EPEL ...
%if %{?fedora}%{?rhel} > 4
Requires:  perl(Archive::Extract)
Requires:  perl(Net::CUPS)
%endif
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service

%{?perl_default_filter}


%description
FusionInventory Agent is an application designed to help a network
or system administrator to keep track of the hardware and software
configurations of computers that are installed on the network.

This agent can send information about the computer to a OCS Inventory NG
or GLPI server with the FusionInventory for GLPI plugin.

You can add additional packages for optional tasks:

* perl-FusionInventory-Agent-Task-OcsDeploy
    OCS Inventory Software deployment support
* perl-FusionInventory-Agent-Task-NetDiscovery
    Network Discovery support
* perl-FusionInventory-Agent-Task-SNMPQuery
    SNMP Query support



%description -l fr
L'agent FusionInventory est une application destinée à aider l'administrateur
système ou réseau à surveiller la configuration des machines du réseau
et les logiciels qui y sont installés.

Cet agent peut envoyer les informations de l'ordinateur à un serveur
OCS Inventory NG ou à un serveur GLPI disposant de l'extension FusionInventory.

Vous pouvez ajouter les paquets additionnels pour les tâches optionnelles :

* perl-FusionInventory-Agent-Task-OcsDeploy
    Gestion du déploiement logiciel OCS Inventory
* perl-FusionInventory-Agent-Task-NetDiscovery
    Gestion de la découverte réseau
* perl-FusionInventory-Agent-Task-SNMPQuery
    Gestion de l'interrogation SNMP


%prep
%if 0%{?gitver:1}
%setup -q -n fusinv-fusioninventory-agent-%{gitver}
%else
%setup -q -n FusionInventory-Agent-%{version}
%endif

cat <<EOF | tee logrotate
%{_localstatedir}/log/%{name}/*.log {
    weekly
    rotate 7
    compress
    notifempty
    missingok
}
EOF

cat <<EOF | tee %{name}.conf
#
# Fusion Inventory Agent Configuration File
# used by hourly cron job used to override the %{name}.cfg setup.
#
# Add tools directory if needed (tw_cli, hpacucli, ipssend, ...)
PATH=/sbin:/bin:/usr/sbin:/usr/bin
# Global options
#FUSINVOPT=--debug
# Mode, change to "cron" or "daemon" to activate
OCSMODE[0]=none
# OCS server URI
# OCSSERVER[0]=your.ocsserver.name
# corresponds with --local=%{_localstatedir}/lib/%{name}
# OCSSERVER[0]=local
# Wait before inventory
OCSPAUSE[0]=120
# Administrative TAG (optional, must be filed before first inventory)
OCSTAG[0]=
EOF

cat <<EOF | tee agent.cfg
# This file provides global and command line settings
# For CRON or DAEMON configuration, see %{_sysconfdir}/sysconfig/%{name}
basevardir=%{_localstatedir}/lib/%{name}
logger=Stderr
server=""
EOF


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'

%{_fixperms} $RPM_BUILD_ROOT/*


%{__mkdir_p} %{buildroot}%{_localstatedir}/{log,lib}/%{name}

%{__install} -m 644 -D  logrotate    %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -m 644 -D  %{name}.conf %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -m 644 -D  agent.cfg    %{buildroot}%{_sysconfdir}/fusioninventory/agent.cfg
%{__install} -m 755 -Dp %{SOURCE1}   %{buildroot}%{_sysconfdir}/cron.hourly/%{name}
%{__install} -m 755 -Dp %{SOURCE2}   %{buildroot}%{_initrddir}/%{name}


%clean
rm -rf %{buildroot}


%post
/sbin/chkconfig --add %{name}


%preun
if [ $1 -eq 0 ] ; then
    /sbin/service %{name} stop &>/dev/null
    /sbin/chkconfig --del %{name}
fi
exit 0


%postun
if [ $1 -ge 1 ]; then
    /sbin/service %{name} condrestart &>/dev/null
fi
exit 0


%files
%defattr(-, root, root, -)
%doc AUTHORS Changes LICENSE README THANKS
%dir %{_sysconfdir}/fusioninventory
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/fusioninventory/agent.cfg
%{_sysconfdir}/cron.hourly/%{name}
%{_initrddir}/%{name}
%{perl_vendorlib}/FusionInventory
%{_bindir}/%{name}
%exclude %{_bindir}/%{name}-config
%{_mandir}/man1/%{name}*
%{_mandir}/man3/Fusion*
%dir %{_localstatedir}/log/%{name}
%dir %{_localstatedir}/lib/%{name}


%changelog
* Sat May 29 2010 Remi Collet <Fedora@famillecollet.com> 2.0.6-1
- update to 2.0.6
- swicth download URL to forge

* Wed May 12 2010 Remi Collet <Fedora@famillecollet.com> 2.0.5-1
- update to 2.0.5

* Tue May 11 2010 Remi Collet <Fedora@famillecollet.com> 2.0.4-4.gitf7c5492
- git snapshot fix perl 5.8.8 (EL5) issue

* Sat May 08 2010 Remi Collet <Fedora@famillecollet.com> 2.0.4-4.gitddfdeaf
- git snapshot fix daemon issue
- add FUSINVOPT for global options (p.e.--debug)

* Sat May 08 2010 Remi Collet <Fedora@famillecollet.com> 2.0.4-3
- add support for daemon mode

* Fri May 07 2010 Remi Collet <Fedora@famillecollet.com> 2.0.4-2
- info about perl-FusionInventory-Agent-Task-OcsDeploy
- spec cleanup
- french translation
- set Net::CUPS and Archive::Extract optionnal on RHEL4

* Fri May 07 2010 Remi Collet <Fedora@famillecollet.com> 2.0.4-1
- update to 2.0.4 which fixes important bugs when cron is used

* Sat May 01 2010 Remi Collet <Fedora@famillecollet.com> 2.0.3-1
- initial spec

