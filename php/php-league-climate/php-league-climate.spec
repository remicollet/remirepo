#
# Fedora spec file for php-league-climate
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     thephpleague
%global github_name      climate
%global github_version   3.2.1
%global github_commit    b103fc8faa3780c802cc507d5f0ff534ecc94fb5

%global composer_vendor  league
%global composer_project climate

# "php": ">=5.4.0"
%global php_min_ver 5.4.0
# "mikey179/vfsStream": "~1.4"
#     NOTE: Min version not 1.4 because autoloader required
%global vfsstream_min_ver 1.6.0
%global vfsstream_max_ver 2.0
# "mockery/mockery": "~0.9"
#     NOTE: Min version not 0.9 because autoloader required
%global mockery_min_ver 0.9.3
%global mockery_max_ver 1.0
# "seld/cli-prompt": "~1.0"
%global seld_cli_prompt_min_ver 1.0
%global seld_cli_prompt_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Allows you to easily output colored text, special formats, and more

Group:         Development/Libraries
License:       MIT
URL:           http://climate.thephpleague.com/

# GitHub export does not include tests.
# Run php-league-climate-get-source.sh to create full source.
Source0:       %{name}-%{github_version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language)                    >= %{php_min_ver}
BuildRequires: php-composer(mikey179/vfsStream) >= %{vfsstream_min_ver}
BuildRequires: php-composer(mockery/mockery)    >= %{mockery_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(seld/cli-prompt)    >= %{seld_cli_prompt_min_ver}
## phpcompatinfo (computed from version 3.2.1)
BuildRequires: php-json
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-posix
BuildRequires: php-reflection
BuildRequires: php-zlib
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                 >= %{php_min_ver}
Requires:      php-composer(seld/cli-prompt) >= %{seld_cli_prompt_min_ver}
Requires:      php-composer(seld/cli-prompt) <  %{seld_cli_prompt_max_ver}
# phpcompatinfo (computed from version 3.2.1)
Requires:      php-json
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-posix
Requires:      php-reflection
Requires:      php-zlib
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
If you’re running PHP from the command line, CLImate is your new best bud.

CLImate allows you to easily output colored text, special formatting, and more.
It makes output to the terminal clearer and debugging a lot simpler.

Autoloader: %{phpdir}/League/CLImate/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

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

$fedoraClassLoader->addPrefix('League\\CLImate\\', dirname(dirname(__DIR__)));

// Required dependencies
require_once '%{phpdir}/Seld/CliPrompt/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing to build


%install
mkdir -p %{buildroot}%{phpdir}/League/CLImate
cp -rp src/* %{buildroot}%{phpdir}/League/CLImate/


%check
%if %{with_tests}
: Make PSR-0 tests
mkdir -p tests-psr0/League/CLImate
ln -s ../../../tests tests-psr0/League/CLImate/Tests

: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require_once '%{buildroot}%{phpdir}/League/CLImate/autoload.php';

$fedoraClassLoader->addPrefix('League\\CLImate\\Tests\\', __DIR__.'/tests-psr0');

require_once '%{phpdir}/Mockery/autoload.php';
require_once '%{phpdir}/org/bovigo/vfs/autoload.php';
BOOTSTRAP

: Remove Composer vendor file load
sed '/require.*vendor\/mikey179/d' -i tests/FileTest.php

%{_bindir}/phpunit --verbose --bootstrap bootstrap.php
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc CHANGELOG.md
%doc composer.json
%doc README.md
%dir %{phpdir}/League
     %{phpdir}/League/CLImate


%changelog
* Mon Apr 11 2016 Shawn Iwinski <shawn@iwin.ski> - 3.2.1-1
- Initial package
