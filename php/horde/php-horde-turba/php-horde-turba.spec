# remirepo/fedora spec file for php-horde-turba
#
# Copyright (c) 2012-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    turba
%global pear_channel pear.horde.org

Name:           php-horde-turba
Version:        4.2.19
Release:        1%{?dist}
Summary:        A web based address book

Group:          Development/Libraries
License:        ASL 1.0
URL:            http://www.horde.org/apps/turba
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  php-pear(%{pear_channel}/Horde_Role) >= 1.0.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Core) >= 2.12.0
BuildRequires:  php-pear(%{pear_channel}/content) >= 2.0.5

Requires(post): %{__pear}
Requires(postun): %{__pear}

# Web stuff
Requires:       mod_php
Requires:       httpd
# From package.xml required
Requires:       php(language) >= 5.3.0
Requires:       php-gettext
Requires:       php-hash
Requires:       php-json
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Role) >= 1.0.0
Requires:       php-pear(%{pear_channel}/content) >= 2.0.5
Requires:       php-pear(%{pear_channel}/content) <  3.0.0
Requires:       php-pear(%{pear_channel}/horde) >= 5.0.0
Requires:       php-pear(%{pear_channel}/horde) <  6.0.0
Requires:       php-pear(%{pear_channel}/Horde_Auth) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Auth) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Core) >= 2.12.0
Requires:       php-pear(%{pear_channel}/Horde_Core) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Data) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Data) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Dav) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Dav) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Form) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Form) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Group) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Group) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_History) >= 2.1.0
Requires:       php-pear(%{pear_channel}/Horde_History) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Icalendar) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Icalendar) <  3.0.0
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
Requires:       php-pear(%{pear_channel}/Horde_Serialize) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Serialize) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Share) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Share) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Url) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Url) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.5.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Vfs) >= 2.1.3
Requires:       php-pear(%{pear_channel}/Horde_Vfs) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_View) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_View) <  3.0.0
# Optional an implicitly required
#    Horde_Db, Horde_Imsp, Horde_Ldap
#    Horde_Kolab_Format, Horde_Kolab_Storage
# Not yet available Horde_Service_Facebook
# From phpcompatinfo report for version 4.1.4
Requires:       php-date
Requires:       php-pcre
Requires:       php-spl

Provides:       php-pear(%{pear_channel}/turba) = %{version}
Provides:       php-compposer(horde/turba) = %{version}
Obsoletes:      turba < 4
Provides:       turba = %{version}


%description
Turba is the Horde contact management application. Leveraging the Horde
framework to provide seamless integration with IMP and other Horde
applications, it supports storing contacts in SQL, LDAP, Kolab, and IMSP
address books.

%prep
%setup -q -c

cat <<EOF >httpd.conf
<DirectoryMatch %{pear_hordedir}/%{pear_name}/(config|lib|locale|scripts|templates)>
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
   : msgfmt --statistics $po -o $(dirname $po)/$(basename $po .po).mo
done


%install
cd %{pear_name}-%{version}
rm -rf %{buildroot}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
install -Dpm 644 %{name}.xml %{buildroot}%{pear_xmldir}/%{name}.xml

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


%clean
rm -rf %{buildroot}


%check
cd %{pear_name}-%{version}/test/Turba
# disable as this test use Horde_ActiveSync (non-free)
sed -e 's/function testDuplicateDetectionFromAsWithNoEmail/function SKIP_testDuplicateDetectionFromAsWithNoEmail/' \
    -i Unit/Driver/Base.php

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
        pear.horde.org/%{pear_name} >/dev/null || :
fi


