# remirepo/fedora spec file for php-horde-wicked
#
# Copyright (c) 2014-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    wicked
%global pear_channel pear.horde.org
# all tests are ignored
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-horde-wicked
Version:        2.0.6
Release:        1%{?dist}
Summary:        Wiki application

Group:          Development/Libraries
License:        GPLv2
URL:            http://www.horde.org/apps/wicked
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  php-pear(%{pear_channel}/Horde_Role) >= 1.0.0
%if %{with_tests}
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}

# Web stuff (as we provide httpd configuration)
Requires:       mod_php
Requires:       httpd
# From package.xml, required
Requires:       php(language) >= 5.3.0
Requires:       php-gettext
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/horde) >= 5.0.0
Requires:       php-pear(%{pear_channel}/horde) <  6.0.0
Requires:       php-pear(%{pear_channel}/Horde_Auth) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Auth) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Autoloader) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Autoloader) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Core) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Core) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Db) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Db) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Form) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Form) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Http) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Http) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Lock) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Lock) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime_Viewer) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime_Viewer) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Notification) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Notification) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Perms) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Perms) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Prefs) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Prefs) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Rpc) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Rpc) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Diff) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Diff) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Url) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Url) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Vfs) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Vfs) <  3.0.0
Requires:       php-pear(Text_Wiki) >= 1.2.0
# From package.xml, optional
Requires:       php-pear(Text_Figlet)
# Optional and not yet available:
#   Text_Wiki_Creole, Text_Wiki_Mediawiki, Text_Wiki_Tiki
# From phpcompatinfo report for version 2.0.1
Requires:       php-date
Requires:       php-pcre
Requires:       php-spl

Provides:       php-pear(%{pear_channel}/wicked) = %{version}
Provides:       php-compposer(horde/wicked) = %{version}
Obsoletes:      wicked < 2
Provides:       wicked = %{version}


%description
Wicked is a wiki application for Horde.


%prep
%setup -q -c

cat <<EOF | tee httpd.conf
<DirectoryMatch %{pear_hordedir}/%{pear_name}/(config|lib|locale|templates)>
     Deny from all
</DirectoryMatch>

<Directory %{pear_hordedir}/%{pear_name}>
  <IfModule mod_rewrite.c>
    RewriteEngine On
      RewriteCond   %%{REQUEST_FILENAME}  !-d
      RewriteCond   %%{REQUEST_FILENAME}  !-f
      RewriteRule   ^([A-Za-z0-9].*)$ display.php?page=$1 [QSA]
  </IfModule>
</Directory>
EOF

cd %{pear_name}-%{version}
# Don't install .po and .pot files
# Remove checksum for .mo, as we regenerate them
sed -e '/%{pear_name}.po/d' \
    -e '/htaccess/d' \
    -e '/%{pear_name}.mo/s/md5sum=.*name=/name=/' \
    ../package.xml >%{name}.xml
touch -r ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.

# Regenerate the locales
for po in $(find locale -name \*.po)
do
   msgfmt $po -o $(dirname $po)/$(basename $po .po).mo
done


%install
cd %{pear_name}-%{version}
rm -rf %{buildroot}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}

# Install Apache configuration
install -Dpm 0644 ../httpd.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Move configuration to /etc
mkdir -p %{buildroot}%{_sysconfdir}/horde
mv %{buildroot}%{pear_hordedir}/%{pear_name}/config \
   %{buildroot}%{_sysconfdir}/horde/%{pear_name}
ln -s %{_sysconfdir}/horde/%{pear_name} %{buildroot}%{pear_hordedir}/%{pear_name}/config

# Locales
for loc in locale/?? locale/??_??
do
    lang=$(basename $loc)
    echo "%%lang(${lang%_*}) %{pear_hordedir}/%{pear_name}/$loc"
done | tee ../%{pear_name}.lang

# fix shebang and include
sed -e 's:#!/usr/bin/env php:#!%{_bindir}/php:' \
    -e "s:__DIR__ . '/../:'%{pear_hordedir}/%{pear_name}/:" \
    -i  %{buildroot}%{_bindir}/wicke*


%check
%if %{with_tests}
cd %{pear_name}-%{version}/test/Wicked

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit . || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit . || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose .
# remirepo:2
fi
exit $ret
%endif


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.horde.org/%{pear_name} >/dev/null || :
fi


%files -f %{pear_name}.lang
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%attr(0770,apache,apache) %dir %{_sysconfdir}/horde/%{pear_name}
%attr(0640,apache,apache) %config %{_sysconfdir}/horde/%{pear_name}/*.dist
%attr(0660,apache,apache) %config %{_sysconfdir}/horde/%{pear_name}/*.xml
%{pear_xmldir}/%{name}.xml
%{pear_testdir}/wicked
%{_bindir}/wicked
%{_bindir}/wicked-convert-to-utf8
%{_bindir}/wicked-mail-filter
%dir %{pear_hordedir}/%{pear_name}
%dir %{pear_hordedir}/%{pear_name}/locale
%{pear_hordedir}/%{pear_name}/*.php
%{pear_hordedir}/%{pear_name}/config
%{pear_hordedir}/%{pear_name}/lib
%{pear_hordedir}/%{pear_name}/data
%{pear_hordedir}/%{pear_name}/js
%{pear_hordedir}/%{pear_name}/migration
%{pear_hordedir}/%{pear_name}/templates
%{pear_hordedir}/%{pear_name}/themes


%changelog
* Sat Jul 02 2016 Remi Collet <remi@fedoraproject.org> - 2.0.6-1
- Update to 2.0.6

* Mon Mar 21 2016 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- Update to 2.0.5

* Sat Aug 01 2015 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4

* Wed Dec 03 2014 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3

* Wed Oct 29 2014 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2

* Sat May 17 2014 Remi Collet <remi@fedoraproject.org> - 2.0.1-2
- fix from review #1087769
- explicitly requires httpd + mod_php
- preserve timestamp of package.xml

* Tue Apr 15 2014 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Initial package, version 2.0.1
