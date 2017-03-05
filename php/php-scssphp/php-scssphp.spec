# remirepo spec file for php-scssphp, from:
#
# Fedora spec file for php-scssphp
#
# Copyright (c) 2012-2017 Shawn Iwinski <shawn.iwinski@gmail.com>
#                         Remi Collet <remi@fedoraproject.org>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     leafo
%global github_name      scssphp
%global github_version   0.6.7
%global github_commit    562213cd803e42ea53b0735554794c4022d8db89

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
## phpcompatinfo (computed from version 0.6.7)
BuildRequires: php-ctype
BuildRequires: php-date
BuildRequires: php-mbstring
BuildRequires: php-pcre
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

Requires:      php-cli
# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 0.6.7)
Requires:      php-ctype
Requires:      php-date
Requires:      php-mbstring
Requires:      php-pcre
# Autoloader
Requires:      php-composer(fedora/autoloader)

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

Autoloader: %{phpdir}/Leafo/ScssPhp/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Adjust bin autoload require
sed "/scss.inc.php/s#.*#require_once '%{phpdir}/Leafo/ScssPhp/autoload.php';#" \
    -i bin/pscss


%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 */
require_once '%{phpdir}/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Leafo\\ScssPhp\\', __DIR__);
AUTOLOAD


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
BOOTSTRAP=%{buildroot}%{phpdir}/Leafo/ScssPhp/autoload.php

: Upstream tests
%{_bindir}/phpunit --verbose --bootstrap $BOOTSTRAP

: Upstream tests with SCLs if available
SCL_RETURN_CODE=0
for SCL in %{?rhel:php55} php56 php70 php71; do
    if which $SCL; then
        $SCL %{_bindir}/phpunit --verbose --bootstrap $BOOTSTRAP || SCL_RETURN_CODE=1
    fi
done
exit $SCL_RETURN_CODE
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
* Sat Mar 04 2017 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.6.7-1
- Updated to 0.6.7 (RHBZ #1426927)
- Switch autoloader to php-composer(fedora/autoloader)
- Test with SCLs if available

* Sun Sep 25 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.6.6-1
- Updated to 0.6.6 (RHBZ #1376293)

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
