%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    PHPUnit_Story
%global pear_channel pear.phpunit.de

Name:           php-phpunit-PHPUnit-Story
Version:        1.0.1
Release:        1%{?dist}
Summary:        Story extension for PHPUnit to facilitate Behaviour-Driven Development

Group:          Development/Libraries
License:        BSD
URL:            http://www.phpunit.de
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.2.7
BuildRequires:  php-pear(PEAR) >= 1.9.4
BuildRequires:  php-channel(%{pear_channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.2.7
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.9.4
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/PHPUnit) >= 3.6.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
Story extension for PHPUnit to facilitate Behaviour-Driven Development

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
%{pear_phpdir}/PHPUnit/Extensions/Story


%changelog
* Thu Mar 28 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.0.1-1
- initial package
