%global confdir  %{_sysconfdir}/%{name}
%global apacheuser apache 
%global apachegroup apache 
%global webconf %{_sysconfdir}/httpd/conf.d/ 


Summary:   Web Based LDAP Administration Program 
Name:      gosa
Version:   2.6.10
Release:   1
License:   GPLv2

URL:       https://oss.GONICUS.de/labs/gosa/
Source0:   http://oss.gonicus.de/pub/gosa/%{name}-core-%{version}.tar.bz2
Group:     Applications/System

Patch0:    01_fix_template_location.patch
Patch1:    02_fix_class_mapping.patch
Patch2:    03_fix_locale_location.patch
Patch3:    04_fix_online_help_location.patch

Buildarch: noarch
Requires:  php >= 5.2.0
Requires:  php-ldap php-imap php-snmp php-mysql php-mbstring
Requires:  ImageMagick
Requires:  perl(Crypt::SmbHash)

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


%description
GOsa is a combination of system-administrator and end-user web
interface, designed to handle LDAP based setups.
Provided is access to posix, shadow, samba, proxy, fax, and kerberos
accounts. It is able to manage the postfix/cyrus server combination
and can write user adapted sieve scripts.

%description -l fr
GOsa est un ensemble d'outils WEB pour administrateurs système et
utilisateurs finaux permettant de gérer des configurations basées sur
un annuaire LDAP.
GOsa permet de gérer des comptes de type Posix, Shadow, Samba, Proxy,
Fax et Kerberos.
Il est également possible de gérer des serveurs Postfix/Cyrus et 
de produire des scripts bases sur Sieve.


%package devel
Summary:   GOsa development utiles
Group:     Applications/System
Requires:  php-cli,latex2html,lyx

%description devel
This package contains a couple of tools to generate
online help, extract localizations, and aid developing.


%package desktop
Summary:   Desktop integration for GOsa
Group:     Applications/System
BuildRequires:  desktop-file-utils
Requires:  firefox

%description desktop
This package includes a menu definition for your
desktop environment.


%package schema
Summary:   Schema Definitions for the GOSA package
Group:     Applications/System
Requires:  openldap-servers 

%description schema
Contains the Schema definition files for the GOSA admin package.


%package help-en
Summary:   English online manual for GOSA package
Group:     Applications/System
Requires:  gosa = %{version}-%{release}

%description help-en
English online manual page for GOSA package


%package help-de
Summary:   German localized online manual for GOSA package
Group:     Applications/System
Requires:  gosa = %{version}-%{release}

%description help-de
German localized online manual page for GOSA package


%package help-fr
Summary:   French localized online manual for GOSA package
Group:     Applications/System
Requires:  gosa = %{version}-%{release}

%description help-fr
French localized online manual page for GOSA package


%package help-nl
Summary:   Dutch localized online manual for GOSA package
Group:     Applications/System
Requires:  gosa = %{version}-%{release}

%description help-nl
Dutch localized online manual page for GOSA package


%package help-es
Summary:   Spain localized online manual for GOSA package
Group:     Applications/System
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
mkdir -p %{buildroot}%{confdir}
mkdir -p %{buildroot}%{webconf}

touch %{buildroot}%{confdir}/gosa.secrets
install -p -m 755 update-gosa                 %{buildroot}%{_sbindir}
install -p -m 755 bin/gosa-encrypt-passwords  %{buildroot}%{_sbindir}
install -p -m 755 bin/mkntpasswd              %{buildroot}%{_sbindir}
install -p -m 644 debian/gosa-apache.conf     %{buildroot}%{webconf}
install -p -m 644 contrib/shells              %{buildroot}%{confdir}
install -p -m 644 contrib/encodings           %{buildroot}%{confdir}

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

# Copy files for gosa-devel
mkdir -p %{buildroot}%{_bindir}
install -p update-locale %{buildroot}%{_bindir}
install -p update-online-help %{buildroot}%{_bindir}
install -p update-pdf-help %{buildroot}%{_bindir}
install -p dh-make-gosa %{buildroot}%{_bindir}

# Copy files for desktop
mkdir -p %{buildroot}%{confdir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_mandir}/man5/

