%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_Crypt

Name:           php-horde-Horde-Crypt
Version:        1.1.2
Release:        1%{?dist}
Summary:        Horde Cryptography API

Group:          Development/Libraries
License:        LGPLv2
URL:            http://pear.horde.org
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz

BuildArch:      noarch

BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(pear.horde.org)
BuildRequires:  gettext

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(pear.horde.org/Horde_Exception) >= 1.0.0
Requires:       php-pear(pear.horde.org/Horde_Exception) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Mime) >= 1.0.0
Requires:       php-pear(pear.horde.org/Horde_Mime) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Stream_Filter) >= 1.0.0
Requires:       php-pear(pear.horde.org/Horde_Stream_Filter) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Translation) >= 1.0.0
Requires:       php-pear(pear.horde.org/Horde_Translation) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Util) >= 1.0.0
Requires:       php-pear(pear.horde.org/Horde_Util) < 2.0.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(pear.horde.org)

Provides:       php-pear(pear.horde.org/Horde_Crypt) = %{version}

%description
The Horde_Crypt package class provides an API for various cryptographic
systems.

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
# Expand this as needed to avoid owning dirs owned by our dependencies
# and to avoid unowned dirs
%{pear_phpdir}/Horde/Crypt/Exception.php
%{pear_phpdir}/Horde/Crypt/Pgp.php
%{pear_phpdir}/Horde/Crypt/Smime.php
%{pear_phpdir}/Horde/Crypt/Translation.php
%{pear_phpdir}/Horde/Crypt.php
%{pear_testdir}/Horde_Crypt
# own locales (non standard) directories, .mo own by find_lang
%dir %{pear_datadir}/Horde_Crypt
%dir %{pear_datadir}/Horde_Crypt/locale
%dir %{pear_datadir}/Horde_Crypt/locale/*
%dir %{pear_datadir}/Horde_Crypt/locale/*/LC_MESSAGES

%changelog
* Thu Jun 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.1.2-1
- Initial package
