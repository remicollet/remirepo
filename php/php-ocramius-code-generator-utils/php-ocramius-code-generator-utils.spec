# remirepo spec file for php-ocramius-code-generator-utils, from
#
# Fedora spec file for php-ocramius-code-generator-utils
#
# Copyright (c) 2014-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     Ocramius
%global github_name      CodeGenerationUtils
%global github_version   0.3.2
%global github_commit    0e2f6c593fc82801cbb5c8fa90559d923bd1445c

%global composer_vendor  ocramius
%global composer_project code-generator-utils

# "php": ">=5.3.3"
%global php_min_ver 5.3.3
# "nikic/php-parser": "~1.3"
%global php_parser_min_ver 1.3
%global php_parser_max_ver 2

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       4%{?github_release}%{?dist}
Summary:       A set of code generator utilities built on top of PHP-Parsers

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:     noarch
%if %{with_tests}
# composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(nikic/php-parser) >= %{php_parser_min_ver}
BuildRequires: php-composer(nikic/php-parser) <  %{php_parser_max_ver}
BuildRequires: php-composer(phpunit/phpunit)
# phpcompatinfo (computed from version 0.3.0)
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
# Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(nikic/php-parser) >= %{php_parser_min_ver}
Requires:      php-composer(nikic/php-parser) <  %{php_parser_max_ver}
# phpcompatinfo (computed from version 0.3.0)
Requires:      php-pcre
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
A set of code generator utilities built on top of PHP-Parsers that ease its use
when combined with Reflection.

Autoloader: %{phpdir}/CodeGenerationUtils/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/CodeGenerationUtils/autoload.php
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

$fedoraClassLoader->addPrefix('CodeGenerationUtils\\', dirname(__DIR__));

// Required dependency
require_once '%{phpdir}/PhpParser/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}
cp -rp src/CodeGenerationUtils %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
$fedoraClassLoader = require '%{buildroot}%{phpdir}/CodeGenerationUtils/autoload.php';
$fedoraClassLoader->addPrefix('CodeGenerationUtilsTest\\', __DIR__.'/tests');
BOOTSTRAP

%{_bindir}/phpunit --verbose --bootstrap bootstrap.php
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
%{phpdir}/CodeGenerationUtils


%changelog
* Wed Oct 12 2016 Remi Collet <remi@fedoraproject.org> - 0.3.2-4
- add missing dependency for autoloader

* Tue Oct 11 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.3.2-3
- Add autoloader

* Sun Aug  9 2015 Remi Collet <remi@fedoraproject.org> - 0.3.2-1
- update to 0.3.2

* Wed Feb 25 2015 Remi Collet <remi@fedoraproject.org> - 0.3.1-1
- update to 0.3.1 (no change)
- raise nikic/php-parser max version

* Thu Nov  6 2014 Remi Collet <remi@fedoraproject.org> - 0.3.0-2
- backport for remi repository

* Wed Nov 05 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.3.0-2
- Silenced include in autoloader
- Removed debug from %%check

* Mon Oct 27 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.3.0-1
- Initial package
