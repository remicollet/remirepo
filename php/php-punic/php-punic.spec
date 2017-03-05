# remirepo spec file for php-punic, from
#
# Fedora spec file for php-punic
#
# Copyright (c) 2015-2017 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     punic
%global github_name      punic
%global github_version   1.6.5
%global github_commit    7bc85ce1137cf52db4d2a6298256a4c4a24da99a

%global composer_vendor  punic
%global composer_project punic

# "php": ">=5.3"
%global php_min_ver 5.3

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       PHP-Unicode CLDR

Group:         Development/Libraries
# Code is MIT, data is Unicode
License:       MIT and Unicode
URL:           http://punic.github.io/

# GitHub export does not include tests.
# Run php-punic-get-source.sh to create full source.
Source0:       %{name}-%{github_version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Relative paths
BuildRequires: python
# Tests
%if %{with_tests}
BuildRequires: php-composer(phpunit/phpunit)
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
## phpcompatinfo (computed from version 1.6.5)
BuildRequires: php-date
BuildRequires: php-iconv
BuildRequires: php-intl
BuildRequires: php-json
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-spl
BuildRequires: php-zip
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.6.5)
Requires:      php-date
Requires:      php-iconv
Requires:      php-intl
Requires:      php-json
Requires:      php-mbstring
Requires:      php-pcre
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming
Provides:      php-%{composer_vendor}-%{composer_project} = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
PHP-Unicode CLDR Toolkit

Punic is a PHP library using the CLDR data to help you localize various
variables like numbers, dates, units, lists, ...

For full API reference see the APIs reference [1].

Autoloader: %{phpdir}/Punic/autoload.php

[1] http://punic.github.io/docs


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Create autoloader
cat <<'AUTOLOAD' | tee code/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 */
require_once '%{phpdir}/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Punic\\', __DIR__);
AUTOLOAD


%install
rm -rf     %{buildroot}

: Library
mkdir -p %{buildroot}%{phpdir}/Punic
cp -rp code/* %{buildroot}%{phpdir}/Punic/

: Data
mkdir -p %{buildroot}%{_datadir}
mv %{buildroot}%{phpdir}/Punic/data %{buildroot}%{_datadir}/%{name}
ln -s \
    ../../%{name} \
    %{buildroot}%{phpdir}/Punic/data


%check
%if %{with_tests}
: Skip tests known to fail
sed 's/function testDescribeInterval/function SKIP_testDescribeInterval/' \
    -i tests/Calendar/CalendarTest.php

BOOTSTRAP=%{buildroot}%{phpdir}/Punic/autoload.php

%{_bindir}/phpunit --verbose --bootstrap $BOOTSTRAP

: Upstream tests with SCLs if available
SCL_RETURN_CODE=0
for SCL in %{?rhel:php54 php55} php56 php70 php71; do
    if which $SCL; then
        $SCL %{_bindir}/phpunit --verbose --bootstrap $BOOTSTRAP || SCL_RETURN_CODE=1
    fi
done
exit $SCL_RETURN_CODE
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%license UNICODE-LICENSE.txt
%doc *.md
%doc composer.json
%{phpdir}/Punic
%{_datadir}/%{name}


%changelog
* Sat Mar 04 2017 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.6.5-1
- Update to 1.6.5 (RHBZ #1419293)
- Test with SCLs if available

* Sat Feb  4 2017 Remi Collet <remi@remirepo.net> - 1.6.5-1
- update to 1.6.5

* Sat Nov 26 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.6.4-1
- Update to 1.6.4 (RHBZ #1397224)
- Switch autoloader from php-composer(symfony/class-loader) to
  php-composer(fedora/autoloader)
- Fix FTBFS

* Tue Nov 22 2016 Remi Collet <remi@remirepo.net> - 1.6.4-1
- update to 1.6.4

* Mon Sep 21 2015 Remi Collet <remi@remirepo.net> - 1.6.3-1
- backport for #remirepo

* Fri Sep 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.6.3-1
- Initial package
