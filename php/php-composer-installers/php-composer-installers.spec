# remirepo spec file for php-composer-installers, from:
#
# Fedora spec file for php-composer-installers
#
# Copyright (c) 2015-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     composer
%global github_name      installers
%global github_version   1.0.25
%global github_commit    36e5b5843203d7f1cf6ffb0305a97e014387bd8e

%global composer_vendor  composer
%global composer_project installers

# "composer-plugin-api": "^1.0"
%global composer_plugin_min_ver 1.0
%global composer_plugin_max_ver 2.0
# "composer/composer": "1.0.*@dev"
%global composer_min_ver 1.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       A multi-framework Composer library installer

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php-composer(composer-plugin-api) >= %{composer_plugin_min_ver}
BuildRequires: php-composer(composer/composer)   >= %{composer_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
## phpcompatinfo (computed from version 1.0.23)
BuildRequires: php(language) >= 5.3.0
BuildRequires: php-pcre
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php-composer(composer-plugin-api) >= %{composer_plugin_min_ver}
Requires:      php-composer(composer-plugin-api) <  %{composer_plugin_max_ver}
# phpcompatinfo (computed from version 1.0.23)
Requires:      php(language) >= 5.3.0
Requires:      php-pcre
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
This is for PHP package authors to require in their composer.json. It will
install their package to the correct location based on the specified package
type.

The goal of installers is to be a simple package type to install path map.
Users can also customize the install path per package and package authors
can modify the package name upon installing.

installers isn't intended on replacing all custom installers. If your package
requires special installation handling then by all means, create a custom
installer to handle it.


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee src/Composer/Installers/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Composer\\Installers\\', dirname(dirname(__DIR__)));

require_once '%{phpdir}/Composer/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing to build


%install
rm -rf   %{buildroot}

mkdir -p %{buildroot}%{phpdir}
cp -rp src/Composer %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require_once '%{buildroot}%{phpdir}/Composer/Installers/autoload.php';
$fedoraClassLoader->addPrefix('Composer\\Installers\\Test\\', __DIR__ . '/tests');
BOOTSTRAP

: Run tests
%{_bindir}/phpunit --verbose --bootstrap bootstrap.php

if which php70; then
   php70 %{_bindir}/phpunit --verbose --bootstrap bootstrap.php
fi
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
%{phpdir}/Composer/Installers


%changelog
* Thu Apr 14 2016 Remi Collet <remi@remirepo.net> - 1.0.25-1
- update to 1.0.25

* Wed Apr  6 2016 Remi Collet <remi@remirepo.net> - 1.0.24-1
- update to 1.0.24

* Sat Mar 12 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.23-1
- Updated to 1.0.23 (RHBZ #1302488)

* Fri Feb 26 2016 Remi Collet <remi@remirepo.net> - 1.0.23-1
- update to 1.0.23
- run test suite with both PHP 5 and 7 when available

* Wed Nov 04 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.22-2
- Dependency updates

* Wed Nov 04 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.22-1
- Updated to 1.0.22 (RHBZ #1276816)

* Fri Oct 30 2015 Remi Collet <remi@remirepo.net> - 1.0.22-1
- update to 1.0.22

* Tue Aug 25 2015 Remi Collet <remi@remirepo.net> - 1.0.21-1
- backport for #remirepo

* Thu Aug 20 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.21-1
- Initial package
