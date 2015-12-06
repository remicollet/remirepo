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

%global php_version_id %(%{_bindir}/php -r "echo PHP_VERSION_ID;")

%if %{php_version_id} < 50400
%global with_php54 1
%else
%global with_php54 0
%endif

%if %{php_version_id} < 50500
%global with_php55 1
%else
%global with_php55 0
%endif

%if %{php_version_id} < 50600
%global with_php56 1
%else
%global with_php56 0
%endif

%if %{php_version_id} < 70000
%global with_php70 1
%else
%global with_php70 0
%endif

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Symfony polyfills backporting features to lower PHP versions

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

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
%if %{with_php55}
BuildRequires: php-composer(ircmaxell/password-compat)
%endif
%if %{with_php70}
BuildRequires: php-composer(paragonie/random_compat)
%endif
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
%if %{with_php55}
Requires:      php-composer(ircmaxell/password-compat)
%endif
%if %{with_php70}
Requires:      php-composer(paragonie/random_compat)
%endif
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
%if %{with_php54}
Provides:      php-composer(%{composer_vendor}/%{composer_project}-php54) = %{version}
%endif
%if %{with_php55}
Provides:      php-composer(%{composer_vendor}/%{composer_project}-php55) = %{version}
%endif
%if %{with_php56}
Provides:      php-composer(%{composer_vendor}/%{composer_project}-php56) = %{version}
%endif
%if %{with_php70}
Provides:      php-composer(%{composer_vendor}/%{composer_project}-php70) = %{version}
%endif

%description
%{summary}.

Autoloader: %{phpdir}/Symfony/Polyfill/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Docs
mkdir docs
mv *.md composer.json docs/

: Remove unneeded polyfills
rm -rf {src,tests}/{Iconv,Intl,Mbstring,Xml}

: Php54
%if %{with_php54}
: Docs
mkdir docs/Php54
cp -p src/Php54/{*.md,composer.json} docs/Php54/
%else
: Remove unneeded polyfill
rm -rf {src,tests}/Php54
%endif

: Php55
%if %{with_php55}
: Docs
mkdir docs/Php55
cp -p src/Php55/{*.md,composer.json} docs/Php55/
%else
: Remove unneeded polyfill
rm -rf {src,tests}/Php55
%endif

: Php56
%if %{with_php56}
: Docs
mkdir docs/Php56
cp -p src/Php56/{*.md,composer.json} docs/Php56/
%else
: Remove unneeded polyfill
rm -rf {src,tests}/Php56
%endif

: Php70
%if %{with_php70}
: Docs
mkdir docs/Php70
cp -p src/Php70/{*.md,composer.json} docs/Php70/
%else
: Remove unneeded polyfill
rm -rf {src,tests}/Php70
%endif


%build
: Create autoloader
%{_bindir}/phpab --nolower --tolerant --output src/autoload.php src/
cat <<'AUTOLOAD' >> src/autoload.php

%if %{with_php54}
require_once __DIR__ . '/Php54/bootstrap.php';
%endif
%if %{with_php55}
require_once '%{phpdir}/password_compat/password.php';
require_once __DIR__ . '/Php55/bootstrap.php';
%endif
%if %{with_php56}
require_once __DIR__ . '/Php56/bootstrap.php';
%endif
%if %{with_php70}
require_once '%{phpdir}/random_compat/autoload.php';
require_once __DIR__ . '/Php70/bootstrap.php';
%endif
AUTOLOAD
cat src/autoload.php


%install
mkdir -p %{buildroot}%{phpdir}/Symfony/Polyfill
cp -rp src/* %{buildroot}%{phpdir}/Symfony/Polyfill/


%check
%if 0%{with_php54}%{with_php55}%{with_php56}%{with_php70} < 1
: No polyfills required
exit 1
%endif

%if %{with_tests}
%{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}%{phpdir}/Symfony/Polyfill/autoload.php
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc docs/*
%{phpdir}/Symfony/Polyfill
%exclude %{phpdir}/Symfony/Polyfill/*/*.md
%exclude %{phpdir}/Symfony/Polyfill/*/composer.json
%exclude %{phpdir}/Symfony/Polyfill/*/LICENSE


%changelog
* Wed Nov 25 2015 Shawn Iwinski <shawn@iwin.ski> - 1.0.0-1
- Initial package
