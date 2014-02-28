Name:           remi-release
Version:        %{fedora}
%if %{fedora} >= 18
Release:        2%{?dist}
%else
Release:        7%{?dist}
%endif
Summary:        YUM configuration for remi repository
Summary(fr):	Configuration de YUM pour le dépôt remi

Group:          System Environment/Base
License:        GPLv2+
URL:            http://rpms.famillecollet.com/
Source0:        RPM-GPG-KEY-remi
Source1:	    remi-fc.repo
Source3:	    remi.list
BuildRoot:      %{_tmppath}/%{name}-%{version}
BuildArchitectures: noarch

Requires:       yum
Requires:       fedora-release >= %{fedora}
Conflicts:      apt < 0.5.15lorg3

%description
This package contains yum configuration for the "remi" RPM Repository, 
as well as the public GPG keys used to sign them.

The repository is not enabled after installation, so you must use
the --enablerepo=remi option for yum.

It also provides apt configuration.

%description -l fr
Ce paquetage contient le fichier de configuration de YUM pour utiliser
les RPM du dépôt "remi" ainsi que la clé GPG utilisée pour les signer.

Le dépôt n'est pas activé après l'installation, vous devez donc utiliser
l'option --enablerepo=remi de yum.

Il fournit également la configuration de apt.


%prep
%setup -c -T


%build
echo empty build


%install
rm -rf %{buildroot}

# PGP
install -Dp -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-remi

# YUM
install -Dp -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/yum.repos.d/remi.repo

# APT
install -dm 755 %{buildroot}%{_sysconfdir}/apt/{gpg,sources.list.d}
install -m 644 -p %{SOURCE3} \
    %{buildroot}%{_sysconfdir}/apt/sources.list.d/remi.list
ln -s ../../pki/rpm-gpg/RPM-GPG-KEY-remi \
    %{buildroot}%{_sysconfdir}/apt/gpg/gpg-pubkey-00f97f56-467e318a


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/remi.repo
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-remi
%{_sysconfdir}/apt/gpg/gpg-pubkey-00f97f56-467e318a
%config(noreplace) %{_sysconfdir}/apt/sources.list.d/remi.list


%changelog
* Fri Feb 28 2014 Remi Collet <RPMS@FamilleCollet.com> - 19-2 and 20-2
- add php56 repository

* Tue Sep 10 2013 Remi Collet <RPMS@FamilleCollet.com> - 20-1.fc20.remi
- Fedora release 20 (Heisenbug)

* Wed Apr 24 2013 Remi Collet <RPMS@FamilleCollet.com> - 19-1.fc19.remi
- Fedora release 19 (Schrödinger's Cat)

* Sun Oct 21 2012 Remi Collet <RPMS@FamilleCollet.com> - 18-1.fc18.remi
- Fedora release 18 (Spherical Cow)

* Tue Jun 26 2012 Remi Collet <RPMS@FamilleCollet.com> - 17-7.fc17.remi
- remove post scriptlet (smart stuff)

* Sat May 05 2012 Remi Collet <RPMS@FamilleCollet.com> - 17-6.fc17.remi
- Fedora release 17 (Beefy Miracle)
- drop Smart config

* Sun Oct 02 2011 Remi Collet <RPMS@FamilleCollet.com> - 16-6.fc16.remi
- F16 build - Verne

* Sat Apr 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 15-6.fc15.remi
- F15 build - Lovelock

* Wed Sep 22 2010 Remi Collet <RPMS@FamilleCollet.com> - 14-6.fc14.remi
- F14 build - Laughlin

* Sat May 01 2010 Remi Collet <RPMS@FamilleCollet.com> - ##-6.fc##.remi
- use a mirrorlist URL

* Sat Apr 17 2010 Remi Collet <RPMS@FamilleCollet.com> - 13-5.fc13.remi
- F13 build - Goddard

* Fri Nov 06 2009 Remi Collet <RPMS@FamilleCollet.com> - 12-5.fc12.remi
- F12 build

* Thu Apr 30 2009 Remi Collet <RPMS@FamilleCollet.com> - ##-5.fc##.remi
- F11 build
- new repo layout

* Wed Nov 12 2008 Remi Collet <RPMS@FamilleCollet.com> - 10-4.fc10.remi
- F10 build
- remove old site (remi.collet.free.fr)

* Wed May  7 2008 Remi Collet <RPMS@FamilleCollet.com> - 9-4.fc9.remi
- F9 build

* Sat Feb  2 2008 Remi Collet <RPMS@FamilleCollet.com> - {3-8}-4.fc{3-8}.remi
- new mirror http://rpms.famillecollet.com/

* Thu Nov 02 2007 Remi Collet <RPMS@FamilleCollet.com> - 8-3.fc8.remi
- F8 build

* Thu Aug 23 2007 Remi Collet <RPMS@FamilleCollet.com> - {3-5}-3.fc{3-5}.remi
- update smart.channel during %%post only on fc > 5

* Sun Jun 24 2007 Remi Collet <RPMS@FamilleCollet.com> - {3-7}-2.el4.remi
- New key (email change, same ID)

* Sun May 20 2007 Remi Collet <RPMS@FamilleCollet.com> - 7-1.fc7.remi
- F-7 rebuild

* Sat Mar 24 2007 Remi Collet <RPMS@FamilleCollet.com> - 6-1.fc6.remi
- add remi.channel for smart
- add remi.list for apt

* Mon Nov 20 2006 Remi Collet <RPMS@FamilleCollet.com> - 1-2.fc6.remi
- change mirror list (iut-info.ens.univ-reims.fr to iut-info.univ-reims.fr)

* Tue Oct 24 2006 Remi Collet <RPMS@FamilleCollet.com> - 1-1.fc6.remi
- open FC6 repo

* Sun Mar 26 2006 Remi Collet <RPMS@FamilleCollet.com> - 1-1.fc5.remi
- open FC5 repo

* Tue Jan 03 2006  Remi Collet <remi.collet@univ-reims.fr> - 1-1.fc{3,4}.remi
- initial package
