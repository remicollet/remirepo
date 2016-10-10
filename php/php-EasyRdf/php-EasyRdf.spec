# remirepo spec file for php-EasyRdf, from:
#
# Fedora spec file for php-EasyRdf
#
# Copyright (c) 2013-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
#

%global composer_vendor  easyrdf
%global composer_project easyrdf

# "php": ">=5.2.8"
%global php_min_ver 5.2.8

%if 0%{?el6}
%global raptor_pkg raptor
%else
%global raptor_pkg raptor2
%endif

# php-redland not available in remirepo
%global redland_support 0

%if 0%{?fedora} > 9 || 0%{?rhel} > 5
# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}
%else
# need raptor 1.4.17
%global with_tests 0
%endif

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-EasyRdf
Version:       0.9.0
Release:       4%{?dist}
Summary:       A PHP library designed to make it easy to consume and produce RDF

Group:         Development/Libraries
License:       BSD
URL:           http://www.easyrdf.org
Source0:       %{url}/downloads/easyrdf-%{version}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: graphviz
BuildRequires: %{raptor_pkg}
%if %{redland_support}
BuildRequires: php-redland
%endif
## composer.json
BuildRequires: %{_bindir}/phpunit
BuildRequires: php(language) >= %{php_min_ver}
## phpcompatinfo (computed from version 0.9.0)
BuildRequires: php-ctype
BuildRequires: php-date
BuildRequires: php-dom
BuildRequires: php-json
BuildRequires: php-libxml
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-simplexml
BuildRequires: php-spl
BuildRequires: php-xml
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo requires (computed from version 0.9.0)
Requires:      php-ctype
Requires:      php-date
Requires:      php-dom
Requires:      php-json
Requires:      php-libxml
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-simplexml
Requires:      php-spl
Requires:      php-xml
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

Obsoletes:     %{name}-test

%description
EasyRdf is a PHP library designed to make it easy to consume and produce RDF
(http://en.wikipedia.org/wiki/Resource_Description_Framework). It was designed
for use in mixed teams of experienced and inexperienced RDF developers. It is
written in Object Oriented PHP and has been tested extensively using PHPUnit.

After parsing EasyRdf builds up a graph of PHP objects that can then be walked
around to get the data to be placed on the page. Dump methods are available to
inspect what data is available during development.

Data is typically loaded into a EasyRdf_Graph object from source RDF documents,
loaded from the web via HTTP. The EasyRdf_GraphStore class simplifies loading
and saving data to a SPARQL 1.1 Graph Store.

SPARQL queries can be made over HTTP to a Triplestore using the
EasyRdf_Sparql_Client class. SELECT and ASK queries will return an
EasyRdf_Sparql_Result object and CONSTRUCT and DESCRIBE queries will
return an EasyRdf_Graph object.
%if %{redland_support}
Optional dependencies: graphviz, graphviz-gd, %{raptor_pkg}, php-redland
%else
Optional dependencies: graphviz, graphviz-gd, %{raptor_pkg}
%endif


%package doc
Summary: Documentation for %{name}
Group:   Documentation

%description doc
%{summary}.


%prep
%setup -qn easyrdf-%{version}

: Create autoloader
cat <<'AUTOLOAD' | tee lib/EasyRdf/autoload.php
<?php
/**
 * Autoloader created by %{name}-%{version}-%{release}
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

$fedoraClassLoader->addPrefix('EasyRdf_', dirname(__DIR__));

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}
cp -rp lib/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Skip tests that sometimes cause timeout exceptions
sed -e 's/testSerialiseSvg/SKIP_testSerialiseSvg/' \
    -e 's/testSerialiseGif/SKIP_testSerialiseGif/' \
    -e 's/testSerialiseSvg/SKIP_testSerialisePng/' \
    -i test/EasyRdf/Serialiser/GraphVizTest.php

: Create PHPUnit config
cat <<'PHPUNIT' | tee phpunit.xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit
    bootstrap="%{buildroot}%{phpdir}/EasyRdf/autoload.php"
    colors="true">
    <testsuites>
      <testsuite name="EasyRdf Library">
        <directory suffix="Test.php">./test/EasyRdf/</directory>
      </testsuite>
    </testsuites>
</phpunit>
PHPUNIT

%if !%{redland_support}
: No redland support
rm -f test/EasyRdf/Parser/RedlandTest.php
%endif

: Run tests
%{_bindir}/phpunit --verbose
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc CHANGELOG.md
%doc README.md
%doc composer.json
%doc doap.rdf
%{phpdir}/EasyRdf.php
%{phpdir}/EasyRdf

%files doc
%defattr(-,root,root,-)
%doc docs
%doc examples


%changelog
* Sun Oct 09 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.9.0-4
- No Redland support for Fedora 25+ (RHBZ #1350621)

* Sun Jun 28 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.9.0-1
- Updated to 0.9.0 (RHBZ #1163321)
- Added autoloader

* Tue Nov 18 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.8.0-5
- Modified raptor and redland logic

* Fri Nov 14 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.8.0-4
- No raptor or redland for el7

* Thu Nov 13 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.8.0-3
- Added php-composer(easyrdf/easyrdf) virtual provide
- Added option to build without tests ("--without tests")
- Reduce PHP min version from 5.3.3 to 5.2.8 (per composer.json)
- %%license usage

* Fri Jan  3 2014 Remi Collet <remi@fedoraproject.org> - 0.8.0-1
- backport 0.8.0 for remi repo.

* Thu Jan 02 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 0.8.0-1
- Updated to 0.8.0
- Updated PHP min version from 5.2.8 to 5.3.3
- Added php-[libxml,mbstring,reflection,simplexml] requires
- Removed pre-0.8.0 fixes
- Updated %%check to use PHPUnit directly and skip tests that sometimes cause
  timeout exceptions

* Fri Nov 15 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.7.2-5
- Removed test sub-package
- php-common => php(language)

* Thu Feb  7 2013 Remi Collet <remi@fedoraproject.org> - 0.7.2-3
- backport 0.7.2 for remi repo.
- disable tests on RHEL-5 (requires raptor 1.4.17)

* Mon Feb 04 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.7.2-3
- Added note in %%description about optional dependencies
- Temporarily skip "EasyRdf_Serialiser_GraphVizTest::testSerialiseSvg" test
  for Fedora > 18

* Mon Jan 28 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.7.2-2
- Tests run by default (i.e. without "--with tests")
- Fixes for tests
- Removed Mac files
- Separated docs into sub-package

* Sun Jan 27 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.7.2-1
- Initial package
