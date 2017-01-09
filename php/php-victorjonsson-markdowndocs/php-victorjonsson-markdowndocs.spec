#
# Fedora spec file for php-victorjonsson-markdowndocs
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     victorjonsson
%global github_name      PHP-Markdown-Documentation-Generator
%global github_version   1.3.7
%global github_commit    a8244617cdce4804cd94ea508c82e8d7e29a273a

%global composer_vendor  victorjonsson
%global composer_project markdowndocs

# "php" : ">=5.5.0"
%global php_min_ver 5.5.0
# "symfony/console": ">=2.6"
%global symfony_min_ver 2.6
%global symfony_max_ver 3

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Command line tool for generating markdown-formatted class documentation

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

# Add LICENSE file
# https://patch-diff.githubusercontent.com/raw/victorjonsson/PHP-Markdown-Documentation-Generator/pull/10
Patch0:        %{name}-pull-request-10.patch
# Set CLI version (instead of reading composer.json)
Patch1:        %{name}-cli-version.patch
# Modify bin autoloader
Patch2:        %{name}-bin.patch


BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(symfony/console) <  %{symfony_max_ver}
BuildRequires: php-composer(symfony/console) >= %{symfony_min_ver}
## phpcompatinfo (computed from version 1.3.7)
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

Requires:      php-cli
# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(symfony/console) <  %{symfony_max_ver}
Requires:      php-composer(symfony/console) >= %{symfony_min_ver}
# phpcompatinfo (computed from version 1.3.7)
Requires:      php-json
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Documentation is just as important as the code it's referring to. With this
command line tool you will be able to write your documentation once, and only
once!

This project will write a single-page markdown-formatted API document based on
the DocBlock comments in your source code. The phpdoc standard is used.

Autoloader: %{phpdir}/PHPDocsMD/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Add LICENSE file
%patch0 -p1

: Set CLI version -- instead of reading composer.json
%patch1 -p1
sed -i 's#__VERSION__#%{version}#' src/PHPDocsMD/Console/CLI.php

: Modify bin autoloader
%patch2 -p1
sed -i 's#__PHPDIR__#%{phpdir}#' bin/phpdoc-md

: Fix rpmlint "wrong-file-end-of-line-encoding" warning
sed -i 's/\r$//' README.md


%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/PHPDocsMD/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 */
require_once '%{phpdir}/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('PHPDocsMD\\', __DIR__);

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/Symfony/Component/Console/autoload.php',
));
AUTOLOAD


%install
: Library
mkdir -p %{buildroot}%{phpdir}
cp -rp src/PHPDocsMD %{buildroot}%{phpdir}/

: Bin
mkdir -p %{buildroot}%{_bindir}
install -pm 0755 bin/phpdoc-md %{buildroot}%{_bindir}/phpdoc-md


%check
%if %{with_tests}
BOOTSTRAP=%{buildroot}%{phpdir}/PHPDocsMD/autoload.php

: Upstream tests
%{_bindir}/phpunit --verbose --bootstrap $BOOTSTRAP

: Upstream tests with SCLs if available
SCL_RETURN_CODE=0
for SCL in php56 php70 php71; do
    if which $SCL; then
       $SCL %{_bindir}/phpunit --bootstrap $BOOTSTRAP || SCL_RETURN_CODE=1
    fi
done
exit $SCL_RETURN_CODE
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{phpdir}/PHPDocsMD
%{_bindir}/phpdoc-md


%changelog
* Mon Dec 26 2016 Shawn Iwinski <shawn@iwin.ski> - 1.3.7-1
- Initial package
