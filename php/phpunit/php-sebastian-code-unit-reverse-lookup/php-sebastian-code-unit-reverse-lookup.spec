# remirepo/fedora spec file for php-sebastian-code-unit-reverse-lookup
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    4419fcdb5eabb9caa61a27c7a1db532a6b55dd18
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   code-unit-reverse-lookup
%global php_home     %{_datadir}/php/SebastianBergmann
%global ns_name      CodeUnitReverseLookup
%if %{bootstrap}
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-sebastian-%{gh_project}
Version:        1.0.1
Release:        1%{?dist}
Summary:        Looks up which function or method a line of code belongs to

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-fedora-autoloader-devel
%if %{with_tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "^5.7 || ^6.0"
# Ignore min version on purpose, avoid bootstrap (tested with 4.8)
BuildRequires:  php-composer(phpunit/phpunit)
%endif

# from composer.json, "require": {
#        "php": "^5.6 || ^7.0"
Requires:       php(language) >= 5.6
# From phpcompatinfo report for version 1.0.0
Requires:       php-reflection
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(sebastian/%{gh_project}) = %{version}


%description
Looks up which function or method a line of code belongs to.

Autoloader: %{php_home}/%{ns_name}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the Autoloader
phpab --template fedora --output src/autoload.php src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/%{ns_name}


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require 'SebastianBergmann/%{ns_name}/autoload.php';
EOF

: Run upstream test suite
# remirepo:13
run=0
ret=0
if which php56; then
  php56 -d include_path=.:%{buildroot}%{_datadir}/php:%{_datadir}/php \
  %{_bindir}/phpunit --verbose || ret=1
   run=1
fi
if which php71; then
  php71 -d include_path=.:%{buildroot}%{_datadir}/php:%{_datadir}/php \
  %{_bindir}/phpunit6 --verbose || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/php -d include_path=.:%{buildroot}%{_datadir}/php:%{_datadir}/php \
%{_bindir}/phpunit --verbose
# remirepo:2
fi
exit $ret
%else
: bootstrap build with test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%dir %{php_home}
%{php_home}/%{ns_name}


%changelog
* Sat Mar  4 2017 Remi Collet <remi@remirepo.net> - 1.0.1-1
- Update to 1.0.1 (no change)

* Mon Oct 31 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- switch to fedora/autoloader

* Sat Feb 13 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
