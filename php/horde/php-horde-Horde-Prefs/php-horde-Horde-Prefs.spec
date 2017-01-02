# remirepo/fedora spec file for php-horde-Horde-Prefs
#
# Copyright (c) 2012-2017 Nick Bebout, Remi Collet
#
# License: MIT
# https://fedoraproject.org/wiki/Licensing:MIT#Modern_Style_with_sublicense
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Prefs
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Prefs
Version:        2.8.0
Release:        1%{?dist}
Summary:        Horde Preferences API

Group:          Development/Libraries
License:        LGPLv2
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  gettext
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Db) >= 2.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-json
Requires:       php-pdo
Requires:       php-pcre
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) >= 2.2.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
# Optional
Requires:       php-pear(%{pear_channel}/Horde_Autoloader) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Autoloader) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cache) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cache) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Db) >= 2.2.0
Requires:       php-pear(%{pear_channel}/Horde_Db) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Image) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Image) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Ldap) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Ldap) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Kolab_Storage) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Kolab_Storage) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Imsp) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Imsp) <  3.0.0
# Optional and implicitly required: Horde_Mongo

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-prefs) = %{version}


%description
The Horde_Prefs package provides a common abstracted interface into the
various preferences storage mediums. It also includes all of the functions
for retrieving, storing, and checking preference values.


%prep
%setup -q -c

cd %{pear_name}-%{version}

# Don't install .po and .pot files
# Remove checksum for .mo, as we regenerate them
sed -e '/%{pear_name}.po/d' \
    -e '/Horde_Other.po/d' \
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
%{_bindir}/horde-prefs
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Prefs
%{pear_phpdir}/Horde/Prefs.php
%{pear_testdir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}/locale
%{pear_datadir}/%{pear_name}/migration


%changelog
* Fri Sep 02 2016 Remi Collet <remi@fedoraproject.org> - 2.8.0-1
- Update to 2.8.0

* Wed Mar 09 2016 Remi Collet <remi@fedoraproject.org> - 2.7.6-1
- Update to 2.7.6

* Wed Jan 06 2016 Remi Collet <remi@fedoraproject.org> - 2.7.5-1
- Update to 2.7.5
- raise dependency on Horde_Db >= 2.2.0

* Fri Jul 31 2015 Remi Collet <remi@fedoraproject.org> - 2.7.4-1
- Update to 2.7.4

* Tue Apr 28 2015 Remi Collet <remi@fedoraproject.org> - 2.7.3-1
- Update to 2.7.3

* Wed Feb 11 2015 Remi Collet <remi@fedoraproject.org> - 2.7.2-1
- Update to 2.7.2
- add provides php-composer(horde/horde-prefs)

* Mon Dec 29 2014 Remi Collet <remi@fedoraproject.org> - 2.7.1-1
- Update to 2.7.1
- raise dependency on Horde_Translation >= 2.2.0

* Sat Aug 30 2014 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- Update to 2.7.0

* Sat May 03 2014 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0
- add optional dep on Horde_Cache

* Mon Nov 11 2013 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- Update to 2.5.2

* Mon Oct 28 2013 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- Update to 2.5.1

* Wed Jul 17 2013 Remi Collet <remi@fedoraproject.org> - 2.5.0-1
- Update to 2.5.0

* Fri May 17 2013 Remi Collet <remi@fedoraproject.org> - 2.4.1-1
- Update to 2.4.1
- switch from Conflicts >= max to Requires < max

* Tue May 07 2013 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0
- raise dependency on Horde_Db >= 2.0.3

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 2.3.2-1
- Update to 2.3.2

* Thu Feb 14 2013 Remi Collet <remi@fedoraproject.org> - 2.3.1-1
- Update to 2.3.1

* Tue Feb 12 2013 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0

* Tue Jan 29 2013 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0

* Wed Jan  9 2013 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0
- use local script instead of find_lang
- new test layout (requires Horde_Test 2.1.0)

* Wed Nov  7 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1

* Sat Nov  3 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0

* Thu Jun 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.1.8-1
- Upgrade to 1.1.8

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.1.7-1
- Initial package
