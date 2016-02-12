# remirepo/fedora spec file for php-mock-phpunit
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    d2edb32ec05584bb6bd8f1b7e94284022fb12d75
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     php-mock
%global gh_project   php-mock-phpunit
%global with_tests   0%{!?_without_tests:1}

Name:           php-mock-phpunit
Version:        1.1.1
Release:        1%{?dist}
Summary:        Mock built-in PHP functions with PHPUnit.

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

Patch0:         %{name}-upstream.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.5
%if %{with_tests}
BuildRequires:  php-composer(php-mock/php-mock-integration) >= 1
BuildRequires:  php-composer(phpunit/phpunit) > 4
%endif

# from composer.json, "require": {
#        "php": ">=5.5",
#        "phpunit/phpunit": "^4.0.0 || ^5.0.0",
#        "php-mock/php-mock-integration": "^1"
Requires:       php(language) >= 5.5
Requires:       php-composer(phpunit/phpunit)               >= 4
Requires:       php-composer(phpunit/phpunit)               <  6
Requires:       php-composer(php-mock/php-mock-integration) >= 1
Requires:       php-composer(php-mock/php-mock-integration) <  2
# From phpcompatinfo report from version 1.1.1
# only Core

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Mock built-in PHP functions (e.g. time()) with PHPUnit.
This package relies on PHP's namespace fallback policy.
No further extension is needed.


%prep
%setup -q -n %{gh_project}-%{gh_commit}
%patch0 -p1

# Same namespace than php-mock, not specific autoloader needed


%build
# Nothing


%install
rm -rf         %{buildroot}
mkdir -p       %{buildroot}%{_datadir}/php/
mkdir -p       %{buildroot}%{_datadir}/php/phpmock
cp -pr classes %{buildroot}%{_datadir}/php/phpmock/phpunit


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{_datadir}/tests/phpmock/autoload.php';
$fedoraClassLoader->addPrefix('phpmock\\', '%{buildroot}%{_datadir}/php');
EOF

%{_bindir}/phpunit

if which php70; then
   php70 %{_bindir}/phpunit
fi
%else
: bootstrap build with test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json
%doc *.md
%{_datadir}/php/phpmock/phpunit


%changelog
* Fri Feb 12 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- initial package