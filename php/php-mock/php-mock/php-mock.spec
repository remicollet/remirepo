# remirepo/fedora spec file for php-mock
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    bfa2d17d64dbf129073a7ba2051a96ce52749570
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     php-mock
%global gh_project   php-mock
%global with_tests   0%{!?_without_tests:1}

Name:           php-mock
Version:        1.0.1
Release:        2%{?dist}
Summary:        PHP-Mock can mock built-in PHP functions

Group:          Development/Libraries
License:        WTFPL
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz
Source1:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.5
%if %{with_tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "^4|^5"
BuildRequires:  php-composer(phpunit/php-text-template) >= 1
BuildRequires:  php-composer(phpunit/phpunit) > 4
%endif
# For autoloader
BuildRequires: php-composer(symfony/class-loader)

# from composer.json, "require": {
#        "php": ">=5.5",
#        "phpunit/php-text-template": "^1"
Requires:       php(language) >= 5.5
Requires:       php-composer(phpunit/php-text-template) >= 1
Requires:       php-composer(phpunit/php-text-template) <  2
# From phpcompatinfo report from version 1.0.1
Requires:       php-date
Requires:       php-reflection
Requires:       php-spl
# For autoloader
Requires:       php-composer(symfony/class-loader)
%if 0%{?fedora} > 21
# from composer.json, "suggest": {
#        "php-mock/php-mock-phpunit": "Allows integration into PHPUnit testcase with the trait PHPMock.",
#        "php-mock/php-mock-mockery": "Allows using PHPMockery for Mockery integration"
Suggests:       php-composer(php-mock/php-mock-phpunit)
Suggests:       php-composer(php-mock/php-mock-mockery)
%endif

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
PHP-Mock can mock built-in PHP functions (e.g. time()).
PHP-Mock relies on PHP's namespace fallback policy.
No further extension is needed.

Autoloader: %{_datadir}/php/phpmock/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE1} classes/autoload.php


%build
# Nothing


%install
rm -rf            %{buildroot}
# Library
mkdir -p          %{buildroot}%{_datadir}/php/
cp -pr classes    %{buildroot}%{_datadir}/php/phpmock
# Unit tests
mkdir -p          %{buildroot}%{_datadir}/tests
cp -pr tests/unit %{buildroot}%{_datadir}/tests/phpmock
cat <<'EOF' | tee %{buildroot}%{_datadir}/tests/phpmock/autoload.php
<?php
require_once '%{_datadir}/php/phpmock/autoload.php';
$fedoraClassLoader->addPrefix('phpmock\\', '%{_datadir}/tests');
EOF


%check
%if %{with_tests}
%{_bindir}/phpunit --bootstrap %{buildroot}%{_datadir}/php/phpmock/autoload.php

if which php70; then
   php70 %{_bindir}/phpunit --bootstrap %{buildroot}%{_datadir}/php/phpmock/autoload.php
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
%{_datadir}/php/phpmock
%{_datadir}/tests/phpmock


%changelog
* Mon Feb 22 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-2
- Fix: license is WTFPL, from review #1306968

* Fri Feb 12 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- initial package