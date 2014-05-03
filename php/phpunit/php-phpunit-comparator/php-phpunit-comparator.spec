# spec file for php-phpunit-comparator
#
# Copyright (c) 2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    f7069ee51fa9fb6c038e16a9d0e3439f5449dcf2
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   comparator
%global php_home     %{_datadir}/php/SebastianBergmann
# Circular dependency with phpunit
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-phpunit-comparator
Version:        1.0.0
Release:        1%{?dist}
Summary:        Compare PHP values for equality

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
%endif

# from composer.json
Requires:       php(language) >= 5.3.3
Requires:       php-phpunit-diff >= 1.1
Requires:       php-phpunit-exporter >= 1.0
# from phpcompatinfo report for version 1.0.0
Requires:       php-date
Requires:       php-dom
Requires:       php-spl


%description
This component provides the functionality to compare PHP values for equality.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the Autoloader
phpab --output src/autoload.php src
cat src/autoload.php


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/Comparator


%if %{with_tests}
%check
sed -e 's/vendor/src/' -i tests/bootstrap.php
phpunit \
  --bootstrap tests/bootstrap.php \
  -d date.timezone=UTC
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README.md composer.json

%{php_home}/Comparator


%changelog
* Sat May  3 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package