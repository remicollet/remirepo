# remirepo spec file for php-egulias-email-validator, from
#
# Fedora spec file for php-egulias-email-validator
#
# Copyright (c) 2014-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     egulias
%global github_name      EmailValidator
%global github_version   1.2.13
%global github_commit    b8bb147f46cc9790326ce2440a13be06cc5a63bb

%global composer_vendor  egulias
%global composer_project email-validator

# "php": ">= 5.3.3"
%global php_min_ver 5.3.3
# "doctrine/lexer": "^1.0.1"
#     NOTE: Min version not 1.0.1 because autoloader required
%global doctrine_lexer_min_ver 1.0.1-4
%global doctrine_lexer_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       A library for validating emails

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: php-composer(phpunit/phpunit)
## composer.json
BuildRequires: php(language)                >= %{php_min_ver}
#BuildRequires: php-composer(doctrine/lexer) >= %%{doctrine_lexer_min_ver}
BuildRequires: php-doctrine-lexer           >= %{doctrine_lexer_min_ver}
BuildRequires: php-composer(doctrine/lexer) <  %{doctrine_lexer_max_ver}
## phpcompatinfo (computed from version 1.2.13)
BuildRequires: php-filter
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                >= %{php_min_ver}
#Requires:      php-composer(doctrine/lexer) >= %%{doctrine_lexer_min_ver}
Requires:      php-doctrine-lexer           >= %{doctrine_lexer_min_ver}
Requires:      php-composer(doctrine/lexer) <  %{doctrine_lexer_max_ver}
# phpcompatinfo (computed from version 1.2.13)
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.

Autoloader: %{phpdir}/Egulias/EmailValidator/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee src/Egulias/EmailValidator/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Egulias\\EmailValidator\\', dirname(dirname(__DIR__)));

// Required dependency
require_once '%{phpdir}/Doctrine/Common/Lexer/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Skip testValidEmailsWithWarningsCheck and testInvalidEmailsWithDnsCheckAndStrictMode
# because Koji does not have network access so assertEquals(expected_warnings, actual_warnings)
# fails because EmailValidator::DNSWARN_NO_RECORD is not an expected warning
sed -e 's/function testValidEmailsWithWarningsCheck/function SKIP_testValidEmailsWithWarningsCheck/' \
    -e 's/function testInvalidEmailsWithDnsCheckAndStrictMode/function SKIP_testInvalidEmailsWithDnsCheckAndStrictMode/' \
    -i tests/egulias/Tests/EmailValidator/EmailValidatorTest.php

: Run tests
ret=0
run=0
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/Egulias/EmailValidator/autoload.php || ret=1
   run=1
fi
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/Egulias/EmailValidator/autoload.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
  %{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}%{phpdir}/Egulias/EmailValidator/autoload.php
fi
exit $ret;
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%doc composer.json
%dir %{phpdir}/Egulias
     %{phpdir}/Egulias/EmailValidator


%changelog
* Mon Aug 08 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.13-1
- Updated to 1.2.13 (RHBZ #1336594)

* Mon Jan 04 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.11-1
- Updated to 1.2.10 (RHBZ #1280283)

* Sun Oct 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.10-1
- Updated to 1.2.10 (RHBZ #1270623)
- Modified autoloader to load dependencies after self-registration

* Sat Jun 27 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.9-1
- Updated to 1.2.9 (RHBZ #1215684)
- Added autoloader

* Mon Jan 05 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.7-1
- Updated to 1.2.7 (BZ #1178809)

* Sun Dec 07 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.6-1
- Updated to 1.2.6 (BZ #1171051)

* Sun Nov 09 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.5-1
- Updated to 1.2.5

* Thu Nov  6 2014 Remi Collet <remi@fedoraproject.org> - 1.2.4-1
- backport for remi repository

* Mon Nov 03 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.4-1
- Updated to 1.2.4

* Mon Oct 27 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.3-1
- Updated to 1.2.3

* Wed Sep 10 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.2-1
- Initial package
