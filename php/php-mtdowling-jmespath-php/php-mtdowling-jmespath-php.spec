#
# RPM spec file for php-mtdowling-jmespath-php
#
# Copyright (c) 2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     jmespath
%global github_name      jmespath.php
%global github_version   2.1.0
%global github_commit    88b6d646de963396dd227d028cce114fe85f9857

%global composer_vendor  mtdowling
%global composer_project jmespath.php

# "php": ">=5.4.0"
%global php_min_ver 5.4.0

# Build using "--without tests" to disable tests
%global with_tests  %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-jmespath-php
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Declaratively specify how to extract elements from a JSON document

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# For autoload generation
BuildRequires: %{_bindir}/phpab
%if %{with_tests}
# For tests
## composer.json
BuildRequires: %{_bindir}/phpunit
BuildRequires: php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 2.1.0)
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 2.1.0)
Requires:      php-json
Requires:      php-pcre
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
JMESPath (pronounced "jaymz path") allows you to declaratively specify how to
extract elements from a JSON document. jmespath.php allows you to use JMESPath
in PHP applications with PHP data structures.


%prep
%setup -qn %{github_name}-%{github_commit}

: Modify bin script
sed -e "s#/usr/bin/env php#%{_bindir}/php#" \
    -e "s#.*require.*autoload.*#require '%{phpdir}/JmesPath/autoload.php';#" \
    -i bin/jp.php



%build
: Generate autoloader
%{_bindir}/phpab --nolower --output src/autoload.php src

cat >> src/autoload.php <<'AUTOLOAD'

require __DIR__ . '/JmesPath.php';
AUTOLOAD


%install
: Lib
mkdir -p %{buildroot}%{phpdir}/JmesPath
cp -rp src/* %{buildroot}%{phpdir}/JmesPath/

: Bin
mkdir -p %{buildroot}%{_bindir}
install -pm 0755 bin/jp.php %{buildroot}%{_bindir}/


%check
%if %{with_tests}
%{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/JmesPath/autoload.php
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGELOG.md
%doc README.rst
%doc composer.json
%{phpdir}/JmesPath
%{_bindir}/jp.php


%changelog
* Sat May 16 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.1.0-1
- Initial package
