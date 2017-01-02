# remirepo/fedora spec file for php-herrera-io-json
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    60c696c9370a1e5136816ca557c17f82a6fa83f1
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     kherge-abandoned
%global gh_project   php-json
%global php_home     %{_datadir}/php
%global ns_vendor    Herrera
%global ns_project   Json
%global c_vendor     herrera-io
%global c_project    json
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{c_vendor}-%{c_project}
Version:        1.0.3
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        A library for simplifying JSON linting and validation

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

Source1:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-composer(justinrainbow/json-schema) >= 1.0
BuildRequires:  php-composer(seld/jsonlint) >= 1.0
# From composer.json, "require-dev": {
#        "herrera-io/phpunit-test-case": "1.*",
#        "mikey179/vfsStream": "1.1.0",
#        "phpunit/phpunit": "3.7.*"
BuildRequires:  php-composer(%{c_vendor}/phpunit-test-case) >= 1
BuildRequires:  php-composer(mikey179/vfsStream) >= 1.1.0
BuildRequires:  php-composer(phpunit/phpunit) >= 3.7
# Autoloader
BuildRequires:  php-composer(symfony/class-loader)
%endif

# from composer.json, "require": {
#        "php": ">=5.3.3",
#        "ext-json": "*",
#        "justinrainbow/json-schema": ">=1.0,<2.0-dev",
#        "seld/jsonlint": ">=1.0,<2.0-dev"
Requires:       php(language) >= 5.3.3
Requires:       php-json
Requires:       php-composer(justinrainbow/json-schema) >= 1.0
Requires:       php-composer(justinrainbow/json-schema) <  2
Requires:       php-composer(seld/jsonlint) >= 1.0
Requires:       php-composer(seld/jsonlint) <  2
# Autoloader
Requires:       php-composer(symfony/class-loader)
# from phpcompatinfo report for version 1.2.1
Requires:       php-pcre

Provides:       php-composer(%{c_vendor}/%{c_project}) = %{version}


%description
%{summary}.

Uses the justinrainbow/json-schema and seld/jsonlint libraries to lint and
validate JSON data. Also decodes JSON data as to only lint when an error is
encountered, minimizing performance impact.

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE1} src/lib/%{ns_vendor}/%{ns_project}/autoload.php


%build
# Empty


%install
rm -rf                      %{buildroot}
mkdir -p                    %{buildroot}%{php_home}
cp -pr src/lib/%{ns_vendor} %{buildroot}%{php_home}/%{ns_vendor}
cp -p  src/lib/*php         %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/


%check
%if %{with_tests}
cat << 'EOF' | tee src/tests/bootstrap.php
<?php
// This library
require_once '%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';
// Dependencies
require_once '%{php_home}/%{ns_vendor}/PHPUnit/autoload.php';
require_once '%{php_home}/org/bovigo/vfs/autoload.php';
// From old bootstrap
org\bovigo\vfs\vfsStreamWrapper::register();
EOF

%{_bindir}/phpunit \
   --verbose
%else
: test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%doc composer.json
%dir %{php_home}/%{ns_vendor}
     %{php_home}/%{ns_vendor}/%{ns_project}


%changelog
* Wed Oct 21 2015 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- initial package