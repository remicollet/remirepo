# remirepo/fedora spec file for php-phpunit-diff
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    13edfd8706462032c2f52b4b862974dd46b71c9e
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   diff
%global php_home     %{_datadir}/php
%global pear_name    Diff
%global pear_channel pear.phpunit.de
%if %{bootstrap}
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-phpunit-diff
Version:        1.4.1
Release:        1%{?dist}
Summary:        Diff implementation

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "~4.8"
# min version ignored
BuildRequires:  php-composer(phpunit/phpunit)
%endif

# from composer.json
#      "php": ">=5.3.3"
Requires:       php(language) >= 5.3.3
# from phpcompatinfo report for version 1.1.0
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(sebastian/diff) = %{version}

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
# Package have be renamed
Obsoletes:      php-phpunit-Diff < 1.1.0-2
Provides:       php-phpunit-Diff = %{version}-%{release}


%description
Diff implementation.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

# Restore PSR-0 tree
mkdir  SebastianBergmann
mv src SebastianBergmann/Diff


%build
phpab \
  --output   SebastianBergmann/Diff/autoload.php \
  SebastianBergmann/Diff


%install
rm -rf   %{buildroot}
mkdir -p %{buildroot}%{php_home}/SebastianBergmann
cp -pr                           SebastianBergmann/Diff \
         %{buildroot}%{php_home}/SebastianBergmann/Diff


%if %{with_tests}
%check
%{_bindir}/phpunit --bootstrap SebastianBergmann/Diff/autoload.php

if which php70; then
  php70 %{_bindir}/phpunit --bootstrap SebastianBergmann/Diff/autoload.php
fi
%endif


%clean
rm -rf %{buildroot}

%post
if [ -x %{_bindir}/pear ]; then
  %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md composer.json

%dir %{php_home}/SebastianBergmann
     %{php_home}/SebastianBergmann/Diff


%changelog
* Sun Dec  6 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- update to 1.4.1 (no change)
- run test suite with both php 5 and 7 when available

* Fri Apr  3 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- update to 1.3.0

* Fri Oct  3 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0
- run test suite during build
- generate autoload.php for compatibility
- fix license handling

* Wed Jun 25 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-6
- composer dependencies

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-4
- cleanup pear registry

* Wed Apr 23 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-3
- get sources from github
- run test suite when build --with tests

* Sun Oct 20 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-2
- rename to lowercase

* Thu Sep 12 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- initial package
