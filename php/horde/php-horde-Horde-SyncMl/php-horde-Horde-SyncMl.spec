# remirepo/fedora spec file for php-horde-Horde-Date
#
# Copyright (c) 2012-2017 Nick Bebout, Remi Collet
#
# License: MIT
# https://fedoraproject.org/wiki/Licensing:MIT#Modern_Style_with_sublicense
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_SyncMl
%global pear_channel pear.horde.org
# No run of unit tests - because tests are not ready (oudated)
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-horde-Horde-SyncMl
Version:        2.0.7
Release:        1%{?dist}
Summary:        Horde_SyncMl provides an API for processing SyncML requests

Group:          Development/Libraries
License:        LGPLv2
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  gettext

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-date
Requires:       php-pcre
Requires:       php-session
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Date) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Date) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Icalendar) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Icalendar) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Log) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Log) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Support) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Util) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Xml_Wbxml) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Xml_Wbxml) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) >= 2.2.0
Conflicts:      php-pear(%{pear_channel}/Horde_Translation) >= 3.0.0
# Optional
Requires:       php-pear(%{pear_channel}/Horde_Auth) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Auth) >= 3.0.0
# Keep optional : Horde_Core

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
Classes for implementing a SyncML server.


%prep
%setup -q -c
cd %{pear_name}-%{version}

# Don't install .po and .pot files
# Remove checksum for .mo, as we regenerate them
sed -e '/%{pear_name}.po/d' \
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
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}

for loc in locale/{??,??_??}
do
    lang=$(basename $loc)
    test -d %{buildroot}%{pear_datadir}/%{pear_name}/$loc \
         && echo "%%lang(${lang%_*}) %{pear_datadir}/%{pear_name}/$loc"
done | tee ../%{pear_name}.lang

# make rpmlint happy
for fic in %{buildroot}%{pear_testdir}/%{pear_name}/Horde/SyncMl/*.php
do
  sed -e '/s^#!/s:/usr/bin/env php:%{_bindir}/php:' -i $fic
  chmod +x $fic
done


%check
%if %{with_tests}
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
%{_bindir}/phpunit .

if which php70; then
   php70 %{_bindir}/phpunit .
fi
%else
: Test disabled, missing '--with tests' option.
%endif


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
%{pear_phpdir}/Horde/SyncMl
%{pear_phpdir}/Horde/SyncMl.php
%{pear_testdir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}/locale
%{pear_datadir}/%{pear_name}/migration


%changelog
* Tue Apr 05 2016 Remi Collet <remi@fedoraproject.org> - 2.0.7-1
- Update to 2.0.7

* Tue Feb 02 2016 Remi Collet <remi@fedoraproject.org> - 2.0.6-1
- Update to 2.0.6
- PHP 7 compatible version
- run test suite with both PHP 5 and 7 when available

* Wed Dec 03 2014 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- Update to 2.0.5
- raise dependency on Horde_Translation >= 2.2.0

* Fri Jul 25 2014 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4

* Tue Mar 26 2013 Remi Collet <remi@fedoraproject.org> - 2.0.3-2
- cleanups before review

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3

* Thu Jan 10 2013 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2
- use local script instead of find_lang

* Wed Nov  7 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1

* Sun Nov  4 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.8-1
- Initial package
