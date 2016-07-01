# remirepo/Fedora spec file for php-aura-di
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    81d5d9c602ca292a16e32001dcbd2adab5350e28
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     auraphp
%global gh_project   Aura.Di
%global pk_owner     aura
%global pk_project   di
%global ns_owner     Aura
%global ns_project   Di
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{pk_owner}-%{pk_project}
Version:        2.2.4
Release:        1%{?dist}
Summary:        Dependency injection container system

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
BuildRequires:  php-reflection
BuildRequires:  php-spl
BuildRequires:  php-composer(phpunit/phpunit)
%endif

# From composer, "require": {
#        "php": ">=5.3.0"
Requires:       php(language) >= 5.3.0
# From phpcompatinfo report for version 2.2.4
Requires:       php-reflection
Requires:       php-spl

Provides:       php-composer(%{pk_owner}/%{pk_project}) = %{version}


%description
The Aura.Di package provides a dependency injection container system
with the following features:

* constructor and setter injection
* explicit and implicit auto-resolution of typehinted constructor
  parameter values
* configuration of setters across interfaces and traits
* inheritance of constructor parameter and setter method values
* lazy-loaded services, values, and instances
* instance factories

Autoloader: %{php_home}/%{ns_owner}/%{ns_project}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

# Uggly hack, need by this package and others
# Only usable in phpunit environment
mv tests/_Config src/_Config


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
%{_bindir}/phpab --output vendor/autoload.php tests
cat << 'EOF' | tee -a vendor/autoload.php
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
* Fri Jul  1 2016 Remi Collet <remi@fedoraproject.org> - 2.2.4-1
- initial package

