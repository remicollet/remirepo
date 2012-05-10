%if 0%{?fedora} >= 17
%global  with_systemd  1
%else
%global  with_systemd  0
%endif

#global gitver 9bd1238
#global prever _beta1


Name:        fusioninventory-agent
Summary:     FusionInventory agent
Summary(fr): Agent FusionInventory
Group:       Applications/System
License:     GPLv2+
URL:         http://fusioninventory.org/

Version:     2.2.0

%if 0%{?gitver:1}
Release:     0.2.git%{gitver}%{?dist}
# From http://github.com/fusinv/fusioninventory-agent/tarball/master
Source0:     fusinv-fusioninventory-agent-2.1.8-95-g9bd1238.tar.gz
%else
Release:     2%{?dist}
Source0:     http://search.cpan.org/CPAN/authors/id/F/FU/FUSINV/FusionInventory-Agent-%{version}%{?prever}.tar.gz
%endif

Source1:   %{name}.cron
Source2:   %{name}.init
Source3:   %{name}.service

# See http://forge.fusioninventory.org/issues/1581
# Upstream desagree on this patch, but it will avoid behavior change
# until managed properly, as part of the XML file
Patch0:    %{name}-arch.patch


BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: perl(Module::Install)
# For tests 
BuildRequires: perl(Time::HiRes) perl(UNIVERSAL::require) perl(Test::More)
BuildRequires: perl(Class::Accessor::Fast) perl(Class::Data::Inheritable) perl(Test::Exception)
BuildRequires: perl(File::Which) perl(IPC::Run) perl(Test::MockModule) perl(Text::Template)
BuildRequires: perl(IO::Capture::Stderr) perl(Net::IP) perl(YAML)
%if 0%{?fedora} >= 14
BuildRequires: perl(LWP::Protocol::https) perl(IO::Socket::SSL)
BuildRequires: perl(HTTP::Server::Simple::Authen) perl(CGI)
%endif
%if 0%{?fedora}>= 12 || 0%{?rhel} >= 5
BuildRequires: perl(XML::TreePP)
%endif
%if 0%{?fedora}>= 10 || 0%{?rhel} >= 5
BuildRequires: perl(JSON)
%endif
%if 0%{?fedora} >= 11
BuildRequires: perl(Test::Compile) perl(HTTP::Proxy)
%endif
%if %{with_systemd}
BuildRequires: systemd-units
%endif

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:  perl(LWP) perl(Net::IP) perl(HTTP::Status) perl(Net::SSLeay)
Requires:  perl(Proc::Daemon) perl(Proc::PID::File)
%if 0%{?fedora} >= 6 || 0%{?rhel} >= 5
Requires:  perl(Net::CUPS)
%endif
%if %{with_systemd}
# We require this to be present for /etc/tmpfiles.d
Requires: systemd-units
# Make sure it's there when scriptlets run, too
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%else
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
%endif


