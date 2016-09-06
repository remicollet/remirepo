# remirepo/fedora spec file for php-horde-Horde-Core
#
# Copyright (c) 2012-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Core
%global pear_channel pear.horde.org
# To use system js
%global with_sysjs   0

Name:           php-horde-Horde-Core
Version:        2.26.0
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
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.6.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Url) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Injector) >= 2.0.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Group) >= 2.1.0
%if 0%{?fedora} >= 24
BuildRequires:  glibc-langpack-en
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
%if %{with_sysjs}
Requires:       prototype
Requires:       scriptaculous
%else
Provides:       horde-prototype
Provides:       horde-scriptaculous
%endif
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
Requires:       php-pear(%{pear_channel}/Horde_Alarm) >= 2.2.0
Requires:       php-pear(%{pear_channel}/Horde_Alarm) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Auth) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Auth) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Autoloader) >= 2.1.0
Requires:       php-pear(%{pear_channel}/Horde_Autoloader) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Browser) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Browser) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cache) >= 2.5.0
Requires:       php-pear(%{pear_channel}/Horde_Cache) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cli) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cli) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Compress) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Compress) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Compress_Fast) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Compress_Fast) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Controller) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Controller) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_CssMinify) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_CssMinify) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Data) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Data) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Group) >= 2.1.0
Requires:       php-pear(%{pear_channel}/Horde_Group) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_HashTable) >= 1.2.0
Requires:       php-pear(%{pear_channel}/Horde_HashTable) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_History) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_History) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Injector) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Injector) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_JavascriptMinify) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_JavascriptMinify) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Lock) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Lock) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Log) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Log) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_LoginTasks) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_LoginTasks) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) >= 2.5.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime_Viewer) >= 2.2.0
Requires:       php-pear(%{pear_channel}/Horde_Mime_Viewer) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Notification) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Notification) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Pack) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Pack) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Perms) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Perms) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Prefs) >= 2.8.0
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
Requires:       php-pear(%{pear_channel}/Horde_Translation) >= 2.2.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Url) >= 2.1.0
Requires:       php-pear(%{pear_channel}/Horde_Url) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_View) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_View) <  3.0.0
# Optional
Requires:       php-pear(Net_DNS2) >= 1.3.0
Requires:       php-pear(Text_CAPTCHA)
Requires:       php-pear(Text_Figlet)
Requires:       php-pear(%{pear_channel}/Horde_Crypt) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Crypt) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Editor) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Editor) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_ElasticSearch) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_ElasticSearch) <  2.0.0
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
Requires:       php-pear(%{pear_channel}/Horde_Vfs) >= 2.2.0
Requires:       php-pear(%{pear_channel}/Horde_Vfs) <  3.0.0

# Optional and omited to avoid circular dep:
#    Horde_Dav
# Optional and explicitly required:
#    Horde_HashTable, Horde_Http, Horde_Icalendar, Horde_Image, Horde_Imap_Client
#    Horde_Ldap, Horde_Mail, Horde_Mongo, Horde_Nls, Horde_Routes, Horde_Tree
# Horde_ActiveSync, Horde_JavascriptMinify_Jsmin (non free)
# Horde_Service_Twitter
# PEAR: Text_LanguageDetect

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-core) = %{version}


%description
These classes provide the core functionality of the Horde Application
Framework.


%prep
%setup -q -c
cd %{pear_name}-%{version}

# Don't install .po and .pot files
# Don't install prototype, scriptaculous, use system one
# Remove checksum for .mo, as we regenerate them
sed -e '/%{pear_name}\.po/d' \
%if %{with_sysjs}
    -e '/js\/prototype.js/d' \
    -e '/js\/scriptaculous/d' \
%endif
    -e '/%{pear_name}\.mo/s/md5sum=.*name=/name=/' \
    ../package.xml >%{name}.xml
touch -r ../package.xml %{name}.xml


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

# Locales
for loc in locale/{??,??_??}
do
    lang=$(basename $loc)
    test -d %{buildroot}%{pear_datadir}/%{pear_name}/$loc && \
         echo "%%lang(${lang%_*}) %{pear_datadir}/%{pear_name}/$loc"
done | tee ../%{pear_name}.lang


%clean
rm -rf %{buildroot}


