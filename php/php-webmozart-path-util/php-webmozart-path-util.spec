# remirepo spec file for php-webmozart-path-util, from
#
# Fedora spec file for php-webmozart-path-util
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     webmozart
%global github_name      path-util
%global github_version   2.3.0
%global github_commit    d939f7edc24c9a1bb9c0dee5cb05d8e859490725

%global composer_vendor  webmozart
%global composer_project path-util

# "php": ">=5.3.3"
%global php_min_ver 5.3.3
# "webmozart/assert": "~1.0"
%global webmozart_assert_min_ver 1.0
%global webmozart_assert_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Cross-platform utilities for file paths

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(webmozart/assert) >= %{webmozart_assert_min_ver}
## phpcompatinfo (computed from version 2.3.0)
BuildRequires: php-ctype
BuildRequires: php-mbstring
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(webmozart/assert) >= %{webmozart_assert_min_ver}
Requires:      php-composer(webmozart/assert) <  %{webmozart_assert_max_ver}
# phpcompatinfo (computed from version 2.3.0)
Requires:      php-ctype
Requires:      php-mbstring
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
This package provides robust, cross-platform utility functions for normalizing,
comparing and modifying file paths and URLs..

Autoloader: %{phpdir}/Webmozart/PathUtil/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}


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

$fedoraClassLoader->addPrefix('Webmozart\\PathUtil\\', dirname(dirname(__DIR__)));

// Required dependency
require_once '%{phpdir}/Webmozart/Assert/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}/Webmozart/PathUtil
cp -rp src/* %{buildroot}%{phpdir}/Webmozart/PathUtil/


%check
%if %{with_tests}
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/Webmozart/PathUtil/autoload.php || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/Webmozart/PathUtil/autoload.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}%{phpdir}/Webmozart/PathUtil/autoload.php
# remirepo:2
fi
exit $ret
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{phpdir}/Webmozart/PathUtil


%changelog
* Thu Oct  6 2016 Remi Collet <remi@remirepo.net> - 2.3.0-1
- backport for remi repo, add EL-5 stuff

* Wed Sep 28 2016 Shawn Iwinski <shawn@iwin.ski> - 2.3.0-1
- Initial package
