# remirepo/fedora spec file for php-justinrainbow-json-schema
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    5c133a3e336c2b35a4233f5da4cc15f083ea128d
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     justinrainbow
%global gh_project   json-schema
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

# Some sample files, only used for tests
#        "json-schema/JSON-Schema-Test-Suite": "1.1.0",
%global ts_commit    f3d5aeb5ffbe9d9a5a0ceb761dc47c7c4c2efa68
%global ts_short     %(c=%{ts_commit}; echo ${c:0:7})
%global ts_owner     json-schema
%global ts_project   JSON-Schema-Test-Suite
%global ts_version   1.2.0

%global eolv1   0
%if 0
%global with_script  0
%else
%global with_script  1
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.0.4
Release:        2%{?dist}
Summary:        A library to validate a json schema

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
# git snapshot to get upstream test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        https://github.com/%{ts_owner}/%{ts_project}/archive/%{ts_commit}/%{ts_project}-%{ts_version}-%{ts_short}.tar.gz
Source2:        %{name}-autoload.php
Source3:        %{name}-makesrc.sh

# Autoloader
Patch0:         %{name}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# For tests
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-curl
BuildRequires:  php-date
BuildRequires:  php-filter
BuildRequires:  php-json
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
BuildRequires:  php-spl
# From composer.json, "require-dev": {
#        "json-schema/JSON-Schema-Test-Suite": "1.1.0",
#        "phpunit/phpunit": "^4.8.22",
#        "phpdocumentor/phpdocumentor": "~2"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.8.22
# Autoloader
BuildRequires:  php-composer(symfony/class-loader) >= 2.5
# For composer schema
BuildRequires:  composer
%endif

# From composer.json, "require": {
#        "php": ">=5.3.3"
Requires:       php(language) >= 5.3.3
# From phpcompatinfo report for version 2.0.0
Requires:       php-curl
Requires:       php-date
Requires:       php-filter
Requires:       php-json
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-spl
# Autoloader (2.5 for PSR-4)
Requires:       php-composer(symfony/class-loader) >= 2.5
%if %{eolv1}
Obsoletes:      php-JsonSchema < 2
%endif
%if %{with_script}
Requires:       php-cli
# previous version provides the validate-json command
Conflicts:      php-JsonSchema < 1.6.1-3
%endif

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
A PHP Implementation for validating JSON Structures against a given Schema.
%if %{with_script}
This package provides the library version 2 and the validate-json command.
The php-JsonSchema package provides the library version 1.
%else
This package provides the library version 2.
The php-JsonSchema package provides the library version 1
and the validate-json command.
%endif
See http://json-schema.org/

Autoloader: %{php_home}/JsonSchema2/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit} -a 1

%patch0 -p0 -b .rpm

cp %{SOURCE2} src/JsonSchema/autoload.php

: Needed for the test suite - use composer default path, as easier
mkdir -p vendor/json-schema/JSON-Schema-Test-Suite
mv %{ts_project}-%{ts_commit}/tests \
   vendor/json-schema/JSON-Schema-Test-Suite/tests

: But without online tests
find vendor/json-schema/JSON-Schema-Test-Suite/tests \
   -name \*.json \
   -exec grep -q 'http://' {} \; \
   -exec rm {} \; \
   -print

%if ! %{with_script}
chmod -x bin/validate-json
%endif


%build
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

: Library
mkdir -p              %{buildroot}%{php_home}
cp -pr src/JsonSchema %{buildroot}%{php_home}/JsonSchema2

%if %{with_script}
: Command
install -Dpm 0755 bin/validate-json %{buildroot}%{_bindir}/validate-json
%endif


%check
%if %{with_tests}
: Test suite autoloader
cat << 'EOF' | tee vendor/autoload.php
<?php
require '%{buildroot}%{php_home}/JsonSchema2/autoload.php';
$fedoraPsr4ClassLoader->addPrefix('JsonSchema\\Tests\\', 'tests/');
EOF

: Test the command
sed -e 's:%{php_home}:%{buildroot}%{php_home}:' \
    bin/validate-json > bin/validate-json-test
php bin/validate-json-test \
    composer.json \
    /usr/share/composer/res/composer-schema.json

: Upstream test suite
%{_bindir}/phpunit --verbose

if which php70; then
   php70 %{_bindir}/phpunit --verbose
fi
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json
%doc *.md
%if %{with_script}
%{_bindir}/validate-json
%else
%doc bin/validate-json
%endif
%{php_home}/JsonSchema2


%changelog
* Wed Jun  1 2016 Remi Collet <remi@fedoraproject.org> - 2.0.4-2
- add the validate-json command, dropped from php-JsonSchema

* Wed May 25 2016 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- update to 2.0.4
- use json-schema/JSON-Schema-Test-Suite 1.2.0

* Wed May 11 2016 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- update to 2.0.3
- use json-schema/JSON-Schema-Test-Suite 1.1.2

* Fri Apr 29 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1

* Fri Apr 15 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- initial package, version 2.0.0