%check
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)

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
%{pear_hordedir}/js/excanvas
%{pear_hordedir}/js/flotr2
%{pear_hordedir}/js/jquery.mobile
%{pear_hordedir}/js/map
%{pear_hordedir}/js/*js
%if ! %{with_sysjs}
%{pear_hordedir}/js/scriptaculous
%endif


%changelog
* Tue Sep 06 2016 Remi Collet <remi@fedoraproject.org> - 2.26.0-1
- Update to 2.26.0

* Thu Jul 28 2016 Remi Collet <remi@fedoraproject.org> - 2.25.0-1
- Update to 2.25.0
- raise dependency on Horde_Mime_Viewer 2.2.0

* Sat Jul 02 2016 Remi Collet <remi@fedoraproject.org> - 2.24.0-1
- Update to 2.24.0

* Wed Mar 09 2016 Remi Collet <remi@fedoraproject.org> - 2.23.0-1
- Update to 2.23.0

* Tue Feb 23 2016 Remi Collet <remi@fedoraproject.org> - 2.22.7-1
- Update to 2.22.7

* Thu Feb 04 2016 Remi Collet <remi@fedoraproject.org> - 2.22.6-1
- Update to 2.22.6
- raise dependency on Horde_Group >= 2.1.0
- raise build dependency on Horde_Test >= 2.6.0
- PHP 7 compatible version

* Wed Jan 06 2016 Remi Collet <remi@fedoraproject.org> - 2.22.5-1
- Update to 2.22.5
- run test suite with both PHP 5 and 7 when available

* Mon Dec 14 2015 Remi Collet <remi@fedoraproject.org> - 2.22.4-1
- Update to 2.22.4

* Fri Dec 04 2015 Remi Collet <remi@fedoraproject.org> - 2.22.3-1
- Update to 2.22.3

* Wed Nov 25 2015 Remi Collet <remi@fedoraproject.org> - 2.22.2-1
- Update to 2.22.2

* Wed Oct 21 2015 Remi Collet <remi@fedoraproject.org> - 2.22.1-1
- Update to 2.22.1

* Sat Sep 26 2015 Remi Collet <remi@fedoraproject.org> - 2.22.0-1
- Update to 2.22.0

* Tue Sep 08 2015 Remi Collet <remi@fedoraproject.org> - 2.21.0-1
- Update to 2.21.0

* Sun Aug 30 2015 Remi Collet <remi@fedoraproject.org> - 2.20.9-1
- Update to 2.20.9

* Fri Jul 31 2015 Remi Collet <remi@fedoraproject.org> - 2.20.8-1
- Update to 2.20.8

* Wed Jul 22 2015 Remi Collet <remi@fedoraproject.org> - 2.20.7-1
- Update to 2.20.7

* Tue Jul 07 2015 Remi Collet <remi@fedoraproject.org> - 2.20.6-1
- Update to 2.20.6

* Fri Jun 12 2015 Remi Collet <remi@fedoraproject.org> - 2.20.5-1
- Update to 2.20.5

* Tue Jun 02 2015 Remi Collet <remi@fedoraproject.org> - 2.20.4-1
- Update to 2.20.4

* Fri May 29 2015 Remi Collet <remi@fedoraproject.org> - 2.20.3-1
- Update to 2.20.3

* Tue May 19 2015 Remi Collet <remi@fedoraproject.org> - 2.20.2-1
- Update to 2.20.2

* Tue May 19 2015 Remi Collet <remi@fedoraproject.org> - 2.20.1-1
- Update to 2.20.1

* Tue Apr 28 2015 Remi Collet <remi@fedoraproject.org> - 2.20.0-1
- Update to 2.20.0

* Wed Mar 04 2015 Remi Collet <remi@fedoraproject.org> - 2.19.2-1
- Update to 2.19.2

* Tue Mar 03 2015 Remi Collet <remi@fedoraproject.org> - 2.19.1-1
- Update to 2.19.1

* Wed Feb 11 2015 Remi Collet <remi@fedoraproject.org> - 2.19.0-1
- Update to 2.19.0

* Fri Jan 09 2015 Remi Collet <remi@fedoraproject.org> - 2.18.3-1
- Update to 2.18.3

* Thu Jan 08 2015 Remi Collet <remi@fedoraproject.org> - 2.18.2-1
- Update to 2.18.2
- add provides php-composer(horde/horde-core)

* Tue Jan 06 2015 Remi Collet <remi@fedoraproject.org> - 2.18.1-1
- Update to 2.18.1

* Mon Dec 29 2014 Remi Collet <remi@fedoraproject.org> - 2.18.0-1
- Update to 2.18.0

* Tue Dec 16 2014 Remi Collet <remi@fedoraproject.org> - 2.17.2-1
- Update to 2.17.2

* Tue Nov 25 2014 Remi Collet <remi@fedoraproject.org> - 2.17.1-1
- Update to 2.17.1

* Sun Nov 23 2014 Remi Collet <remi@fedoraproject.org> - 2.17.0-1
- Update to 2.17.0
- raise dependency on Horde_Mime >= 2.5.0

* Thu Nov 06 2014 Remi Collet <remi@fedoraproject.org> - 2.16.1-1
- Update to 2.16.1
- raise dependency on Horde_Translation >= 2.2.0

* Wed Nov 05 2014 Remi Collet <remi@fedoraproject.org> - 2.16.0-1
- Update to 2.16.0

* Thu Oct 30 2014 Remi Collet <remi@fedoraproject.org> - 2.15.0-2
- add upstream patch to avoid error on front page from
  an unconfigured block

* Sun Oct 12 2014 Remi Collet <remi@fedoraproject.org> - 2.15.0-1
- Update to 2.15.0

* Thu Oct 02 2014 Remi Collet <remi@fedoraproject.org> - 2.14.2-1
- Update to 2.14.2

* Tue Sep 23 2014 Remi Collet <remi@fedoraproject.org> - 2.14.1-2
- don't use system prototype and scriptaculous as
  this breaks horde and its cache system

* Fri Sep 19 2014 Remi Collet <remi@fedoraproject.org> - 2.14.1-1
- Update to 2.14.1

* Tue Sep 09 2014 Remi Collet <remi@fedoraproject.org> - 2.14.0-1
- Update to 2.14.0
- add mandatory dependency on Horde_HashTable

* Fri Aug 22 2014 Remi Collet <remi@fedoraproject.org> - 2.13.1-1
- Update to 2.13.1

* Mon Aug 04 2014 Remi Collet <remi@fedoraproject.org> - 2.13.0-1
- Update to 2.13.0
- raise dependency on Horde_Vfs >= 2.2.0

* Tue Jul 15 2014 Remi Collet <remi@fedoraproject.org> - 2.12.6-1
- Update to 2.12.6

* Fri Jul 11 2014 Remi Collet <remi@fedoraproject.org> - 2.12.5-1
- Update to 2.12.5

* Wed Jul 09 2014 Remi Collet <remi@fedoraproject.org> - 2.12.4-1
- Update to 2.12.4
- add dep on Horde_Pack

* Tue Jul 08 2014 Remi Collet <remi@fedoraproject.org> - 2.12.2-1
- Update to 2.12.2

* Tue Jul 08 2014 Remi Collet <remi@fedoraproject.org> - 2.12.1-1
- Update to 2.12.1

* Tue Jul 08 2014 Remi Collet <remi@fedoraproject.org> - 2.12.0-1
- Update to 2.12.0
- add dep on Horde_CssMinify and Horde_JavascriptMinify
- del dep on Horde_Smtp and Horde_Css_Parser
- raise dep for Horde_Alarm, Horde_Autoloader, Horde_Cache,
  Horde_Mime, Horde_Prefs and Net_DNS2

* Mon Jul 07 2014 Remi Collet <remi@fedoraproject.org> - 2.11.2-1
- Update to 2.11.2

* Fri Jan 10 2014 Remi Collet <remi@fedoraproject.org> - 2.11.1-2
- cleanups from reviews #908329

* Wed Nov 20 2013 Remi Collet <remi@fedoraproject.org> - 2.11.1-1
- Update to 2.11.1

* Tue Nov 12 2013 Remi Collet <remi@fedoraproject.org> - 2.11.0-1
- Update to 2.11.0

* Mon Oct 28 2013 Remi Collet <remi@fedoraproject.org> - 2.10.2-1
- Update to 2.10.2

* Mon Oct 21 2013 Remi Collet <remi@fedoraproject.org> - 2.10.1-1
- Update to 2.10.1

* Tue Oct 15 2013 Remi Collet <remi@fedoraproject.org> - 2.10.0-1
- Update to 2.10.0

* Tue Oct 08 2013 Remi Collet <remi@fedoraproject.org> - 2.9.0-1
- Update to 2.9.0

* Sun Sep 08 2013 Remi Collet <remi@fedoraproject.org> - 2.8.0-1
- Update to 2.8.0
- add Requires Horde_Smtp

* Tue Aug 27 2013 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- Update to 2.7.0

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
