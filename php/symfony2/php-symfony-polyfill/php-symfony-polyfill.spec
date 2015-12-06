# remirepo spec file for php-symfony-polyfill
#
# Fedora spec file for php-symfony-polyfill
#
# Copyright (c) 2015 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     symfony
%global github_name      polyfill
%global github_version   1.0.0
%global github_commit    fef21adc706d3bb8f31d37c503ded2160c76c64a

%global composer_vendor  symfony
%global composer_project polyfill

# "php": ">=5.3.3"
%global php_min_ver 5.3.3

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Symfony polyfills backporting features to lower PHP versions

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

# See https://github.com/symfony/polyfill/pull/15
Patch0:        %{name}-pr15.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# PHP_VERSION_ID
BuildRequires: php-cli
# Autoloader
BuildRequires: php-composer(theseer/autoload)
# Tests
%if %{with_tests}
BuildRequires: php-composer(phpunit/phpunit)
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(ircmaxell/password-compat)
BuildRequires: php-composer(paragonie/random_compat)
## phpcompatinfo (computed from version 1.0.0)
BuildRequires: php-hash
BuildRequires: php-json
BuildRequires: php-ldap
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(ircmaxell/password-compat)
Requires:      php-composer(paragonie/random_compat)
# phpcompatinfo (computed from version 1.0.0)
Requires:      php-hash
Requires:      php-json
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project})       = %{version}
Provides:      php-composer(%{composer_vendor}/%{composer_project}-util)  = %{version}
Provides:      php-composer(%{composer_vendor}/%{composer_project}-php54) = %{version}
Provides:      php-composer(%{composer_vendor}/%{composer_project}-php55) = %{version}
Provides:      php-composer(%{composer_vendor}/%{composer_project}-php56) = %{version}
Provides:      php-composer(%{composer_vendor}/%{composer_project}-php70) = %{version}


%description
%{summary}.

Autoloader: %{phpdir}/Symfony/Polyfill/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

%patch0 -p1

: Docs
mkdir docs
mv *.md composer.json docs/

: Remove unneeded polyfills
rm -rf {src,tests}/{Iconv,Intl,Mbstring,Xml}

: Php54
: Docs
mkdir docs/Php54
cp -p src/Php54/{*.md,composer.json} docs/Php54/

: Php55
: Docs
mkdir docs/Php55
cp -p src/Php55/{*.md,composer.json} docs/Php55/

: Php56
: Docs
mkdir docs/Php56
cp -p src/Php56/{*.md,composer.json} docs/Php56/

: Php70
: Docs
mkdir docs/Php70
cp -p src/Php70/{*.md,composer.json} docs/Php70/

: Util
: Docs
mkdir docs/Util
cp -p src/Util/{*.md,composer.json} docs/Php70/


%build
: Create autoloader
%{_bindir}/phpab --nolower --tolerant --output src/autoload.php src/
cat <<'AUTOLOAD' >> src/autoload.php

require_once __DIR__ . '/Php54/bootstrap.php';
require_once '%{phpdir}/password_compat/password.php';
require_once __DIR__ . '/Php55/bootstrap.php';
require_once __DIR__ . '/Php56/bootstrap.php';
require_once '%{phpdir}/random_compat/autoload.php';
require_once __DIR__ . '/Php70/bootstrap.php';
AUTOLOAD
cat src/autoload.php


%install
rm -rf     %{buildroot}

mkdir -p %{buildroot}%{phpdir}/Symfony/Polyfill
cp -rp src/* %{buildroot}%{phpdir}/Symfony/Polyfill/


%check
%if %{with_tests}
%{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}%{phpdir}/Symfony/Polyfill/autoload.php

if which php70; then
  php70 %{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}%{phpdir}/Symfony/Polyfill/autoload.php
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
%doc docs/*
%{phpdir}/Symfony/Polyfill
%exclude %{phpdir}/Symfony/Polyfill/*/*.md
%exclude %{phpdir}/Symfony/Polyfill/*/composer.json
%exclude %{phpdir}/Symfony/Polyfill/*/LICENSE


%changelog
* Sun Dec  6 2015 Remi Collet <remi@remirepo.net> - 1.0.0-1
- provide everything for all PHP version
- add backport stuff

* Wed Nov 25 2015 Shawn Iwinski <shawn@iwin.ski> - 1.0.0-1
- Initial package
