%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name XML_SVG

Name:           php-pear-XML-SVG
Version:        1.1.0
Release:        2%{?dist}
Summary:        API for building SVG documents

Group:          Development/Libraries
# https://pear.php.net/bugs/19690 - Please Provides LICENSE file
License:        LGPLv3
URL:            http://pear.php.net/package/%{pear_name}
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)

Provides:       php-pear(%{pear_name}) = %{version}


%description
This package provides an object-oriented API for building SVG documents.


%prep
%setup -q -c
cd %{pear_name}-%{version}

# https://pear.php.net/bugs/19718 - README is Doc
sed -e '/README/s/role="data"/role="doc"/' \
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
install -Dpm 644 %{name}.xml %{buildroot}%{pear_xmldir}/%{name}.xml


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.php.net/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%dir %{pear_phpdir}/XML
%{pear_phpdir}/XML/SVG.php
%{pear_phpdir}/XML/SVG


%changelog
* Fri Nov 23 2012 Remi Collet <remi@fedoraproject.org> - 1.1.0-2
- fix README Role (from review #872957)

* Sun Nov  4 2012 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Initial package
