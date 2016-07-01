# remirepo/Fedora spec file for php-aura-router
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    457efd185e4306fa671d659a66a2d9d28bf91a56
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     auraphp
%global gh_project   Aura.Router
%global pk_owner     aura
%global pk_project   router
%global ns_owner     Aura
%global ns_project   Router
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{pk_owner}-%{pk_project}
Version:        2.3.0
Release:        1%{?dist}
Summary:        A web router implementation

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  %{_bindir}/phpab
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(phpunit/phpunit)
# From composer.json, "require-dev": {
#        "aura/di": "~2.0"
BuildRequires:  php-composer(%{pk_owner}/di) >= 2.0
%endif

# From composer, "require": {
#        "php": ">=5.3.0"
Requires:       php(language) >= 5.3.0
# From phpcompatinfo report for version 2.3.0
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(%{pk_owner}/%{pk_project}) = %{version}


%description
Provides a web router implementation: given a URL path and a copy of
$_SERVER, it will extract path-info and $_SERVER values for a specific route.

This package does not provide a dispatching mechanism. Your application is
expected to take the information provided by the matching route and dispatch
it on its own. For one possible dispatch system, please see Aura.Dispatcher.

Autoloader: %{php_home}/%{ns_owner}/%{ns_project}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

# Restore sources tree matching namespaces
mv config src/_Config


%build
: Generate a classmap autoloader
%{_bindir}/phpab --output src/autoload.php src


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/%{ns_owner}
cp -pr src %{buildroot}%{php_home}/%{ns_owner}/%{ns_project}


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee -a vendor/autoload.php
<?php
require '%{php_home}/%{ns_owner}/Di/autoload.php';
require '%{buildroot}/%{php_home}/%{ns_owner}/%{ns_project}/autoload.php';
EOF

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --verbose || ret=1
   run=1
fi
if which php71; then
   php70 %{_bindir}/phpunit --verbose || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose
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
%doc *.md
%doc composer.json
%dir %{php_home}/%{ns_owner}/
     %{php_home}/%{ns_owner}/%{ns_project}/


%changelog
* Fri Jul  1 2016 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- initial package

