# remirepo spec file for php-PhpCollection, from Fedora:
#
# RPM spec file for php-PhpCollection
#
# Copyright (c) 2013-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner      schmittjoh
%global github_name       php-collection
%global github_version    0.4.0
%global github_commit     b8bf55a0a929ca43b01232b36719f176f86c7e83

%global composer_vendor   phpcollection
%global composer_project  phpcollection

%global php_min_ver       5.3.0
# "phpoption/phpoption": "1.*"
#     NOTE: min version not 1.0 because autoloader required
%global phpoption_min_ver 1.4.0-4
%global phpoption_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-PhpCollection
Version:       %{github_version}
Release:       4%{?dist}
Summary:       General purpose collection library for PHP

Group:         Development/Libraries
License:       ASL 2.0
URL:           http://jmsyst.com/libs/%{github_name}

# GitHub export contains non-allowable licened documentation.
# Run php-PhpCollection-get-source.sh to create allowable source.
Source0:       %{name}-%{github_version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: %{_bindir}/phpunit
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
#BuildRequires: php-composer(phpoption/phpoption) >= %%{phpoption_min_ver}
BuildRequires: php-PhpOption >= %{phpoption_min_ver}
## phpcompatinfo (computed from version 0.4.0)
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

Requires:      php(language)                     >= %{php_min_ver}
#Requires:      php-composer(phpoption/phpoption) >= %%{phpoption_min_ver}
Requires:      php-PhpOption                     >= %{phpoption_min_ver}
Requires:      php-composer(phpoption/phpoption) <  %{phpoption_max_ver}
# phpcompatinfo (computed from version 0.4.0)
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming
Provides:      php-%{composer_vendor}-%{composer_project} = %{version}-%{release}
Provides:      php-%{composer_vendor} = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
This library adds basic collections for PHP.

Collections can be seen as more specialized arrays for which certain contracts
are guaranteed.

Supported Collections:
* Sequences
** Keys: numerical, consequentially increasing, no gaps
** Values: anything, duplicates allowed
** Classes: Sequence, SortedSequence
* Maps
** Keys: strings or objects, duplicate keys not allowed
** Values: anything, duplicates allowed
** Classes: Map, ObjectMap (not yet implemented)
* Sets (not yet implemented)
** Keys: not meaningful
** Values: anything, each value must be unique (===)
** Classes: Set

General Characteristics:
* Collections are mutable (new elements may be added, existing elements may be
  modified or removed). Specialized immutable versions may be added in the
  future though.
* Equality comparison between elements are always performed using the shallow
  comparison operator (===).
* Sorting algorithms are unstable, that means the order for equal elements is
  undefined (the default, and only PHP behavior).


%prep
%setup -q -n %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee src/PhpCollection/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 *
 * Created by %{name}-%{version}-%{release}
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

require_once '%{phpdir}/PhpOption/autoload.php';

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('PhpCollection\\', dirname(__DIR__));

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
: Skip test known to fail
sed 's/function testMap/function SKIP_testMap/' \
    -i tests/PhpCollection/Tests/SequenceTest.php

: Run tests
%{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/PhpCollection/autoload.php
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
%{phpdir}/PhpCollection


%changelog
* Sun Jul 12 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.4.0-4
- Added spec license
- New source script %%{name}-get-source.sh instead of %%{name}-strip.sh
- Added autoloader
- Added standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming provides
- Added php-composer(phpcollection/phpcollection) provide
- %%license usage

* Tue Apr 22 2014 Remi Collet <remi@fedoraproject.org> 0.4.0-1
- backport 0.4.0 for remi repo.

* Mon Apr 21 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.4.0-1
- Updated to 0.4.0 (BZ #1078754)

* Mon Dec 30 2013 Remi Collet <remi@fedoraproject.org> 0.3.1-1
- backport 0.3.1 for remi repo.

* Mon Dec 30 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.3.1-1
- Updated to 0.3.1 (BZ #1045915)
- Spec cleanup

* Thu Jul 18 2013 Remi Collet <remi@fedoraproject.org> 0.3.0-1
- backport 0.3.0 for remi repo.

* Wed Jul 17 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.3.0-1
- Updated to 0.3.0

* Tue Mar 19 2013 Remi Collet <remi@fedoraproject.org> 0.2.0-2
- backport 0.2.0 for remi repo.

* Mon Mar 18 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.2.0-2
- Added %%{name}-strip.sh as Source1

* Sat Mar 16 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.2.0-1
- Updated to version 0.2.0
- Added phpoption_max_ver global
- Bad licensed files stripped from source
- php-common => php(language)
- Removed tests sub-package

* Wed Jan 23 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.1.0-1
- Initial package
