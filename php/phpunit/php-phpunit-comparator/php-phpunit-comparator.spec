# spec file for php-phpunit-comparator
#
# Copyright (c) 2014-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    1dd8869519a225f7f2b9eb663e225298fade819e
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
Version:        1.1.1
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
#        "sebastian/diff": "~1.2",
#        "sebastian/exporter": "~1.2"
Requires:       php(language) >= 5.3.3
Requires:       php-composer(sebastian/diff)  >= 1.2
Requires:       php-composer(sebastian/diff)  <  2
Requires:       php-composer(sebastian/exporter) >= 1.2
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


%check
%if %{with_tests}
sed -e 's/vendor/src/' -i tests/bootstrap.php
sed -e '/log/d' phpunit.xml.dist >phpunit.xml

phpunit \
  --include-path %{_datadir}/php \
  --bootstrap tests/bootstrap.php
%else
: bootstrap build with test suite disabled
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
* Fri Jan 30 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1
- raise dependency on sebastian/diff >= 1.2
- raise dependency on sebastian/exporter >= 1.2

* Thu Dec  4 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0

* Sun Oct  5 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- enable test suite

* Fri Jul 18 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- add composer dependencies

* Sat May  3 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package