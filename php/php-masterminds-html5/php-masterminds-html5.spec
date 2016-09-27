# remirepo spec file for php-masterminds-html5, from:
#
# Fedora spec file for php-masterminds-html5
#
# Copyright (c) 2015-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     Masterminds
%global github_name      html5-php
%global github_version   2.2.2
%global github_commit    7866e93dcf0245de22378414e0c2c7350abc45af

%global composer_vendor  masterminds
%global composer_project html5

# "php" : ">=5.3.0"
%global php_min_ver 5.3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       An HTML5 parser and serializer

Group:         Development/Libraries
License:       MIT
URL:           http://masterminds.github.io/html5-php
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
# Autoload generation
BuildRequires: %{_bindir}/phpab
# Tests
%if %{with_tests}
## composer.json
BuildRequires: %{_bindir}/phpunit
BuildRequires: php(language) >= %{php_min_ver}
## phpcompatinfo (computed from version 2.2.2)
BuildRequires: php-ctype
BuildRequires: php-dom
BuildRequires: php-iconv
BuildRequires: php-json
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
BuildRequires: php-xml
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 2.2.2)
Requires:      php-ctype
Requires:      php-dom
Requires:      php-iconv
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-spl
Requires:      php-xml

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
The need for an HTML5 parser in PHP is clear. This project initially began with
the seemingly abandoned html5lib project original source. But after some initial
refactoring work, we began a new parser.

* An HTML5 serializer
* Support for PHP namespaces
* Composer support
* Event-based (SAX-like) parser
* DOM tree builder
* Interoperability with QueryPath


%prep
%setup -qn %{github_name}-%{github_commit}

: Docs
mkdir -p docs/{Parser,Serializer}
mv composer.json *.md docs/
mv src/HTML5/Parser/*.md docs/Parser/
mv src/HTML5/Serializer/*.md docs/Serializer/


%build
: Generate autoloader
# Vendor-level autoloader to pick up "Masterminds/HTML5" class
%{_bindir}/phpab --nolower --output src/autoload-html5.php src


%install
rm -rf %{buildroot}
mkdir -p  %{buildroot}%{phpdir}/Masterminds
cp -pr src/* %{buildroot}%{phpdir}/Masterminds/
# Project-level autoloader for consistency with other pkgs
ln -s ../autoload-html5.php %{buildroot}%{phpdir}/Masterminds/HTML5/autoload.php


%check
%if %{with_tests}
: Generate test autoloader
%{_bindir}/phpab --nolower --output test/autoload.php test

: Create mock Composer autoloader
mkdir vendor
cat > vendor/autoload.php <<'AUTOLOAD'
<?php

require '%{buildroot}%{phpdir}/Masterminds/HTML5/autoload.php';
require __DIR__ . '/../test/autoload.php';
AUTOLOAD

: Run tests
run=0
if which php56; then
   php56 %{_bindir}/phpunit
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit
   run=1
fi
if [ $run -eq 0 ]; then
   %{_bindir}/phpunit -v
fi
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc docs/*
%{phpdir}/Masterminds


%changelog
* Sun Sep 25 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.2.2-1
- Updated to 2.2.2 (RHBZ #1378444)

* Sun Jun 28 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.1.2-1
- Updated to 2.1.2 (RHBZ #1229011)

* Sun May 31 2015 Remi Collet <remi@remirepo.net> - 2.1.1-1
- backport in remi repository

* Fri May 22 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.1.1-1
- Initial package
