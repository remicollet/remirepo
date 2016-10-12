# remirpeo spec file for php-ocramius-generated-hydrator, from
#
# Fedora spec file for php-ocramius-generated-hydrator
#
# Copyright (c) 2014-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     Ocramius
%global github_name      GeneratedHydrator
%global github_version   1.2.0
%global github_commit    ba0c96cfbf311203cf7664c566463f4530024ad1

%global composer_vendor  ocramius
%global composer_project generated-hydrator

# "php": "~5.4|~7.0"
%global php_min_ver 5.4
# "nikic/php-parser": "~1.0"
%global php_parser_min_ver 1.0
%global php_parser_max_ver 2
# "ocramius/code-generator-utils": "0.3.*"
#     NOTE: Min version not 0.3.0 because autoloader required
%global ocramius_cgu_min_ver 0.3.2-4
%global ocramius_cgu_max_ver 0.4.0
# "zendframework/zend-stdlib": "~2.3"
%global zf_stdlib_min_ver 2.3
%global zf_stdlib_max_ver 3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       An object hydrator

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
%if %{with_tests}
# composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(nikic/php-parser) >= %{php_parser_min_ver}
BuildRequires: php-composer(nikic/php-parser) <  %{php_parser_max_ver}
#BuildRequires: php-composer(ocramius/code-generator-utils) >= %%{ocramius_cgu_min_ver}
BuildRequires: php-ocramius-code-generator-utils           >= %{ocramius_cgu_min_ver}
BuildRequires: php-composer(ocramius/code-generator-utils) <  %{ocramius_cgu_max_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(zendframework/zend-stdlib) >= %{zf_stdlib_min_ver}
BuildRequires: php-composer(zendframework/zend-stdlib) <  %{zf_stdlib_max_ver}
# phpcompatinfo (computed from version 1.2.0)
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
#Requires:      php-composer(ocramius/code-generator-utils) >= %%{ocramius_cgu_min_ver}
Requires:      php-ocramius-code-generator-utils           >= %{ocramius_cgu_min_ver}
Requires:      php-composer(ocramius/code-generator-utils) <  %{ocramius_cgu_max_ver}
Requires:      php-composer(zendframework/zend-stdlib) >= %{zf_stdlib_min_ver}
Requires:      php-composer(zendframework/zend-stdlib) <  %{zf_stdlib_max_ver}
# phpcompatinfo (computed from version 1.2.0)
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
GeneratedHydrator is a library about high performance transition of data from
arrays to objects and from objects to arrays.

Autoloader: %{phpdir}/GeneratedHydrator/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/GeneratedHydrator/autoload.php
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

$fedoraClassLoader->addPrefix('GeneratedHydrator\\', dirname(__DIR__));

// Required dependencies
require_once '%{phpdir}/CodeGenerationUtils/autoload.php';
require_once '%{phpdir}/PhpParser/autoload.php';
require_once '%{phpdir}/Zend/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}
cp -rp src/GeneratedHydrator %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
$fedoraClassLoader = require '%{buildroot}%{phpdir}/GeneratedHydrator/autoload.php';
$fedoraClassLoader->addPrefix('GeneratedHydratorPerformance\\', __DIR__.'/tests');
$fedoraClassLoader->addPrefix('GeneratedHydratorTest\\', __DIR__.'/tests');
$fedoraClassLoader->addPrefix('GeneratedHydratorTestAsset\\', __DIR__.'/tests');
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
%{phpdir}/GeneratedHydrator


%changelog
* Wed Oct 12 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.0-1
- Update to 1.2.0
- Add autoloader

* Wed Feb 25 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1

* Sat Nov 29 2014 Remi Collet <rpms@famillecollet.com> - 1.1.0-1
- backport for remi repo

* Mon Oct 27 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.0-1
- Initial package
