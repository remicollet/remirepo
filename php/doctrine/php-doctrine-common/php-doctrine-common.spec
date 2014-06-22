#
# RPM spec file for php-doctrine-common
#
# Copyright (c) 2013-2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      common
%global github_version   2.4.2
%global github_commit    5db6ab40e4c531f14dad4ca96a394dfce5d4255b

%global composer_vendor  doctrine
%global composer_project common

# "php": ">=5.3.2"
%global php_min_ver      5.3.2
# "doctrine/*": "1.*"
%global doctrine_min_ver 1.0
%global doctrine_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests       %{?_without_tests:0}%{!?_without_tests:1}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       3%{?dist}
Summary:       Common library for Doctrine projects

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
%if %{with_tests}
# For tests
BuildRequires: php(language)                      >= %{php_min_ver}
BuildRequires: php-composer(doctrine/annotations) >= %{doctrine_min_ver}
BuildRequires: php-composer(doctrine/annotations) <  %{doctrine_max_ver}
BuildRequires: php-composer(doctrine/cache)       >= %{doctrine_min_ver}
BuildRequires: php-composer(doctrine/cache)       <  %{doctrine_max_ver}
BuildRequires: php-composer(doctrine/collections) >= %{doctrine_min_ver}
BuildRequires: php-composer(doctrine/collections) <  %{doctrine_max_ver}
BuildRequires: php-composer(doctrine/inflector)   >= %{doctrine_min_ver}
BuildRequires: php-composer(doctrine/inflector)   <  %{doctrine_max_ver}
BuildRequires: php-composer(doctrine/lexer)       >= %{doctrine_min_ver}
BuildRequires: php-composer(doctrine/lexer)       <  %{doctrine_max_ver}
BuildRequires: php-phpunit-PHPUnit
# For tests: phpcompatinfo (computed from version 2.4.2)
BuildRequires: php-date
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
BuildRequires: php-tokenizer
%endif

Requires:      php(language)                      >= %{php_min_ver}
Requires:      php-composer(doctrine/annotations) >= %{doctrine_min_ver}
Requires:      php-composer(doctrine/annotations) <  %{doctrine_max_ver}
Requires:      php-composer(doctrine/cache)       >= %{doctrine_min_ver}
Requires:      php-composer(doctrine/cache)       <  %{doctrine_max_ver}
Requires:      php-composer(doctrine/collections) >= %{doctrine_min_ver}
Requires:      php-composer(doctrine/collections) <  %{doctrine_max_ver}
Requires:      php-composer(doctrine/inflector)   >= %{doctrine_min_ver}
Requires:      php-composer(doctrine/inflector)   <  %{doctrine_max_ver}
Requires:      php-composer(doctrine/lexer)       >= %{doctrine_min_ver}
Requires:      php-composer(doctrine/lexer)       <  %{doctrine_max_ver}
# phpcompatinfo (computed from version 2.4.2)
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
Requires:      php-tokenizer

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


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/php
cp -rp lib/* %{buildroot}/%{_datadir}/php/


%check
%if %{with_tests}
# Create tests' init
cat > tests/Doctrine/Tests/TestInit.php <<'TESTINIT'
<?php
namespace Doctrine\Tests;

spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', str_replace('_', '/', $class)).'.php';
    @include_once $src;
});

\Doctrine\Common\Annotations\AnnotationRegistry::registerAutoloadNamespace(
    'Doctrine\Tests\Common\Annotations\Fixtures', __DIR__ . '/../../'
);
TESTINIT

# Create PHPUnit config w/ colors turned off
sed 's/colors="true"/colors="false"/' phpunit.xml.dist > phpunit.xml

%{_bindir}/phpunit --include-path ./lib:./tests -d date.timezone="UTC"
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE *.md UPGRADE* composer.json
%{_datadir}/php/Doctrine/Common/*.php
%{_datadir}/php/Doctrine/Common/Persistence
%{_datadir}/php/Doctrine/Common/Proxy
%{_datadir}/php/Doctrine/Common/Reflection
%{_datadir}/php/Doctrine/Common/Util


%changelog
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
