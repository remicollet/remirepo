%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name fDOMDocument
%global channel   pear.netpirates.net

Name:           php-theseer-fDOMDocument
Version:        1.3.1
Release:        1%{?dist}
Summary:        An Extension to PHP standard DOM

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/theseer/fDOMDocument
Source0:        http://%{channel}/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.9.1
BuildRequires:  php-channel(%{channel})

Requires:       php-pear(PEAR) >= 1.9.1
Requires:       php-channel(%{channel})
Requires:       php-common >= 5.3.3
Requires:       php-dom
Requires:       php-libxml
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}


%description
An Extension to PHP's standard DOM to add various convinience methods
and exceptions by default


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
%{pear_phpdir}/TheSeer/%{pear_name}


%changelog
* Thu Oct 11 2012 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- Version 1.3.1 (stable) - API 1.3.0 (stable)
- Initial packaging

