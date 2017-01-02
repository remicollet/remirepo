# spec file for php-pear-Net-IMAP
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}

%global pear_channel pear.php.net
%global pear_name    Net_IMAP

# Cannot run test suite which requires a valid IMAP account

Name:           php-pear-Net-IMAP
Version:        1.1.3
Release:        1%{?dist}
Summary:        Provides an implementation of the IMAP protocol

Group:          Development/Libraries
License:        GPLv2+ and PHP
URL:            http://%{pear_channel}/package/%{pear_name}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-date
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-pear(PEAR)
Requires:       php-pear(Net_Socket) >= 1.0.8
# Optional
Requires:       php-pear(Auth_SASL) >= 1.0.2

Provides:       php-pear(%{pear_name}) = %{version}


%description
Provides an implementation of the IMAP4Rev1 protocol using PEAR's
Net_Socket and the optional Auth_SASL class.


%prep
%setup -q -c

cd %{pear_name}-%{version}
cp ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


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
%{pear_phpdir}/Net/IMAP*
%{pear_testdir}/%{pear_name}
%{pear_datadir}/%{pear_name}


%changelog
* Tue Apr 01 2014 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3

* Wed Apr  3 2013 Remi Collet <remi@fedoraproject.org> - 1.1.2-2
- fix license, from review comment #929214

* Fri Mar 29 2013 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- initial pakage
