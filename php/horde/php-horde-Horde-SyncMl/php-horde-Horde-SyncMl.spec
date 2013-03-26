%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_SyncMl
%global pear_channel pear.horde.org

# No run of unit tests - because tests are not ready (oudated)

Name:           php-horde-Horde-SyncMl
Version:        2.0.3
Release:        2%{?dist}
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
Requires:       php-pear(%{pear_channel}/Horde_Translation) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Translation) >= 3.0.0
# Optional
Requires:       php-pear(%{pear_channel}/Horde_Auth) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Auth) >= 3.0.0
# Keep optional : Horde_Core, MDB2

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
