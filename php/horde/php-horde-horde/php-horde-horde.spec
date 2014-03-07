# spec file for php-horde-horde
#
# Copyright (c) 2012-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    horde
%global pear_channel pear.horde.org

Name:           php-horde-horde
Version:        5.1.6
Release:        1%{?dist}
Summary:        Horde Application Framework

Group:          Development/Libraries
License:        LGPLv2
URL:            http://www.horde.org/apps/horde
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz
Source2:        horde.conf

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  php-pear(%{pear_channel}/Horde_Role) >= 1.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
# Web stuff
Requires:       mod_php
Requires:       httpd
Requires:       prototype-httpd
Requires:       scriptaculous-httpd
Requires:       syntaxhighlighter-httpd
Requires:       ckeditor
# PHP stuff
Requires:       php(language) >= 5.3.0
Requires:       php-calendar
Requires:       php-date
Requires:       php-fileinfo
Requires:       php-gettext
Requires:       php-hash
Requires:       php-iconv
Requires:       php-libxml
Requires:       php-pcre
Requires:       php-posix
Requires:       php-session
Requires:       php-soap
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Role) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Alarm) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Alarm) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Argv) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Argv) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Auth) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Auth) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Autoloader) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Autoloader) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Browser) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Browser) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Core) >= 2.11.0
Requires:       php-pear(%{pear_channel}/Horde_Core) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Feed) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Feed) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Form) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Form) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Group) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Group) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Http) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Http) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Image) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Image) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_LoginTasks) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_LoginTasks) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Nls) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Nls) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Perms) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Perms) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Prefs) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Prefs) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Rpc) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Rpc) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Serialize) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Serialize) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Diff) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Diff) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Token) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Token) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Filter) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Filter) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Tree) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Tree) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Url) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Url) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_View) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_View) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Vfs) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Vfs) <  3.0.0
# Optional
Requires:       php-pear(File_Find)
Requires:       php-pear(File_Fstab)
Requires:       php-pear(Console_Getopt)
Requires:       php-pear(Console_Table)
Requires:       php-pear(Net_DNS2)
Requires:       php-pear(Services_Weather)
Requires:       php-pear(%{pear_channel}/Horde_Service_Weather) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Service_Weather) <  3.0.0
# Optional but implicitly required
#               Horde_Db, Horde_Feed, Horde_Oauth, Horde_SyncMl
# Optional but TODO
#               Horde_Service_Facebook
#               Horde_Service_Twitter

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Obsoletes:      horde < 5
Provides:       horde = %{version}


%description
The Horde Application Framework is a flexible, modular, general-purpose web
application framework written in PHP. It provides an extensive array of
components that are targeted at the common problems and tasks involved in
developing modern web applications. It is the basis for a large number of
production-level web applications, notably the Horde Groupware suites. For
more information on Horde or the Horde Groupware suites, visit
http://www.horde.org.

%prep
%setup -q -c
cd %{pear_name}-%{version}

# Don't install .po and .pot files
# Remove checksum for .mo, as we regenerate them
sed -e '/%{pear_name}.po/d' \
    -e '/htaccess/d' \
    -e '/%{pear_name}.mo/s/md5sum=.*name=/name=/' \
    ../package.xml >%{name}.xml


%build
cd %{pear_name}-%{version}

# Regenerate the locales
for po in $(find locale -name \*.po)
do
   msgfmt $po -o $(dirname $po)/$(basename $po .po).mo
done


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}

# Move configuration to /etc
mkdir -p %{buildroot}%{_sysconfdir}
mv %{buildroot}%{pear_hordedir}/config \
   %{buildroot}%{_sysconfdir}/horde
ln -s %{_sysconfdir}/horde %{buildroot}%{pear_hordedir}/config
cp %{buildroot}%{_sysconfdir}/horde/conf.php.dist \
   %{buildroot}%{_sysconfdir}/horde/conf.php

install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Locales
for loc in locale/{??,??_??}
do
    lang=$(basename $loc)
    test -d %{buildroot}%{pear_hordedir}/$loc \
         && echo "%%lang(${lang%_*}) %{pear_hordedir}/$loc"
