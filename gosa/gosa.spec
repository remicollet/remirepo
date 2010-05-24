%global confdir  %{_sysconfdir}%{name}
%global apacheuser apache 
%global apachegroup apache 
%global webconf %{_sysconfdir}/httpd/conf.d/ 
%global docdir %{_datadir}/doc/gosa-%{version}

Summary:   Web Based LDAP Administration Program 
Name:      gosa
Version:   2.6.10
Release:   1
License:   GPLv2

URL:       https://oss.GONICUS.de/labs/gosa/
Source0:   http://oss.gonicus.de/pub/gosa/%{name}-core-%{version}.tar.bz2
Group:     System/Administration

Patch0:    01_fix_template_location.patch
Patch1:    02_fix_class_mapping.patch
Patch2:    03_fix_locale_location.patch
Patch3:    04_fix_online_help_location.patch

Buildarch: noarch
Requires:  httpd,php,php-ldap,php-imap,php-snmp,php-mysql,php-mbstring,ImageMagick,perl-Crypt-SmbHash
Obsoletes: gosa-ldap

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
GOsa is a combination of system-administrator and end-user web
interface, designed to handle LDAP based setups.
Provided is access to posix, shadow, samba, proxy, fax, and kerberos
accounts. It is able to manage the postfix/cyrus server combination
and can write user adapted sieve scripts.

%description -l fr
GOsa est un ensemble d'outils WEB pour administrateurs systeme et
utilisateurs finaux permettant de gerer des configurations basees sur
un annuaire LDAP.
GOsa permet de gerer des comptes de type Posix, Shadow, Samba, Proxy,
Fax et Kerberos.
Il est egalement possible de gerer des serveurs Postfix/Cyrus et 
de produire des scripts bases sur Sieve.


%package devel
Summary:   GOsa development utiles
Group:     System/Administration
Requires:  php-cli,latex2html,lyx

%description devel
This package contains a couple of tools to generate
online help, extract localisations and aid developing.


%package desktop
Summary:   Desktop integration for GOsa
Group:     System/Administration
BuildRequires:  desktop-file-utils
Requires:  firefox

%description desktop
This package includes a menu definition for your
desktop environment.


%package schema
Summary:   Schema Definitions for the GOSA package
Group:     System/Administration
Requires:  openldap-servers	

%description schema
Contains the Schema definition files for the GOSA admin package.


%package help-en
Summary:   English online manual for GOSA package
Group:     System/Administration
Requires:  gosa = %{version}-%{release}

%description help-en
English online manual page for GOSA package


%package help-de
Summary:   German localized online manual for GOSA package
Group:     System/Administration
Requires:  gosa = %{version}-%{release}

%description help-de
German localized online manual page for GOSA package


%package help-fr
Summary:   French localized online manual for GOSA package
Group:     System/Administration
Requires:  gosa = %{version}-%{release}

%description help-fr
French localized online manual page for GOSA package


%package help-nl
Summary:   Dutch localized online manual for GOSA package
Group:    System/Administration
Requires:  gosa = %{version}-%{release}

%description help-nl
Dutch localized online manual page for GOSA package


%package help-es
Summary:   Spain localized online manual for GOSA package
Group:    System/Administration
Requires:  gosa = %{version}-%{release}

%description help-es
Spain localized online manual page for GOSA package


%prep
%setup -q -n %{name}-core-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1


%build
# nothing to build


%install
# Create buildroot
mkdir -p %{buildroot}%{_datadir}/gosa

# Create files for temporary stuff
for i in compile config cache; do
  mkdir -p %{buildroot}/var/spool/gosa/$i
done
mkdir -p %{buildroot}/var/cache/gosa

# Copy
DIRS="doc ihtml plugins html include locale setup"
for i in $DIRS; do \
  cp -a $i %{buildroot}%{_datadir}/gosa/$i ; \
done

# Copy files for gosa
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/gosa
mkdir -p %{buildroot}%{_datadir}/doc/gosa
mkdir -p %{buildroot}%{webconf}

touch %{buildroot}%{_sysconfdir}/gosa/gosa.secrets
install -p contrib/gosa.conf		%{buildroot}%{_datadir}/doc/gosa
install -p update-gosa 			%{buildroot}%{_sbindir}
install -p bin/gosa-encrypt-passwords 	%{buildroot}%{_sbindir}
install -p debian/gosa-apache.conf 	%{buildroot}%{webconf}
install -p contrib/shells 		%{buildroot}%{_sysconfdir}/gosa
install -p contrib/encodings 		%{buildroot}%{_sysconfdir}/gosa
install -p contrib/openldap/slapd.conf 	%{buildroot}%{_datadir}/doc/gosa/slapd.conf-example

# Cleanup manual dirs
for i in admin ; do \
  rm -rf %{buildroot}%{_datadir}/gosa/doc/$i ; \
done

# Remove (some) unneeded files
for i in gen_locale.sh gen_online_help.sh gen_function_list.php update.sh; do \
 rm -rf %{buildroot}%{_datadir}/gosa/$i ; \
done

# Cleanup lyx warnings
find %{buildroot}%{_datadir}/gosa -name WARNINGS |xargs rm

