%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_Nls

Name:           php-horde-Horde-Nls
Version:        1.1.4
Release:        1%{?dist}
Summary:        Native Language Support (NLS)

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pear.horde.org
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz
# /usr/lib/rpm/find-lang.sh from fedora 16
Source1:        find-lang.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(pear.horde.org)
BuildRequires:  gettext

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(pear.horde.org/Horde_Util) >= 1.0.0
Requires:       php-pear(pear.horde.org/Horde_Util) < 2.0.0
# Optionnal
Requires:       php-pecl(geoip)

Provides:       php-pear(pear.horde.org/Horde_Nls) = %{version}

%description
Common methods for handling language data, timezones, and hostname->country
lookups.

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
rm -rf $RPM_BUILD_ROOT
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}

%if 0%{?fedora} > 13
%find_lang %{pear_name}
%else
sh %{SOURCE1} $RPM_BUILD_ROOT %{pear_name}
%endif
head %{pear_name}.lang


%clean
rm -rf $RPM_BUILD_ROOT

%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.horde.org/%{pear_name} >/dev/null || :
fi


%files -f %{pear_name}-%{version}/%{pear_name}.lang
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Nls
%{pear_phpdir}/Horde/Nls.php
# own locales (non standard) directories, .mo own by find_lang
%dir %{pear_datadir}/Horde_Nls
%dir %{pear_datadir}/Horde_Nls/locale
%dir %{pear_datadir}/Horde_Nls/locale/*
%dir %{pear_datadir}/Horde_Nls/locale/*/LC_MESSAGES

%changelog
* Mon Feb 20 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.4-1
- update to 1.1.4
- backport for remi repo
- hack for find_lang on old distro

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.1.3-1
- Initial package
