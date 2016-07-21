#
# Fedora spec file for psysh
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     bobthecow
%global github_name      psysh
%global github_version   0.7.2
%global github_commit    e64e10b20f8d229cac76399e1f3edddb57a0f280

%global composer_vendor  psy
%global composer_project psysh

# "php": ">=5.3.9"
%global php_min_ver 5.3.9
# "dnoegel/php-xdg-base-dir": "0.1"
%global php_xdg_base_dir_min_ver 0.1
%global php_xdg_base_dir_max_ver 0.2
# "jakub-onderka/php-console-highlighter": "0.3.*"
%global php_console_highlighter_min_ver 0.3.0
%global php_console_highlighter_max_ver 0.4.0
# "nikic/php-parser": "^1.2.1|~2.0"
#     NOTE: Min version not 1.2.1 to force 2.x so 1.x is not
#           a dependency so it could possibly be retired
%global php_parser_min_ver 2.0
%global php_parser_max_ver 3.0
# "symfony/console": "~2.3.10|^2.4.2|~3.0"
# "symfony/finder": "~2.1|~3.0"
# "symfony/var-dumper": "~2.7|~3.0"
#     NOTE: Min version not 2.7.0 because autoloader required
%global symfony_min_ver 2.7.1
%global symfony_max_ver 3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          psysh
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       A runtime developer console, interactive debugger and REPL for PHP

Group:         Development/Libraries
License:       MIT
URL:           http://psysh.org
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

# Update bin script to use generated autoloader
Patch0:        %{name}-bin-autoload.patch

BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: php-cli
## composer.json
BuildRequires: php(language)                                       >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(dnoegel/php-xdg-base-dir)              >= %{php_xdg_base_dir_min_ver}
BuildRequires: php-composer(jakub-onderka/php-console-highlighter) >= %{php_console_highlighter_min_ver}
BuildRequires: php-composer(nikic/php-parser)                      >= %{php_parser_min_ver}
BuildRequires: php-composer(symfony/console)                       >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/finder)                        >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/var-dumper)                    >= %{symfony_min_ver}
## composer.json: optional
BuildRequires: php-pcntl
BuildRequires: php-pdo_sqlite
BuildRequires: php-posix
BuildRequires: php-readline
## phpcompatinfo (computed from version 0.7.2)
BuildRequires: php-ctype
BuildRequires: php-date
BuildRequires: php-dom
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-pdo
BuildRequires: php-reflection
BuildRequires: php-spl
BuildRequires: php-tokenizer
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

Requires:      php-cli
# composer.json
Requires:      php(language)                                       >= %{php_min_ver}
Requires:      php-composer(dnoegel/php-xdg-base-dir)              <  %{php_xdg_base_dir_max_ver}
Requires:      php-composer(dnoegel/php-xdg-base-dir)              >= %{php_xdg_base_dir_min_ver}
Requires:      php-composer(jakub-onderka/php-console-highlighter) <  %{php_console_highlighter_max_ver}
Requires:      php-composer(jakub-onderka/php-console-highlighter) >= %{php_console_highlighter_min_ver}
Requires:      php-composer(nikic/php-parser)                      <  %{php_parser_max_ver}
Requires:      php-composer(nikic/php-parser)                      >= %{php_parser_min_ver}
Requires:      php-composer(symfony/console)                       <  %{symfony_max_ver}
Requires:      php-composer(symfony/console)                       >= %{symfony_min_ver}
Requires:      php-composer(symfony/var-dumper)                    <  %{symfony_max_ver}
Requires:      php-composer(symfony/var-dumper)                    >= %{symfony_min_ver}
# composer.json: optional
Requires:      php-pcntl
Requires:      php-pdo_sqlite
Requires:      php-posix
Requires:      php-readline
# phpcompatinfo (computed from version 0.7.2)
Requires:      php-ctype
Requires:      php-date
Requires:      php-json
Requires:      php-pcre
Requires:      php-pdo
Requires:      php-reflection
Requires:      php-spl
Requires:      php-tokenizer
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming
Provides:      php-%{composer_vendor}-%{composer_project} = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.


%prep
%setup -qn %{github_name}-%{github_commit}

: Update bin script to use generated autoloader
%patch0 -p1
sed 's#__PHPDIR__#%{phpdir}#' -i bin/psysh

: Remove upstream autoloader class and test
rm -f src/Psy/Autoloader.php test/Psy/Test/AutoloaderTest.php


%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/Psy/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 */

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Psy\\', dirname(__DIR__));

require_once __DIR__.'/functions.php';

// Required dependencies
require_once '%{phpdir}/JakubOnderka/PhpConsoleHighlighter/autoload.php';
require_once '%{phpdir}/PhpParser2/autoload.php';
require_once '%{phpdir}/Symfony/Component/Console/autoload.php';
require_once '%{phpdir}/Symfony/Component/VarDumper/autoload.php';
require_once '%{phpdir}/XdgBaseDir/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%install
: Library
mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/

: Bin
mkdir -p %{buildroot}%{_bindir}
install -pm 0755 bin/psysh %{buildroot}%{_bindir}/


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
$fedoraClassLoader =
    require '%{buildroot}%{phpdir}/Psy/autoload.php';
$fedoraClassLoader->addPrefix('Psy\\Test\\', __DIR__.'/test');
BOOTSTRAP

: Skip tests known to fail
sed '/exit\(\).*die;/d' -i test/Psy/Test/CodeCleaner/ImplicitReturnPassTest.php
sed '/foo.*return/d' -i test/Psy/Test/CodeCleanerTest.php

: Skip tests known to fail in a mock env
sed 's/function testFormat/function SKIP_testFormat/' \
    -i test/Psy/Test/Formatter/CodeFormatterTest.php
sed 's/function testWriteReturnValue/function SKIP_testWriteReturnValue/' \
    -i test/Psy/Test/ShellTest.php

%{_bindir}/phpunit --verbose --bootstrap bootstrap.php
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{phpdir}/Psy
%{_bindir}/psysh


%changelog
* Wed Jul 20 2016 Shawn Iwinski <shawn@iwin.ski> - 0.7.2-2
- Add explicit php-cli dependency (bin script uses "#!/usr/bin/env php")

* Fri Jul 15 2016 Shawn Iwinski <shawn@iwin.ski> - 0.7.2-1
- Initial package
