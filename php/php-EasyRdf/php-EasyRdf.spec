%global php_min_ver 5.3.3

%if 0%{?fedora} > 9 || 0%{?rhel} > 5
%global with_test 1
%else
# need raptor 1.4.17
%global with_test 0
%endif

# TODO see for php-redland not yet available in remirepo

Name:          php-EasyRdf
Version:       0.8.0
Release:       1%{?dist}
Summary:       A PHP library designed to make it easy to consume and produce RDF

Group:         Development/Libraries
License:       BSD
URL:           http://www.easyrdf.org
Source0:       %{url}/downloads/easyrdf-%{version}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# For tests
BuildRequires: php(language) >= %{php_min_ver}
%if %{with_test}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
BuildRequires: graphviz
# provided by raptor or raptor2
BuildRequires: %{_bindir}/rapper
# For tests: phpcompatinfo (computed from 0.8.0)
BuildRequires: php-ctype
BuildRequires: php-date
BuildRequires: php-dom
BuildRequires: php-json
BuildRequires: php-libxml
BuildRequires: php-mbstring
BuildRequires: php-pcre
#BuildRequires: php-redland
BuildRequires: php-reflection
BuildRequires: php-simplexml
BuildRequires: php-spl
BuildRequires: php-xml
%endif

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo requires (computed from 0.8.0)
Requires:      php-ctype
Requires:      php-date
Requires:      php-dom
Requires:      php-json
Requires:      php-libxml
Requires:      php-mbstring
Requires:      php-pcre
#Requires:      php-redland
Requires:      php-simplexml
Requires:      php-spl
Requires:      php-xml

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

Optional dependencies: graphviz, graphviz-gd, raptor, raptor2


%package doc
Summary: Documentation for %{name}
Group:   Documentation

%description doc
%{summary}.


%prep
%setup -q -n easyrdf-%{version}


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php
cp -rp lib/* %{buildroot}%{_datadir}/php/


%check
%if %{with_test}
: Temporarily skipping tests that sometimes cause timeout exceptions
sed -e 's/testSerialiseSvg/SKIP_testSerialiseSvg/' \
    -e 's/testSerialiseGif/SKIP_testSerialiseGif/' \
    -e 's/testSerialiseSvg/SKIP_testSerialisePng/' \
    -i test/EasyRdf/Serialiser/GraphVizTest.php

# Create PHPUnit config
cat > phpunit.xml <<'PHPUNIT'
<?xml version="1.0" encoding="UTF-8"?>
<phpunit
    backupGlobals="false"
    backupStaticAttributes="false"
    colors="false"
    convertErrorsToExceptions="true"
    convertNoticesToExceptions="true"
    convertWarningsToExceptions="true"
    processIsolation="false"
    stopOnFailure="false"
    strict="true"
    syntaxCheck="false"
    verbose="false">
    <testsuites>
      <testsuite name="EasyRdf Library">
        <directory suffix="Test.php">./test/EasyRdf/</directory>
      </testsuite>
    </testsuites>
</phpunit>
PHPUNIT

phpunit -d date.timezone="UTC"
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


%changelog
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
