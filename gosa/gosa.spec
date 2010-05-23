# Some sort of "detection" of suse
%{?suse_version:%define suse 1}
%{!?suse_version:%define suse 0}

# Define Packagename, e.g.:
# rpmbuild --rebuild --define 'sourcename gosa' gosa.srpm
%{!?sourcename:%define sourcename %{name}-%{version}}

#
# Distribution
#
Summary: 		Web Based LDAP Administration Program 
Name:			gosa
Version: 		2.6.10
Release:		1
License: 		GPL
Source: 		ftp://oss.GONICUS.de/pub/gosa/%{sourcename}.tar.bz2
URL: 			https://oss.GONICUS.de/labs/gosa/
Group: 			System/Administration
Vendor:			GONICUS GmbH
Packager:		Stefan Japes <japes@GONICUS.de>
Buildarch: 		noarch
Patch:			01_fix_template_location.patch
Patch1:			02_fix_class_mapping.patch
Patch2:			03_fix_locale_location.patch
Patch3:			04_fix_online_help_location.patch
%if %{suse}
Requires:		apache2,apache2-mod_php5,php5,php5-gd,php5-ldap,php5-mcrypt,php5-mysql,php5-imap,php5-iconv,php5-hash,php5-posix,php5-mbstring,php5-gettext,ImageMagick,gettext-tools
%else
Requires: 		httpd,php,php-ldap,php-imap,php-snmp,php-mysql,php-mbstring,ImageMagick,perl-Crypt-SmbHash
%endif
BuildRoot: 		%{_tmppath}/%{name}-%{version}-root
BuildArch:		noarch

########################

%define confdir 	/etc/%{name}

%if %{suse}
	%{echo:Building SuSE rpm}
	%define apacheuser wwwrun
	%define apachegroup root
	%define webconf	/etc/apache2/conf.d/
	%define docdir /usr/share/doc/packages/gosa
%else
	%{echo:Building other rpm}
	%define apacheuser apache 
	%define apachegroup apache 
	%define webconf	/etc/httpd/conf.d/	
	%define docdir /usr/share/doc/gosa-%{version}
%endif

%description
GOsa is a combination of system-administrator and end-user web
interface, designed to handle LDAP based setups.
Provided is access to posix, shadow, samba, proxy, fax, and kerberos
accounts. It is able to manage the postfix/cyrus server combination
and can write user adapted sieve scripts.

########################

%package dev
Group:                  System/Administration
Summary:                GOsa development utiles
%if %{suse}
Requires:               lyx
%else
Requires:               php-cli,latex2html,lyx
%endif
Obsoletes:              gosa-ldap

%description dev
This package contains a couple of tools to generate
online help, extract localisations and aid developing.

########################

%package desktop
Group:                  System/Administration
Summary:                Desktop integration for GOsa
%if %{suse}
Requires:               firefox
%else
Requires:               firefox
%endif
Obsoletes:              gosa-ldap

%description desktop
This package includes a menu definition for your
desktop environment.

########################

%package schema
Group: 			System/Administration
Summary: 		Schema Definitions for the GOSA package
%if %{suse}
Requires:		gosa >= %{version}
%else
Requires:		gosa >= %{version}
%endif
Obsoletes:		gosa-ldap

%description schema
Contains the Schema definition files for the GOSA admin package.

########################

%package help-en
Group: 			System/Administration
Summary: 		English online manual for GOSA package
Requires:		gosa >= %{version}

%description help-en
English online manual page for GOSA package

########################

%package help-de
Group: 			System/Administration
Summary: 		German localized online manual for GOSA package
Requires:		gosa >= %{version}

%description help-de
German localized online manual page for GOSA package

########################

%package help-fr
Group: 			System/Administration
Summary: 		French localized online manual for GOSA package
Requires:		gosa >= %{version}

%description help-fr
French localized online manual page for GOSA package

########################

%package help-nl
Group: 			System/Administration
Summary: 		Dutch localized online manual for GOSA package
Requires:		gosa >= %{version}

%description help-nl
Dutch localized online manual page for GOSA package

########################

%package help-es
Group: 			System/Administration
Summary: 		Spain localized online manual for GOSA package
Requires:		gosa >= %{version}

%description help-es
Spain localized online manual page for GOSA package

########################