install -p -m 644 contrib/desktoprc  %{buildroot}%{confdir}
install -p -m 755 contrib/gosa       %{buildroot}%{_bindir}
install -p -m 644 debian/gosa.xpm    %{buildroot}%{_datadir}/pixmaps
install -p -m 644 debian/gosa-16.xpm %{buildroot}%{_datadir}/pixmaps
desktop-file-install \
    --dir=%{buildroot}%{_datadir}/applications \
    debian/gosa-desktop.desktop 

# Copy manpages
for x in update-gosa.1 dh-make-gosa.1 update-locale.1 update-online-help.1 update-pdf-help.1 gosa-encrypt-passwords.1 contrib/gosa.1
do
   install -p -m 644  $x %{buildroot}%{_mandir}/man1/
done
install -p -m 644 contrib/gosa.conf.5 %{buildroot}%{_mandir}/man5/


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
%defattr(-,root,root,-)
%doc AUTHORS README README.safemode Changelog COPYING INSTALL FAQ CODING
%doc contrib/gosa.conf contrib/openldap/slapd.conf
%dir %{confdir}
%config(noreplace) %{confdir}/gosa.secrets
%config(noreplace) %{confdir}/shells
%config(noreplace) %{confdir}/encodings
%config(noreplace) %{webconf}/gosa-apache.conf
%{_sbindir}/update-gosa
%{_sbindir}/gosa-encrypt-passwords
%{_sbindir}/mkntpasswd
%{_mandir}/man1/update-gosa.1*
%{_mandir}/man1/gosa-encrypt-passwords.1*
%{_mandir}/man5/gosa.conf.5*
%attr(0700,%{apacheuser},%{apachegroup}) /var/spool/gosa
%dir %{_datadir}/gosa
%{_datadir}/gosa/html
%{_datadir}/gosa/ihtml
%{_datadir}/gosa/include
%{_datadir}/gosa/locale
%{_datadir}/gosa/plugins
%{_datadir}/gosa/setup
%dir %{_datadir}/gosa/doc
%dir %{_datadir}/gosa/doc/core
%exclude %{_datadir}/gosa/doc/guide.xml
%{_datadir}/gosa/doc/core/guide.xml
/var/cache/gosa

########################

%files devel
%defattr(-,root,root)
%{_bindir}/dh-make-gosa
%{_bindir}/update-locale
%{_bindir}/update-online-help
%{_bindir}/update-pdf-help
%{_mandir}/man1/dh-make-gosa.1*
%{_mandir}/man1/update-locale.1*
%{_mandir}/man1/update-online-help.1*
%{_mandir}/man1/update-pdf-help.1*

########################

%files desktop
%defattr(-,root,root)
%dir %{confdir}
%config(noreplace) %{confdir}/desktoprc
%{_bindir}/gosa
%{_datadir}/pixmaps/gosa*
%{_datadir}/applications/gosa*
%{_mandir}/man1/gosa.1*

########################

%files schema
%defattr(-,root,root)
%doc COPYING AUTHORS README contrib/openldap
%{_sysconfdir}/openldap/schema/gosa

########################

%files help-en
%defattr(-,root,root)
%{_datadir}/gosa/doc/core/en
#%{_datadir}/gosa/doc/plugins/*/en

########################

%files help-de
%defattr(-,root,root)
%{_datadir}/gosa/doc/core/de
#%{_datadir}/gosa/doc/plugins/*/de

########################

%files help-fr
%defattr(-,root,root)
%{_datadir}/gosa/doc/core/fr
#%{_datadir}/gosa/doc/plugins/*/fr

########################

%files help-nl
%defattr(-,root,root)
%{_datadir}/gosa/doc/core/nl
#%{_datadir}/gosa/doc/plugins/*/nl

########################

%files help-es
%defattr(-,root,root)
%{_datadir}/gosa/doc/core/es
#%{_datadir}/gosa/doc/plugins/*/es

########################

%changelog
* Sat May 23 2010 Remi Collet <Fedora@FamilleCollet.com> - 2.6.10-1
- work on fedora spec

* Thu May 14 2010 Olivier BONHOMME <obonhomme@nerim.net>
- Corrected errors when building RPM and plugins where not on right
  place Closes #957 and #970

* Fri Nov 17 2008 Stefan Japes <japes@GONICUS.de>
- First build of GOsa 2.6 as an RPM, should work on SuSE and RedHat

