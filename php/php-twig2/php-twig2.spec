# fedora/remirepo spec file for php-twig2, from
#
# Fedora spec file for php-twig
#
# Copyright (c) 2014-2017 Shawn Iwinski <shawn.iwinski@gmail.com>
#                         Remi Collet <remi@fedoraproject.org>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global with_tests       0%{!?_without_tests:1}
%global github_owner     twigphp
%global github_name      Twig
%global github_commit    29bb02dde09ff56291d30f7687eb8696918023af
%global github_short     %(c=%{github_commit}; echo ${c:0:7})

%global composer_vendor  twig
%global composer_project twig

# "php": "^7.0"
%global php_min_ver 7.0
%global phpdir      %{_datadir}/php

Name:          php-%{composer_project}2
Version:       2.2.0
Release:       1%{?dist}
Summary:       The flexible, fast, and secure template engine for PHP

Group:         Development/Libraries
License:       BSD
URL:           http://twig.sensiolabs.org
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz

BUildArch:     noarch
## Autoloader
BuildRequires: php-fedora-autoloader-devel
%if %{with_tests}
# For tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(symfony/phpunit-bridge)
BuildRequires: php-composer(symfony/debug) >= 2.7
BuildRequires: php-composer(psr/container) >= 1.0
## phpcompatinfo (computed from version 2.0.0)
BuildRequires: php-ctype
BuildRequires: php-date
BuildRequires: php-hash
BuildRequires: php-iconv
BuildRequires: php-json
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
BuildRequires: php-simplexml
%endif

## composer.json
Requires:      php(language) >= %{php_min_ver}
## phpcompatinfo (computed from version 2.0.0)
Requires:      php-ctype
Requires:      php-date
Requires:      php-hash
Requires:      php-iconv
Requires:      php-json
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

## Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}


%description
%{summary}.

* Fast: Twig compiles templates down to plain optimized PHP code. The
  overhead compared to regular PHP code was reduced to the very minimum.

* Secure: Twig has a sandbox mode to evaluate untrusted template code. This
  allows Twig to be used as a template language for applications where users
  may modify the template design.

* Flexible: Twig is powered by a flexible lexer and parser. This allows the
  developer to define its own custom tags and filters, and create its own
  DSL.

Autoloader: %{phpdir}/Twig2/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Create classmap autoloader
phpab --template fedora --output lib/Twig/autoload.php lib/Twig


%install
mkdir -p %{buildroot}%{phpdir}
cp -rp lib/Twig %{buildroot}%{phpdir}/Twig2


%check
: Check library version
%{_bindir}/php -r 'require_once "%{buildroot}%{phpdir}/Twig2/autoload.php";
    exit(version_compare("%{version}", Twig_Environment::VERSION, "=") ? 0 : 1);'

%if %{with_tests}
mkdir vendor
phpab --output vendor/autoload.php test

cat << 'EOF' | tee -a vendor/autoload.php
// This library
require_once '%{buildroot}%{phpdir}/Twig2/autoload.php';
// Dependencies (require-dev)
require_once '%{phpdir}/Symfony/Bridge/PhpUnit/autoload.php';
require_once '%{phpdir}/Symfony/Component/Debug/autoload.php';
require_once '%{phpdir}/Psr/Container/autoload.php';
EOF

: Upstream test suite
RETURN_CODE=0
%{_bindir}/phpunit --verbose || RETURN_CODE=1

: Upstream tests with SCLs if available
for SCL in php70 php71; do
    if which $SCL; then
        $SCL %{_bindir}/phpunit --verbose || RETURN_CODE=1
    fi
done
exit $RETURN_CODE
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGELOG README.rst composer.json
%{phpdir}/Twig2


%changelog
* Mon Feb 27 2017 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- update to 2.2.0

* Wed Jan 11 2017 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- update to 2.1.0

* Fri Jan  6 2017 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0
- rename to php-twig2
- cleanup spec file, no more C extension
- use fedora/autoloader
- raise dependency on PHP version 7

* Fri Dec 23 2016 Remi Collet <remi@fedoraproject.org> - 1.30.0-1
- Update to 1.30.0

* Wed Dec 14 2016 Remi Collet <remi@fedoraproject.org> - 1.29.0-1
- Update to 1.29.0

* Thu Nov 24 2016 Remi Collet <remi@fedoraproject.org> - 1.28.2-1
- Update to 1.28.2

* Tue Nov 22 2016 Remi Collet <remi@fedoraproject.org> - 1.28.1-1
- Update to 1.28.1

* Fri Nov 18 2016 Remi Collet <remi@fedoraproject.org> - 1.28.0-1
- Update to 1.28.0

* Wed Oct 26 2016 Remi Collet <remi@fedoraproject.org> - 1.27.0-1
- Update to 1.27.0

* Thu Oct  6 2016 Remi Collet <remi@fedoraproject.org> - 1.26.1-1
- Update to 1.26.1