%prep
%setup -q -n %{sourcename}
%patch -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

find . -depth -name CVS -type d | xargs rm -rf

########################

%build

########################

%install
# Create buildroot
mkdir -p %{buildroot}/usr/share/gosa

# Create files for temporary stuff
for i in compile config cache; do \
  mkdir -p %{buildroot}/var/spool/gosa/$i ; \
done
mkdir -p %{buildroot}/var/cache/gosa

# Copy
DIRS="doc ihtml plugins html include locale setup"
echo `pwd`
for i in $DIRS; do \
  cp -ua $i %{buildroot}/usr/share/gosa/$i ; \
done

# Copy files for gosa
mkdir -p %{buildroot}/usr/sbin
mkdir -p %{buildroot}/etc/gosa
mkdir -p %{buildroot}/usr/share/doc/gosa
mkdir -p %{buildroot}%{webconf}

touch %{buildroot}/etc/gosa/gosa.secrets
mv contrib/gosa.conf		%{buildroot}/usr/share/doc/gosa
mv update-gosa 			%{buildroot}/usr/sbin
mv bin/gosa-encrypt-passwords 	%{buildroot}/usr/sbin
mv debian/gosa-apache.conf 	%{buildroot}%{webconf}
mv contrib/shells 		%{buildroot}/etc/gosa
mv contrib/encodings 		%{buildroot}/etc/gosa
mv contrib/openldap/slapd.conf 	%{buildroot}/usr/share/doc/gosa/slapd.conf-example
mv -f doc manual

# Cleanup manual dirs
for i in admin ; do \
  rm -rf %{buildroot}/usr/share/gosa/doc/$i ; \
done

# Remove (some) unneeded files
for i in gen_locale.sh gen_online_help.sh gen_function_list.php update.sh; do \
 rm -rf %{buildroot}/usr/share/gosa/$i ; \
done

# Cleanup lyx warnings
find %{buildroot}/usr/share/gosa -name WARNINGS |xargs rm

