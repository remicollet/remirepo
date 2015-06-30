# remirepo spec file for php-egulias-email-validator, from
#
# Fedora spec file for php-egulias-email-validator
#
# Copyright (c) 2014-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     egulias
%global github_name      EmailValidator
%global github_version   1.2.9
%global github_commit    af864423f50ea59f96c87bb1eae147a70bcf67a1

%global composer_vendor  egulias
%global composer_project email-validator

# "php": ">= 5.3.3"
%global php_min_ver 5.3.3
# "doctrine/lexer": "~1.0,>=1.0.1"
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
BuildRequires: %{_bindir}/phpunit
## composer.json
BuildRequires: php(language)                >= %{php_min_ver}
#BuildRequires: php-composer(doctrine/lexer) >= %%{doctrine_lexer_min_ver}
BuildRequires: php-doctrine-lexer           >= %{doctrine_lexer_min_ver}
BuildRequires: php-composer(doctrine/lexer) <  %{doctrine_lexer_max_ver}
## phpcompatinfo (computed from version 1.2.9)
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
# phpcompatinfo (computed from version 1.2.9)
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
(cat <<'AUTOLOAD'
<?php
/**
 * Autoloader created by %{name}-%{version}-%{release}
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

require_once '%{phpdir}/Doctrine/Common/Lexer/autoload.php';

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Egulias\\EmailValidator\\', dirname(dirname(__DIR__)));

return $fedoraClassLoader;
AUTOLOAD
) | tee src/Egulias/EmailValidator/autoload.php


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
%{_bindir}/phpunit -v --bootstrap %{buildroot}%{phpdir}/Egulias/EmailValidator/autoload.php
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