done | tee ../%{pear_name}.lang


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files -f %{pear_name}.lang
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%attr(0770,apache,apache) %dir %{_sysconfdir}/horde
%attr(0770,apache,apache) %dir %{_sysconfdir}/horde/registry.d
%attr(0640,apache,apache) %config %{_sysconfdir}/horde/*.dist
%attr(0660,apache,apache) %config(noreplace) %{_sysconfdir}/horde/*.php
%attr(0660,apache,apache) %config %{_sysconfdir}/horde/*.xml
%attr(0640,apache,apache) %{_sysconfdir}/horde/registry.d/README
%{pear_xmldir}/%{name}.xml
%{_bindir}/horde-*
%{pear_hordedir}/*php
%{pear_hordedir}/admin
%{pear_hordedir}/config
%{pear_hordedir}/install
%{pear_hordedir}/lib
%dir %{pear_hordedir}/locale
%{pear_hordedir}/rpc
%{pear_hordedir}/services
%{pear_hordedir}/static
%{pear_hordedir}/templates
%{pear_hordedir}/themes
%{pear_hordedir}/util
%{pear_hordedir}/js/plupload
%{pear_hordedir}/js/*.js
%{pear_datadir}/%{pear_name}


%changelog
* Fri Mar 07 2014 Remi Collet <remi@fedoraproject.org> - 5.1.6-1
- Update to 5.1.6
- raide dependency: Horde_Core >= 2.11.0

* Tue Oct 29 2013 Remi Collet <remi@fedoraproject.org> - 5.1.5-1
- Update to 5.1.5
- raide dependency: Horde_Core >= 2.10.0

* Sun Sep 08 2013 Remi Collet <remi@fedoraproject.org> - 5.1.4-1
- Update to 5.1.4

* Tue Aug 27 2013 Remi Collet <remi@fedoraproject.org> - 5.1.3-1
- Update to 5.1.3
- raise dependency Horde_Core >= 2.7.0

* Wed Jul 17 2013 Remi Collet <remi@fedoraproject.org> - 5.1.2-1
- Update to 5.1.2

* Tue Jun 18 2013 Remi Collet <remi@fedoraproject.org> - 5.1.1-1
- Update to 5.1.1

* Wed Jun 05 2013 Remi Collet <remi@fedoraproject.org> - 5.1.0-1
- Update to 5.1.0
- raise dependency on Horde_Core 2.5.0
- drop dependency on Horde_Template

* Fri May 31 2013 Remi Collet <remi@fedoraproject.org> - 5.0.5-1
- Update to 5.0.5
- switch from Conflicts to Requires

* Fri Apr  5 2013 Remi Collet <remi@fedoraproject.org> - 5.0.4-2
- improves optional dependencies

* Tue Feb 12 2013 Remi Collet <remi@fedoraproject.org> - 5.0.4-1
- Update to 5.0.4

* Thu Jan 24 2013 Remi Collet <remi@fedoraproject.org> - 5.0.3-3
- define Alias for JavaScript Libraries

* Sun Jan 13 2013 Remi Collet <remi@fedoraproject.org> - 5.0.3-2
- obsoletes/provides horde

* Thu Jan 10 2013 Remi Collet <remi@fedoraproject.org> - 5.0.3-1
- Update to 5.0.3
- use local script instead of find_lang
- add more optional requires

* Mon Nov 19 2012 Remi Collet <remi@fedoraproject.org> - 5.0.2-2
- fix apache config and rename to php-horde-horde.conf

* Thu Nov 15 2012 Remi Collet <remi@fedoraproject.org> - 5.0.2-1
- update to 5.0.2

* Wed Nov  7 2012 Remi Collet <remi@fedoraproject.org> - 5.0.1-1
- update to 5.0.1

* Sun Nov  4 2012 Remi Collet <remi@fedoraproject.org> - 5.0.0-2
- fix locale

* Sun Nov  4 2012 Remi Collet <remi@fedoraproject.org> - 5.0.0-1
- Initial package
