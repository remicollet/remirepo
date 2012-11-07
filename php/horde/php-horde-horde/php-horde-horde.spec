%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    horde
%global pear_channel pear.horde.org

# TODO :
# static -> /var/lib
# /var/log
# cron (alarm)
# config: Image, Log
# "horbe" sub-package, with apache stuff

Name:           php-horde-horde
Version:        5.0.1
Release:        1%{?dist}
Summary:        Horde Application Framework

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://www.horde.org/apps/horde
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz
# /usr/lib/rpm/find-lang.sh from fedora 16
Source1:        find-lang.sh
Source2:        horde.conf

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext
BuildRequires:  php-pear
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  php-pear(%{pear_channel}/Horde_Role) >= 1.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Role) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Alarm) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Alarm) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Argv) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Argv) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Auth) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Auth) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Autoloader) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Autoloader) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Browser) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Browser) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Core) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Core) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Date) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Exception) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Form) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Form) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Group) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Group) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Http) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Http) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Image) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Image) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_LoginTasks) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_LoginTasks) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Mail) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Mime) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Nls) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Nls) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Perms) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Perms) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Prefs) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Prefs) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Rpc) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Rpc) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Serialize) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Serialize) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Support) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Template) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Template) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Diff) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Text_Diff) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Token) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Token) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Filter) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Text_Filter) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Tree) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Tree) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Url) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Url) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Util) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_View) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_View) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Vfs) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Vfs) >= 3.0.0
# Optionnal: Net_DNS2, Services_Weather, Horde_ActiveSync, Horde_Db, Horde_Feed, Horde_Oauth, Horde_Service_Facebook,
#            Horde_Service_Twitter, Horde_Service_Weather, Horde_SyncMl, Console_Getopt, Console_Table, File_Find

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


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

install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/httpd/conf.d/horde.conf

%if 0%{?fedora} > 13
%find_lang %{pear_name}
%else
sh %{SOURCE1} %{buildroot} %{pear_name}
%endif
for xml in locale/*/help.xml
do
    lang=$(basename $(dirname $xml))
    echo "%%lang(${lang%_*}) %{pear_hordedir}/$xml" >> %{pear_name}.lang
done


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


%files -f %{pear_name}-%{version}/%{pear_name}.lang
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/horde.conf
%attr(0770,apache,apache) %dir %{_sysconfdir}/horde
%attr(0770,apache,apache) %dir %{_sysconfdir}/horde/registry.d
%attr(0640,apache,apache) %config %{_sysconfdir}/horde/*.dist
%attr(0660,apache,apache) %config(noreplace) %{_sysconfdir}/horde/*.php
%attr(0660,apache,apache) %config %{_sysconfdir}/horde/*.xml
%attr(0640,apache,apache) %config %{_sysconfdir}/horde/registry.d/README
%{pear_xmldir}/%{name}.xml
%{_bindir}/horde-active-sessions
%{_bindir}/horde-alarms
%{_bindir}/horde-check-logger
%{_bindir}/horde-clear-cache
%{_bindir}/horde-crond
%{_bindir}/horde-db-migrate
%{_bindir}/horde-import-squirrelmail-prefs
%{_bindir}/horde-memcache-stats
%{_bindir}/horde-run-task
%{_bindir}/horde-set-perms
%{_bindir}/horde-themes
%{_bindir}/horde-translation
%{pear_hordedir}/*php
%{pear_hordedir}/admin
%{pear_hordedir}/config
%{pear_hordedir}/install
%{pear_hordedir}/lib
# own locales (non standard) directories, .mo own by find_lang
%dir %{pear_hordedir}/locale
%dir %{pear_hordedir}/locale/*
%dir %{pear_hordedir}/locale/*/LC_MESSAGES
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
* Wed Nov  7 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.0.1-1
- update to 5.0.1 for remi repo

* Sun Nov  4 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.0.0-2
- fix locale

* Sun Nov  4 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.0.0-1
- Initial package
