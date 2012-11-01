%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_Argv

Name:           php-horde-Horde-Argv
Version:        1.0.5
Release:        1%{?dist}
Summary:        Horde command-line argument parsing package

Group:          Development/Libraries
License:        BSD
URL:            http://pear.horde.org
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz

BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  gettext
Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(pear.horde.org/Horde_Exception) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Translation) < 2.0.0
Requires:       php-pear(PEAR) >= 1.7.0
Provides:       php-pear(pear.horde.org/Horde_Argv) = %{version}
BuildRequires:  php-channel(pear.horde.org)
Requires:       php-channel(pear.horde.org)

%description
Classes for parsing command line arguments with various actions, providing
help, grouping options, and more.

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
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

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
%{pear_phpdir}/Horde/Argv
%{pear_testdir}/Horde_Argv
# own locales (non standard) directories, .mo own by find_lang
%dir %{pear_datadir}/Horde_Argv
%dir %{pear_datadir}/Horde_Argv/locale
%dir %{pear_datadir}/Horde_Argv/locale/*
%dir %{pear_datadir}/Horde_Argv/locale/*/LC_MESSAGES

%changelog
* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.5-1
- Initial package
