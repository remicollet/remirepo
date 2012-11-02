%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_Imap_Client

Name:           php-horde-Horde-Imap-Client
Version:        1.5.4
Release:        1%{?dist}
Summary:        Horde IMAP abstraction interface

Group:          Development/Libraries
License:        LGPL-2.1
URL:            http://pear.horde.org/package/Horde_Imap_Client
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz

BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.7.0
Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(pear.horde.org/Horde_Exception) >= 1.0.0
Requires:       php-pear(pear.horde.org/Horde_Exception) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Mail) >= 1.1.0
Requires:       php-pear(pear.horde.org/Horde_Mail) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Mime) >= 1.4.0
Requires:       php-pear(pear.horde.org/Horde_Mime) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Util) >= 1.0.0
Requires:       php-pear(pear.horde.org/Horde_Util) < 2.0.0
Requires:       php-pear(PEAR) >= 1.7.0
Provides:       php-pear(pear.horde.org/Horde_Imap_Client) = %{version}
BuildRequires:  php-channel(pear.horde.org)
Requires:       php-channel(pear.horde.org)

%description
An abstracted API interface to various IMAP4rev1 (RFC 3501) backend
drivers.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{name}.xml

cd %{pear_name}-%{version}

%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

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
%{pear_phpdir}/Horde/Imap/Client
%{pear_phpdir}/Horde/Imap/Client.php
%{pear_datadir}/Horde_Imap_Client
%{pear_testdir}/Horde_Imap_Client

%changelog
