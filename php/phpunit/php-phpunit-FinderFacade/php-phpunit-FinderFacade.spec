%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name FinderFacade
%global channel pear.phpunit.de

Name:           php-phpunit-FinderFacade
Version:        1.0.7
Release:        1%{?dist}
Summary:        Wrapper for Symfony Finder component

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/sebastianbergmann/finder-facade
Source0:        http://pear.phpunit.de/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-pear(PEAR) >= 1.9.4
BuildRequires:  php-channel(%{channel})

Requires:       php-pear(PEAR) >= 1.9.4
Requires:       php-channel(%{channel})
Requires:       php(language) >= 5.3.3
Requires:       php-ctype
Requires:       php-spl
Requires:       php-pear(pear.netpirates.net/fDOMDocument) >= 1.3.1
Requires:       php-pear(pear.symfony.com/Finder) >= 2.2.0
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
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%dir %{pear_phpdir}/SebastianBergmann
%{pear_phpdir}/SebastianBergmann/%{pear_name}


%changelog
* Mon May 27 2013 Remi Collet <remi@fedoraproject.org> - 1.0.7-1
- Update to 1.0.7 (no change)

* Wed Mar  6 2013 Remi Collet <remi@fedoraproject.org> - 1.0.6-2
- upstream patch for Finder 2.2.0 compatibility

* Thu Jan 10 2013 Remi Collet <remi@fedoraproject.org> - 1.0.6-1
- Version 1.0.6 (stable) - API 1.0.1 (stable)

* Thu Oct 11 2012 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- Version 1.0.5 (stable) - API 1.0.1 (stable)
- Initial packaging

