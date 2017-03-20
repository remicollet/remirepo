# remirepo spec file for psysh, from:
#
# Fedora spec file for psysh
#
# Copyright (c) 2016-2017 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     bobthecow
%global github_name      psysh
%global github_version   0.8.3
%global github_commit    1dd4bbbc64d71e7ec075ffe82b42d9e096dc8d5e

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
# "nikic/php-parser": "~1.3|~2.0|~3.0"
#     NOTE: Min version not 1.2.1 to force 2.x so 1.x is not
#           a dependency so it could possibly be retired
%global php_parser_min_ver 2.0
%global php_parser_max_ver 4.0
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
Release:       1%{?github_release}%{?dist}
Summary:       A runtime developer console, interactive debugger and REPL for PHP

Group:         Development/Libraries
License:       MIT
URL:           http://psysh.org
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

# Update bin script to use generated autoloader
Patch0:        %{name}-bin-autoload.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: php-cli
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(dnoegel/php-xdg-base-dir) <  %{php_xdg_base_dir_max_ver}
BuildRequires: php-composer(dnoegel/php-xdg-base-dir) >= %{php_xdg_base_dir_min_ver}
BuildRequires: php-composer(jakub-onderka/php-console-highlighter) <  %{php_console_highlighter_max_ver}
BuildRequires: php-composer(jakub-onderka/php-console-highlighter) >= %{php_console_highlighter_min_ver}
BuildRequires: php-composer(nikic/php-parser) <  %{php_parser_max_ver}
BuildRequires: php-composer(nikic/php-parser) >= %{php_parser_min_ver}
BuildRequires: php-composer(symfony/console) <  %{symfony_max_ver}
BuildRequires: php-composer(symfony/console) >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/finder) <  %{symfony_max_ver}
BuildRequires: php-composer(symfony/finder) >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/var-dumper) <  %{symfony_max_ver}
BuildRequires: php-composer(symfony/var-dumper) >= %{symfony_min_ver}
## composer.json: optional
BuildRequires: php-pcntl
BuildRequires: php-pdo_sqlite
BuildRequires: php-posix
BuildRequires: php-readline
## phpcompatinfo (computed from version 0.8.2)
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
BuildRequires: php-composer(fedora/autoloader)
%endif

Requires:      php-cli
# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(dnoegel/php-xdg-base-dir) <  %{php_xdg_base_dir_max_ver}
Requires:      php-composer(dnoegel/php-xdg-base-dir) >= %{php_xdg_base_dir_min_ver}
Requires:      php-composer(jakub-onderka/php-console-highlighter) <  %{php_console_highlighter_max_ver}
Requires:      php-composer(jakub-onderka/php-console-highlighter) >= %{php_console_highlighter_min_ver}
Requires:      php-composer(nikic/php-parser) <  %{php_parser_max_ver}
Requires:      php-composer(nikic/php-parser) >= %{php_parser_min_ver}
Requires:      php-composer(symfony/console) <  %{symfony_max_ver}
Requires:      php-composer(symfony/console) >= %{symfony_min_ver}
Requires:      php-composer(symfony/var-dumper) <  %{symfony_max_ver}
Requires:      php-composer(symfony/var-dumper) >= %{symfony_min_ver}
# composer.json: optional
Requires:      php-pcntl
Requires:      php-pdo_sqlite
Requires:      php-posix
Requires:      php-readline
# phpcompatinfo (computed from version 0.8.0)
Requires:      php-ctype
Requires:      php-date
Requires:      php-json
Requires:      php-pcre
Requires:      php-pdo
Requires:      php-reflection
Requires:      php-spl
Requires:      php-tokenizer
# Autoloader
Requires:      php-composer(fedora/autoloader)

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
require_once '%{phpdir}/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Psy\\', __DIR__);
require_once __DIR__.'/functions.php';

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/JakubOnderka/PhpConsoleHighlighter/autoload.php',
    '%{phpdir}/Symfony/Component/Console/autoload.php',
    '%{phpdir}/Symfony/Component/VarDumper/autoload.php',
    '%{phpdir}/XdgBaseDir/autoload.php',
    array(
        '%{phpdir}/PhpParser3/autoload.php',
        '%{phpdir}/PhpParser2/autoload.php',
    ),
));
AUTOLOAD


%install
rm -rf   %{buildroot}

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
require '%{buildroot}%{phpdir}/Psy/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('Psy\\Test\\', __DIR__.'/test/Psy/Test');
BOOTSTRAP

: Skip tests known to fail
sed '/exit\(\).*die;/d' -i test/Psy/Test/CodeCleaner/ImplicitReturnPassTest.php
sed '/foo.*return/d' -i test/Psy/Test/CodeCleanerTest.php
sed 's/function testFilesAndDirectories/function SKIP_testFilesAndDirectories/' \
    -i test/Psy/Test/ConfigurationTest.php

: Skip tests known to fail in a mock env
sed 's/function testFormat/function SKIP_testFormat/' \
    -i test/Psy/Test/Formatter/CodeFormatterTest.php
sed 's/function testWriteReturnValue/function SKIP_testWriteReturnValue/' \
    -i test/Psy/Test/ShellTest.php

: Drop unneeded test as readline is always there
rm test/Psy/Test/Readline/HoaConsoleTest.php

: Upstream tests
%{_bindir}/phpunit --verbose --bootstrap bootstrap.php

: Upstream tests with SCLs if available
SCL_RETURN_CODE=0
for SCL in %{?rhel:php54 php55} php56 php70 php71; do
    if which $SCL; then
        $SCL %{_bindir}/phpunit --verbose --bootstrap bootstrap.php || SCL_RETURN_CODE=1
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
%license LICENSE
%doc *.md
%doc composer.json
%{phpdir}/Psy
%{_bindir}/psysh


%changelog
* Mon Mar 20 2017 Remi Collet <remi@remirepo.net> - 0.8.3-1
- Update to 0.8.3

* Sat Mar 04 2017 2017 Shawn Iwinski <shawn@iwin.ski> - 0.8.2-1
- Update to 0.8.2 (RHBZ #1413429)
- Test with SCLs if available

* Wed Mar  1 2017 Remi Collet <remi@remirepo.net> - 0.8.2-1
- update to 0.8.2

* Mon Jan 16 2017 Remi Collet <remi@fedoraproject.org> - 0.8.1-1
- update to 0.8.1

* Sun Dec 11 2016 Shawn Iwinski <shawn@iwin.ski> - 0.8.0-1
- Update to 0.8.0 (RHBZ #1403040)
- Switch autoloader from php-composer(symfony/class-loader) to
  php-composer(fedora/autoloader)

* Fri Dec  9 2016 Remi Collet <remi@fedoraproject.org> - 0.8.0-1
- update to 0.8.0
- allow nikic/php-parser version 3
- switch to fedora/autoloader

* Thu Jul 21 2016 Remi Collet <remi@fedoraproject.org> - 0.7.2-2
- backport for remi repository

* Wed Jul 20 2016 Shawn Iwinski <shawn@iwin.ski> - 0.7.2-2
- Add explicit php-cli dependency (bin script uses "#!/usr/bin/env php")

* Fri Jul 15 2016 Shawn Iwinski <shawn@iwin.ski> - 0.7.2-1
- Initial package
