# remirepo spec file for php-PhpOption, from Fedora:
#
# RPM spec file for php-PhpOption
#
# Copyright (c) 2013-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     schmittjoh
%global github_name      php-option
%global github_version   1.4.0
%global github_commit    5d099bcf0393908bf4ad69cc47dafb785d51f7f5

%global composer_vendor  phpoption
%global composer_project phpoption

# "php": ">=5.3.0"
%global php_min_ver      5.3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-PhpOption
Version:       %{github_version}
Release:       4%{?dist}
Summary:       Option type for PHP

Group:         Development/Libraries
License:       ASL 2.0
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: %{_bindir}/phpunit
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
## phpcompatinfo (computed from version 1.4.0)
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.4.0)
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming
Provides:      php-%{composer_vendor}-%{composer_project} = %{version}-%{release}
Provides:      php-%{composer_vendor} = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
This package adds an Option type for PHP.

The Option type is intended for cases where you sometimes might return a value
(typically an object), and sometimes you might return no value (typically null)
depending on arguments, or other runtime factors.

Often times, you forget to handle the case where no value is returned. Not
intentionally of course, but maybe you did not account for all possible states
of the system; or maybe you indeed covered all cases, then time goes on, code
is refactored, some of these your checks might become invalid, or incomplete.
Suddenly, without noticing, the no value case is not handled anymore. As a
result, you might sometimes get fatal PHP errors telling you that you called a
method on a non-object; users might see blank pages, or worse.

On one hand, the Option type forces a developer to consciously think about both
cases (returning a value, or returning no value). That in itself will already
make your code more robust. On the other hand, the Option type also allows the
API developer to provide more concise API methods, and empowers the API user in
how he consumes these methods.


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee src/PhpOption/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 *
 * Created by %{name}-%{version}-%{release}
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

$fedoraClassLoader->addPrefix('PhpOption\\', dirname(__DIR__));

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/PhpOption/autoload.php


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{phpdir}/PhpOption


%changelog
* Sat Jul 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.4.0-4
- Added spec license
- Added autoloader
- Added standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming provides
- Added php-composer(phpoption/phpoption) provide
- %%license usage

* Mon Feb 17 2014 Remi Collet <RPMS@famillecollet.com> 1.4.0-1
- backport 1.4.0 for remi repo

* Wed Feb 12 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.4.0-1
- Updated to 1.4.0 (BZ #1055299)

* Sun Sep 29 2013 Remi Collet <RPMS@famillecollet.com> 1.3.0-1
- backport 1.3.0 for remi repo

* Sat Sep 28 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.0-1
- Updated to 1.3.0
- Other minor updates

* Tue Apr  2 2013 Remi Collet <RPMS@famillecollet.com> 1.2.0-1
- backport 1.2.0 for remi repo

* Sat Mar 30 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.2.0-1
- Updated to version 1.2.0
- Removed tests sub-package

* Fri Jan 25 2013 Remi Collet <RPMS@famillecollet.com> 1.1.0-1
- backport 1.1.0 for remi repo

* Tue Jan 22 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-1
- Initial package
