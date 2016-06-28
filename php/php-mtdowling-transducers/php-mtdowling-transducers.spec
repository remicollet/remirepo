# remirepo spec file for php-mtdowling-transducers from Fedora:
#
# RPM spec file for php-mtdowling-transducers
#
# Copyright (c) 2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     mtdowling
%global github_name      transducers.php
%global github_version   0.3.0
%global github_commit    32ff6a67b5d5d1930533277a505b4f9d360dbe6c

%global composer_vendor  mtdowling
%global composer_project transducers

# "php": ">=5.5.0"
%global php_min_ver 5.5.0

# Build using "--without tests" to disable tests
%global with_tests %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       4%{?github_release}%{?dist}
Summary:       Composable algorithmic transformations

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}

# GitHub download/export does not include tests
# Run "php-mtdowling-transducers-get-source.sh" to create source
Source0:       %{name}-%{version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:     noarch
%if %{with_tests}
# For tests
## composer.json
BuildRequires: %{_bindir}/phpunit
BuildRequires: php(language) >= %{php_min_ver}
## phpcompatinfo (computed from version 0.3.0)
BuildRequires: php-json
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 0.3.0)
Requires:      php-json
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Transducers [1] are composable algorithmic transformations. They are independent
from the context of their input and output sources and specify only the essence
of the transformation in terms of an individual element. Because transducers are
decoupled from input or output sources, they can be used in many different
processes - collections, streams, channels, observables, etc. Transducers
compose directly, without awareness of input or creation of intermediate
aggregates.

[1] http://clojure.org/transducers


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Generate autoloader
cat > src/autoload.php <<'AUTOLOAD'
<?php
/**
 * While an autoloader is not really necessary for this (currently) single-file
 * library, it is provided for future-proofing the loading of this library.
 */

require __DIR__ . '/transducers.php';
AUTOLOAD


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}/%{composer_project}
cp -rp src/* %{buildroot}%{phpdir}/%{composer_project}/


%check
%if %{with_tests}
: Temporarily skip failing tests
: See https://github.com/mtdowling/transducers.php/issues/4
sed -e 's/function testToTraversableReturnsStreamsIter/function SKIP_testToTraversableReturnsStreamsIter/' \
    -e 's/function testCanStepInClosing/function SKIP_testCanStepInClosing/' \
    -i tests/transducersTest.php

%{_bindir}/phpunit \
    --bootstrap %{buildroot}%{phpdir}/%{composer_project}/autoload.php

if which php56; then
  php56 %{_bindir}/phpunit \
    --bootstrap %{buildroot}%{phpdir}/%{composer_project}/autoload.php
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
%doc CHANGELOG.md
%doc README.rst
%doc composer.json
%{phpdir}/%{composer_project}


%changelog
* Mon May 18 2015 Remi Collet <remi@fedoraproject.org> - 0.3.0-4
- drop dependency on php-ereg (false positive)

* Mon May 18 2015 Remi Collet <RPMS@FamilleCollet.com> - 0.3.0-1
- add needed backport stuff for remi repository

* Sat May 16 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.3.0-1
- Initial package
