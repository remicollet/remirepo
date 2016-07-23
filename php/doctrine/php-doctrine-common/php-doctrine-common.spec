# remirepo spec file for php-doctrine-common, from:
#
# Fedora spec file for php-doctrine-common
#
# Copyright (c) 2013-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      common
%global github_version   2.5.3
%global github_commit    10f1f19651343f87573129ca970aef1a47a6f29e

%global composer_vendor  doctrine
%global composer_project common

# "php": ">=5.3.2"
%global php_min_ver      5.3.2
# "doctrine/annotations": "1.*"
#     NOTE: Min version not 1.0 because autoloader required
%global doctrine_annotations_min_ver 1.2.6
%global doctrine_annotations_max_ver 2.0
# "doctrine/cache": "1.*"
#     NOTE: Min version not 1.0 because autoloader required
%global doctrine_cache_min_ver 1.4.1
%global doctrine_cache_max_ver 2.0
# "doctrine/collections": "1.*"
#     NOTE: Min version not 1.0 because autoloader required
%global doctrine_collections_min_ver 1.3.0
%global doctrine_collections_max_ver 2.0
# "doctrine/inflector": "1.*"
#     NOTE: Min version not 1.0 because autoloader required
%global doctrine_inflector_min_ver 1.0.1-4
%global doctrine_inflector_max_ver 2.0
# "doctrine/lexer": "1.*"
#     NOTE: Min version not 1.0 because autoloader required
%global doctrine_lexer_min_ver 1.0.1-4
%global doctrine_lexer_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       Common library for Doctrine projects

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Library version value check
BuildRequires: php-cli
# Tests
%if %{with_tests}
## composer.json
BuildRequires: %{_bindir}/phpunit
BuildRequires: php(language)                      >= %{php_min_ver}
BuildRequires: php-composer(doctrine/annotations) >= %{doctrine_annotations_min_ver}
BuildRequires: php-composer(doctrine/cache)       >= %{doctrine_cache_min_ver}
BuildRequires: php-composer(doctrine/collections) >= %{doctrine_collections_min_ver}
#BuildRequires: php-composer(doctrine/inflector)   >= %%{doctrine_inflector_min_ver}
BuildRequires: php-doctrine-inflector             >= %{doctrine_inflector_min_ver}
#BuildRequires: php-composer(doctrine/lexer)       >= %%{doctrine_lexer_min_ver}
BuildRequires: php-doctrine-lexer                 >= %{doctrine_lexer_min_ver}
## phpcompatinfo (computed from version 2.5.3)
BuildRequires: php-date
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
BuildRequires: php-tokenizer
# Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                      >= %{php_min_ver}
Requires:      php-composer(doctrine/annotations) >= %{doctrine_annotations_min_ver}
Requires:      php-composer(doctrine/annotations) <  %{doctrine_annotations_max_ver}
Requires:      php-composer(doctrine/cache)       >= %{doctrine_cache_min_ver}
Requires:      php-composer(doctrine/cache)       <  %{doctrine_cache_max_ver}
Requires:      php-composer(doctrine/collections) >= %{doctrine_collections_min_ver}
Requires:      php-composer(doctrine/collections) <  %{doctrine_collections_max_ver}
#Requires:      php-composer(doctrine/inflector)   >= %%{doctrine_inflector_min_ver}
Requires:      php-doctrine-inflector             >= %{doctrine_inflector_min_ver}
Requires:      php-composer(doctrine/inflector)   <  %{doctrine_inflector_max_ver}
#Requires:      php-composer(doctrine/lexer)       >= %%{doctrine_lexer_min_ver}
Requires:      php-doctrine-lexer                 >= %{doctrine_lexer_min_ver}
Requires:      php-composer(doctrine/lexer)       <  %{doctrine_lexer_max_ver}
# phpcompatinfo (computed from version 2.5.0)
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
Requires:      php-tokenizer
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}
# PEAR
Provides:      php-pear(pear.doctrine-project.org/DoctrineCommon) = %{version}
# Rename
Obsoletes:     php-doctrine-DoctrineCommon < %{version}
Provides:      php-doctrine-DoctrineCommon = %{version}

%description
The Doctrine Common project is a library that provides extensions to core PHP
functionality.

Autoloader: %{phpdir}/Doctrine/Common/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Create autoloader
cat <<'AUTOLOAD' | tee lib/Doctrine/Common/autoload.php
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

$fedoraClassLoader->addPrefix('Doctrine\\Common\\', dirname(dirname(__DIR__)));

require_once '%{phpdir}/Doctrine/Common/Annotations/autoload.php';
require_once '%{phpdir}/Doctrine/Common/Cache/autoload.php';
require_once '%{phpdir}/Doctrine/Common/Collections/autoload.php';
require_once '%{phpdir}/Doctrine/Common/Inflector/autoload.php';
require_once '%{phpdir}/Doctrine/Common/Lexer/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%install
rm -rf   %{buildroot}
mkdir -p %{buildroot}%{phpdir}
cp -rp lib/* %{buildroot}%{phpdir}/


%check
: Library version value check
%{_bindir}/php -r '
    require_once "%{buildroot}%{phpdir}/Doctrine/Common/Version.php";
    $version = \Doctrine\Common\Version::VERSION;
    echo "Version $version (expected %{version})\n";
    exit(version_compare("%{version}", "$version", "=") ? 0 : 1);
'

%if %{with_tests}
: Modify tests init
sed "s#require.*autoload.*#require_once '%{buildroot}%{phpdir}/Doctrine/Common/autoload.php';#" \
     -i tests/Doctrine/Tests/TestInit.php

%if 1
: PHPUnit greater than 3.7
# Non-static method PHPUnit_Framework_MockObject_Generator::getMock() should not
# be called statically, assuming $this from incompatible context
sed -e 's/function testGetManagerForAliasedClass/function SKIP_testGetManagerForAliasedClass/' \
    -e 's/function testGetManagerForClass/function SKIP_testGetManagerForClass/' \
    -i tests/Doctrine/Tests/Common/Persistence/ManagerRegistryTest.php
%endif

run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose
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
%doc UPGRADE*
%doc composer.json
%{phpdir}/Doctrine/Common/*.php
%{phpdir}/Doctrine/Common/Persistence
%{phpdir}/Doctrine/Common/Proxy
%{phpdir}/Doctrine/Common/Reflection
%{phpdir}/Doctrine/Common/Util


%changelog
* Fri Jul 22 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.5.3-1
- Updated to 2.5.3 (RHBZ #1347924 / CVE-2015-5723)
- Added library version value check

* Sat Jun 27 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.5.0-1
- Updated to 2.5.0 (RHBZ #1209683)
- Added autoloader
- %%license usage

* Fri Jun 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.4.2-3
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide
- Added option to build without tests ("--without tests")
- Updated dependencies to use php-composer virtual provides

* Mon May 26 2014 Remi Collet <rpms@famillecollet.com> 2.4.2-1
- backport 2.4.2 for remi repo

* Fri May 23 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.4.2-1
- Updated to 2.4.2 (BZ #1100718)

* Sat Jan 11 2014 Remi Collet <rpms@famillecollet.com> 2.4.1-2
- backport for remi repo

* Sat Jan 04 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 2.4.1-2
- Conditional %%{?dist}
- Removed php-channel-doctrine obsolete

* Fri Dec 27 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.4.1-1
- Initial package
