# spec file for php-phpunit-phpcov
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%global pear_name    phpcov
%global pear_channel pear.phpunit.de

Name:           php-phpunit-phpcov
Version:        1.1.0
Release:        1%{?dist}
Summary:        TextUI front-end for PHP_CodeCoverage

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/sebastianbergmann/phpcov
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-pear(PEAR) >= 1.9.4
BuildRequires:  php-channel(%{pear_channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
# from package.xml
Requires:       php(language) >= 5.3.3
Requires:       php-pear(PEAR) >= 1.9.4
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(components.ez.no/ConsoleTools) >= 1.6
Requires:       php-pear(%{pear_channel}/PHPUnit) >= 3.7.0
Requires:       php-pear(%{pear_channel}/PHP_CodeCoverage) >= 1.2.0
# from phpcompatinfo report for version 1.1.0
Requires:       php-reflection
Requires:       php-spl

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
# Project name
Provides:       phpcov = %{version}


%description
TextUI front-end for PHP_CodeCoverage.


%prep
%setup -q -c

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
%dir %{pear_phpdir}/SebastianBergmann
%{pear_phpdir}/SebastianBergmann/PHPCOV
%{_bindir}/phpcov


%changelog
* Thu Sep 12 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- initial package