# Cleanup guide
rm -rf %{buildroot}%{_datadir}/gosa/doc/guide/user/*/lyx-source

# Copy default config
mkdir -p %{buildroot}%{confdir}
mkdir -p %{buildroot}%{webconf}

# Copy file for gosa-schema
mkdir -p %{buildroot}%{_sysconfdir}/openldap/schema/gosa

install -p contrib/openldap/*.schema %{buildroot}%{_sysconfdir}/openldap/schema/gosa

# Copy files for gosa-dev
mkdir -p %{buildroot}/usr/bin
install -p update-locale %{buildroot}/usr/bin
install -p update-online-help %{buildroot}/usr/bin
install -p update-pdf-help %{buildroot}/usr/bin
install -p dh-make-gosa %{buildroot}/usr/bin

# Copy files for desktop
mkdir -p %{buildroot}%{_sysconfdir}/gosa
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_mandir}/man5/

install -p contrib/desktoprc 		%{buildroot}%{_sysconfdir}/gosa
install -p contrib/gosa 		%{buildroot}/usr/bin
install -p debian/gosa.xpm 		%{buildroot}%{_datadir}/pixmaps
install -p debian/gosa-16.xpm 		%{buildroot}%{_datadir}/pixmaps
desktop-file-install --dir=%{buildroot}%{_datadir}/applications	debian/gosa-desktop.desktop 

# Copy manpages
for x in update-gosa.1 dh-make-gosa.1 update-locale.1 update-online-help.1 update-pdf-help.1 gosa-encrypt-passwords.1 contrib/gosa.1
do
   install -p $x %{buildroot}%{_mandir}/man1/
done
install -p contrib/gosa.conf.5 %{buildroot}%{_mandir}/man5/


%clean
rm -rf %{buildroot}


%pre
# Cleanup compile dir on updates, always exit cleanly even on errors
[ -d /var/spool/gosa ] && rm -rf /var/spool/gosa/* ; exit 0


%post
%{_sbindir}/update-gosa


%post desktop
update-desktop-database &> /dev/null || :


%postun desktop 
update-desktop-database &> /dev/null || :


%files
%defattr(-,root,root)
%doc %attr(-,root,root) AUTHORS README README.safemode Changelog COPYING INSTALL FAQ CODING
%config %attr(-,root,root) %{_datadir}/doc/gosa/gosa.conf
#%attr(-,root,root) /contrib/openldap
%config %attr(-,root,root) %{_datadir}/doc/gosa/slapd.conf-example
%attr(755,root,root) %{_sbindir}/update-gosa
%attr(755,root,root) %{_mandir}/man1/gosa-encrypt-passwords.1.gz
%attr(755,root,root) %{_mandir}/man1/update-gosa.1.gz
%attr(755,root,root) %{_mandir}/man5/gosa.conf.5.gz
%attr(644,root,root) %{_sysconfdir}/gosa/shells
%attr(644,root,root) %{_sysconfdir}/gosa/encodings
%attr(755,root,root) %{_sbindir}/gosa-encrypt-passwords
%config(noreplace) %attr(0644,root,root) %{webconf}/gosa-apache.conf
%attr(0700, %{apacheuser}, %{apachegroup}) /var/spool/gosa
%attr(0755, root,root) %{_datadir}/gosa
#%attr(0755, root,root) %{_datadir}/gosa/html
#%attr(0755, root,root) %{_datadir}/gosa/ihtml
#%attr(0755, root,root) %{_datadir}/gosa/include
#%attr(0755, root,root) %{_datadir}/gosa/locale
#%attr(0755, root,root) %{_datadir}/gosa/plugins
#%attr(0755, root,root) %{_datadir}/gosa/setup
%attr(0755, root,root) %{_datadir}/gosa/doc/core/guide.xml
%attr(0755, root,root) /var/cache/gosa
%attr(0700, root,root) %{_sysconfdir}/gosa/gosa.secrets

########################

%files devel
%defattr(-,root,root)
/usr/bin
%attr(755,root,root) %{_mandir}/man1/dh-make-gosa.1.gz
%attr(755,root,root) %{_mandir}/man1/update-locale.1.gz
%attr(755,root,root) %{_mandir}/man1/update-online-help.1.gz
%attr(755,root,root) %{_mandir}/man1/update-pdf-help.1.gz

########################

%files desktop
%defattr(-,root,root)
%{_sysconfdir}/gosa
/usr/bin
%{_datadir}/pixmaps
%{_datadir}/applications
%attr(755,root,root) %{_mandir}/man1/gosa.1.gz

########################

%files schema
%defattr(-,root,root)
%doc COPYING AUTHORS README contrib/openldap
%{_sysconfdir}/openldap/schema/gosa

########################

%files help-en
%defattr(-,root,root)
%{_datadir}/gosa/doc/core/en

########################

%files help-de
%defattr(-,root,root)
%{_datadir}/gosa/doc/core/de

########################

%files help-fr
%defattr(-,root,root)
%{_datadir}/gosa/doc/core/fr

########################

%files help-nl
%defattr(-,root,root)
%{_datadir}/gosa/doc/core/nl

########################

%files help-es
%defattr(-,root,root)
%{_datadir}/gosa/doc/core/es

########################

%changelog
* Sat May 23 2010 Remi Collet <Fedora@FamilleCollet.com> - 2.6.10-1
- work on fedora spec

* Thu May 14 2010 Olivier BONHOMME <obonhomme@nerim.net>
- Corrected errors when building RPM and plugins where not on right
  place Closes #957 and #970

* Fri Nov 17 2008 Stefan Japes <japes@GONICUS.de>
- First build of GOsa 2.6 as an RPM, should work on SuSE and RedHat


