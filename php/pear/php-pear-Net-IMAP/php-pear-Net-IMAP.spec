%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

%global pear_channel pear.php.net
%global pear_name    Net_IMAP

# Cannot run test suite which requires a valid IMAP account

Name:           php-pear-Net-IMAP
Version:        1.1.2
Release:        2%{?dist}
Summary:        Provides an implementation of the IMAP protocol

Group:          Development/Libraries
# https://pear.php.net/bugs/19875
# tests/* are GPL
# docs/* are PHP version 2
# NET/* are PHP
License:        GPLv2+ and PHP
URL:            http://%{pear_channel}/package/%{pear_name}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz
Source1:        http://www.php.net/license/3_01.txt

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
# http://pear.php.net/bugs/19730
%setup -q -c -T
tar xif %{SOURCE0}

cp %{SOURCE1} LICENSE

cd %{pear_name}-%{version}
# https://pear.php.net/bugs/19876
sed -e '/README/s/role="data"/role="doc"/' \
    -e '/docs/s/role="test"/role="doc"/' \
    -e '/phpunit.xml/s/role="data"/role="test"/' \
    ../package.xml >%{name}.xml


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
%doc LICENSE
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Net/IMAP*
%{pear_testdir}/%{pear_name}


%changelog
* Wed Apr  3 2013 Remi Collet <remi@fedoraproject.org> - 1.1.2-2
- fix license, from review comment #929214

* Fri Mar 29 2013 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- initial pakage