# RPM 4.8
%{?filter_from_requires: %filter_from_requires /perl(Win32/d}
%{?perl_default_filter}
# RPM 4.9
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(Win32


%description
FusionInventory Agent is an application designed to help a network
or system administrator to keep track of the hardware and software
configurations of computers that are installed on the network.

This agent can send information about the computer to a OCS Inventory NG
or GLPI server with the FusionInventory for GLPI plugin.

You can add additional packages for optional tasks:

* perl-FusionInventory-Agent-Task-NetDiscovery
    Network Discovery support
* perl-FusionInventory-Agent-Task-NetInventory
    Network Inventory support
* perl-FusionInventory-Agent-Task-Deploy
    Software deployment support
* perl-FusionInventory-Agent-Task-ESX
    vCenter/ESX/ESXi remote inventory

Edit the /etc/sysconfig/%{name} file for service configuration.

%description -l fr
L'agent FusionInventory est une application destinée à aider l'administrateur
système ou réseau à surveiller la configuration des machines du réseau
et les logiciels qui y sont installés.

Cet agent peut envoyer les informations de l'ordinateur à un serveur
OCS Inventory NG ou à un serveur GLPI disposant de l'extension FusionInventory.

Vous pouvez ajouter les paquets additionnels pour les tâches optionnelles :

* perl-FusionInventory-Agent-Task-NetDiscovery
    Gestion de la découverte réseau
* perl-FusionInventory-Agent-Task-NetInventory
    Gestion de l'inventaire réseau
* perl-FusionInventory-Agent-Task-Deploy
    Gestion de déploiement de logiciels
* perl-FusionInventory-Agent-Task-ESX
    Inventaire à distance des vCenter/ESX/ESXi

Modifier le fichier /etc/sysconfig/%{name} pour configurer
le service.


%package yum-plugin
Summary:       Ask FusionInventory agent to send an inventory when yum exits
Summary(fr):   Demande à l'agent FusionInventory l'envoi d'un inventaire
Group:         System Environment/Base
BuildRequires: python-devel
Requires:      yum >= 2.4
Requires:      %{name}

%description yum-plugin
fusioninventory-agent-yum-plugin asks the running service agent to send an
inventory when yum exits.

This requires the service to be running with the --rpc-trust-localhost option.

%description -l fr yum-plugin
fusioninventory-agent-yum-plugin demande au service de l'agent d'envoyer un
inventaire à la fin de l'exécution de yum.

Le service doit être actif et lancé avec l'option --rpc-trust-localhost.

%prep
%if 0%{?gitver:1}
%setup -q -n fusinv-fusioninventory-agent-%{gitver}
%else
%setup -q -n FusionInventory-Agent-%{version}%{?prever}
%endif

%patch0 -p1 -b .rpmarch

# This work only on older version, and is ignored on recent
cat <<EOF | tee %{name}-req
#!/bin/sh
%{__perl_requires} $* | \
sed -e '/perl(Win32/d'
EOF

%if 0%{?gitver:1}
%global __perl_requires %{_builddir}/fusinv-fusioninventory-agent-%{gitver}/%{name}-req
%else
%global __perl_requires %{_builddir}/FusionInventory-Agent-%{version}%{?prever}/%{name}-req
%endif
chmod +x %{__perl_requires}

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
# used by hourly cron job and service launcher to override the %{name}.cfg setup.
#
# DONT FORGET to enable the service !
#
# Add tools directory if needed (tw_cli, hpacucli, ipssend, ...)
PATH=/sbin:/bin:/usr/sbin:/usr/bin
# Global options (debug for verbose log, rpc-trust-localhost for yum-plugin)
FUSINVOPT="--debug --rpc-trust-localhost"
# Mode, change to "cron" or "daemon" to activate
# - none (default on install) no activity
# - cron (inventory only) use the cron.hourly
%if %{with_systemd}
# NB systemd service launcher only use FUSINVOPT and agent.cfg
%else
# - daemon (recommanded) use the service
%endif
OCSMODE[0]=none
# OCS Inventory or FusionInventory server URI
# OCSSERVER[0]=your.ocsserver.name
# OCSSERVER[0]=http://your.ocsserver.name/ocsinventory
# OCSSERVER[0]=http://your.glpiserveur.name/glpi/plugins/fusioninventory/
# corresponds with --local=%{_localstatedir}/lib/%{name}
# OCSSERVER[0]=local
# Wait before inventory (for cron mode)
OCSPAUSE[0]=120
# Administrative TAG (optional, must be filed before first inventory)
OCSTAG[0]=
EOF


%build
perl Makefile.PL \
     PREFIX=%{_prefix} \
     SYSCONFDIR=%{_sysconfdir}/fusioninventory \
     LOCALSTATEDIR=%{_localstatedir}/lib/%{name}

make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

mkdir -p %{buildroot}%{_localstatedir}/{log,lib}/%{name}

install -m 644 -D  logrotate     %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -m 644 -D  %{name}.conf  %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -m 755 -Dp %{SOURCE1}    %{buildroot}%{_sysconfdir}/cron.hourly/%{name}
%if %{with_systemd}
install -m 644 -Dp %{SOURCE3}    %{buildroot}%{_unitdir}/%{name}.service
%else
install -m 755 -Dp %{SOURCE2}    %{buildroot}%{_initrddir}/%{name}
%endif

# Yum plugin installation
install -m 644 -D contrib/yum-plugin/%{name}.py   %{buildroot}%{_prefix}/lib/yum-plugins/%{name}.py
install -m 644 -D contrib/yum-plugin/%{name}.conf %{buildroot}%{_sysconfdir}/yum/pluginconf.d/%{name}.conf


%check
make test


%clean
rm -rf %{buildroot} %{buildroot}%{_datarootdir}


%post
%if %{with_systemd}
/sbin/chkconfig --del %{name} &>/dev/null || :
/bin/systemctl daemon-reload &>/dev/null || :
%else
if [ $1 = 1 ]; then
    # Initial installation
    /sbin/chkconfig --add %{name} || :
fi
%endif
exit 0

%preun
if [ $1 -eq 0 ] ; then
%if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}.service &>/dev/null
    /bin/systemctl stop %{name}.service &>/dev/null
%else
    /sbin/service %{name} stop &>/dev/null
    /sbin/chkconfig --del %{name}
%endif
fi
exit 0


%postun
%if %{with_systemd}
/bin/systemctl daemon-reload &>/dev/null
if [ $1 -ge 1 ]; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart %{name}.service &>/dev/null
fi
%else
if [ $1 -ge 1 ]; then
    /sbin/service %{name} condrestart &>/dev/null
fi
%endif
exit 0


%files
%defattr(-, root, root, -)
%doc Changes LICENSE THANKS
%dir %{_sysconfdir}/fusioninventory
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/fusioninventory/agent.cfg
%{_sysconfdir}/cron.hourly/%{name}
%if %{with_systemd}
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif
%{_datadir}/fusioninventory
%{_bindir}/fusioninventory-agent
%{_bindir}/fusioninventory-injector
%{_mandir}/man1/fusioninventory-agent*
%{_mandir}/man1/fusioninventory-injector*
%{_mandir}/man3/Fusion*
%dir %{_localstatedir}/log/%{name}
%dir %{_localstatedir}/lib/%{name}

%files yum-plugin
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/%{name}.conf
%{_prefix}/lib/yum-plugins/%{name}.*


%changelog
* Mon Apr 16 2012 Remi Collet <remi@fedoraproject.org> - 2.2.0-2
- revert change in 2.2.0: don't loose arch information
  see http://forge.fusioninventory.org/issues/1581

* Sat Apr 14 2012 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- update to 2.2.0
  http://search.cpan.org/src/FUSINV/FusionInventory-Agent-2.2.0/Changes

* Sun Feb 26 2012 Remi Collet <remi@fedoraproject.org> - 2.1.14-1
- update to 2.1.14
  http://cpansearch.perl.org/src/FUSINV/FusionInventory-Agent-2.1.14/Changes

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Remi Collet <remi@fedoraproject.org> - 2.1.12-1
- update to 2.1.12
  http://cpansearch.perl.org/src/FUSINV/FusionInventory-Agent-2.1.12/Changes
- upstream patch for http://forge.fusioninventory.org/issues/1161

* Sat Aug 06 2011 Remi Collet <remi@fedoraproject.org> - 2.1.9-3
- adapt filter

* Fri Jul 25 2011 Petr Sabata <contyk@redhat.com> - 2.1.9-2
- Perl mass rebuild

* Sun Jun 26 2011 Remi Collet <Fedora@famillecollet.com> 2.1.9-1
- missing dist tag

* Wed Jun 15 2011 Remi Collet <Fedora@famillecollet.com> 2.1.9-1
- update to 2.1.9
  http://cpansearch.perl.org/src/FUSINV/FusionInventory-Agent-2.1.9/Changes

* Sat Jun 11 2011 Remi Collet <Fedora@famillecollet.com> 2.1.9-0.1.git9bd1238
- update to 2.1.9 from git
- improved init script for systemd
- improved comment for use with glpi-fusioninventory

* Thu Mar 31 2011 Remi Collet <Fedora@famillecollet.com> 2.1.8-2
- revert change for issue 656 which breaks compatibility

* Wed Mar 30 2011 Remi Collet <Fedora@famillecollet.com> 2.1.8-1
- update to 2.1.8
  http://cpansearch.perl.org/src/FUSINV/FusionInventory-Agent-2.1.8/Changes

* Thu Dec 30 2010 Remi Collet <Fedora@famillecollet.com> 2.1.7-2
- add the yum-plugin sub-package

* Mon Dec 13 2010 Remi Collet <Fedora@famillecollet.com> 2.1.7-1
- update to 2.1.7
  http://cpansearch.perl.org/src/FUSINV/FusionInventory-Agent-2.1.7/Changes

* Sun Nov 28 2010 Remi Collet <Fedora@famillecollet.com> 2.1.7-0.1.beta1
- update to 2.1.7 beta1

* Sat Nov 13 2010 Remi Collet <Fedora@famillecollet.com> 2.1.6-1.1
- fix perl filter on EL-6

* Wed Oct 06 2010 Remi Collet <Fedora@famillecollet.com> 2.1.6-1
- update to 2.1.6
  http://cpansearch.perl.org/src/FUSINV/FusionInventory-Agent-2.1.6/Changes
- fix init script for multi-server in daemon mode
- workaround for http://forge.fusioninventory.org/issues/414

* Wed Sep 15 2010 Remi Collet <Fedora@famillecollet.com> 2.1.5-1
- update to 2.1.5
  http://cpansearch.perl.org/src/FUSINV/FusionInventory-Agent-2.1.5/Changes

* Fri Sep 10 2010 Remi Collet <Fedora@famillecollet.com> 2.1.3-2
- add %%check

* Sat Sep 04 2010 Remi Collet <Fedora@famillecollet.com> 2.1.3-1
- update to 2.1.3
  http://cpansearch.perl.org/src/FUSINV/FusionInventory-Agent-2.1.3/Changes

* Wed Aug 25 2010 Remi Collet <Fedora@famillecollet.com> 2.1.2-1
- update to 2.1.2
  http://cpansearch.perl.org/src/FUSINV/FusionInventory-Agent-2.1.2/Changes

* Wed Aug 18 2010 Remi Collet <Fedora@famillecollet.com> 2.1.1-1
- update to 2.1.1

* Wed Aug 18 2010 Remi Collet <Fedora@famillecollet.com> 2.1-2.gita7532c0
- update to git snaphost which fix EL issues
- fix init script
- adapt perl filter for recent/old fedora or EL

* Mon Aug 16 2010 Remi Collet <Fedora@famillecollet.com> 2.1-1
- update to 2.1
- switch download URL back to CPAN
- add %%{perl_vendorlib}/auto
- filter perl(Win32*) from Requires
- add patch (from git) to reopen the file logger if needed

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