* Mon Oct  3 2016 Remi Collet <remi@fedoraproject.org> - 1.26.0-1
- Update to 1.26.0

* Thu Sep 22 2016 Remi Collet <remi@fedoraproject.org> - 1.25.0-1
- Update to 1.25.0

* Fri Sep  2 2016 Remi Collet <remi@fedoraproject.org> - 1.24.2-1
- Update to 1.24.2

* Mon Jun 27 2016 Remi Collet <remi@fedoraproject.org> - 1.24.1-2
- fix dependency with PHP-7

* Mon May 30 2016 Remi Collet <remi@fedoraproject.org> - 1.24.1-1
- Update to 1.24.1
- disable deprecation warning
- disable extension build with PHP 7

* Tue Jan 26 2016 Remi Collet <remi@fedoraproject.org> - 1.24.0-1
- Update to 1.24.0

* Mon Jan 11 2016 Remi Collet <remi@fedoraproject.org> - 1.23.3-1
- Update to 1.23.3
- run test suite with both PHP 5 and 7 when available

* Thu Nov 05 2015 Remi Collet <remi@fedoraproject.org> - 1.23.1-1
- Update to 1.23.1

* Fri Oct 30 2015 Remi Collet <remi@fedoraproject.org> - 1.23.0-1
- Update to 1.23.0

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 1.22.3-1
- Update to 1.22.3

* Sun Oct 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.22.2-1
- Updated to 1.22.2 (RHBZ #1262655)
- Added lib and ext version checks

* Wed Sep 23 2015 Remi Collet <remi@fedoraproject.org> - 1.22.2-1
- Update to 1.22.2

* Tue Sep 15 2015 Remi Collet <remi@fedoraproject.org> - 1.22.1-1
- Update to 1.22.1

* Sun Sep 13 2015 Remi Collet <remi@fedoraproject.org> - 1.22.0-1
- Update to 1.22.0

* Sat Sep 12 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.21.2-1
- Updated to 1.21.2 (BZ #1256767)

* Wed Sep  9 2015 Remi Collet <remi@fedoraproject.org> - 1.21.2-1
- Update to 1.21.2

* Wed Aug 26 2015 Remi Collet <remi@fedoraproject.org> - 1.21.1-1
- Update to 1.21.1

* Tue Aug 25 2015 Remi Collet <remi@fedoraproject.org> - 1.21.0-1
- Update to 1.21.0

* Wed Aug 12 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.20.0-1
- Updated to 1.20.0 (BZ #1249259)

* Wed Aug 12 2015 Remi Collet <remi@fedoraproject.org> - 1.20.0-1
- Update to 1.20.0

* Fri Jul 31 2015 Remi Collet <remi@fedoraproject.org> - 1.19.0-1
- Update to 1.19.0

* Mon Jun 22 2015 Remi Collet <rcollet@redhat.com> - 1.18.2-4
- add virtual "rh-php56" provides

* Fri Jun 19 2015 Remi Collet <remi@fedoraproject.org> - 1.18.2-3
- allow build against rh-php56 (as more-php56)

* Mon Jun 15 2015 Remi Collet <remi@fedoraproject.org> - 1.18.2-2
- rebuild for remirepo with rawhide changes (autoloader)

* Thu Jun 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.18.2-1
- Updated to 1.18.2 (BZ #1183601)
- Added autoloader

* Sun Jun  7 2015 Remi Collet <remi@fedoraproject.org> - 1.18.2-1
- Update to 1.18.2

* Sun Apr 19 2015 Remi Collet <remi@fedoraproject.org> - 1.18.1-1
- Update to 1.18.1

* Mon Jan 26 2015 Remi Collet <remi@fedoraproject.org> - 1.18.0-1
- Update to 1.18.0

* Wed Jan 14 2015 Remi Collet <remi@fedoraproject.org> - 1.17.0-1
- Update to 1.17.0

* Fri Dec 26 2014 Remi Collet <remi@fedoraproject.org> - 1.16.3-1
- Update to 1.16.3

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.16.2-1.1
- Fedora 21 SCL mass rebuild

* Fri Oct 17 2014 Remi Collet <remi@fedoraproject.org> - 1.16.2-1
- Update to 1.16.2

* Sat Oct 11 2014 Remi Collet <remi@fedoraproject.org> - 1.16.1-1
- Update to 1.16.1

* Thu Aug 28 2014 Remi Collet <remi@fedoraproject.org> - 1.16.0-2
- allow SCL build
- add backport stuff for EL-5

* Mon Aug 25 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.16.0-2
- Removed obsolete and provide of php-twig-CTwig (never imported into Fedora/EPEL)
- Obsolete php-channel-twig
- Removed comment about optional Xdebug in description (does not provide any new feature)
- Always run extension minimal load test

* Tue Jul 29 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.16.0-1
- Initial package
