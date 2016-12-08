# remirepo spec file for php-mtdowling-jmespath-php from:
#
# Fedora spec file for php-mtdowling-jmespath-php
#
# Copyright (c) 2015-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     jmespath
%global github_name      jmespath.php
%global github_version   2.4.0
%global github_commit    adcc9531682cf87dfda21e1fd5d0e7a41d292fac

%global composer_vendor  mtdowling
%global composer_project jmespath.php

# "php": ">=5.4.0"
%global php_min_ver 5.4.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-jmespath-php
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Declaratively specify how to extract elements from a JSON document

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
## phpcompatinfo (computed from version 2.4.0)
BuildRequires: php-json
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

Requires:      php-cli
# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 2.4.0)
Requires:      php-json
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}
Provides:      php-%{composer_vendor}-%{composer_project}           = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
JMESPath (pronounced "jaymz path") allows you to declaratively specify how to
extract elements from a JSON document. jmespath.php allows you to use JMESPath
in PHP applications with PHP data structures.


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 */
require_once '%{phpdir}/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('JmesPath\\', __DIR__);

require_once __DIR__ . '/JmesPath.php';
AUTOLOAD

: Modify bin script
sed "s#.*require.*autoload.*#require_once '%{phpdir}/JmesPath/autoload.php';#" \
    -i bin/jp.php


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}
: Lib
mkdir -p %{buildroot}%{phpdir}/JmesPath
cp -rp src/* %{buildroot}%{phpdir}/JmesPath/

: Bin
mkdir -p %{buildroot}%{_bindir}
install -pm 0755 bin/jp.php %{buildroot}%{_bindir}/


%check
%if %{with_tests}
: Skip test known to fail
sed 's/function testTokenizesJsonNumbers/function SKIP_testTokenizesJsonNumbers/' \
    -i tests/LexerTest.php

: Run tests
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/JmesPath/autoload.php || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/JmesPath/autoload.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}%{phpdir}/JmesPath/autoload.php
# remirepo:2
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
%doc CHANGELOG.md
%doc README.rst
%doc composer.json
%{phpdir}/JmesPath
%{_bindir}/jp.php


%changelog
* Wed Dec 07 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.4.0-1
- Update to 2.4.0 (RHBZ #1401271)
- Change autoloader from php-composer(symfony/class-loader) to
  php-composer(fedora/autoloader)

* Sun Jun 28 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.3.0-1
- Updated to 2.3.0 (RHBZ #1295982)
- Added "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" ("php-mtdowling-jmespath.php")
  virtual provide

* Sun Jun 28 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.2.0-1
- Updated to 2.2.0 (RHBZ #1225677)
- Changed autoloader from phpab to Symfony ClassLoader

* Mon May 18 2015 Remi Collet <RPMS@FamilleCollet.com> - 2.1.0-1
- add needed backport stuff for remi repository

* Sat May 16 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.1.0-1
- Initial package
