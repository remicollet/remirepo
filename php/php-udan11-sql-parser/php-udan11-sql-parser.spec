# remirepo/fedora spec file for php-udan11-sql-parser
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    a0d8069906d464de75bea761acb9fdde0aa2ee72
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     phpmyadmin
#global gh_date      20150820
%global gh_project   sql-parser
%global with_tests   0%{!?_without_tests:1}
%global psr0         SqlParser

Name:           php-udan11-%{gh_project}
Version:        3.4.6
Release:        1%{?gh_date?%{gh_date}git%{gh_short}}%{?dist}
Summary:        A validating SQL lexer and parser with a focus on MySQL dialect

Group:          Development/Libraries
License:        GPLv2+
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{?gh_short}.tar.gz

# Use our autoloader
Patch0:         %{name}-autoload.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.0
# For tests, from composer.json "require-dev": {
#        "phpunit/php-code-coverage": "~2.0 || ~3.0",
#        "phpunit/phpunit": "~4.8 || ~5.1"
BuildRequires:  php-composer(phpunit/phpunit)
%endif
# For autoloader
BuildRequires:  php-composer(theseer/autoload)

# From composer.json, "require": {
#        "php": ">=5.3.0",
#        "ext-mbstring": "*"
Requires:       php(language) >= 5.3
Requires:       php-mbstring
# From phpcompatinfo report for 3.4.5
Requires:       php-ctype
Requires:       php-pcre
# For generated autoloader
Requires:       php-spl

# Rename
Obsoletes:      php-dmitry-php-sql-parser < 0-0.2
Provides:       php-dmitry-php-sql-parser = %{version}-%{release}
# New packagist name
Provides:       php-phpmyadmin-sql-parser = %{version}-%{release}

# Composer
Provides:       php-composer(udan11/%{gh_project})      = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
A validating SQL lexer and parser with a focus on MySQL dialect.

This library was originally developed for phpMyAdmin during
the Google Summer of Code 2015.

Autoloader: %{_datadir}/php/%{psr0}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}
%patch0 -p0 -b .rpm


%build
: generate an simple autoloader
%{_bindir}/phpab --output src/autoload.php src


%install
rm -rf     %{buildroot}

: Library
mkdir -p   %{buildroot}%{_datadir}/php
cp -pr src %{buildroot}%{_datadir}/php/%{psr0}

: Commands
install -Dpm 0755 bin/highlight-query %{buildroot}%{_bindir}/%{gh_project}-highlight-query
install -Dpm 0755 bin/lint-query      %{buildroot}%{_bindir}/%{gh_project}-lint-query


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require '%{buildroot}%{_datadir}/php/%{psr0}/autoload.php';
EOF

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --no-coverage || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --no-coverage || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
if %{_bindir}/phpunit --atleast-version 4.8; then
   %{_bindir}/phpunit --no-coverage --verbose
fi
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
%license LICENSE.txt
%doc composer.json
%doc README.md
%{_datadir}/php/%{psr0}
%{_bindir}/%{gh_project}-highlight-query
%{_bindir}/%{gh_project}-lint-query


%changelog
* Tue Sep 13 2016 Remi Collet <remi@fedoraproject.org> - 3.4.6-1
- update to 3.4.6
- lower dependency on php >= 5.3

* Tue Sep 13 2016 Remi Collet <remi@fedoraproject.org> - 3.4.5-1
- update to 3.4.5

* Tue Jul 26 2016 Remi Collet <remi@fedoraproject.org> - 3.4.4-1
- update to 3.4.4
- switch from udan11/sql-parser to phpmyadmin/sql-parser
- add sql-parser-highlight-query and sql-parser-lint-query commands

* Tue Mar  1 2016 Remi Collet <remi@fedoraproject.org> - 3.4.0-1
- update to 3.4.0 (for phpMyAdmin 4.5.5.1)
- add patch from phpMyAdmin
- raise dependency on php >= 5.4

* Tue Feb 23 2016 Remi Collet <remi@fedoraproject.org> - 3.3.1-1
- update to 3.3.1 (for phpMyAdmin 4.5.5)
- don't run test with old PHPUnit (EPEL-6)

* Sat Dec 26 2015 Remi Collet <remi@fedoraproject.org> - 3.0.8-1
- update to 3.0.8 (for phpMyAdmin 4.5.3)

* Fri Nov 13 2015 Remi Collet <remi@fedoraproject.org> - 3.0.7-1
- update to 3.0.7
- run test suite with both PHP 5 and 7 when available

* Sun Nov  8 2015 Remi Collet <remi@fedoraproject.org> - 3.0.5-1
- update to 3.0.5

* Thu Oct 22 2015 Remi Collet <remi@fedoraproject.org> - 3.0.4-1
- update to 3.0.4 (for upcoming phpMyAdmin 4.5.1)

* Mon Oct 19 2015 Remi Collet <remi@fedoraproject.org> - 3.0.3-1
- update to 3.0.3 (for upcoming phpMyAdmin 4.5.1)

* Wed Sep 23 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- upstream patch for phpMyAdmin 4.5.0.2

* Wed Sep 23 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- tagged as 1.0.0 (no change)

* Sun Sep 20 2015 Remi Collet <remi@fedoraproject.org> - 0-0.3.20150820git1b2988f
- fix provides and self-obsoletion (review #1262807)

* Mon Sep 14 2015 Remi Collet <remi@fedoraproject.org> - 0-0.2.20150820git1b2988f
- rename to php-udan11-sql-parser

* Mon Sep 14 2015 Remi Collet <remi@fedoraproject.org> - 0-0.1.20150629git4aaed44
- initial package
