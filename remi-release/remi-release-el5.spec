Name:           remi-release
%if %{rhel} >= 6
Version:        6.4
Release:        1%{?dist}
%else
Version:        5.9
Release:        1%{?dist}
%endif
Summary:        YUM configuration for remi repository
Summary(fr):    Configuration de YUM pour le dépôt remi

Group:          System Environment/Base
License:        GPL
URL:            http://remi.collet.free.fr
Source0:        RPM-GPG-KEY-remi
Source1:        remi-el.repo
BuildRoot:      %{_tmppath}/%{name}-%{version}
BuildArchitectures: noarch

Requires:       yum
Requires:       redhat-release >= %{rhel}
Requires:       epel-release >= %{rhel}


%description
This package contains yum configuration for the "remi" RPM Repository, 
as well as the public GPG keys used to sign them.

The repository is not enabled after installation, so you must use
the --enablerepo=remi option for yum.

%description -l fr
Ce paquetage contient le fichier de configuration de YUM pour utiliser
les RPM du dépôt "remi" ainsi que la clé GPG utilisée pour les signer.

Le dépôt n'est pas activé après l'installation, vous devez donc utiliser
l'option --enablerepo=remi de yum.

%prep
%setup -c -T
sed -e "s/VERSION/%{rhel}/" %{SOURCE1} | tee remi.repo


%build
echo empty build


%install
rm -rf %{buildroot}

# PGP
%{__install} -Dp -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-remi

# YUM
%{__install} -Dp -m 644 remi.repo %{buildroot}%{_sysconfdir}/yum.repos.d/remi.repo


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/remi.repo
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-remi

%changelog
* Thu Oct  3 2013 Remi Collet <RPMS@FamilleCollet.com> - 5.9-1 and 6.4-1
- add php55 repository

* Tue Feb 12 2013 Remi Collet <RPMS@FamilleCollet.com> - 5-9 and 6-2
- add debuginfo repo
- drop failovermethod option (switch to roundrobin)

* Sat Nov 13 2010 Remi Collet <RPMS@FamilleCollet.com> - 6-1.el6.remi
- EL-6 rebuild

* Sat May 01 2010 Remi Collet <RPMS@FamilleCollet.com> - 5-8.el5.remi
- use a mirrorlist URL

* Sun May 03 2009 Remi Collet <RPMS@FamilleCollet.com> - 5-7.el5.remi
- new repo layout

* Thu Jan 22 2009 Remi Collet <RPMS@FamilleCollet.com> - 5-6.el5.remi
- fix bad $releasever in remi.repo (5Server doesn't work)

* Tue Jan 20 2009 Remi Collet <RPMS@FamilleCollet.com> - 5-5.el5.remi
- remove free.fr mirror

* Sat Feb  2 2008 Remi Collet <RPMS@FamilleCollet.com> - 5-4.el5.remi
- new mirror http://rpms.famillecollet.com/

* Sat Nov 17 2007 Remi Collet <RPMS@FamilleCollet.com> - 5-3.el5.remi
- add requires epel-release

* Sun Jun 24 2007 Remi Collet <RPMS@FamilleCollet.com> - 5-2.el5.remi
- New key (email change, same ID)

* Sat May 26 2007 Remi Collet <RPMS@FamilleCollet.com> - 5-1.el5.remi
- EL-5 rebuild

