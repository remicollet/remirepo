%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Mongo
%global pear_channel pear.horde.org
%global prever       RC1

Name:           php-horde-Horde-Mongo
Version:        1.0.0
Release:        0.2.%{prever}%{?dist}
Summary:        Horde Mongo Configuration

Group:          Development/Libraries
License:        LGPLv2
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}%{?prever}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-spl
Requires:       php-pecl(mongo) >= 1.3.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
Provides an API to ensure that the PECL Mongo extension can be used
consistently across various Horde packages.

%prep
%setup -q -c

cd %{pear_name}-%{version}%{?prever}
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}%{?prever}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}%{?prever}
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
%dir %{pear_phpdir}/Horde
%{pear_phpdir}/Horde/Mongo


%changelog
* Thu May 30 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.RC1
- update to 1.0.0RC1

* Mon May  6 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.beta1
- initial package
