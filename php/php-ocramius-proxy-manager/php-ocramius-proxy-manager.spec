# remirepo spec file for php-ocramius-proxy-manager from Fedora:
#
# Fedora spec file for php-ocramius-proxy-manager
#
# Copyright (c) 2015-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
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

%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       OOP proxy wrappers utilities

Group:         Development/Libraries
License:       MIT
URL:           http://ocramius.github.io/ProxyManager/
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:     noarch
# Autoloader
BuildRequires: %{_bindir}/phpab
%if %{with_tests}
# Tests
## composer.json
BuildRequires: %{_bindir}/phpunit
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(zendframework/zend-code) >= %{zf_min_ver}
BuildRequires: php-composer(zendframework/zend-code) <  %{zf_max_ver}
BuildRequires: php-composer(ocramius/generated-hydrator) >= 1.2.0
## phpcompatinfo (computed from version 1.0.2)
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(zendframework/zend-code) >= %{zf_min_ver}
Requires:      php-composer(zendframework/zend-code) <  %{zf_max_ver}
# phpcompatinfo (computed from version 1.0.2)
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl

# Weak dependencies
%if 0%{?fedora} >= 21
Suggests:      php-composer(ocramius/generated-hydrator)
Suggests:      php-composer(zendframework/zend-json)
Suggests:      php-composer(zendframework/zend-soap)
Suggests:      php-composer(zendframework/zend-stdlib)
Suggests:      php-composer(zendframework/zend-xmlrpc)
%endif
# For autoloader
Conflicts:     php-ocramius-generated-hydrator < 1.2.0


# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
A library providing utilities to generate, instantiate and generally operate
with Object Proxies.

Autoloader: %{phpdir}/ProxyManager/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Generate autoloader
%{_bindir}/phpab --output src/ProxyManager/autoload.php src/ProxyManager

cat <<'AUTOLOAD' | tee -a src/ProxyManager/autoload.php

// Dependencies (autoloader => required)
foreach (array(
    // Required
    '%{phpdir}/Zend/autoload.php' => true,
    // Optional
    '%{phpdir}/GeneratedHydrator/autoload.php' => false,
) as $dependencyAutoloader => $required) {
    if ($required || file_exists($dependencyAutoloader)) {
        require_once $dependencyAutoloader;
    }
}
AUTOLOAD


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create tests autoload
%{_bindir}/phpab --output tests/autoload.php tests %{phpdir}/PHPUnit

: Create mock Composer "vendor/autoload.php"
mkdir vendor
cat <<'AUTOLOAD' | tee vendor/autoload.php
<?php
require __DIR__.'/../tests/autoload.php';
require '%{buildroot}%{phpdir}/ProxyManager/autoload.php';
AUTOLOAD

: Skip test known to fail
sed 's/function testCodeGeneration/function SKIP_testCodeGeneration/' \
    -i tests/ProxyManagerTest/Functional/FatalPreventionFunctionalTest.php

: Run tests
%{_bindir}/phpunit --verbose --exclude-group Performance
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
* Tue Oct 18 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.2-2
- Update to 1.0.2 (RHBZ #1251784)
- Add weak dependencies
- Use dependencies' autoloaders
- Temporarily skip tests on Fedora 25+ (RHBZ #1350615)

* Mon Aug 10 2015 Remi Collet <remi@remirepo.net> - 1.0.2-1
- update to 1.0.2

* Fri May 29 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.0-2
- Fix autoloader to load all optional pkgs
- Some spec cleanup

* Mon May 18 2015 Remi Collet <RPMS@FamilleCollet.com> - 1.0.0-1
- add needed backport stuff for remi repository

* Sat May 16 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.0-1
- Initial package
