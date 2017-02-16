# remirepo/fedora spec file for php-justinrainbow-json-schema5
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    9b6ebfeece6efaaeacb6cc061beb69cd007b75c1
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     justinrainbow
%global gh_project   json-schema
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}
%global major        5
%global minor        0.0


# Some sample files, only used for tests
#        "json-schema/JSON-Schema-Test-Suite": "1.1.0",
%global ts_commit    f3d5aeb5ffbe9d9a5a0ceb761dc47c7c4c2efa68
%global ts_short     %(c=%{ts_commit}; echo ${c:0:7})
%global ts_owner     json-schema
%global ts_project   JSON-Schema-Test-Suite
%global ts_version   1.2.0

%global eolv1        0
%global eolv2        0

Name:           php-%{gh_owner}-%{gh_project}%{major}
Version:        %{major}.%{minor}
Release:        1%{?dist}
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
#        "json-schema/JSON-Schema-Test-Suite": "1.2.0",
#        "phpunit/phpunit": "^4.8.22",
#        "phpdocumentor/phpdocumentor": "~2"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.8.22
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)
# For composer schema
BuildRequires:  composer
%endif

# From composer.json, "require": {
#        "php": ">=5.3.3"
Requires:       php(language) >= 5.3.3
# From phpcompatinfo report for version 4.0.1
Requires:       php-curl
Requires:       php-date
Requires:       php-filter
Requires:       php-json
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)
%if %{eolv1}
Obsoletes:      php-JsonSchema < 2
%endif
%if %{eolv2}
Obsoletes:      php-justinrainbow-json-schema < 3
%endif
Requires:       php-cli

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
A PHP Implementation for validating JSON Structures against a given Schema.

This package provides the library version %{major}.

See http://json-schema.org/

Autoloader: %{php_home}/JsonSchema%{major}/autoload.php


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


%build
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

: Library
mkdir -p              %{buildroot}%{php_home}
cp -pr src/JsonSchema %{buildroot}%{php_home}/JsonSchema%{major}

: Command
install -Dpm 0755 bin/validate-json %{buildroot}%{_bindir}/validate-json%{major}


%check
%if %{with_tests}
: Test suite autoloader
cat << 'EOF' | tee vendor/autoload.php
<?php
require '%{buildroot}%{php_home}/JsonSchema%{major}/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('JsonSchema\\Tests\\', 'tests/');
EOF

: Test the command
sed -e 's:%{php_home}:%{buildroot}%{php_home}:' \
    bin/validate-json > bin/validate-json-test
php bin/validate-json-test \
    composer.json \
    /usr/share/composer/res/composer-schema.json

: Upstream test suite
# remirepo:11
run=0
ret=0
if which php56; then
   php56 -d memory_limit=1G %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
   php71 -d memory_limit=1G %{_bindir}/phpunit || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit -d memory_limit=1G --verbose
# remirepo:2
fi
exit $ret
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
%{_bindir}/validate-json%{major}
%{php_home}/JsonSchema%{major}


%changelog
* Thu Feb 16 2017 Remi Collet <remi@fedoraproject.org> - 5.0.0-1
- rename to php-justinrainbow-json-schema5
- update to 5.0.0

* Thu Feb 16 2017 Remi Collet <remi@fedoraproject.org> - 4.1.0-2
- always provide the command as validate-json4

* Fri Dec 23 2016 Remi Collet <remi@fedoraproject.org> - 4.1.0-1
- update to 4.1.0
- drop patch merged upstream

* Mon Dec 12 2016 Remi Collet <remi@fedoraproject.org> - 4.0.1-1
- rename to php-justinrainbow-json-schema4
- update to 4.0.1

* Fri Oct 21 2016 Remi Collet <remi@fedoraproject.org> - 2.0.5-3
- switch from symfony/class-loader to fedora/autoloader

* Thu Jul 21 2016 Remi Collet <remi@fedoraproject.org> - 2.0.5-2
- fix failed test, FTBFS detected by Koschei
  open https://github.com/justinrainbow/json-schema/pull/292

* Thu Jun  2 2016 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- update to 2.0.5

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