%files -f %{pear_name}.lang
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%attr(0770,apache,apache) %dir %{_sysconfdir}/horde/%{pear_name}
%attr(0640,apache,apache) %config %{_sysconfdir}/horde/%{pear_name}/*.dist
%attr(0660,apache,apache) %config(noreplace) %{_sysconfdir}/horde/%{pear_name}/*.php
%attr(0660,apache,apache) %config %{_sysconfdir}/horde/%{pear_name}/*.xml
%{pear_xmldir}/%{name}.xml
%{pear_datadir}/turba
%{pear_testdir}/turba
%{_bindir}/turba-convert-datatree-shares-to-sql
%{_bindir}/turba-convert-sql-shares-to-sqlng
%{_bindir}/turba-import-openxchange
%{_bindir}/turba-import-squirrelmail-file-abook
%{_bindir}/turba-import-squirrelmail-sql-abook
%{_bindir}/turba-import-vcards
%{_bindir}/turba-public-to-horde-share
%dir %{pear_hordedir}/%{pear_name}
%{pear_hordedir}/%{pear_name}/*.php
%{pear_hordedir}/%{pear_name}/addressbooks
%{pear_hordedir}/%{pear_name}/config
%{pear_hordedir}/%{pear_name}/js
%{pear_hordedir}/%{pear_name}/lib
%{pear_hordedir}/%{pear_name}/migration
%{pear_hordedir}/%{pear_name}/themes
%{pear_hordedir}/%{pear_name}/templates
%dir %{pear_hordedir}/%{pear_name}/locale


%changelog
* Mon Mar 20 2017 Remi Collet <remi@remirepo.net> - 4.2.19-1
- Update to 4.2.19

* Tue Dec 20 2016 Remi Collet <remi@fedoraproject.org> - 4.2.18-2
- Update to 4.2.18
- use upstream locale files

* Thu Nov 03 2016 Remi Collet <remi@fedoraproject.org> - 4.2.17-1
- Update to 4.2.17

* Wed Sep 07 2016 Remi Collet <remi@fedoraproject.org> - 4.2.16-1
- Update to 4.2.16

* Sat Jul 02 2016 Remi Collet <remi@fedoraproject.org> - 4.2.15-1
- Update to 4.2.15

* Tue Apr 05 2016 Remi Collet <remi@fedoraproject.org> - 4.2.14-1
- Update to 4.2.14

* Mon Mar 21 2016 Remi Collet <remi@fedoraproject.org> - 4.2.13-1
- Update to 4.2.13

* Tue Feb 02 2016 Remi Collet <remi@fedoraproject.org> - 4.2.12-1
- Update to 4.2.12
- run test suite with both PHP 5 and 7 when available

* Thu Oct 29 2015 Remi Collet <remi@fedoraproject.org> - 4.2.11-1
- Update to 4.2.11

* Thu Oct 22 2015 Remi Collet <remi@fedoraproject.org> - 4.2.10-1
- Update to 4.2.10

* Wed Oct 21 2015 Remi Collet <remi@fedoraproject.org> - 4.2.9-1
- Update to 4.2.9

* Sat Aug 01 2015 Remi Collet <remi@fedoraproject.org> - 4.2.8-1
- Update to 4.2.8

* Fri Jun 19 2015 Remi Collet <remi@fedoraproject.org> - 4.2.7-1
- Update to 4.2.7

* Wed Apr 29 2015 Remi Collet <remi@fedoraproject.org> - 4.2.6-1
- Update to 4.2.6

* Tue Feb 10 2015 Remi Collet <remi@fedoraproject.org> - 4.2.5-1
- Update to 4.2.5
- add provides php-compposer(horde/turba)

* Wed Dec 03 2014 Remi Collet <remi@fedoraproject.org> - 4.2.4-1
- Update to 4.2.4

* Wed Oct 29 2014 Remi Collet <remi@fedoraproject.org> - 4.2.3-1
- Update to 4.2.3

* Sat Sep 06 2014 Remi Collet <remi@fedoraproject.org> - 4.2.2-1
- Update to 4.2.2
- raise dep on Horde_Util 2.5.0

* Tue Aug 05 2014 Remi Collet <remi@fedoraproject.org> - 4.2.1-1
- Update to 4.2.1

* Wed Jul 09 2014 Remi Collet <remi@fedoraproject.org> - 4.2.0-1
- Update to 4.2.0
- add dep on content, Horde_Vfs
- raise dep on Horde_Core

* Mon Jul 07 2014 Remi Collet <remi@fedoraproject.org> - 4.1.5-1
- Update to 4.1.5
- run test suite during build

* Fri May 16 2014 Remi Collet <remi@fedoraproject.org> - 4.1.4-2
- preserve package.xml timestamp
- fix license (ASL 1.0) from review #1087742

* Mon Mar 10 2014 Remi Collet <remi@fedoraproject.org> - 4.1.4-1
- Update to 4.1.4
- add dependency on Horde_Dav

* Tue Oct 29 2013 Remi Collet <remi@fedoraproject.org> - 4.1.3-1
- Update to 4.1.3

* Tue Aug 27 2013 Remi Collet <remi@fedoraproject.org> - 4.1.2-1
- Update to 4.1.2

* Wed Jul 17 2013 Remi Collet <remi@fedoraproject.org> - 4.1.1-1
- Update to 4.1.1

* Wed Jun 05 2013 Remi Collet <remi@fedoraproject.org> - 4.1.0-1
- Update to 4.1.0

* Fri May 31 2013 Remi Collet <remi@fedoraproject.org> - 4.0.4-1
- Update to 4.0.4
- switch from Conflicts to Requires

* Tue Feb 12 2013 Remi Collet <remi@fedoraproject.org> - 4.0.3-1
- Update to 4.0.3

* Sun Jan 13 2013 Remi Collet <RPMS@FamilleCollet.com> - 4.0.2-2
- obsoletes/provides turba

* Thu Jan 10 2013 Remi Collet <RPMS@FamilleCollet.com> - 4.0.2-1
- Update to 4.0.2 for remi repo

* Tue Nov 27 2012 Remi Collet <RPMS@FamilleCollet.com> - 4.0.1-1
- Update to 4.0.1 for remi repo

* Sun Nov  4 2012 Remi Collet <RPMS@FamilleCollet.com> - 4.0.0-1
- Initial package
