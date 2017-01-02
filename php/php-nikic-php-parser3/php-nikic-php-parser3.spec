# remirepo/fedora spec file for php-nikic-php-parser3
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    adf44419c0fc014a0f191db6f89d3e55d4211744
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nikic
%global gh_project   PHP-Parser
%global pk_project   php-parser
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}
%global major        3
%global minor        0.2

%global eolv1   0
%global eolv2   0
%global script  0
%if 0%{?fedora} >= 26
%global script  1
%endif
# remirepo:1
%global script  1

Name:           php-%{gh_owner}-%{pk_project}%{major}
Version:        %{major}.%{minor}
Release:        1%{?dist}
Summary:        A PHP parser written in PHP

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source:         https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz

# Autoloader
Patch0:         %{name}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# For tests
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-tokenizer
BuildRequires:  php-filter
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-xmlreader
BuildRequires:  php-xmlwriter
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "~4.0|~5.0"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.0
%endif

# From composer.json, "require": {
#        "php": ">=5.5",
#        "ext-tokenizer": "*"
Requires:       php(language) >= 5.5
Requires:       php-tokenizer
# From phpcompatinfo report for version 3.0.2
Requires:       php-filter
Requires:       php-json
Requires:       php-pcre
Requires:       php-spl
Requires:       php-xmlreader
Requires:       php-xmlwriter
%if %{eolv1}
Obsoletes:      php-PHPParser < %{major}
%endif
%if %{eolv2}
Obsoletes:      php-%{gh_owner}-%{pk_project} < %{major}
%endif
%if %{script}
Requires:       php-cli
# previous version provides the php-parse command
Conflicts:      php-PHPParser < 1.4.1-4
Conflicts:      php-%{gh_owner}-%{pk_project} < 2.1.1-2
%endif

Provides:       php-composer(%{gh_owner}/%{pk_project}) = %{version}


%description
This is a PHP 5.2 to PHP 7.1 parser written in PHP.
Its purpose is to simplify static code analysis and manipulation.
%if %{script}
This package provides the library version 3 and the php-parse command.
%else
This package provides the library version 3.
%endif
The php-%{gh_owner}-%{pk_project} package provides the library version 2.
The php-PHPParser package provides the library version 1.

Documentation: https://github.com/nikic/PHP-Parser/tree/master/doc

Autoloader: %{php_home}/PhpParser%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1 -b .rpm

%if ! %{script}
chmod -x bin/*
%endif


%build
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

: Library
mkdir -p                 %{buildroot}%{php_home}
cp -pr lib/PhpParser     %{buildroot}%{php_home}/PhpParser%{major}
cp -p  lib/bootstrap.php %{buildroot}%{php_home}/PhpParser%{major}/autoload.php

%if %{script}
: Command
install -Dpm 0755 bin/php-parse %{buildroot}%{_bindir}/php-parse
%endif


%check
%if %{with_tests}
: Test the command
sed -e 's:%{php_home}:%{buildroot}%{php_home}:' \
    bin/php-parse > bin/php-parse-test
php bin/php-parse-test --help

: Test suite autoloader
sed -e 's:@BUILDROOT@:%{buildroot}:' -i test/bootstrap.php

: Upstream test suite
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose
# remirepo:2
fi
exit $ret
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json
%doc *.md
%if %{script}
%{_bindir}/php-parse
%else
%doc bin/php-parse
%endif
%{php_home}/PhpParser%{major}


%changelog
* Wed Dec 7  2016 Remi Collet <remi@fedoraproject.org> - 3.0.2-1
- new package for library version 3

