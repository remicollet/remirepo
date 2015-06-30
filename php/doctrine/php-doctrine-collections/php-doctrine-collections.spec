# remirepo spec file for php-doctrine-collections, from:
#
# Fedora spec file for php-doctrine-collections
#
# Copyright (c) 2013-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      collections
%global github_version   1.3.0
%global github_commit    6c1e4eef75f310ea1b3e30945e9f06e652128b8a

%global composer_vendor  doctrine
%global composer_project collections

# "php": ">=5.3.2"
%global php_min_ver      5.3.2

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       3%{?github_release}%{?dist}
Summary:       Collections abstraction library

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: %{_bindir}/phpunit
BuildRequires: php(language) >= %{php_min_ver}
## phpcompatinfo (computed from version 1.3.0)
BuildRequires: php-spl
# Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.3.0)
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

# Extracted from Doctrine Common as of version 2.4
Conflicts:     php-pear(pear.doctrine-project.org/DoctrineCommon) < 2.4

%description
%{summary}.


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
(cat <<'AUTOLOAD'
<?php
/**
 * Autoloader created by %{name}-%{version}-%{release}
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

$fedoraClassLoader->addPrefix('Doctrine\\Common\\Collections\\', dirname(dirname(dirname(__DIR__))));

return $fedoraClassLoader;
AUTOLOAD
) | tee lib/Doctrine/Common/Collections/autoload.php


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}
cp -rp lib/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create tests autoloader
(cat <<'AUTOLOAD'
<?php

$fedoraClassLoader =
    require_once '%{buildroot}%{phpdir}/Doctrine/Common/Collections/autoload.php';

$fedoraClassLoader->addPrefix('Doctrine\\Tests', __DIR__ . '/tests');
AUTOLOAD
) | tee autoload.php

: Run tests
%{_bindir}/phpunit -v --bootstrap autoload.php
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
%dir %{phpdir}/Doctrine
%dir %{phpdir}/Doctrine/Common
     %{phpdir}/Doctrine/Common/Collections


%changelog
* Sat Jun 27 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.0-3
- Updated autoloader with trailing separator

* Wed Jun 24 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.0-2
- Added autoloader dependencies

* Wed Jun 24 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.0-1
- Updated to 1.3.0 (RHBZ #1211818)
- Added autoloader
- %%license usage

* Fri Jun 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2-3
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide
- Added option to build without tests ("--without tests")

* Mon Feb 17 2014 Remi Collet <rpms@famillecollet.com> 1.2-1
- backport 1.2 for remi repo

* Wed Feb 12 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.2-1
- Updated to 1.2 (BZ #1061117)

* Sat Jan 11 2014 Remi Collet <rpms@famillecollet.com> 1.1-3.20131221git8198717
- backport for remi repo

* Mon Jan 06 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1-3.20131221git8198717
- Minor syntax changes

* Fri Jan 03 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1-2.20131221git8198717
- Conditional %%{?dist}
- Added conflict w/ PEAR-based DoctrineCommon pkg (version < 2.4)

* Mon Dec 23 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1-1.20131221git8198717
- Initial package
