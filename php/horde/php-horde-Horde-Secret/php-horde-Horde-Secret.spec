%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Secret
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Secret
Version:        2.0.0
Release:        1%{?dist}
Summary:        Secret Encryption API

Group:          Development/Libraries
License:        LGPL-2.1
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear
BuildRequires:  php-channel(%{pear_channel})
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.0.0
BuildRequires:  php-pear(Crypt_Blowfish) >= 1.0.1

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-hash
Requires:       php-session
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(PEAR)
Requires:       php-pear(Crypt_Blowfish) >= 1.0.1
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Exception) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Support) >= 3.0.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
An API for encrypting and decrypting small pieces of data with the use of a
shared key.

%prep
%setup -q -c -T
tar xif %{SOURCE0}

cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml


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


%check
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
# Test suite not ready
sed -e 's/E_ALL.*E_STRICT/E_ALL \& ~E_STRICT/' -i Autoload.php
phpunit -d date.timezone=UTC AllTests.php || exit 0


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
%{pear_phpdir}/Horde/Secret
%{pear_phpdir}/Horde/Secret.php
%{pear_testdir}/%{pear_name}


%changelog
* Sat Nov  3 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-1
- Initial package

