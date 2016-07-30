#
# Fedora spec file for php-simplesamlphp-saml2
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve the changelog entries
#

%global github_owner     simplesamlphp
%global github_name      saml2
%global github_version   2.2
%global github_commit    0d6861bc2966249702e623d325609adb2a782612

%global composer_vendor  simplesamlphp
%global composer_project saml2

# "php": ">=5.3.3"
%global php_min_ver 5.3.3
# "mockery/mockery": "~0.9"
%global mockery_min_ver 0.9
%global mockery_max_ver 1.0
# "psr/log": "~1.0"
#     NOTE: Min version not 1.0 because autoloader required
%global psr_log_min_ver 1.0.0-8
%global psr_log_max_ver 2.0
# "robrichards/xmlseclibs": "^2.0"
%global robrichards_xmlseclibs_min_ver 2.0
%global robrichards_xmlseclibs_max_ver 3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       SAML2 PHP library from SimpleSAMLphp

Group:         Development/Libraries
License:       LGPLv2
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language)                        >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
#BuildRequires: php-composer(psr/log)                >= %%{psr_log_min_ver}
BuildRequires: php-PsrLog                           >= %{psr_log_min_ver}
BuildRequires: php-composer(robrichards/xmlseclibs) >= %{robrichards_xmlseclibs_min_ver}
BuildRequires: php-dom
BuildRequires: php-openssl
%if 0%{!?el6:1}
BuildRequires: php-composer(mockery/mockery)        >= %{mockery_min_ver}
%endif
## phpcompatinfo (computed from version 2.2)
BuildRequires: php-date
BuildRequires: php-libxml
BuildRequires: php-mcrypt
BuildRequires: php-pcre
BuildRequires: php-soap
BuildRequires: php-spl
BuildRequires: php-zlib
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                        >= %{php_min_ver}
Requires:      php-composer(psr/log)                <  %{psr_log_max_ver}
#Requires:      php-composer(psr/log)                >= %%{psr_log_min_ver}
Requires:      php-PsrLog                           >= %{psr_log_min_ver}
Requires:      php-composer(robrichards/xmlseclibs) <  %{robrichards_xmlseclibs_max_ver}
Requires:      php-composer(robrichards/xmlseclibs) >= %{robrichards_xmlseclibs_min_ver}
Requires:      php-dom
Requires:      php-openssl
# phpcompatinfo (computed from version 2.2)
Requires:      php-date
Requires:      php-libxml
Requires:      php-pcre
Requires:      php-soap
Requires:      php-spl
Requires:      php-zlib
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}


%description
A PHP library for SAML2 related functionality. Extracted from SimpleSAMLphp [1],
used by OpenConext [2]. This library started as a collaboration between
UNINETT [3] and SURFnet [4] but everyone is invited to contribute.

Autoloader: %{phpdir}/SAML2/autoload.php

[1] https://www.simplesamlphp.org/
[2] https://www.openconext.org/
[3] https://www.uninett.no/
[4] https://www.surfnet.nl/


%prep
%setup -qn %{github_name}-%{github_commit}

: Remove upstream temporary autoloader
rm -f src/_autoload.php


%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/SAML2/autoload.php
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

$fedoraClassLoader->addPrefix('SAML2', dirname(__DIR__));

// Required dependencies
require_once '%{phpdir}/Psr/Log/autoload.php';
require_once '%{phpdir}/RobRichards/XMLSecLibs/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create pseudo Composer autoloader
mkdir vendor
cat <<'AUTOLOAD' | tee vendor/autoload.php
<?php
$fedoraClassLoader = require '%{buildroot}%{phpdir}/SAML2/autoload.php';
$fedoraClassLoader->addPrefix('SAML2', dirname(__DIR__).'/tests');
%if 0%{!?el6:1}
require_once '%{phpdir}/Mockery/autoload.php';
%endif
AUTOLOAD

%if 0%{?el6}
: Remove tests requiring Mockery
grep -r --files-with-matches Mockery tests | xargs rm -f
%endif

: Run tests
%{_bindir}/phpunit --configuration=tools/phpunit --verbose
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{phpdir}/SAML2


%changelog
* Fri Jul 29 2016 Shawn Iwinski <shawn@iwin.ski> - 2.2-2
- Remove upstream temporary autoloader

* Sun Jul 10 2016 Shawn Iwinski <shawn@iwin.ski> - 2.2-1
- Initial package
