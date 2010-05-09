Name:           remi-release
Version:        4
Release:        7%{?dist}
Summary:        YUM configuration for remi repository
Summary(fr):	Configuration de YUM pour le dépôt remi

Group:          System Environment/Base
License:        GPL
URL:            http://remi.collet.free.fr
Source0:        RPM-GPG-KEY-remi
Source1:	remi-el.repo
BuildRoot:      %{_tmppath}/%{name}-%{version}
BuildArchitectures: noarch

Requires:       redhat-release >= %{rhel}
Requires:       epel-release >= %{rhel}

%description
This package contains yum configuration for the "remi" RPM Repository, 
as well as the public GPG keys used to sign them.

The repository is not enabled after installation, so you must use
the --enablerepo=remi option for yum.

It also provides up2date configuration.

%description -l fr
Ce paquetage contient le fichier de configuration de YUM pour utiliser
les RPM du dépôt "remi" ainsi que la clé GPG utilisée pour les signer.

Le dépôt n'est pas activé après l'installation, vous devez donc utiliser
l'option --enablerepo=remi de yum.

Il fournit également la configuration de up2date.

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

%post
echo "# remi repo -- added by remi-release " \
    >> %{_sysconfdir}/sysconfig/rhn/sources
echo "yum remi http://rpms.famillecollet.com/enterprise/%{version}/remi/\$ARCH" \
    >> %{_sysconfdir}/sysconfig/rhn/sources

%postun 
sed -i '/^yum\ remi/d' %{_sysconfdir}/sysconfig/rhn/sources
sed -i '/^\#\ remi\ repo\ /d' %{_sysconfdir}/sysconfig/rhn/sources


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/remi.repo
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-remi

%changelog
* Sun May 03 2009 Remi Collet <RPMS@FamilleCollet.com> - 4-7.el5.remi
- new repo layout

* Tue Jan 20 2009 Remi Collet <RPMS@FamilleCollet.com> - 4-5.el4.remi
- remove free.fr mirror

* Sat Feb  2 2008 Remi Collet <RPMS@FamilleCollet.com> - 4-4.el4.remi
- new mirror http://rpms.famillecollet.com/

* Sat Nov 17 2007 Remi Collet <RPMS@FamilleCollet.com> - 4-3.el4.remi
- add requires epel-release

* Sun Jun 24 2007 Remi Collet <RPMS@FamilleCollet.com> - 4-2.el4.remi
- New key (email change, same ID)

* Sat May 26 2007 Remi Collet <RPMS@FamilleCollet.com> - 4-1.el4.remi
- EL-4 rebuild

