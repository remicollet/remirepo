# remirepo/fedora spec file for php-herrera-io-annotations
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    7d8b9a536da7f12aad8de7f28b2cb5266bde8da1
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     kherge-abandoned
%global gh_project   php-annotations
%global php_home     %{_datadir}/php
%global ns_vendor    Herrera
%global ns_project   Annotations
%global c_vendor     herrera-io
%global c_project    annotations
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{c_vendor}-%{c_project}
Version:        1.0.1
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        A tokenizer for Doctrine annotations

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

Source1:        %{name}-autoload.php

# Relocate the resources
Patch0:         %{name}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-dom
BuildRequires:  php-spl
BuildRequires:  php-composer(doctrine/annotations) >= 1.0
# From composer.json, "require-dev": {
#        "herrera-io/phpunit-test-case": "1.*",
#        "phpunit/phpunit": "3.7.*"
BuildRequires:  php-composer(%{c_vendor}/phpunit-test-case) >= 1
BuildRequires:  php-composer(phpunit/phpunit) >= 3.7
# Autoloader
BuildRequires:  php-composer(symfony/class-loader)
%endif

# from composer.json, "require": {
#        "php": ">=5.3.3",
#        "doctrine/annotations": "~1.0"
Requires:       php(language) >= 5.3.3
Requires:       php-composer(doctrine/annotations) >= 1.0
Requires:       php-composer(doctrine/annotations) <  2
# Autoloader
Requires:       php-composer(symfony/class-loader)
# from phpcompatinfo report for version 1.0.1
Requires:       php-dom
Requires:       php-spl

Provides:       php-composer(%{c_vendor}/%{c_project}) = %{version}


%description
%{summary}.

The Annotations library is for tokenizing and converting Doctrine-styled
annotations. Unlike the Doctrine Annotations library, this one does not
require that classes or constants exist, nor are they evaluated.

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p0

cp %{SOURCE1} src/lib/%{ns_vendor}/%{ns_project}/autoload.php


%build
# Empty


%install
rm -rf                      %{buildroot}

: library
mkdir -p                    %{buildroot}%{php_home}
cp -pr src/lib/%{ns_vendor} %{buildroot}%{php_home}/%{ns_vendor}

: resources
mkdir -p                    %{buildroot}%{_datadir}/%{name}
cp -pr res                  %{buildroot}%{_datadir}/%{name}/res


%check
%if %{with_tests}
export HERRERA_ANNOTATIONS_SCHEMA=%{buildroot}%{_datadir}/%{name}/res/annotations.xsd

cat << 'EOF' | tee src/tests/bootstrap.php
<?php
// This library
require_once '%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';
// Dependencies
require_once '%{php_home}/%{ns_vendor}/PHPUnit/autoload.php';
// Test classes
$fedoraClassLoader->addPrefix('Herrera\\Annotations\\Test\\', __DIR__);
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
%{_datadir}/%{name}/res
%dir %{php_home}/%{ns_vendor}
     %{php_home}/%{ns_vendor}/%{ns_project}


%changelog
* Tue Oct 27 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- initial package