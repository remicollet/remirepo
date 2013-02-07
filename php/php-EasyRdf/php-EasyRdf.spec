# phpci false positive for 5.3.3 because usage of JSON_ERROR_* constants in
# lib/EasyRdf/Parser/Json.php are conditional
%global php_min_ver 5.2.8

%if 0%{?fedora} > 9 || 0%{?rhel} > 5
%global with_test 1
%else
# need raptor 1.4.17
%global with_test 0
%endif

# TODO see for php-redland not yet available in remirepo

Name:          php-EasyRdf
Version:       0.7.2
Release:       3%{?dist}
Summary:       A PHP library designed to make it easy to consume and produce RDF

Group:         Development/Libraries
License:       BSD
URL:           http://www.easyrdf.org
Source0:       %{url}/downloads/easyrdf-%{version}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
BuildRequires: php(language) >= %{php_min_ver}
%if %{with_test}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
BuildRequires: graphviz
BuildRequires: raptor >= 1.4.17
# phpci
BuildRequires: php-ctype
BuildRequires: php-date
BuildRequires: php-dom
BuildRequires: php-json
BuildRequires: php-pcre
#BuildRequires: php-redland
BuildRequires: php-spl
BuildRequires: php-xml
%endif

Requires:      php(language) >= %{php_min_ver}
# phpci requires
Requires:      php-ctype
Requires:      php-date
Requires:      php-dom
Requires:      php-json
Requires:      php-pcre
#Requires:      php-redland
Requires:      php-spl
Requires:      php-xml

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

Optional dependencies: graphviz, graphviz-gd, raptor, raptor2


%package doc
Summary: Documentation for %{name}
Group:   Documentation

%description doc
%{summary}.


%package test
Summary:  Test suite for %{name}
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
# Yes, test requires doc (for examples)
Requires: %{name}-doc = %{version}-%{release}
Requires: php-pear(pear.phpunit.de/PHPUnit)
Requires: graphviz-gd
Requires: raptor

%description test
%{summary}.


%prep
%setup -q -n easyrdf-%{version}

# Update test file
chmod +x test/cli_example_wrapper.php
sed -e 's:/usr/bin/env php:%{_bindir}/php:' \
    -e '/EXAMPLES_DIR = /s|\.\.|../../doc/%{name}-doc-%{version}|' \
    -i test/cli_example_wrapper.php

#
# The following fixes will not be required as of pre-release 0.8.8-beta1.
#

# Remove Mac files
find . | grep -e '/\._' | xargs rm -f

# Add "EasyRdf/Isomorphic.php" require
( cat <<'REQUIRE'

/**
 * @see EasyRdf_Isomorphic
 */
require_once "EasyRdf/Isomorphic.php";
REQUIRE
) >> lib/EasyRdf.php


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php
cp -rp lib/* %{buildroot}%{_datadir}/php/

mkdir -p -m 755 %{buildroot}%{_datadir}/tests/%{name}
cp -rp test/* %{buildroot}%{_datadir}/tests/%{name}/


%check
%if 0%{?fedora} > 18
: Temporarily skipping "EasyRdf_Serialiser_GraphVizTest::testSerialiseSvg" test
: because of unknown failure in Fedora 19
sed 's/testSerialiseSvg/SKIP_TEST_testSerialiseSvg/' \
    -i test/EasyRdf/Serialiser/GraphVizTest.php
%endif

%if %{with_test}
: graphviz have optional gif support
sed 's/testSerialiseGif/SKIP_TEST_testSerialiseGif/' \
    -i test/EasyRdf/Serialiser/GraphVizTest.php

make test-lib
%else
: test suite disabled
%endif


%files
%defattr(-,root,root,-)
%doc *.md composer.json
%{_datadir}/php/EasyRdf.php
%{_datadir}/php/EasyRdf

%files doc
%defattr(-,root,root,-)
%doc LICENSE.md docs examples

%files test
%defattr(-,root,root,-)
%dir %{_datadir}/tests
     %{_datadir}/tests/%{name}


%changelog
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
