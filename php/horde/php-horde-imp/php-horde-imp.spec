# remirepo/fedora spec file for php-horde-imp
#
# Copyright (c) 2012-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    imp
%global pear_channel pear.horde.org

Name:           php-horde-imp
Version:        6.2.18
Release:        1%{?dist}
Summary:        A web based webmail system

Group:          Development/Libraries
# imp is GPLv2, murmurhash3.js is MIT
License:        GPLv2 and MIT
URL:            http://www.horde.org/apps/imp
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  php-pear(%{pear_channel}/Horde_Role) >= 1.0.0
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Core) >= 2.17.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Itip) >= 2.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}

# Web stuff
Requires:       mod_php
Requires:       httpd
# From package.xml required
Requires:       php(language) >= 5.3.0
Requires:       php-dom
Requires:       php-gettext
Requires:       php-hash
Requires:       php-json
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Role) >= 1.0.0
Requires:       php-pear(%{pear_channel}/horde) >= 5.0.0
Requires:       php-pear(%{pear_channel}/horde) <  6.0.0
Requires:       php-pear(%{pear_channel}/Horde_Auth) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Auth) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Browser) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Browser) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cache) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cache) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Compress) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Compress) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Core) >= 2.17.0
Requires:       php-pear(%{pear_channel}/Horde_Core) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Css_Parser) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Css_Parser) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Crypt) >= 2.5.0
Requires:       php-pear(%{pear_channel}/Horde_Crypt) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Editor) >= 2.0.4
Requires:       php-pear(%{pear_channel}/Horde_Editor) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Icalendar) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Icalendar) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Image) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Image) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Imap_Client) >= 2.23.0
Requires:       php-pear(%{pear_channel}/Horde_Imap_Client) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Itip) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Itip) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_ListHeaders) >= 1.1.0
Requires:       php-pear(%{pear_channel}/Horde_ListHeaders) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_LoginTasks) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_LoginTasks) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) >= 2.2.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail_Autoconfig) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail_Autoconfig) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) >= 2.3.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime_Viewer) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime_Viewer) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Nls) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Nls) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Notification) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Notification) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Pack) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Pack) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Perms) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Perms) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_SpellChecker) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_SpellChecker) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream) >= 1.4.0
Requires:       php-pear(%{pear_channel}/Horde_Stream) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream_Filter) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream_Filter) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream_Wrapper) >= 2.1.0
Requires:       php-pear(%{pear_channel}/Horde_Stream_Wrapper) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) >= 2.0.5
Requires:       php-pear(%{pear_channel}/Horde_Support) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Filter) >= 2.1.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Filter) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Flowed) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Flowed) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Tree) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Tree) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Url) >= 2.2.0
Requires:       php-pear(%{pear_channel}/Horde_Url) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.4.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Vfs) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Vfs) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_View) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_View) <  3.0.0
# From package.xml, optional
Requires:       php-pear(%{pear_channel}/Horde_Service_Gravatar) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Service_Gravatar) <  2.0.0
Requires:       php-pear(phpseclib.sourceforge.net/File_ASN1)
# Optional and implicitly required:
#     Horde_History, Horde_Http
# From phpcompatinfo report for version 6.1.7
Requires:       php-date
Requires:       php-filter
Requires:       php-openssl
Requires:       php-pcre
Requires:       php-spl

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/imp) = %{version}
Obsoletes:      imp < 5
Provides:       imp = %{version}


%description
IMP, the Internet Mail Program, is one of the most popular and widely
deployed open source webmail applications in the world. It allows
universal, web-based access to IMAP and POP3 mail servers and provides
Ajax, mobile and traditional interfaces with a rich range of features
normally found only in desktop email clients.


%prep
%setup -q -c

cat <<EOF | tee httpd.conf
<DirectoryMatch %{pear_hordedir}/%{pear_name}/(config|lib|locale|templates)>
     Deny from all
</DirectoryMatch>
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

# Regenerate the locales
for po in $(find locale -name \*.po)
do
   : msgfmt $po -o $(dirname $po)/$(basename $po .po).mo
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


