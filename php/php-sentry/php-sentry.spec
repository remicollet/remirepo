# remirepo spec file for php-sentry, from
#
# Fedora spec file for php-sentry
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve the changelog entries
#

%global github_owner     getsentry
%global github_name      sentry-php
%global github_version   0.22.0
%global github_commit    49d4c0c4f2c298c9f15a07416debb5352a209b79

%global composer_vendor  sentry
%global composer_project sentry

# "php": ">=5.2.4"
%global php_min_ver      5.2.4
# "monolog/monolog": "*"
#     NOTE: Min version because autoloader required
%global monolog_min_ver  1.15.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       PHP client for Sentry

Group:         Development/Libraries
# ASL 2.0:
#     - lib/Raven/Serializer.php
# BSD:
#     - Everything else
License:       BSD and ASL 2.0
URL:           https://github.com/%{github_owner}/%{github_name}

# GitHub export does not include tests.
# Run php-sentry-get-source.sh to create full source.
Source0:       %{name}-%{github_version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:     noarch
# Library version value check
BuildRequires: php-cli
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(monolog/monolog) >= %{monolog_min_ver}
BuildRequires: php-curl
## phpcompatinfo (computed from version 0.22.0)
BuildRequires: php-date
BuildRequires: php-hash
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-session
BuildRequires: php-spl
BuildRequires: php-zlib
%if 0%{?fedora} >= 25
# Required for PHPUnit with PHP 7
# See https://github.com/getsentry/sentry-php/pull/365
BuildRequires: php-uopz
%endif
# Conflict because Monolog will load obsoleted package's autoloader and classes.
BuildConflicts: php-Raven
%endif

Requires:      php-cli
# use path as ca-certificates doesn't exists on EL-5
Requires:      /etc/pki/tls/cert.pem
# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(monolog/monolog) >= %{monolog_min_ver}
Requires:      php-curl
# phpcompatinfo (computed from version 0.22.0)
Requires:      php-date
Requires:      php-hash
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-session
Requires:      php-spl
Requires:      php-zlib

# Standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming
Provides:      php-%{composer_vendor}-%{composer_project} = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

# Rename
Obsoletes:     php-Raven < %{version}
Provides:      php-Raven = %{version}-%{release}
Provides:      php-composer(raven/raven) = %{version}


%description
%{summary} (http://getsentry.com).

Autoloader: %{phpdir}/Raven/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Remove bundled cert
rm -rf lib/Raven/data
sed "/return.*cacert\.pem/s#.*#        return '%{_sysconfdir}/pki/tls/cert.pem';#" \
    -i lib/Raven/Client.php

: Update autoloader require in bin
sed "/require.*Autoloader/s#.*#require_once '%{phpdir}/Raven/Autoloader.php';#" \
    -i bin/sentry


%build
: Create autoloader
cat <<'AUTOLOAD' | tee lib/Raven/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 */

require_once dirname(__FILE__).'/Autoloader.php';
Raven_Autoloader::register();

// Required dependency
require_once '%{phpdir}/Monolog/autoload.php';
AUTOLOAD


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}
cp -rp lib/* %{buildroot}%{phpdir}/

mkdir -p %{buildroot}%{_bindir}
install -pm 0755 bin/sentry %{buildroot}%{_bindir}/
: Compat bin
ln -s sentry %{buildroot}%{_bindir}/raven


%check
: Library version value check
%{_bindir}/php -r '
    require_once "%{buildroot}%{phpdir}/Raven/Client.php";
    $version = Raven_Client::VERSION;
    echo "Version $version (expected %{version})\n";
    exit(version_compare("%{version}", "$version", "=") ? 0 : 1);
'

%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
session_start();
require_once '%{buildroot}%{phpdir}/Raven/autoload.php';
BOOTSTRAP

: Run tests
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap bootstrap.php || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap bootstrap.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose --bootstrap bootstrap.php
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
%doc *.rst
%doc AUTHORS
%doc CHANGES
%doc composer.json
%{phpdir}/Raven
%{_bindir}/raven
%{_bindir}/sentry


%changelog
* Sun Nov  6 2016 Remi Collet <remi@remirepo.net> - 0.22.0-1
- add backport stuff for remi repo.

* Thu Nov 03 2016 Shawn Iwinski <shawn@iwin.ski> - 0.22.0-1
- Initial package
