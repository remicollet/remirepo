# remirepo spec file for php-gliph, from Fedora:
#
# RPM spec file for php-gliph
#
# Copyright (c) 2013-2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     sdboyer
%global github_name      gliph
%global github_version   0.1.8
%global github_commit    db9e4b77622f91e2d338cc45f83c2cd0e3cf0e1e

%global composer_vendor  sdboyer
%global composer_project gliph

# "php": ">=5.3"
%global php_min_ver      5.3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_project}
Version:       %{github_version}
Release:       4%{?github_release}%{?dist}
Summary:       A graph library for PHP

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}

# Run "php-gliph-get-source.sh" to create source
Source0:       %{name}-%{version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: %{_bindir}/phpunit
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
## phpcompatinfo (computed from version 0.1.8)
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 0.1.8)
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming
Provides:      php-%{composer_vendor}-%{composer_project} = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Gliph is a graph library for PHP. It provides graph building blocks and
data structures for use by other PHP applications. It is (currently) designed
for use with in-memory graphs, not for interaction with a graph database like
Neo4J (http://neo4j.org/).


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee src/Gliph/autoload.php
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
        require_once 'Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Gliph\\', dirname(__DIR__));

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php

$fedoraClassLoader =
    require_once '%{buildroot}%{phpdir}/Gliph/autoload.php';

$fedoraClassLoader->addPrefix(null, __DIR__ . '/tests');
BOOTSTRAP

: Run tests
%{_bindir}/phpunit --verbose --bootstrap ./bootstrap.php .
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
%{phpdir}/Gliph


%changelog
* Sat Jul 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.1.8-4
- Added missing autoloader require

* Sat Jul 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.1.8-3
- Added autoloader
- Added tests
- Added standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming provides

* Sun Aug 17 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.1.8-1
- Updated to 0.1.8 (BZ #1125361)

* Sat Jul 19 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.1.6-1
- Updated to 0.1.6 (BZ #1119424)
- Added "php-composer(sdboyer/gliph)" virtual provide

* Thu Nov  7 2013 Remi Collet <rpms@famillecollet.com> 0.1.5-1
- backport 0.1.5 for remi repo

* Wed Nov 06 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.1.5-1
- Updated to 0.1.5
- Removed tests (git export-ignored upstream)

* Thu Oct 24 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.1.4-1.20131024git8da23c6
- Updated to latest snapshot (commit 8da23c6397354e9acc7a7e6f8d2a782fdf21ab54)
  which includes LICENSE
- "php-common" -> "php(language)"
- Added PHPUnit min/max versions

* Wed Oct 23 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.1.4-1
- Initial package
