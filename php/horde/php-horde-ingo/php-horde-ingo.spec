# remirepo/fedora spec file for php-horde-ingo
#
# Copyright (c) 2012-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    ingo
%global pear_channel pear.horde.org
%global with_tests   0%{!?_without_tests:1}

Name:           php-horde-ingo
Version:        3.2.11
Release:        1%{?dist}
Summary:        An email filter rules manager

Group:          Development/Libraries
License:        BSD
URL:            http://www.horde.org/apps/ingo
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
BuildRequires:  php-pear(%{pear_channel}/Horde_Core) >= 2.12.0
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}

# Web stuff
Requires:       mod_php
Requires:       httpd
# From package.xml, required
Requires:       php(language) >= 5.3.0
Requires:       php-gettext
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Role) >= 1.0.0
Requires:       php-pear(%{pear_channel}/horde) >= 5.0.0
Requires:       php-pear(%{pear_channel}/horde) <  6.0.0
Requires:       php-pear(%{pear_channel}/Horde_Auth) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Auth) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Autoloader) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Autoloader) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Core) >= 2.12.0
Requires:       php-pear(%{pear_channel}/Horde_Core) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Group) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Group) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Form) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Form) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Imap_Client) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Imap_Client) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Perms) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Perms) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Share) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Share) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_View) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_View) <  3.0.0
# From package.xml, optional
Requires:       php-pear(Net_Sieve) >= 1.3.1
Requires:       php-pear(Net_Socket)
# Optional and implicitly requires: Horde_Vfs
# From phpcompatinfo report for version 3.1.4
Requires:       php-date
Requires:       php-ldap
Requires:       php-pcre
Requires:       php-spl

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/ingo) = %{version}
Obsoletes:      ingo < 3
Provides:       ingo = %{version}


%description
Ingo is an email-filter management application. It is fully
internationalized, integrated with Horde and the IMP Webmail client, and
supports both server-side (Sieve, Procmail, Maildrop) and client-side
(IMAP) message filtering.


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
sed -e '/%{pear_name}\.po/d' \
    -e '/htaccess/d' \
    -e '/%{pear_name}.mo/s/md5sum=.*name=/name=/' \
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
%if %{with_tests}
cd %{pear_name}-%{version}/test/Ingo

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
if   %{_bindir}/phpunit --atleast-version 4
then %{_bindir}/phpunit --verbose .
else : PHPUnit is too old
fi
# remirepo:2
fi
exit $ret
%else
: tests disabled
%endif


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
%{pear_xmldir}/%{name}.xml
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%attr(0770,apache,apache) %dir %{_sysconfdir}/horde/%{pear_name}
%attr(0640,apache,apache) %config %{_sysconfdir}/horde/%{pear_name}/*.dist
%attr(0660,apache,apache) %config(noreplace) %{_sysconfdir}/horde/%{pear_name}/*.php
%attr(0660,apache,apache) %config %{_sysconfdir}/horde/%{pear_name}/*.xml
%{_bindir}/ingo-convert-prefs-to-sql
%{_bindir}/ingo-convert-sql-shares-to-sqlng
%{_bindir}/ingo-postfix-policyd
%{_bindir}/ingo-admin-upgrade
%dir %{pear_hordedir}/%{pear_name}
%dir %{pear_hordedir}/%{pear_name}/locale
%{pear_hordedir}/%{pear_name}/*.php
%{pear_hordedir}/%{pear_name}/config
%{pear_hordedir}/%{pear_name}/js
%{pear_hordedir}/%{pear_name}/lib
%{pear_hordedir}/%{pear_name}/migration
%{pear_hordedir}/%{pear_name}/templates
%{pear_hordedir}/%{pear_name}/themes
%{pear_testdir}/ingo


%changelog
* Sat Jul 02 2016 Remi Collet <remi@fedoraproject.org> - 3.2.11-1
- Update to 3.2.11

* Tue Apr 05 2016 Remi Collet <remi@fedoraproject.org> - 3.2.10-1
- Update to 3.2.10

* Tue Mar 22 2016 Remi Collet <remi@fedoraproject.org> - 3.2.9-1
- Update to 3.2.9

* Tue Feb 02 2016 Remi Collet <remi@fedoraproject.org> - 3.2.8-1
- Update to 3.2.8
- run test suite with both PHP 5 and 7 when available

* Wed Oct 21 2015 Remi Collet <remi@fedoraproject.org> - 3.2.7-1
- Update to 3.2.7

* Sun Aug 02 2015 Remi Collet <remi@fedoraproject.org> - 3.2.6-1
- Update to 3.2.6

* Wed Apr 29 2015 Remi Collet <remi@fedoraproject.org> - 3.2.5-1
- Update to 3.2.5

* Tue Feb 10 2015 Remi Collet <remi@fedoraproject.org> - 3.2.4-1
- Update to 3.2.4
- add provides php-composer(horde/ingo)

* Wed Dec 03 2014 Remi Collet <remi@fedoraproject.org> - 3.2.3-1
- Update to 3.2.3

* Wed Oct 29 2014 Remi Collet <remi@fedoraproject.org> - 3.2.2-1
- Update to 3.2.2

* Sat Sep 06 2014 Remi Collet <remi@fedoraproject.org> - 3.2.1-1
- Update to 3.2.1

* Wed Jul 09 2014 Remi Collet <remi@fedoraproject.org> - 3.2.0-1
- Update to 3.2.0
- raise dep on Hode_Core
- run test suite during build

* Mon Jul 07 2014 Remi Collet <remi@fedoraproject.org> - 3.1.5-1
- Update to 3.1.5

* Fri May 16 2014 Remi Collet <remi@fedoraproject.org> - 3.1.4-2
- preserve package.xml timestamp

* Mon Mar 10 2014 Remi Collet <remi@fedoraproject.org> - 3.1.4-1
- Update to 3.1.4

* Tue Oct 29 2013 Remi Collet <remi@fedoraproject.org> - 3.1.3-1
- Update to 3.1.3

* Wed Jul 17 2013 Remi Collet <remi@fedoraproject.org> - 3.1.2-1
- Update to 3.1.2

* Wed Jun 12 2013 Remi Collet <remi@fedoraproject.org> - 3.1.1-1
- Update to 3.1.1

* Wed Jun 05 2013 Remi Collet <remi@fedoraproject.org> - 3.1.0-1
- Update to 3.1.0
- new dependency: Horde_View

* Fri May 31 2013 Remi Collet <remi@fedoraproject.org> - 3.0.4-1
- Update to 3.0.4
- switch from Conflicts to Provides

* Tue Feb 12 2013 Remi Collet <remi@fedoraproject.org> - 3.0.3-1
- Update to 3.0.3

* Sat Jan 12 2013 Remi Collet <remi@fedoraproject.org> - 3.0.2-1
- Initial package
