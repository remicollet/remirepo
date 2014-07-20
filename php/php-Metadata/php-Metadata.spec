#
# RPM spec file for php-Metadata
#
# Copyright (c) 2013-2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner    schmittjoh
%global github_name     metadata
%global github_version  1.5.1
%global github_commit   22b72455559a25777cfd28c4ffda81ff7639f353

%global composer_vendor  jms
%global composer_project metadata

%global lib_name         Metadata

# "php": ">=5.3.0"
%global php_min_ver 5.3.0
# "doctrine/cache" : "~1.0"
%global doctrine_cache_min_ver 1.0
%global doctrine_cache_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests %{?_without_tests:0}%{!?_without_tests:1}

%{!?__phpunit: %global __phpunit %{_bindir}/phpunit}

Name:          php-%{lib_name}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       A library for class/method/property metadata management in PHP

Group:         Development/Libraries
License:       ASL 2.0
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
%if %{with_tests}
# For tests
BuildRequires: php-phpunit-PHPUnit
# For tests: composer.json
BuildRequires: php(language)                >= %{php_min_ver}
BuildRequires: php-composer(doctrine/cache) >= %{doctrine_cache_min_ver}
BuildRequires: php-composer(doctrine/cache) <  %{doctrine_cache_max_ver}
# For tests: phpcompatinfo (computed from version 1.5.1)
BuildRequires: php-date
BuildRequires: php-reflection
BuildRequires: php-spl
%endif

Requires:      php-composer(doctrine/cache) >= %{doctrine_cache_min_ver}
Requires:      php-composer(doctrine/cache) <  %{doctrine_cache_max_ver}
Requires:      php-symfony-dependencyinjection
# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.5.1)
Requires:      php-date
Requires:      php-reflection
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
This library provides some commonly needed base classes for managing metadata
for classes, methods and properties. The metadata can come from many different
sources (annotations, YAML/XML/PHP configuration files).

The metadata classes are used to abstract away that source and provide a common
interface for all of them.


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}
mkdir -pm 0755 %{buildroot}%{_datadir}/php
cp -rp src/%{lib_name} %{buildroot}%{_datadir}/php/


%check
%if %{with_tests}
# Rewrite tests' bootstrap
cat > tests/bootstrap.php <<'BOOTSTRAP'
<?php
spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', str_replace('_', '/', $class)).'.php';
    @include_once $src;
});
BOOTSTRAP

# Create PHPUnit config w/ colors turned off
sed 's/colors\s*=\s*"true"/colors="false"/' phpunit.xml.dist > phpunit.xml

%{__phpunit} --include-path="./src:./tests" -d date.timezone="UTC"
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%{!?_licensedir:%global license %%doc}

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.rst CHANGELOG.md composer.json
%{_datadir}/php/%{lib_name}


%changelog
* Sat Jul 19 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.5.1-1
- Updated to 1.5.1 (BZ #1119425)
- Added "php-composer(jms/metadata)" virtual provide
- Added option to build without tests ("--without tests")

* Mon Jun  2 2014 Remi Collet <RPMS@famillecollet.com> 1.5.0-2
- merge rawhide change

* Fri May 30 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.5.0-2
- Updated dependencies to match newly available pkgs
  -- php-pear(pear.doctrine-project.org/DoctrineCommon) => php-doctrine-cache
     (cache separated out from common)
  -- php-pear(pear.symfony.com/DependencyInjection) => php-symfony-dependencyinjection
- Doctrine cache required instead of just build requirement

* Sat Nov 16 2013 Remi Collet <RPMS@famillecollet.com> 1.5.0-1
- backport 1.5.0 for remi repo

* Fri Nov 15 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.5.0-1
- Updated to 1.5.0

* Tue Apr  2 2013 Remi Collet <RPMS@famillecollet.com> 1.3.0-1
- backport 1.3.0 for remi repo

* Sat Mar 30 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.0-1
- Updated to version 1.3.0
- Removed tests sub-package

* Fri Jan 25 2013 Remi Collet <RPMS@famillecollet.com> 1.1.1-1
- backport 1.1.1 for remi repo

* Wed Jan 23 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.1-1
- Initial package
