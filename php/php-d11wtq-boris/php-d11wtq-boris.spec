#
# RPM spec file for php-d11wtq-boris
#
# Copyright (c) 2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     borisrepl
%global github_name      boris
%global github_version   1.0.10
%global github_commit    31055b15e2d3fe47f31f6aa8e277f8f3fc7eb483

%global composer_vendor  d11wtq
%global composer_project boris

# "php": ">=5.3.0"
%global php_min_ver 5.3.0

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       2%{?dist}
Summary:       A tiny, but robust REPL (Read-Evaluate-Print-Loop) for PHP

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# Autoload generation
BuildRequires: %{_bindir}/phpab

# composer.json
Requires:      php-cli >= %{php_min_ver}
Requires:      php-pcntl
Requires:      php-posix
Requires:      php-readline
# phpcompatinfo (computed from version 1.0.10)
Requires:      php-pcre
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Python has one. Ruby has one. Clojure has one. Now PHP has one, too. Boris is
PHP's missing REPL (read-eval-print loop), allowing developers to experiment
with PHP code in the terminal in an interactive manner. If you make a mistake,
it doesn't matter, Boris will report the error and stand to attention for
further input.

Everything you enter into Boris is evaluated and the result inspected so you
can understand what is happening. State is maintained between inputs, allowing
you to gradually build up a solution to a problem.


%prep
%setup -qn %{github_name}-%{github_commit}

: Fix \\Boris\\Boris::VERSION
: See https://github.com/borisrepl/boris/pull/106
sed 's#1.0.8#%{version}#' -i lib/Boris/Boris.php

: Modify bin autoload require
sed "s#.*autoload.php.*#require_once '%{phpdir}/Boris/autoload.php';#" \
    -i bin/boris

: Remove provided autoloader
rm -f lib/autoload.php


%build
: Generate autoloader
%{_bindir}/phpab --nolower --output lib/Boris/autoload.php lib/Boris


%install
: Lib
mkdir -p %{buildroot}%{phpdir}
cp -pr lib/* %{buildroot}%{phpdir}/

: Bin
mkdir -p %{buildroot}%{_bindir}
install -pm 0755 bin/boris %{buildroot}%{_bindir}/


%check
: No upstream tests


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{_bindir}/boris
%{phpdir}/Boris


%changelog
* Sat May 30 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.10-2
- php(language) => php-cli dependency change

* Fri May 22 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.10-1
- Initial package
