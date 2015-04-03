# spec file for php-phpunit-environment
#
# Copyright (c) 2014-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    5a8c7d31914337b69923db26c4221b81ff5a196e
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   environment
%global php_home     %{_datadir}/php
%if %{bootstrap}
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-phpunit-environment
Version:        1.2.2
Release:        1%{?dist}
Summary:        Handle HHVM/PHP environments

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "~4.4"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.4
%endif

# from composer.json, "require": {
#        "php": ">=5.3.3"
Requires:       php(language) >= 5.3.3

Provides:       php-composer(sebastian/environment) = %{version}


%description
This component provides functionality that helps writing PHP code that
has runtime-specific (PHP / HHVM) execution paths.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

# Restore PSR-0 tree
mkdir  SebastianBergmann
mv src SebastianBergmann/Environment


%build
# Generate the Autoloader
%{_bindir}/phpab \
   --output SebastianBergmann/Environment/autoload.php \
   SebastianBergmann/Environment


%install
rm -rf   %{buildroot}
mkdir -p %{buildroot}%{php_home}/SebastianBergmann
cp -pr                           SebastianBergmann/Environment \
         %{buildroot}%{php_home}/SebastianBergmann/Environment


%if %{with_tests}
%check
%{_bindir}/phpunit --bootstrap SebastianBergmann/Environment/autoload.php
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md composer.json
%dir %{php_home}/SebastianBergmann
     %{php_home}/SebastianBergmann/Environment


%changelog
* Fri Apr  3 2015 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- update to 1.2.2
- fix license handling

* Tue Dec  2 2014 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- update to 1.2.1

* Sat Oct 25 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0

* Wed Oct  8 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0

* Sun Oct  5 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- enable test suite

* Wed Jun 25 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-4
- composer dependencies

* Wed Apr 23 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- add generated autoload.php

* Tue Apr  1 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package