# Cleanup guide
rm -rf %{buildroot}/usr/share/gosa/doc/guide/user/*/lyx-source

# Copy default config
mkdir -p %{buildroot}%{confdir}
mkdir -p %{buildroot}%{webconf}

# Copy file for gosa-schema
mkdir -p %{buildroot}/etc/openldap/schema/gosa

mv contrib/openldap/*.schema %{buildroot}/etc/openldap/schema/gosa

# Copy files for gosa-dev
mkdir -p %{buildroot}/usr/bin
mv update-locale %{buildroot}/usr/bin
mv update-online-help %{buildroot}/usr/bin
mv update-pdf-help %{buildroot}/usr/bin
mv dh-make-gosa %{buildroot}/usr/bin

# Copy files for desktop
mkdir -p %{buildroot}/etc/gosa
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/sbin
mkdir -p %{buildroot}/usr/share/pixmaps
mkdir -p %{buildroot}/usr/share/applications
mkdir -p %{buildroot}/usr/share/man/man1/
mkdir -p %{buildroot}/usr/share/man/man5/

mv contrib/desktoprc 		%{buildroot}/etc/gosa
mv contrib/gosa 		%{buildroot}/usr/bin
mv debian/gosa.xpm 		%{buildroot}/usr/share/pixmaps
mv debian/gosa-16.xpm 		%{buildroot}/usr/share/pixmaps
mv debian/gosa-desktop.desktop 	%{buildroot}/usr/share/applications

# Gzip manpages from source
for x in update-gosa.1 dh-make-gosa.1 update-locale.1 update-online-help.1 update-pdf-help.1 gosa-encrypt-passwords.1
do
	gzip $x
done

%if %{suse}
	sed -i 's#/usr/bin/php#/usr/bin/php5#' %{buildroot}/usr/sbin/update-gosa
	sed -i 's#/usr/bin/php#/usr/bin/php5#' %{buildroot}/usr/sbin/gosa-encrypt-passwords
	cat <<-EOF >> %{buildroot}%{webconf}/gosa-apache.conf
	
	<Directory /usr/share/gosa/html>
	    Options None
	    AllowOverride None
	    Order deny,allow
	    Allow from all
	</Directory>
	EOF
%endif

# Copy manpages
mv ./*.1.gz 			%{buildroot}/usr/share/man/man1/
gzip -c contrib/gosa.1 > contrib/gosa.1.gz
mv contrib/gosa.1.gz 		%{buildroot}/usr/share/man/man1/
gzip -c contrib/gosa.conf.5 > contrib/gosa.conf.5.gz
mv contrib/gosa.conf.5.gz 		%{buildroot}/usr/share/man/man5/

mkdir -p %{buildroot}/usr/share/doc/gosa-%{version}
rm -rf %{buildroot}/usr/share/gosa/contrib

########################

%clean
rm -rf %{buildroot}

########################

%post
/usr/sbin/update-gosa

########################

%pre
# Cleanup compile dir on updates, always exit cleanly even on errors
[ -d /var/spool/gosa ] && rm -rf /var/spool/gosa/* ; exit 0

########################

%postun
# Remove temporary files, just to be sure
[ -d /var/spool/gosa ] && rm -rf /var/spool/gosa ; exit 0
[ -d /usr/share/gosa ] && rm -rf /usr/share/gosa ; exit 0

########################

%files
%defattr(-,root,root)
%doc %attr(-,root,root) AUTHORS README README.safemode Changelog COPYING INSTALL FAQ CODING
%config %attr(-,root,root) /usr/share/doc/gosa/gosa.conf
#%attr(-,root,root) /contrib/openldap
%config %attr(-,root,root) /usr/share/doc/gosa/slapd.conf-example
%attr(755,root,root) /usr/sbin/update-gosa
%attr(755,root,root) /usr/share/man/man1/gosa-encrypt-passwords.1.gz
%attr(755,root,root) /usr/share/man/man1/update-gosa.1.gz
%attr(755,root,root) /usr/share/man/man5/gosa.conf.5.gz
%attr(644,root,root) /etc/gosa/shells
%attr(644,root,root) /etc/gosa/encodings
%attr(755,root,root) /usr/sbin/gosa-encrypt-passwords
%config(noreplace) %attr(0644,root,root) %{webconf}/gosa-apache.conf
%attr(0700, %{apacheuser}, %{apachegroup}) /var/spool/gosa
%attr(0755, root,root) /usr/share/gosa
#%attr(0755, root,root) /usr/share/gosa/html
#%attr(0755, root,root) /usr/share/gosa/ihtml
#%attr(0755, root,root) /usr/share/gosa/include
#%attr(0755, root,root) /usr/share/gosa/locale
#%attr(0755, root,root) /usr/share/gosa/plugins
#%attr(0755, root,root) /usr/share/gosa/setup
%attr(0755, root,root) /usr/share/gosa/doc/core/guide.xml
%attr(0755, root,root) /var/cache/gosa
%attr(0700, root,root) /etc/gosa/gosa.secrets

########################

%files dev
%defattr(-,root,root)
/usr/bin
%attr(755,root,root) /usr/share/man/man1/dh-make-gosa.1.gz
%attr(755,root,root) /usr/share/man/man1/update-locale.1.gz
%attr(755,root,root) /usr/share/man/man1/update-online-help.1.gz
%attr(755,root,root) /usr/share/man/man1/update-pdf-help.1.gz

########################

%files desktop
%defattr(-,root,root)
/etc/gosa
/usr/bin
/usr/share/pixmaps
/usr/share/applications
%attr(755,root,root) /usr/share/man/man1/gosa.1.gz

########################

%files schema
%defattr(-,root,root)
%doc COPYING AUTHORS README contrib/openldap
/etc/openldap/schema/gosa

########################

%files help-en
%defattr(-,root,root)
/usr/share/gosa/doc/core/en

########################

%files help-de
%defattr(-,root,root)
/usr/share/gosa/doc/core/de

########################

%files help-fr
%defattr(-,root,root)
/usr/share/gosa/doc/core/fr

########################

%files help-nl
%defattr(-,root,root)
/usr/share/gosa/doc/core/nl

########################

%files help-es
%defattr(-,root,root)
/usr/share/gosa/doc/core/es

########################

%changelog
* Fri Nov 17 2008 Stefan Japes <japes@GONICUS.de>
- First build of GOsa 2.6 as an RPM, should work on SuSE and RedHat
* Thu May 14 2010 Olivier BONHOMME <obonhomme@nerim.net>
- Corrected errors when building RPM and plugins where not on right
  place Closes #957 and #970
