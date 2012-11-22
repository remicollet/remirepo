%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Imap_Client
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Imap-Client
Version:        2.2.1
Release:        1%{?dist}
Summary:        Horde IMAP abstraction interface

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz
# /usr/lib/rpm/find-lang.sh from fedora 16
Source1:        find-lang.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  gettext
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Stream) >= 1.0.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Mime) >= 2.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-date
Requires:       php-hash
Requires:       php-openssl
Requires:       php-pcre
Requires:       php-spl
BuildRequires:  php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Exception) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Mail) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Mime) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream) >= 1.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Stream) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Util) >= 3.0.0
# Optionnal
Requires:       php-imap
Requires:       php-json
Requires:       php-mbstring
Requires:       php-pear(%{pear_channel}/Horde_Cache) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Cache) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Secret) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Secret) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream_Filter) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Stream_Filter) >= 3.0.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
An abstracted API interface to various IMAP4rev1 (RFC 3501) backend
drivers.


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

%if 0%{?fedora} > 13
%find_lang %{pear_name}
%else
sh %{SOURCE1} %{buildroot} %{pear_name}
%endif


%check
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
%if 0%{?fedora} >= 18
: no test as php segfault, need investigation
%else
phpunit\
    -d include_path=%{buildroot}%{pear_phpdir}:.:%{pear_phpdir} \
    -d date.timezone=UTC \
    .
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
%{pear_phpdir}/Horde/Imap/Client
%{pear_phpdir}/Horde/Imap/Client.php
%{pear_testdir}/%{pear_name}
# own locales (non standard) directories, .mo own by find_lang
%dir %{pear_datadir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}/locale
%dir %{pear_datadir}/%{pear_name}/locale/*
%dir %{pear_datadir}/%{pear_name}/locale/*/LC_MESSAGES


%changelog
* Thu Nov 22 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.2.1-1
- Update to 2.2.1 for remi repo

* Mon Nov 19 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.2.0-1
- Update to 2.2.0 for remi repo

* Mon Nov 12 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.1.6-1
- Update to 2.1.6 for remi repo

* Wed Nov  7 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.1.5-1
- Update to 2.1.5 for remi repo

* Tue Nov  6 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.1.3-1
- Update to 2.1.3 for remi repo

* Sun Nov  4 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.1.1-1
- Update to 2.1.1 for remi repo

* Sat Nov  3 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-1
- Update to 2.0.0 for remi repo

