# spec file for php-phpdocumentor-reflection
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    fc40c3f604ac2287eb5c314174d5109b2c699372
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     phpDocumentor
%global gh_project   Reflection
%global with_tests   0%{!?_without_tests:1}

%global with_php_parser 1

Name:           php-phpdocumentor-reflection
Version:        1.0.7
Release:        1%{?dist}
Summary:        Reflection library to do Static Analysis for PHP Projects

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

%if %{with_php_parser}
# Temporary, bundled nikik/php-parser 0.9.4
%global php_parser_owner   nikic
%global php_parser_project PHP-Parser
%global php_parser_commit  1e5e280ae88a27effa2ae4aa2bd088494ed8594f
%global php_parser_version 0.9.4
Source1:        https://github.com/%{php_parser_owner}/%{php_parser_project}/archive/%{php_parser_commit}/%{php_parser_project}-%{php_parser_version}.tar.gz
Provides:       bundled(nikic/php-parser) = %{php_parser_version}
%endif

# Temporary, missing in old versions
Source2:        https://raw.githubusercontent.com/phpDocumentor/Reflection/develop/LICENSE

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-theseer-autoload
# For tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-composer(psr/log) >= 1.0
%if ! %{with_php_parser}
BuildRequires:  php-composer(nikic/php-parser) >= 0.9.4
%endif
BuildRequires:  php-composer(phpdocumentor/reflection-docblock) >= 2.0
# From composer.json, "require-dev": {
#        "behat/behat": "~2.4",
#        "phpunit/phpunit": "~4.0",
#        "mockery/mockery": "~0.8"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.0
BuildRequires:  php-composer(mockery/mockery) >= 0.8
%endif

# From composer.json, require
#        "php": ">=5.3.3",
#        "psr/log": "~1.0",
#        "nikic/php-parser": "~0.9.4",
#        "phpdocumentor/reflection-docblock": "~2.0"
Requires:       php(language) >= 5.3.3
Requires:       php-composer(psr/log) >= 1.0
Requires:       php-composer(psr/log) <  2
%if ! %{with_php_parser}
Requires:       php-composer(nikic/php-parser) >= 0.9.4
Requires:       php-composer(nikic/php-parser) <  0.10
%endif
Requires:       php-composer(phpdocumentor/reflection-docblock) >= 2.0
Requires:       php-composer(phpdocumentor/reflection-docblock) <  3
# For autoloader
Requires:       php-PsrLog >= 1.0.0-8
# From phpcompatinfo report for 2.0.3
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(phpdocumentor/reflection) = %{version}


%description
Using this library it is possible to statically reflect one or more files
and create an object graph representing your application's structure,
including accompanying in-source documentation using DocBlocks.

The information that this library provides is similar to what the (built-in)
Reflection extension of PHP provides; there are however several advantages
to using this library:

* Due to its Static nature it does not execute procedural code in your
  reflected files where Dynamic Reflection does.
* Because the none of the code is interpreted by PHP (and executed)
  Static Reflection uses less memory.
* Can reflect complete files
* Can reflect a whole project by reflecting multiple files.
* Reflects the contents of a DocBlock instead of just mentioning there is one.
* Is capable of analyzing code written for any PHP version (starting at 5.2)
  up to and including your installed PHP version.

Features
* [Creates an object graph] containing the structure of your application much
  like a site map shows the structure of a website.
* Can read and interpret code of any PHP version starting with 5.2 up to and
  including your currently installed version of PHP.
* Due it's clean interface it can be in any application without a complex setup.

Autoloader: %{_datadir}/php/phpDocumentor/Reflection/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit} -a 1

%if %{with_php_parser}
# Include PHPParser in this library, as old deprecated version required
mv %{php_parser_project}-%{php_parser_commit}/lib/PHPParser \
    src/phpDocumentor/Reflection/PHPParser
mv %{php_parser_project}-%{php_parser_commit}/LICENSE LICENSE-PHPParser
%endif

cp %{SOURCE2} LICENSE


%build
: Generate library autoloader
%{_bindir}/phpab \
  --output  src/phpDocumentor/Reflection/autoload.php \
  src/phpDocumentor/Reflection

cat << 'EOF' | tee -a src/phpDocumentor/Reflection/autoload.php
// Dependencies
require_once '%{_datadir}/php/Psr/Log/autoload.php';
require_once '%{_datadir}/php/phpDocumentor/Reflection/DocBlock/autoload.php';
%if ! %{with_php_parser}
require_once '%{_datadir}/php/PhpParser/autoload.php';
%endif
EOF


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{_datadir}/php
cp -pr src/* %{buildroot}%{_datadir}/php


%check
%if %{with_tests}
: Fix path to Mockery
sed -e 's:vendor/mockery/mockery/library:/usr/share/php:' \
    phpunit.xml.dist > phpunit.xml

: Create tests autoloader
mkdir vendor
%{_bindir}/phpab --output vendor/autoload.php tests

cat << 'EOF' | tee -a vendor/autoload.php
require_once '%{_datadir}/php/Mockery/autoload.php';
require_once '%{buildroot}%{_datadir}/php/phpDocumentor/Reflection/autoload.php';
EOF

%{_bindir}/phpunit --verbose

if which php70; then
  php70 %{_bindir}/phpunit --verbose
fi
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE*
%doc *.md
%doc composer.json
%{_datadir}/php/phpDocumentor/Reflection/*


%changelog
* Thu Apr 14 2016 Remi Collet <remi@fedoraproject.org> - 1.0.7-1
- initial package, version 1.0.7
- bundle nikic/php-parser 0.9.4
