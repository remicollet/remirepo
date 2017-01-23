# remirepo/fedora spec file for php-phpmyadmin-sql-parser
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit    d070a5263f16128cb777c084981c7061a9a2dda3
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     phpmyadmin
#global gh_date      20150820
%global gh_project   sql-parser
%global with_tests   0%{!?_without_tests:1}
%global ns_vendor    PhpMyAdmin
%global ns_project   SqlParser
%if 0%{?fedora} >= 26
%global with_cmd     1
%else
%global with_cmd     0
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        4.0.0
Release:        1%{?gh_date?%{gh_date}git%{gh_short}}%{?dist}
Summary:        A validating SQL lexer and parser with a focus on MySQL dialect

Group:          Development/Libraries
License:        GPLv2+
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}-%{?gh_short}.tar.gz

# Use our autoloader
Patch0:         %{name}-autoload.patch

BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.0
# For tests, from composer.json "require-dev": {
#        "phpunit/php-code-coverage": "~2.0 || ~3.0",
#        "phpunit/phpunit": "~4.8 || ~5.1"
BuildRequires:  php-composer(phpunit/phpunit)
%endif
# For autoloader
BuildRequires:  php-composer(fedora/autoloader)

# From composer.json, "require": {
#        "php": ">=5.3.0",
#        "ext-mbstring": "*"
Requires:       php(language) >= 5.3
Requires:       php-mbstring
# From phpcompatinfo report for 3.4.5
Requires:       php-ctype
Requires:       php-pcre
# For generated autoloader
Requires:       php-composer(fedora/autoloader)
%if %{with_cmd}
Requires:       php-cli
%endif

# Composer
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
A validating SQL lexer and parser with a focus on MySQL dialect.

This library was originally developed for phpMyAdmin during
the Google Summer of Code 2015.

Autoloader: %{_datadir}/php/%{ns_vendor}/%{ns_project}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}
%patch0 -p0 -b .rpm


%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
/* Autoloader for %{name} and its dependencies */
require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('%{ns_vendor}\\%{ns_project}\\', __DIR__);
AUTOLOAD


%install
: Library
mkdir -p   %{buildroot}%{_datadir}/php/%{ns_vendor}
cp -pr src %{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_project}

%if %{with_cmd}
: Commands
install -Dpm 0755 bin/highlight-query %{buildroot}%{_bindir}/%{gh_project}-highlight-query
install -Dpm 0755 bin/lint-query      %{buildroot}%{_bindir}/%{gh_project}-lint-query
%endif


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require '%{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_project}/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('%{ns_vendor}\\%{ns_project}\\Tests\\', dirname(__DIR__).'/tests');
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
%{_bindir}/phpunit --no-coverage --verbose
# remirepo:2
fi
exit $ret
%else
: Test suite disabled
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc composer.json
%doc README.md
%if %{with_cmd}
%{_bindir}/%{gh_project}-highlight-query
%{_bindir}/%{gh_project}-lint-query
%endif
%dir %{_datadir}/php/%{ns_vendor}/
     %{_datadir}/php/%{ns_vendor}/%{ns_project}


%changelog
* Mon Jan 23 2017 Remi Collet <remi@fedoraproject.org> - 4.0.0-1
- update to 4.0.0
- rename to php-phpmyadmin-sql-parser

* Fri Jan 20 2017 Remi Collet <remi@fedoraproject.org> - 3.4.17-1
- update to 3.4.17
- sources from a git snapshot to retrieve test suite
- switch to PSR-4 autoloader

* Fri Jan  6 2017 Remi Collet <remi@fedoraproject.org> - 3.4.16-1
- update to 3.4.16

* Mon Jan  2 2017 Remi Collet <remi@fedoraproject.org> - 3.4.15-1
- update to 3.4.15

* Wed Nov 30 2016 Remi Collet <remi@fedoraproject.org> - 3.4.14-1
- update to 3.4.14

* Wed Nov 16 2016 Remi Collet <remi@fedoraproject.org> - 3.4.13-1
- update to 3.4.13

* Wed Nov  9 2016 Remi Collet <remi@fedoraproject.org> - 3.4.12-1
- update to 3.4.12
- switch to fedora/autoloader

* Tue Oct 25 2016 Remi Collet <remi@fedoraproject.org> - 3.4.11-1
- update to 3.4.11

* Tue Oct  4 2016 Remi Collet <remi@fedoraproject.org> - 3.4.10-1
- update to 3.4.10

* Mon Oct  3 2016 Remi Collet <remi@fedoraproject.org> - 3.4.9-1
- update to 3.4.9

* Thu Sep 22 2016 Remi Collet <remi@fedoraproject.org> - 3.4.8-1
- update to 3.4.8 (no change)

* Tue Sep 20 2016 Remi Collet <remi@fedoraproject.org> - 3.4.7-1
- update to 3.4.7

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
