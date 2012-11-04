%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Cli
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Cli
Version:        2.0.0
Release:        1%{?dist}
Summary:        Horde Command Line Interface API

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pear.horde.org
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz
# /usr/lib/rpm/find-lang.sh from fedora 16
Source1:        find-lang.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php-pear
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  gettext

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(%{pear_channel}/Horde_Support) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Support) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Translation) >= 3.0.0
Requires:       php(language) >= 5.3.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pcre php-session

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
Horde_Cli:: API for basic command-line functionality/checks

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
PHPRC=../php.ini %{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}

%if 0%{?fedora} > 13 || 0%{?rhel} > 6
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
%{pear_phpdir}/Horde/Cli
%{pear_phpdir}/Horde/Cli.php
# own locales (non standard) directories, .mo own by find_lang
%dir %{pear_datadir}/Horde_Cli
%dir %{pear_datadir}/Horde_Cli/locale
%dir %{pear_datadir}/Horde_Cli/locale/*
%dir %{pear_datadir}/Horde_Cli/locale/*/LC_MESSAGES

%changelog
* Thu Nov  1 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-1
- Update to 2.0.0 for remi repo

* Thu Sep 20 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.4-2
- backport for remi repo

* Mon Jun 25 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.4-2
- Fix requires

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.4-1
- Initial package
