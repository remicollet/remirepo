# spec file for php-theseer-fDOMDocument
#
# Copyright (c) 2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#

%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name fDOMDocument
%global channel   pear.netpirates.net

Name:           php-theseer-fDOMDocument
Version:        1.4.3
Release:        1%{?dist}
Summary:        An Extension to PHP standard DOM

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/theseer/fDOMDocument
Source0:        http://%{channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-pear(PEAR) >= 1.9.1
BuildRequires:  php-channel(%{channel})
# For test
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit)
BuildRequires:  php-dom
BuildRequires:  php-libxml

Requires:       php(language) >= 5.3.3
Requires:       php-dom
Requires:       php-libxml
Requires:       php-pcre
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.9.1
Requires:       php-channel(%{channel})
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}


%description
An Extension to PHP's standard DOM to add various convenience methods
and exceptions by default


%prep
%setup -q -c

# Package.xml is V2
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


%check
cd %{pear_name}-%{version}
sed -e s:autoload:TheSeer/fDOMDocument/autoload: \
    phpunit.xml.dist >phpunit.xml
phpunit -d date.timezone=UTC


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
%dir %{pear_phpdir}/TheSeer
%{pear_phpdir}/TheSeer/%{pear_name}
%{pear_testdir}/%{pear_name}


%changelog
* Sat Dec 21 2013 Remi Collet <remi@fedoraproject.org> - 1.4.3-1
- Update to 1.4.3 (stable)

* Sun Jun 30 2013 Remi Collet <remi@fedoraproject.org> - 1.4.2-1
- Update to 1.4.2

* Sun Apr 28 2013 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- Update to 1.4.1

* Fri Apr 26 2013 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- Update to 1.4.0

* Sun Oct 28 2012 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- Version 1.3.2 (stable) - API 1.3.0 (stable)
- run test units

* Thu Oct 11 2012 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Version 1.3.1 (stable) - API 1.3.0 (stable)
- Initial packaging

