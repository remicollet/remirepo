%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_Data

Name:           php-horde-Horde-Data
Version:        1.0.7
Release:        2%{?dist}
Summary:        Horde Data API

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pear.horde.org
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz

BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(pear.horde.org)
BuildRequires:  gettext

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(pear.horde.org/Horde_Browser) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Exception) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Icalendar) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Mime) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Translation) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Util) < 2.0.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(pear.horde.org)
Requires:       php-date php-pcre
Requires:       php-common >= 5.2.0

Provides:       php-pear(pear.horde.org/%{pear_name}) = %{version}

%description
A data import and export API, with backends for:
* CSV
* TSV
* iCalendar
* vCard
* vNote
* vTodo

%prep
%setup -q -c

# Create a "localized" php.ini to avoid build warning
cp /etc/php.ini .
echo "date.timezone=UTC" >>php.ini

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
PHPRC=../php.ini %{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}
%find_lang %{pear_name}

%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.horde.org/%{pear_name} >/dev/null || :
fi

%files -f %{pear_name}-%{version}/%{pear_name}.lang
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Data
%{pear_phpdir}/Horde/Data.php
%{pear_testdir}/Horde_Data
# own locales (non standard) directories, .mo own by find_lang
%dir %{pear_datadir}/Horde_Data
%dir %{pear_datadir}/Horde_Data/locale
%dir %{pear_datadir}/Horde_Data/locale/*
%dir %{pear_datadir}/Horde_Data/locale/*/LC_MESSAGES

%changelog
* Mon Jun 25 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.7-2
- Add requires for php-common

* Wed Jun 20 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.7-1
- Upgrade to 1.0.7, fix packaging issues

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.4-1
- Initial package
