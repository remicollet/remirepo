# remirepo spec file for php-robrichards-xmlseclibs, from
#
# Fedora spec file for php-robrichards-xmlseclibs
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve the changelog entries
#

%global github_owner     robrichards
%global github_name      xmlseclibs
%global github_version   2.0.1
%global github_commit    53bb1e9cae490a8f93af41bd9df6ea897161ca05

%global composer_vendor  robrichards
%global composer_project xmlseclibs

# "php": ">= 5.3"
%global php_min_ver 5.3

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       A PHP library for XML Security

Group:         Development/Libraries
License:       BSD
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: php-composer(phpunit/phpunit)
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
## composer.json: optional
BuildRequires: php-mcrypt
BuildRequires: php-openssl
## phpcompatinfo (computed from version 2.0.0)
BuildRequires: php-dom
BuildRequires: php-hash
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# composer.json: suggest
Requires:      php-openssl
# phpcompatinfo (computed from version 2.0.0)
Requires:      php-dom
Requires:      php-hash
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Weak dependencies
%if 0%{?fedora} >= 21
## composer.json: suggest
Suggests:      php-mcrypt
%endif

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}


%description
xmlseclibs is a library written in PHP for working with XML Encryption and
Signatures.

NOTE: php-mcrypt will not be automatically installed as a dependency of this
package so it will need to be "manually" installed if it is required --
specifically for the following XMLSecurityKey encryption types:
- XMLSecurityKey::AES128_CBC
- XMLSecurityKey::AES192_CBC
- XMLSecurityKey::AES256_CBC
- XMLSecurityKey::TRIPLEDES_CBC

Autoloader: %{phpdir}/RobRichards/XMLSecLibs/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}


%build
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

$fedoraClassLoader->addPrefix('RobRichards\\XMLSecLibs\\', dirname(dirname(__DIR__)));

return $fedoraClassLoader;
AUTOLOAD


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}/RobRichards/XMLSecLibs
cp -rp src/* %{buildroot}%{phpdir}/RobRichards/XMLSecLibs/


%check
%if %{with_tests}
: Use autoloader
sed 's#require.*xmlseclibs.*#require_once "%{buildroot}%{phpdir}/RobRichards/XMLSecLibs/autoload.php";#' \
    -i tests/*.phpt

: Skip tests known to fail
rm -f tests/extract-win-cert.phpt

: Run tests
run=0
if which php56; then
   php56 %{_bindir}/phpunit tests
   run=1
fi
if which php70; then
   # use 7.0 as 7.1 have mcrypt deprecated
   php70 %{_bindir}/phpunit tests
   run=1
fi
if [ $run -eq 0 ]; then
   %{_bindir}/phpunit --verbose tests
fi
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGELOG.txt
%doc composer.json
%doc README.md
%dir %{phpdir}/RobRichards
     %{phpdir}/RobRichards/XMLSecLibs


%changelog
* Thu Sep  8 2016 Remi Collet <remi@remirepo.net> - 2.0.1-1
- update to 2.0.1 (no change)

* Sun Jul 17 2016 Remi Collet <remi@remirepo.net> - 2.0.0-2.20160105git84313ca
- backport for remi repository

* Thu Jul 14 2016 Shawn Iwinski <shawn@iwin.ski> - 2.0.0-2.20160105git84313ca
- Updated to latest snapshot
- Moved php-openssl from weak dependency to hard dependency
- Added php-mcrypt weak dependency and added information to %%description about
  when it is required

* Sun Jul 10 2016 Shawn Iwinski <shawn@iwin.ski> - 2.0.0-1
- Initial package
