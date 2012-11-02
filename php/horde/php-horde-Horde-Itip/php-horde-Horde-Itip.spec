%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_Itip

Name:           php-horde-Horde-Itip
Version:        1.0.7
Release:        1%{?dist}
Summary:        iTip invitation response handling

Group:          Development/Libraries
License:        LGPL-2.1
URL:            http://pear.horde.org/package/Horde_Itip
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz

BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.7.0
Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(pear.horde.org/Horde_Icalendar) >= 1.0.0beta1
Requires:       php-pear(pear.horde.org/Horde_Icalendar) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Mime) >= 1.0.0beta1
Requires:       php-pear(pear.horde.org/Horde_Mime) < 2.0.0
Requires:       php-pear(PEAR) >= 1.7.0
Provides:       php-pear(pear.horde.org/Horde_Itip) = %{version}
BuildRequires:  php-channel(pear.horde.org)
Requires:       php-channel(pear.horde.org)

%description
This package to generates MIME encapsuled responses to iCalendar
invitations.

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
%{pear_phpdir}/Horde/Itip
%{pear_phpdir}/Horde/Itip.php
%{pear_datadir}/Horde_Itip
%{pear_testdir}/Horde_Itip

%changelog
