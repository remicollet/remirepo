# remirepo spec file for php-ocramius-proxy-manager from Fedora:
#
# RPM spec file for php-ocramius-proxy-manager
#
# Copyright (c) 2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner      Ocramius
%global github_name       ProxyManager
%global github_version    1.0.2
%global github_commit     57e9272ec0e8deccf09421596e0e2252df440e11

%global composer_vendor   ocramius
%global composer_project  proxy-manager

# "php": ">=5.3.3"
%global php_min_ver 5.3.3
# "zendframework/zend-code": ">2.2.5,<3.0"
%global zf_min_ver  2.2.5
%global zf_max_ver  3.0

# Skip tests for EPEL 6 b/c PHPUnit < 4
# TODO: Get tests running on EPEL 6!
%if 0%{?el6}
%global with_tests 0
%else
# Build using "--without tests" to disable tests
%global with_tests %{?_without_tests:0}%{!?_without_tests:1}
%endif

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       OOP proxy wrappers utilities

Group:         Development/Libraries
License:       MIT
URL:           http://ocramius.github.io/ProxyManager/
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:     noarch
# Autoload generation
BuildRequires: %{_bindir}/phpab
%if %{with_tests}
# Tests
## composer.json
BuildRequires: %{_bindir}/phpunit
BuildRequires: php(language)                         >= %{php_min_ver}
BuildRequires: php-composer(zendframework/zend-code) >= %{zf_min_ver}
BuildRequires: php-composer(zendframework/zend-code) <  %{zf_max_ver}
## phpcompatinfo (computed from version 1.0.0)
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language)                         >= %{php_min_ver}
Requires:      php-composer(zendframework/zend-code) >= %{zf_min_ver}
Requires:      php-composer(zendframework/zend-code) <  %{zf_max_ver}
# phpcompatinfo (computed from version 1.0.0)
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
A library providing utilities to generate, instantiate and generally operate
with Object Proxies.

Optional:
* php-ZendFramework2-Json
      To have the JsonRpc adapter (Remote Object feature)
* php-ZendFramework2-Soap
      To have the Soap adapter (Remote Object feature)
* php-ZendFramework2-Stdlib
      To use the hydrator proxy
* php-ZendFramework2-XmlRpc
      To have the XmlRpc adapter (Remote Object feature)
* php-ocramius-generated-hydrator
      To have very fast object to array to object conversion for ghost objects


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Generate autoloader
%{_bindir}/phpab --nolower --output src/ProxyManager/autoload.php src/ProxyManager

(cat <<'AUTOLOAD'

// TODO: Add Zend/ZendXml/Ocramius autoloaders from their packages when they are available
spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/',  $class) . '.php';
    @include_once $src;
});
AUTOLOAD
) | tee -a src/ProxyManager/autoload.php


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create tests autoload
%{_bindir}/phpab --nolower --output tests/autoload.php tests %{phpdir}/PHPUnit

: Create mock Composer "vendor/autoload.php"
mkdir vendor
(cat <<'AUTOLOAD'
<?php
require __DIR__ . '/../tests/autoload.php';
require '%{buildroot}%{phpdir}/ProxyManager/autoload.php';
AUTOLOAD
) | tee vendor/autoload.php

: Run tests
%{_bindir}/phpunit -v --exclude-group Performance
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{phpdir}/ProxyManager


%changelog
* Mon Aug 10 2015 Remi Collet <remi@remirepo.net> - 1.0.2-1
- update to 1.0.2

* Fri May 29 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.0-2
- Fix autoloader to load all optional pkgs
- Some spec cleanup

* Mon May 18 2015 Remi Collet <RPMS@FamilleCollet.com> - 1.0.0-1
- add needed backport stuff for remi repository

* Sat May 16 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.0-1
- Initial package
