%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_Form

Name:           php-horde-Horde-Form
Version:        1.1.0
Release:        1%{?dist}
Summary:        Horde Form API

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pear.horde.org
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz

BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(pear.horde.org)

Requires(post): %{__pear}
Requires(postun): %{__pear}

Requires:       php-pear(pear.horde.org/Horde_Core) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Date) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Exception) < 2.0.
Requires:       php-pear(pear.horde.org/Horde_Mime) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Nls) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Token) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Translation) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Util) < 2.0.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(pear.horde.org)

Provides:       php-pear(pear.horde.org/%{pear_name}) = %{version}

%description
The Horde_Form package provides form rendering, validation, and other
functionality for the Horde Application Framework.

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
%{pear_phpdir}/Horde/Form
%{pear_phpdir}/Horde/Form.php
%{pear_datadir}/Horde_Form
%{pear_testdir}/Horde_Form

%changelog
* Thu Jun 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.1.0-1
- Upgrade to 1.1.0

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.6-1
- Initial package
