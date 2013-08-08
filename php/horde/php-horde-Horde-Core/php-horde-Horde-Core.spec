# spec file for php-horde-Horde-Core
#
# Copyright (c) 2012-2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Core
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Core
Version:        2.6.6
Release:        1%{?dist}
Summary:        Horde Core Framework libraries

Group:          Development/Libraries
License:        LGPLv2
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  php-pear(%{pear_channel}/Horde_Role) >= 1.0.0
# To run unit tests (minimal)
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Url) >= 2.0.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Injector) >= 2.0.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Group) >= 2.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       prototype
Requires:       scriptaculous
Requires:       php(language) >= 5.3.0
Requires:       php-date
Requires:       php-dom
Requires:       php-gettext
Requires:       php-hash
Requires:       php-json
Requires:       php-pcre
Requires:       php-pdo_mysql
Requires:       php-reflection
Requires:       php-session
Requires:       php-simplexml
Requires:       php-sockets
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Role) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Alarm) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Alarm) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Auth) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Auth) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Autoloader) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Autoloader) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Browser) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Browser) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cache) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cache) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cli) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cli) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Compress) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Compress) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Compress_Fast) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Compress_Fast) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Controller) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Controller) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Data) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Data) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Group) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Group) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_History) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_History) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Injector) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Injector) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Lock) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Lock) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Log) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Log) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_LoginTasks) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_LoginTasks) <  3.0.0
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
Requires:       php-pear(%{pear_channel}/Horde_Secret) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Secret) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Serialize) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Serialize) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_SessionHandler) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_SessionHandler) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Share) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Share) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Template) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Template) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Token) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Token) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Filter) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Filter) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Css_Parser) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Css_Parser) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Url) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Url) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_View) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_View) <  3.0.0
# Optional
Requires:       php-pear(Net_DNS2)
Requires:       php-pear(Text_CAPTCHA)
Requires:       php-pear(Text_Figlet)
Requires:       php-pear(%{pear_channel}/Horde_Crypt) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Crypt) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Editor) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Editor) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_ElasticSearch) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_ElasticSearch) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Form) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Form) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Kolab_Server) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Kolab_Server) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Kolab_Session) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Kolab_Session) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Oauth) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Oauth) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Queue) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Queue) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_SpellChecker) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_SpellChecker) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Vfs) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Vfs) <  3.0.0

# Optional and omited to avoid circular dep:
#    Horde_Dav
# Optional and explicitly required:
#    Horde_HashTable, Horde_Http, Horde_Icalendar, Horde_Image, Horde_Imap_Client
#    Horde_Ldap, Horde_Mail, Horde_Mongo, Horde_Nls, Horde_Routes, Horde_Tree
# Horde_ActiveSync (non free)
# Horde_Service_Twitter
# PEAR: Text_LanguageDetect

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
These classes provide the core functionality of the Horde Application
Framework.


%prep
%setup -q -c
cd %{pear_name}-%{version}

# Don't install .po and .pot files
# Don't install prototype, scriptaculous, use system one
# Remove checksum for .mo, as we regenerate them
sed -e '/%{pear_name}.po/d' \
    -e '/prototype.js/d' \
    -e '/scriptaculous/d' \
    -e '/LICENSE/s/role="horde"/role="doc"/' \
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
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}

# Locales
for loc in locale/{??,??_??}
do
    lang=$(basename $loc)
    test -d %{buildroot}%{pear_datadir}/%{pear_name}/$loc && \
         echo "%%lang(${lang%_*}) %{pear_datadir}/%{pear_name}/$loc"
done | tee ../%{pear_name}.lang


