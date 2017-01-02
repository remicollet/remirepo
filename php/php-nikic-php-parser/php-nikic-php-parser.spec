# remirepo/fedora spec file for php-nikic-php-parser
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    4dd659edadffdc2143e4753df655d866dbfeedf0
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nikic
%global gh_project   PHP-Parser
%global pk_project   php-parser
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

%global eolv1   0
%global script  0
%if 0%{?fedora} >= 24 && 0%{?fedora} < 26
%global script  1
%endif
# remirepo:1
%global script  0

Name:           php-%{gh_owner}-%{pk_project}
Version:        2.1.1
Release:        2%{?dist}
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
BuildRequires:  php(language) >= 5.4
BuildRequires:  php-tokenizer
BuildRequires:  php-filter
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-xmlreader
BuildRequires:  php-xmlwriter
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "~4.0"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.0
%endif

# From composer.json, "require": {
#        "php": ">=5.4",
#        "ext-tokenizer": "*"
Requires:       php(language) >= 5.4
Requires:       php-tokenizer
# From phpcompatinfo report for version 2.0.1
Requires:       php-filter
Requires:       php-pcre
Requires:       php-spl
Requires:       php-xmlreader
Requires:       php-xmlwriter
%if %{eolv1}
Obsoletes:      php-PHPParser < 2
%endif
%if %{script}
Requires:       php-cli
# previous version provides the php-parse command
Conflicts:      php-PHPParser < 1.4.1-4
%endif

Provides:       php-composer(%{gh_owner}/%{pk_project}) = %{version}


%description
This is a PHP 5.2 to PHP 7.0 parser written in PHP.
Its purpose is to simplify static code analysis and manipulation.
%if %{script}
This package provides the library version 2 and the php-parse command.
%else
This package provides the library version 2.
%endif
The %{name}3 packages provides the library version 3.
The php-PHPParser package provides the library version 1.

Documentation: https://github.com/nikic/PHP-Parser/tree/2.x/doc

Autoloader: %{php_home}/PhpParser2/autoload.php


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
cp -pr lib/PhpParser     %{buildroot}%{php_home}/PhpParser2
cp -p  lib/bootstrap.php %{buildroot}%{php_home}/PhpParser2/autoload.php

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
%{php_home}/PhpParser2


%changelog
* Wed Dec  7 2016 Remi Collet <remi@fedoraproject.org> - 2.1.1-2
- drop the php-parse command, provided by php-nikic-php-parser3

* Mon Sep 19 2016 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- update to 2.1.1

* Fri May 20 2016 Remi Collet <remi@fedoraproject.org> - 2.1.0-3
- add the php-parse command, no more in php-nikic-php-parser

* Mon May 16 2016 Remi Collet <remi@fedoraproject.org> - 2.1.0-3
- drop exec right in doc, fix rpmlint

* Wed Apr 20 2016 Remi Collet <remi@fedoraproject.org> - 2.1.0-2
- fix test suite, add upstream patch

* Wed Apr 20 2016 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- initial package, version 2.1.0
- drop patches merged upstream
- open https://github.com/nikic/PHP-Parser/issues/271
  issue with test/code/parser/expr/new.test

* Fri Apr 15 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- initial package, version 2.0.1
- open https://github.com/nikic/PHP-Parser/pull/268
  make the autoloader more PSR-4
- open https://github.com/nikic/PHP-Parser/pull/269
  support -h and --help standard options

