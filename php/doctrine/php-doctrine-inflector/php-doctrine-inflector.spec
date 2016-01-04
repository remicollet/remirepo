# remirepo spec file for php-doctrine-inflector, from:
#
# Fedora spec file for php-doctrine-inflector
#
# Copyright (c) 2013-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      inflector
%global github_version   1.1.0
%global github_commit    90b2128806bfde671b6952ab8bea493942c1fdae

%global composer_vendor  doctrine
%global composer_project inflector

# "php": ">=5.3.2"
%global php_min_ver      5.3.2

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Common string manipulations with regard to casing and singular/plural rules

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: %{_bindir}/phpunit
BuildRequires: php(language) >= %{php_min_ver}
## phpcompatinfo (computed from version 1.1.0)
BuildRequires: php-pcre
BuildRequires: php-spl
# Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.1.0)
Requires:      php-pcre
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Doctrine Inflector is a small library that can perform string manipulations
with regard to upper-/lowercase and singular/plural forms of words.

Autoloader: %{phpdir}/Doctrine/Common/Inflector/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee lib/Doctrine/Common/Inflector/autoload.php
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

$fedoraClassLoader->addPrefix('Doctrine\\Common\\Inflector\\', dirname(dirname(dirname(__DIR__))));

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}
cp -rp lib/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create tests autoloader
cat <<'AUTOLOAD' | tee autoload.php
<?php

$fedoraClassLoader =
    require_once '%{buildroot}%{phpdir}/Doctrine/Common/Inflector/autoload.php';

$fedoraClassLoader->addPrefix('Doctrine\\Tests', __DIR__ . '/tests');
AUTOLOAD

: Run tests
%{_bindir}/phpunit -v --bootstrap autoload.php

if which php70; then
   php70 %{_bindir}/phpunit -v --bootstrap autoload.php
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
%dir %{phpdir}/Doctrine
%dir %{phpdir}/Doctrine/Common
     %{phpdir}/Doctrine/Common/Inflector


%changelog
* Sun Jan 03 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.0-1
- Updated to 1.1.0 (RHBZ #1279884)

* Sat Jun 27 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.1-5
- Updated autoloader with trailing separator

* Wed Jun 24 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.1-4
- Added autoloader

* Sun Dec 28 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.1-2
- %%license usage

* Sun Dec 28 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.1-1
- Updated to 1.0.1 (BZ #1176943)

* Fri Jun 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0-4.20131221gita81c334
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide
- Added option to build without tests ("--without tests")

* Sat Jan 11 2014 Remi Collet <rpms@famillecollet.com> 1.0-2.20131221gita81c334
- backport for remi repo

* Mon Jan 06 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0-2.20131221gita81c334
- Conditional %%{?dist}

* Mon Dec 23 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0-1.20131221gita81c334
- Initial package
