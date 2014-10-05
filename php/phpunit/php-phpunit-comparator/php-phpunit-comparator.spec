# spec file for php-phpunit-comparator
#
# Copyright (c) 2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    e54a01c0da1b87db3c5a3c4c5277ddf331da4aef
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   comparator
%global php_home     %{_datadir}/php/SebastianBergmann
%if %{bootstrap}
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-phpunit-comparator
Version:        1.0.1
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
#        "php": ">=5.3.3",
#        "sebastian/diff": "~1.1",
#        "sebastian/exporter": "~1.0"
Requires:       php(language) >= 5.3.3
Requires:       php-composer(sebastian/diff)  >= 1.1
Requires:       php-composer(sebastian/diff)  <  2
Requires:       php-composer(sebastian/exporter) >= 1.0
Requires:       php-composer(sebastian/exporter) <  2
# from phpcompatinfo report for version 1.0.0
Requires:       php-date
Requires:       php-dom
Requires:       php-spl

Provides:       php-composer(sebastian/comparator) = %{version}


%description
This component provides the functionality to compare PHP values for equality.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the Autoloader
phpab --output src/autoload.php src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/Comparator


%if %{with_tests}
%check
sed -e 's/vendor/src/' -i tests/bootstrap.php

if [ -d /usr/share/php/PHPUnit ]
then
  # Hack PHPUnit 4 autoloader to not use system library
  mkdir PHPUnit
  sed -e 's:SebastianBergmann/Comparator:src:' \
    -e 's:dirname(__FILE__):"/usr/share/php/PHPUnit":' \
    /usr/share/php/PHPUnit/Autoload.php \
    >PHPUnit/Autoload.php
fi

phpunit \
  --bootstrap tests/bootstrap.php \
  -d date.timezone=UTC
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README.md composer.json
%{!?_licensedir:%global license %%doc}
%license LICENSE

%{php_home}/Comparator


%changelog
* Sun Oct  5 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- enable test suite

* Fri Jul 18 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- add composer dependencies

* Sat May  3 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package