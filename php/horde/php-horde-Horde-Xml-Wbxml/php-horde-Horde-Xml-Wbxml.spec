%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_Xml_Wbxml

Name:           php-horde-Horde-Xml-Wbxml
Version:        1.0.3
Release:        1%{?dist}
Summary:        Provides an API for encoding and decoding WBXML documents

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pear.horde.org
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz

BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.7.0
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(pear.horde.org/%{pear_name}) = %{version}
Requires:       php-pear(pear.horde.org/Horde_Util) < 2.0.0
Requires:       php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(pear.horde.org)
Requires:       php-channel(pear.horde.org)

%description
This package provides encoding and decoding of WBXML (Wireless Binary XML)
documents. WBXML is used in SyncML for transferring smaller amounts of data
with wireless devices.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{name}.xml

# Create a "localized" php.ini to avoid build warning
cp /etc/php.ini .
echo "date.timezone=UTC" >>php.ini

cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
PHPRC=../php.ini %{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}

%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.horde.org/%{pear_name} >/dev/null || :
fi

%files
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Xml/Wbxml
%{pear_phpdir}/Horde/Xml/Wbxml.php
%{pear_testdir}/Horde_Xml_Wbxml

%changelog
* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.3-1
- Initial package
