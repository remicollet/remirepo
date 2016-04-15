#
# Fedora spec file for php-akamai-open-edgegrid-client
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     akamai-open
%global github_name      AkamaiOPEN-edgegrid-php
%global github_version   0.4.4
%global github_commit    4eb9f733cfcd0e1574896b456f62296355bb816f

%global composer_vendor  akamai-open
%global composer_project edgegrid-client

# "php": ">=5.5"
%global php_min_ver 5.5
# "guzzlehttp/guzzle": "~6.0"
%global guzzle_min_ver 6.0
%global guzzle_max_ver 7.0
# "monolog/monolog": "^1.15"
%global monolog_min_ver 1.15
%global monolog_max_ver 2.0
# "psr/log": "^1.0"
#     NOTE: Min version not 1.0 because autoloader required
%global psr_log_min_ver 1.0.0-8
%global psr_log_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Implements the Akamai {OPEN} EdgeGrid Authentication

Group:         Development/Libraries
License:       ASL 2.0
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language)                   >= %{php_min_ver}
BuildRequires: php-composer(guzzlehttp/guzzle) >= %{guzzle_min_ver}
BuildRequires: php-composer(monolog/monolog)   >= %{monolog_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
#BuildRequires: php-composer(psr/log)           >= %%{psr_log_min_ver}
BuildRequires: php-PsrLog                      >= %{psr_log_min_ver}
## phpcompatinfo (computed from version 0.4.4)
BuildRequires: php-date
BuildRequires: php-hash
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                   >= %{php_min_ver}
Requires:      php-composer(guzzlehttp/guzzle) >= %{guzzle_min_ver}
Requires:      php-composer(guzzlehttp/guzzle) <  %{guzzle_max_ver}
Requires:      php-composer(monolog/monolog)   >= %{monolog_min_ver}
Requires:      php-composer(monolog/monolog)   <  %{monolog_max_ver}
#Requires:      php-composer(psr/log)           >= %%{psr_log_min_ver}
Requires:      php-PsrLog                      >= %{psr_log_min_ver}
Requires:      php-composer(psr/log)           <  %{psr_log_max_ver}
# phpcompatinfo (computed from version 0.4.4)
Requires:      php-date
Requires:      php-hash
Requires:      php-json
Requires:      php-pcre
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Akamai {OPEN} EdgeGrid Authentication [1] for PHP

This library implements the Akamai {OPEN} EdgeGrid Authentication scheme on top
of Guzzle, as both a drop-in replacement client, and middleware.

For more information visit the Akamai {OPEN} Developer Community [2].

Autoloader: %{phpdir}/Akamai/Open/EdgeGrid/autoload.php

[1] https://developer.akamai.com/introduction/Client_Auth.html
[2] https://developer.akamai.com/


%prep
%setup -qn %{github_name}-%{github_commit}

: Remove CLI
rm -f src/Cli.php

%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/autoload.php
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

$fedoraClassLoader->addPrefix('Akamai\\Open\\EdgeGrid\\', dirname(dirname(dirname(__DIR__))));

// Required dependencies
require_once '%{phpdir}/GuzzleHttp6/autoload.php';
require_once '%{phpdir}/Monolog/autoload.php';
require_once '%{phpdir}/Psr/Log/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}/Akamai/Open/EdgeGrid
cp -rp src/* %{buildroot}%{phpdir}/Akamai/Open/EdgeGrid/


%check
%if %{with_tests}
: Make PSR-0 tests
mkdir -p tests-psr0/Akamai/Open/EdgeGrid
ln -s ../../../../tests tests-psr0/Akamai/Open/EdgeGrid/Tests

: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require_once '%{buildroot}%{phpdir}/Akamai/Open/EdgeGrid/autoload.php';

$fedoraClassLoader->addPrefix('Akamai\\Open\\EdgeGrid\\Tests\\', __DIR__.'/tests-psr0');
BOOTSTRAP

%{_bindir}/phpunit --verbose --bootstrap bootstrap.php
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%dir %{phpdir}/Akamai
%dir %{phpdir}/Akamai/Open
     %{phpdir}/Akamai/Open/EdgeGrid


%changelog
* Tue Apr 12 2016 Shawn Iwinski <shawn@iwin.ski> - 0.4.4-1
- Initial package
