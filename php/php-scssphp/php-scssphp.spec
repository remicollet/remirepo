# remirepo spec file for php-scssphp, from:
#
# Fedora spec file for php-scssphp
#
# Copyright (c) 2012-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#                         Remi Collet <remi@fedoraproject.org>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     leafo
%global github_name      scssphp
%global github_version   0.6.5
%global github_commit    0649d38dfef6808be1a89040a3312e8bda0b3aed

%global composer_vendor  leafo
%global composer_project scssphp

# "php": ">=5.4.0"
%global php_min_ver 5.4.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{github_name}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       A compiler for SCSS written in PHP

Group:         Development/Libraries
License:       MIT
URL:           http://leafo.github.io/scssphp

# GitHub export does not include tests.
# Run php-scssphp-get-source.sh to create full source.
Source0:       %{name}-%{github_version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Library version check
BuildRequires: php-cli
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
## phpcompatinfo (computed from version 0.6.5)
BuildRequires: php-ctype
BuildRequires: php-date
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

Requires:      php-cli
# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 0.6.5)
Requires:      php-ctype
Requires:      php-date
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming
Provides:      php-%{composer_vendor}-%{composer_project}           = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}


%description
SCSS (http://sass-lang.com/) is a CSS preprocessor that adds many features like
variables, mixins, imports, color manipulation, functions, and tons of other
powerful features.

The entire compiler comes in a single class file ready for including in any kind
of project in addition to a command line tool for running the compiler from the
terminal.

scssphp implements SCSS. It does not implement the SASS syntax, only the SCSS
syntax.


%prep
%setup -qn %{github_name}-%{github_commit}

: Bin
sed "/scss.inc.php/s#.*#require_once '%{phpdir}/Leafo/ScssPhp/autoload.php';#" \
    -i bin/pscss

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

$fedoraClassLoader->addPrefix('Leafo\\ScssPhp\\', dirname(dirname(__DIR__)));

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}

: Lib
mkdir -p %{buildroot}%{phpdir}/Leafo/ScssPhp
cp -pr src/* %{buildroot}%{phpdir}/Leafo/ScssPhp/

: Bin
mkdir -p %{buildroot}%{_bindir}
install -pm 0755 bin/pscss %{buildroot}%{_bindir}/


%check
: Library version value and autoloader check
%{_bindir}/php -r '
    require_once "%{buildroot}%{phpdir}/Leafo/ScssPhp/autoload.php";
    $version = ltrim(\Leafo\ScssPhp\Version::VERSION, "v");
    echo "Version $version (expected %{version})\n";
    exit(version_compare("%{version}", "$version", "=") ? 0 : 1);
'

%if %{with_tests}
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/Leafo/ScssPhp/autoload.php || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/Leafo/ScssPhp/autoload.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}%{phpdir}/Leafo/ScssPhp/autoload.php
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
%license LICENSE.md
%doc composer.json
%doc README.md
%{phpdir}/Leafo/ScssPhp
%{_bindir}/pscss


%changelog
* Sat Jul 23 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.6.5-1
- Updated to 0.6.5 (RHBZ #1347068)
- Dropped pre-0.1.0 compat

* Wed Jan 20 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.4.0-1
- Updated to 0.4.0 (RHBZ #1274939)
- Removed php-json dependency

* Sun Oct 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.3.2-1
- Updated to 0.3.2 (RHBZ #1268709)

* Sun Sep 20 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.3.1-1
- Updated to 0.3.1 (RHBZ #1256168)
- Updated URL
- Added standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming provides
- Added library version value check

* Thu Aug 13 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.1.9-1
- Updated to 0.1.9 (RHBZ #1238727)
- As of version 0.1.7 license is just MIT (i.e. GPLv3 removed)

* Sun Jun 28 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.1.6-1
- Updated to 0.1.6 (RHBZ #1226748)
- Added autoloader

* Thu Oct 30 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.1.1-1
- Updated to 0.1.1 (BZ #1126612)
- Removed man page
- %%license usage

* Tue Aug 19 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.0.15-1
- Updated to 0.0.15 (BZ #1126612)

* Mon Jul 07 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.0.12-1
- Updated to 0.0.12 (BZ #1116615)
- Added option to build without tests ("--without tests")

* Sun Jun  8 2014 Remi Collet <remi@fedoraproject.org> - 0.0.10-2
- fix FTBFS, ignore max version of PHPUnit
- provides php-composer(leafo/scssphp)

* Tue Apr 22 2014 Remi Collet <remi@fedoraproject.org> 0.0.10-1
- backport 0.0.9 for remi repo.

* Mon Apr 21 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.0.10-1
- Updated to 0.0.10 (BZ #1087738)

* Mon Dec 30 2013 Remi Collet <remi@fedoraproject.org> 0.0.9-1
- backport 0.0.9 for remi repo.

* Sun Dec 29 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.0.9-1
- Updated to 0.0.9 (BZ #1046671)
- Spec cleanup

* Sat Nov 16 2013 Remi Collet <remi@fedoraproject.org> 0.0.8-1
- backport 0.0.8 for remi repo.

* Fri Nov 15 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.0.8-1
- Updated to 0.0.8

* Fri Jun 07 2013 Remi Collet <remi@fedoraproject.org> 0.0.7-1
- backport 0.0.7 for remi repo.

* Fri Jun 07 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.0.7-1
- Updated to 0.0.7

* Tue Mar 19 2013 Remi Collet <remi@fedoraproject.org> 0.0.5-1
- backport 0.0.5 for remi repo.

* Sat Mar 16 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.0.5-1
- Updated to version 0.0.5
- php-cli => php(language)
- %%{__php} => %%{_bindir}/php

* Sat Mar 09 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.0.4-2.20130301git3463d7d
- Updated to latest snapshot
- php-common => php-cli
- Added man page
- Removed tests from package

* Tue Nov 27 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 0.0.4-1
- Initial package
