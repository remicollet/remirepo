%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name FinderFacade
%global channel pear.phpunit.de

Name:           php-phpunit-FinderFacade
Version:        1.0.6
Release:        1%{?dist}
Summary:        Wrapper for Symfony Finder component

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/sebastianbergmann/finder-facade
Source0:        http://pear.phpunit.de/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.9.4
BuildRequires:  php-channel(%{channel})

Requires:       php-pear(PEAR) >= 1.9.2
Requires:       php-channel(%{channel})
Requires:       php(language) >= 5.3.3
Requires:       php-ctype
Requires:       php-spl
Requires:       php-pear(pear.netpirates.net/fDOMDocument) >= 1.3.1
Requires:       php-pear(pear.symfony.com/Finder) >= 2.1.0
Conflicts:      php-pear(pear.symfony.com/Finder) >= 2.1.99
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}


%description
Convenience wrapper for Symfony's Finder component.


%prep
%setup -q -c
mv package.xml %{pear_name}-%{version}/%{name}.xml


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
    %{channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/SebastianBergmann/%{pear_name}
%doc %{pear_docdir}/%{pear_name}


%changelog
* Thu Jan 10 2013 Remi Collet <remi@fedoraproject.org> - 1.0.6-1
- Version 1.0.6 (stable) - API 1.0.1 (stable)

* Thu Oct 11 2012 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- Version 1.0.5 (stable) - API 1.0.1 (stable)
- Initial packaging

