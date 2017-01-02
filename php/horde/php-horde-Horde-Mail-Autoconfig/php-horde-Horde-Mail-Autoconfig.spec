# remirepo/fedora spec file for php-horde-Horde-Mail-Autoconfig
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Mail_Autoconfig
%global pear_channel pear.horde.org
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-horde-Horde-Mail-Autoconfig
Version:        1.0.3
Release:        1%{?dist}
Summary:        Horde Mail Autoconfiguration

Group:          Development/Libraries
License:        LGPLv2
URL:            http://pear.horde.org/
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
%if %{with_tests}
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
# From package.xml
Requires:       php(language) >= 5.3.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Http) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Http) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Imap_Client) >= 2.20.1
Requires:       php-pear(%{pear_channel}/Horde_Imap_Client) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) >= 2.1.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Smtp) >= 1.1.0
Requires:       php-pear(%{pear_channel}/Horde_Smtp) <  2.0.0
Requires:       php-pear(Net_DNS2) >= 1.3.0
Requires:       php-simplexml

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-mail-autoconfig) = %{version}


%description
Attempts to automatically determine configuration options for various
remote mail services (IMAP/POP3/SMTP).


%prep
%setup -q -c

cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf %{buildroot}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%check
%if %{with_tests}
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)

%{_bindir}/phpunit .

if which php70; then
   php70 %{_bindir}/phpunit .
fi
%else
: Test disabled, missing '--with tests' option.
%endif


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Mail/Autoconfig/
%{pear_phpdir}/Horde/Mail/Autoconfig.php
%{pear_testdir}/%{pear_name}


%changelog
* Wed Mar 09 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3 (no change)
- PHP 7 compatible version
- run test suite with both PHP 5 and 7 when available

* Fri Jan 09 2015 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2
- add provides php-composer(horde/horde-mail-autoconfig)

* Thu Oct 02 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Tue Jul  8 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- Initial package
