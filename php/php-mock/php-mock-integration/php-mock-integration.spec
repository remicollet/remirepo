# remirepo/fedora spec file for php-mock-integration
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    e83fb65dd20cd3cf250d554cbd4682b96b684f4b
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     php-mock
%global gh_project   php-mock-integration
%global with_tests   0%{!?_without_tests:1}

Name:           php-mock-integration
Version:        1.0.0
Release:        2%{?dist}
Summary:        Integration package for PHP-Mock

Group:          Development/Libraries
License:        WTFPL
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.5
%if %{with_tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "^4|^5"
BuildRequires:  php-composer(php-mock/php-mock)         >= 1
BuildRequires:  php-composer(phpunit/php-text-template) >= 1
BuildRequires:  php-composer(phpunit/phpunit) > 4
%endif

# from composer.json, "require": {
#        "php": ">=5.5",
#        "php-mock/php-mock": "^1",
#        "phpunit/php-text-template": "^1"
Requires:       php(language) >= 5.5
Requires:       php-composer(php-mock/php-mock)         >= 1
Requires:       php-composer(php-mock/php-mock)         <  2
Requires:       php-composer(phpunit/php-text-template) >= 1
Requires:       php-composer(phpunit/php-text-template) <  2
# From phpcompatinfo report from version 1.0.1
# only standard

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
This is a support package for PHP-Mock integration into other frameworks.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

# Same namespace than php-mock, not specific autoloader needed


%build
# Nothing


%install
rm -rf         %{buildroot}
mkdir -p       %{buildroot}%{_datadir}/php/
mkdir -p       %{buildroot}%{_datadir}/php/phpmock
cp -pr classes %{buildroot}%{_datadir}/php/phpmock/integration


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
%{_datadir}/php/phpmock/integration


%changelog
* Mon Feb 22 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- Fix: license is WTFPL

* Fri Feb 12 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package