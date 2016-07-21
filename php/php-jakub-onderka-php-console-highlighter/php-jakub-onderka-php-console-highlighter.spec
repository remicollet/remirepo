# remirepo spec file for php-jakub-onderka-php-console-highlighter, from:
#
# Fedora spec file for php-jakub-onderka-php-console-highlighter
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     JakubOnderka
%global github_name      PHP-Console-Highlighter
%global github_version   0.3.2
%global github_commit    7daa75df45242c8d5b75a22c00a201e7954e4fb5

%global composer_vendor  jakub-onderka
%global composer_project php-console-highlighter

# "php": ">=5.3.0"
%global php_min_ver 5.3.0
# "jakub-onderka/php-console-color": "~0.1"
%global jakub_onderka_php_console_color_min_ver 0.1
%global jakub_onderka_php_console_color_max_ver 1.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Highlight PHP code in console (terminal)

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

# Update tests to use createMock() instead of getMock() for PHPUnit 5.4+
# https://github.com/JakubOnderka/PHP-Console-Highlighter/pull/11
# https://patch-diff.githubusercontent.com/raw/JakubOnderka/PHP-Console-Highlighter/pull/11.patch
Patch0:        %{name}-pr11-phpunit-createMock.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(jakub-onderka/php-console-color) >= %{jakub_onderka_php_console_color_min_ver}
## phpcompatinfo (computed from version 0.3.2)
BuildRequires: php-tokenizer
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                                 >= %{php_min_ver}
Requires:      php-composer(jakub-onderka/php-console-color) >= %{jakub_onderka_php_console_color_min_ver}
Requires:      php-composer(jakub-onderka/php-console-color) <  %{jakub_onderka_php_console_color_max_ver}
# phpcompatinfo (computed from version 0.3.2)
Requires:      php-tokenizer
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.

Autoloader: %{phpdir}/JakubOnderka/PhpConsoleHighlighter/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Update tests to use createMock instead of getMock for PHPUnit 5.4+
%patch0 -p1


%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/JakubOnderka/PhpConsoleHighlighter/autoload.php
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

$fedoraClassLoader->addPrefix('JakubOnderka\\PhpConsoleHighlighter\\', dirname(dirname(__DIR__)));

// Required dependency
require_once '%{phpdir}/JakubOnderka/PhpConsoleColor/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%install
rm -rf   %{buildroot}

mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/JakubOnderka/PhpConsoleHighlighter/autoload.php || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/JakubOnderka/PhpConsoleHighlighter/autoload.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
   %{_bindir}/phpunit --verbose \
      --bootstrap %{buildroot}%{phpdir}/JakubOnderka/PhpConsoleHighlighter/autoload.php
fi
exit $ret
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
%{phpdir}/JakubOnderka/PhpConsoleHighlighter


%changelog
* Thu Jul 21 2016 Remi Collet <remi@fedoraproject.org> - 0.3.2-1
- backport for remi repository

* Fri Jul 15 2016 Shawn Iwinski <shawn@iwin.ski> - 0.3.2-1
- Initial package
