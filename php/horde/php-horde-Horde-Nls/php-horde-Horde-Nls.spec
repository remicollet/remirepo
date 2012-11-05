%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Nls
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Nls
Version:        2.0.0
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
BuildRequires:  gettext
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-date
Requires:       php-pcre
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Util) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Translation) >= 3.0.0
# Optionnal
Requires:       php-pecl(geoip)
Requires:       php-pear(Net_DNS2)

Provides:       php-pear(%{pear_channel}/Horde_Nls) = %{version}

%description
Common methods for handling language data, timezones, and hostname->country
lookups.

%prep
%setup -q -c -T
tar xif %{SOURCE0}

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

%if 0%{?fedora} > 13
%find_lang %{pear_name}
%else
sh %{SOURCE1} %{buildroot} %{pear_name}
%endif


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
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
* Thu Nov  1 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-1
- Update to 2.0.0 for remi repo

* Sun Aug 19 2012 Remi Collet <remi@fedoraproject.org> - 1.1.6-3
- rebuilt for new pear_datadir

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.6-1
- Upgrade to 1.1.6, backport for remi repo

* Thu Jun 14 2012 Nick Bebout <nb@fedoraproject.org> - 1.1.6-1
- Upgrade to 1.1.6

* Thu Mar 22 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.5-1
- update to 1.1.4, backport for remi repo

* Wed Mar 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.1.5-1
- Update to 1.1.5

* Mon Feb 20 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.4-1
- update to 1.1.4
- backport for remi repo
- hack for find_lang on old distro

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.1.3-1
- Initial package