%check
src=$(pwd)/%{pear_name}-%{version}
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
phpunit \
    -d include_path=$src/lib:.:%{pear_phpdir} \
    -d date.timezone=UTC \
    .


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
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Config
%{pear_phpdir}/Horde/Core
%{pear_phpdir}/Horde/Exception/*.php
%{pear_phpdir}/Horde/Registry
%{pear_phpdir}/Horde/Script
%{pear_phpdir}/Horde/Session
%{pear_phpdir}/Horde/Shutdown
%{pear_phpdir}/Horde/Themes
%{pear_phpdir}/Horde/*.php
%{pear_phpdir}/Horde.php
%{pear_testdir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}/locale
%{pear_datadir}/%{pear_name}/migration
# Web files
%dir %{pear_hordedir}/js
%{pear_hordedir}/js/date
%{pear_hordedir}/js/jquery.mobile
%{pear_hordedir}/js/map
%{pear_hordedir}/js/*js


%changelog
* Thu Aug 08 2013 Remi Collet <remi@fedoraproject.org> - 2.6.6-1
- Update to 2.6.6

* Wed Aug 07 2013 Remi Collet <remi@fedoraproject.org> - 2.6.5-1
- Update to 2.6.5

* Thu Jul 25 2013 Remi Collet <remi@fedoraproject.org> - 2.6.4-1
- Update to 2.6.4

* Wed Jul 17 2013 Remi Collet <remi@fedoraproject.org> - 2.6.2-1
- Update to 2.6.2

* Tue Jul 09 2013 Remi Collet <remi@fedoraproject.org> - 2.6.1-1
- Update to 2.6.1

* Tue Jun 18 2013 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0

* Wed Jun 05 2013 Remi Collet <remi@fedoraproject.org> - 2.5.0-1
- Update to 2.5.0
- switch from Conflicts to Requires

* Wed Mar 13 2013 Remi Collet <remi@fedoraproject.org> - 2.4.3-2
- add dependency on Horde_ElasticSearch

* Tue Mar 12 2013 Remi Collet <remi@fedoraproject.org> - 2.4.3-1
- Update to 2.4.3

* Fri Mar 08 2013 Remi Collet <remi@fedoraproject.org> - 2.4.2-1
- Update to 2.4.2

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 2.4.1-1
- Update to 2.4.1
- remove dependency on LZF
- add dependencies on Horde_Compress_Fast and Horde_Queue

* Tue Feb 26 2013 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0

* Tue Feb 12 2013 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0

* Mon Feb 04 2013 Remi Collet <remi@fedoraproject.org> - 2.1.7-1
- Update to 2.1.7

* Tue Jan 29 2013 Remi Collet <remi@fedoraproject.org> - 2.1.6-1
- Update to 2.1.6

* Thu Jan 24 2013 Remi Collet <remi@fedoraproject.org> - 2.1.5-5
- use Alias for system JS

* Thu Jan 24 2013 Remi Collet <remi@fedoraproject.org> - 2.1.5-4
- use system scriptaculous

* Wed Jan 16 2013 Remi Collet <remi@fedoraproject.org> - 2.1.5-3
- spec cleanups
- more optional requires Text_CAPTCHA and Text_Figlet
- use system prototype

* Sat Jan 12 2013 Remi Collet <remi@fedoraproject.org> - 2.1.5-2
- add optional requires on Horde_Editor and Horde_SpellChecker

* Wed Jan  9 2013 Remi Collet <remi@fedoraproject.org> - 2.1.5-1
- Update to 2.1.5

* Sat Jan  5 2013 Remi Collet <remi@fedoraproject.org> - 2.1.4-1
- Update to 2.1.4

* Fri Dec 28 2012 Remi Collet <remi@fedoraproject.org> - 2.1.3-1
- Update to 2.1.3

* Fri Dec 21 2012 Remi Collet <remi@fedoraproject.org> - 2.1.2-1
- Update to 2.1.2

* Thu Dec 13 2012 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- Update to 2.1.1

* Sat Dec  8 2012 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0

* Tue Nov 27 2012 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4

* Thu Nov 22 2012 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3

* Wed Nov  7 2012 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2

* Sun Nov  4 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Initial package