%check
cd %{pear_name}-%{version}/test/Imp
# Ignore this one - Need investigation
rm Unit/Mime/Viewer/ItipTest.php

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
%{pear_xmldir}/%{name}.xml
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%attr(0770,apache,apache) %dir %{_sysconfdir}/horde/%{pear_name}
%attr(0640,apache,apache) %config %{_sysconfdir}/horde/%{pear_name}/*.dist
%attr(0660,apache,apache) %config(noreplace) %{_sysconfdir}/horde/%{pear_name}/*.php
%attr(0660,apache,apache) %config %{_sysconfdir}/horde/%{pear_name}/*.xml
%{pear_testdir}/imp
%{_bindir}/imp-admin-upgrade
%{_bindir}/imp-bounce-spam
%{_bindir}/imp-mailbox-decode
%{_bindir}/imp-query-imap-cache
%dir %{pear_hordedir}/%{pear_name}
%dir %{pear_hordedir}/%{pear_name}/locale
%{pear_hordedir}/%{pear_name}/*.php
%{pear_hordedir}/%{pear_name}/config
%{pear_hordedir}/%{pear_name}/js
%{pear_hordedir}/%{pear_name}/lib
%{pear_hordedir}/%{pear_name}/migration
%{pear_hordedir}/%{pear_name}/templates
%{pear_hordedir}/%{pear_name}/themes


%changelog
* Mon Mar 20 2017 Remi Collet <remi@remirepo.net> - 6.2.18-1
- Update to 6.2.18

* Tue Dec 20 2016 Remi Collet <remi@fedoraproject.org> - 6.2.17-2
- Update to 6.2.17
- use upstream locale files

* Wed Sep 07 2016 Remi Collet <remi@fedoraproject.org> - 6.2.16-1
- Update to 6.2.16

* Sat Jul 02 2016 Remi Collet <remi@fedoraproject.org> - 6.2.15-1
- Update to 6.2.15

* Tue Apr 05 2016 Remi Collet <remi@fedoraproject.org> - 6.2.14-1
- Update to 6.2.14

* Mon Mar 21 2016 Remi Collet <remi@fedoraproject.org> - 6.2.13-1
- Update to 6.2.13

* Tue Feb 02 2016 Remi Collet <remi@fedoraproject.org> - 6.2.12-1
- Update to 6.2.12
- run test suite with both PHP 5 and 7 when available

* Wed Oct 21 2015 Remi Collet <remi@fedoraproject.org> - 6.2.11-1
- Update to 6.2.11

* Sat Aug 01 2015 Remi Collet <remi@fedoraproject.org> - 6.2.10-1
- Update to 6.2.10

* Fri Jun 19 2015 Remi Collet <remi@fedoraproject.org> - 6.2.9-1
- Update to 6.2.9

* Wed Apr 29 2015 Remi Collet <remi@fedoraproject.org> - 6.2.8-1
- Update to 6.2.8

* Tue Feb 10 2015 Remi Collet <remi@fedoraproject.org> - 6.2.7-1
- Update to 6.2.7

* Tue Jan 20 2015 Remi Collet <remi@fedoraproject.org> - 6.2.6-1
- Update to 6.2.6
- phpseclib/File_ASN1 is optional

* Thu Jan 15 2015 Remi Collet <remi@fedoraproject.org> - 6.2.5-1
- Update to 6.2.5
- add dependency on phpseclib/File_ASN1
- add provides php-composer(horde/imp)

* Wed Dec 03 2014 Remi Collet <remi@fedoraproject.org> - 6.2.4-1
- Update to 6.2.4
- raide dependency: Horde_Core >= 2.17.0

* Wed Oct 29 2014 Remi Collet <remi@fedoraproject.org> - 6.2.3-1
- Update to 6.2.3

* Sat Sep 06 2014 Remi Collet <remi@fedoraproject.org> - 6.2.2-1
- Update to 6.2.2

* Mon Aug 04 2014 Remi Collet <remi@fedoraproject.org> - 6.2.1-1
- Update to 6.2.1
- add dependency on Horde_Pack

* Wed Jul 23 2014 Remi Collet <remi@fedoraproject.org> - 6.2.0-2
- add optional dep on Horde_Service_Gravatar

* Tue Jul 08 2014 Remi Collet <remi@fedoraproject.org> - 6.2.0-1
- Update to 6.2.0
- raise dep on Horde_Core, Horde_Crypt, Horde_Editor, Horde_Imap_Client,
  Horde_ListHeaders, Horde_Mail, Horde_Mime, Horde_Stream, Horde_Util
- drop dep on Horde_Serialize, Horde_Token, Horde_Text_Filter_Csstidy
- add dep on Horde_Mail_Autoconfig, Horde_Stream_Wrapper

* Mon Jul 07 2014 Remi Collet <remi@fedoraproject.org> - 6.1.8-1
- Update to 6.1.8

* Mon Apr 28 2014 Remi Collet <remi@fedoraproject.org> - 6.1.7-2
- fix from review #1087734

* Fri Mar 07 2014 Remi Collet <remi@fedoraproject.org> - 6.1.7-1
- Update to 6.1.7

* Wed Nov 20 2013 Remi Collet <remi@fedoraproject.org> - 6.1.6-1
- Update to 6.1.6

* Tue Oct 29 2013 Remi Collet <remi@fedoraproject.org> - 6.1.5-1
- Update to 6.1.5
- raide dependency: Horde_Mail >= 2.1.0

* Tue Aug 27 2013 Remi Collet <remi@fedoraproject.org> - 6.1.4-1
- Update to 6.1.4
- drop dependency on Horde_Secret
- raise dependencies on Horde_Core >= 2.7.0 and Horde_Imap_Client >= 2.14.0
- don't ignore test results during build

* Wed Jul 17 2013 Remi Collet <remi@fedoraproject.org> - 6.1.3-1
- Update to 6.1.3

* Tue Jun 18 2013 Remi Collet <remi@fedoraproject.org> - 6.1.2-1
- Update to 6.1.2

* Wed Jun 12 2013 Remi Collet <remi@fedoraproject.org> - 6.1.1-1
- Update to 6.1.1

* Wed Jun 05 2013 Remi Collet <remi@fedoraproject.org> - 6.1.0-1
- Update to 6.1.0
- new dependencies : Horde_Cache, Horde_Stream, Horde_Secret
- raise various dependency
- drop dependency  on Horde_Form

* Fri May 31 2013 Remi Collet <remi@fedoraproject.org> - 6.0.5-1
- Update to 6.0.5
- switch from Conflicts to Requires
- add requires: Horde_Css_Parser, Horde_Stream_Filter
- drop requires: Horde_Text_Filter_Csstidy

* Tue Feb 12 2013 Remi Collet <remi@fedoraproject.org> - 6.0.4-1
- Update to 6.0.4

* Sat Jan 12 2013 Remi Collet <remi@fedoraproject.org> - 6.0.3-1
- Initial package
