# remirepo spec file for php-react-promise, from Fedora:
#
# RPM spec file for php-react-promise
#
# Copyright (c) 2014-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     reactphp
%global github_name      promise
%global github_version   2.2.0
%global github_commit    365fcee430dfa4ace1fbc75737ca60ceea7eeeef

%global composer_vendor  react
%global composer_project promise

# "php": ">=5.4.0"
%global php_min_ver 5.4.0

# Build using "--without tests" to disable tests
%global with_tests %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       3%{?github_release}%{?dist}
Summary:       A lightweight implementation of CommonJS Promises/A for PHP

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: %{_bindir}/phpunit
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
## phpcompatinfo (computed from version 2.2.0)
BuildRequires: php-json
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader) >= 2.5
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 2.2.0)
Requires:      php-json
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader) >= 2.5

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
A lightweight implementation of CommonJS Promises/A [1] for PHP.

[1] http://wiki.commonjs.org/wiki/Promises/A


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
(cat <<'AUTOLOAD'
<?php
/**
 * Autoloader created by %{name}-%{version}-%{release}
 */

if (!class_exists('Symfony\\Component\\ClassLoader\\Psr4ClassLoader', false)) {
    require_once 'Symfony/Component/ClassLoader/Psr4ClassLoader.php';
}

$loader = new \Symfony\Component\ClassLoader\Psr4ClassLoader();
$loader->addPrefix('React\\Promise', __DIR__);
$loader->register();

require_once __DIR__ . '/functions_include.php';
AUTOLOAD
) | tee src/autoload.php


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}/React/Promise
cp -rp src/* %{buildroot}%{phpdir}/React/Promise/


%check
%if %{with_tests}
: Create tests bootstrap
(cat <<'BOOTSTRAP'
<?php

require_once '%{buildroot}%{phpdir}/React/Promise/autoload.php';

$loader->addPrefix('React\\Promise', __DIR__ . '/tests');
BOOTSTRAP
) | tee bootstrap.php

%{_bindir}/phpunit --bootstrap ./bootstrap.php -v
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
%dir %{phpdir}/React
     %{phpdir}/React/Promise


%changelog
* Mon Jun 01 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.2.0-3
- Use include path in autoloader

* Mon Jun 01 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.2.0-2
- Added autoloader

* Sun Jan 04 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.2.0-1
- Updated to 2.2.0 (BZ #1178411)

* Fri Oct 31 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- backport 2.1.0 for remi repo.

* Mon Oct 27 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.1.0-1
- Updated to 2.1.0

* Wed Oct 15 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.0.0-1
- Initial package
