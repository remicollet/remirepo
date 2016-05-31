#
# Fedora spec file for php-symfony-securiy-acl
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     symfony
%global github_name      security-acl
%global github_version   2.8.0
%global github_commit    4a3f7327ad215242c78f6564ad4ea6d2db1b8347

%global composer_vendor  symfony
%global composer_project security-acl

# "php": ">=5.3.9"
%global php_min_ver 5.3.9
# "symfony/phpunit-bridge": "~2.7|~3.0.0"
# "symfony/security-core": "~2.4|~3.0.0"
%global symfony_min_ver 2.7
%global symfony_max_ver 4.0
# "doctrine/common": "~2.2"
#     NOTE: Min version not 2.2 because autoloader required
%global doctrine_common_min_ver 2.5.0
%global doctrine_common_max_ver 3.0
# "doctrine/dbal": "~2.2"
#     NOTE: Min version not 2.2 because autoloader required
%global doctrine_dbal_min_ver 2.5.4
%global doctrine_dbal_max_ver 3.0
# "psr/log": "~1.0"
#     NOTE: Min version not 1.0 because autoloader required
%global psr_log_min_ver 1.0.0-8
%global psr_log_max_ver 2.0

%global bootstrap 0

%if %{bootstrap}
%global with_tests 0
%else
# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}
%endif

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Symfony Security Component - ACL (Access Control List)

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language)                       >= %{php_min_ver}
BuildRequires: php-composer(doctrine/common)       >= %{doctrine_common_min_ver}
BuildRequires: php-composer(doctrine/dbal)         >= %{doctrine_dbal_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
#BuildRequires: php-composer(psr/log)               >= %%{psr_log_min_ver}
BuildRequires: php-PsrLog                          >= %{psr_log_min_ver}
BuildRequires: php-composer(symfony/security-core) >= %{symfony_min_ver}
## phpcompatinfo (computed from version 2.8.0)
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(symfony/security-core) <  %{symfony_max_ver}
Requires:      php-composer(symfony/security-core) >= %{symfony_min_ver}
# phpcompatinfo (computed from version 2.8.0)
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Weak dependencies
Suggests:      php-composer(doctrine/dbal)
Conflicts:     php-doctrine-dbal  <  %{doctrine_dbal_min_ver}
Conflicts:     php-doctrine-dbal  >= %{doctrine_dbal_max_ver}
Suggests:      php-composer(symfony/finder)
Conflicts:     php-symfony-finder <  %{symfony_min_ver}
Conflicts:     php-symfony-finder >= %{symfony_max_ver}

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

# Extracted from Symfony as of version 2.8.0
Conflicts:     php-symfony-security < 2.8.0

%description
%{summary}.

Autoloader: %{phpdir}/Symfony/Component/Security/Acl/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

if (!isset($fedoraPsr4ClassLoader) || !($fedoraPsr4ClassLoader instanceof \Symfony\Component\ClassLoader\Psr4ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\Psr4ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/Psr4ClassLoader.php';
    }

    $fedoraPsr4ClassLoader = new \Symfony\Component\ClassLoader\Psr4ClassLoader();
    $fedoraPsr4ClassLoader->register(true);
}

$fedoraPsr4ClassLoader->addPrefix('Symfony\\Component\\Security\\Acl\\', __DIR__);

// Dependencies (autoloader => required)
foreach(array(
    '%{phpdir}/Doctrine/DBAL/autoload.php'              => false,
    '%{phpdir}/Symfony/Component/Finder/autoload.php'   => false,
    '%{phpdir}/Symfony/Component/Security/autoload.php' => true,
) as $dependencyAutoloader => $required) {
    if ($required || file_exists($dependencyAutoloader)) {
        require_once $dependencyAutoloader;
    }
}
AUTOLOAD


%build
# Empty build section, nothing to build


%install
mkdir -p %{buildroot}%{phpdir}/Symfony/Component/Security/Acl
cp -rp * %{buildroot}%{phpdir}/Symfony/Component/Security/Acl/


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require_once '%{buildroot}%{phpdir}/Symfony/Component/Security/Acl/autoload.php';

require_once '%{phpdir}/Doctrine/Common/autoload.php';
require_once '%{phpdir}/Psr/Log/autoload.php';
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
%{phpdir}/Symfony/Component/Security/Acl
%exclude %{phpdir}/Symfony/Component/Security/Acl/*.md
%exclude %{phpdir}/Symfony/Component/Security/Acl/composer.json
%exclude %{phpdir}/Symfony/Component/Security/Acl/LICENSE
%exclude %{phpdir}/Symfony/Component/Security/Acl/phpunit.*
%exclude %{phpdir}/Symfony/Component/Security/Acl/Tests


%changelog
* Fri May 20 2016 Shawn Iwinski <shawn@iwin.ski> - 2.8.0-1
- Initial package
