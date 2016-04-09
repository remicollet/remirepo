# remirepo spec file for php-guzzlehttp-guzzle6, from:
#
# Fedora spec file for php-guzzlehttp-guzzle6
#
# Copyright (c) 2015-2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     guzzle
%global github_name      guzzle
%global github_version   6.2.0
%global github_commit    d094e337976dff9d8e2424e8485872194e768662

%global composer_vendor  guzzlehttp
%global composer_project guzzle

# "php": ">=5.5.0"
%global php_min_ver      5.5.0
# "guzzlehttp/promises": "~1.0"
%global promises_min_ver 1.0
%global promises_max_ver 2.0
# "guzzlehttp/psr7": "~1.1"
%global psr7_min_ver     1.1
%global psr7_max_ver     2.0
# "psr/log": "~1.0"
#     NOTE: Min version not 1.0 because autoloader required
%global psr_log_min_ver  1.0.0-8
%global psr_log_max_ver  2.0

%if 0%{?rhel} == 5
# no nodejs available in RHEL-5
%global with_tests 0%{?_with_tests:1}
%else
# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}
%endif

%{!?phpdir:    %global phpdir    %{_datadir}/php}
%{!?testsdir:  %global testsdir  %{_datadir}/tests}

Name:          php-%{composer_vendor}-%{composer_project}6
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       PHP HTTP client library

Group:         Development/Libraries
License:       MIT
URL:           http://guzzlephp.org

# GitHub export does not include tests.
# Run php-guzzlehttp-guzzle6.sh to create full source.
Source0:       %{name}-%{github_version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: nodejs
## composer.json
BuildRequires: php(language)                     >= %{php_min_ver}
BuildRequires: php-composer(guzzlehttp/promises) >= %{promises_min_ver}
BuildRequires: php-composer(guzzlehttp/psr7)     >= %{psr7_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
#BuildRequires: php-composer(psr/log)             >= %%{psr_log_min_ver}
BuildRequires: php-PsrLog                        >= %{psr_log_min_ver}
## phpcompatinfo (computed from version 6.2.0)
BuildRequires: php-curl
BuildRequires: php-date
BuildRequires: php-filter
BuildRequires: php-intl
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
BuildRequires: php-zlib
# Autoloader
## NOTE: Min version 2.5 because class
##       \Symfony\Component\ClassLoader\Psr4ClassLoader required
BuildRequires: php-composer(symfony/class-loader) >= 2.5
%endif

Requires:      ca-certificates
# composer.json
Requires:      php(language)                     >= %{php_min_ver}
Requires:      php-composer(guzzlehttp/promises) >= %{promises_min_ver}
Requires:      php-composer(guzzlehttp/promises) <  %{promises_max_ver}
Requires:      php-composer(guzzlehttp/psr7)     >= %{psr7_min_ver}
Requires:      php-composer(guzzlehttp/psr7)     <  %{psr7_max_ver}
#Requires:      php-composer(psr/log)             >= %%{psr_log_min_ver}
Requires:      php-PsrLog                        >= %{psr_log_min_ver}
Requires:      php-composer(psr/log)             <  %{psr_log_max_ver}
# phpcompatinfo (computed from version 6.2.0)
Requires:      php-curl
Requires:      php-date
Requires:      php-filter
Requires:      php-json
Requires:      php-pcre
Requires:      php-spl
# Autoloader
## NOTE: Min version 2.5 because class
## \Symfony\Component\ClassLoader\Psr4ClassLoader required
Requires:      php-composer(symfony/class-loader) >= 2.5

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Guzzle is a PHP HTTP client that makes it easy to send HTTP requests and trivial
to integrate with web services.

* Simple interface for building query strings, POST requests, streaming large
  uploads, streaming large downloads, using HTTP cookies, uploading JSON data,
  etc...
* Can send both synchronous and asynchronous requests using the same interface.
* Uses PSR-7 interfaces for requests, responses, and streams. This allows you
  to utilize other PSR-7 compatible libraries with Guzzle.
* Abstracts away the underlying HTTP transport, allowing you to write
  environment and transport agnostic code; i.e., no hard dependency on cURL,
  PHP streams, sockets, or non-blocking event loops.
* Middleware system allows you to augment and compose client behavior.

Autoloader: %{phpdir}/GuzzleHttp6/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Create common autoloader
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 */

if (!isset($fedoraPsr4ClassLoader) || !($fedoraPsr4ClassLoader instanceof \Symfony\Component\ClassLoader\Psr4ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\Psr4ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/Psr4ClassLoader.php';
    }

    $fedoraPsr4ClassLoader = new \Symfony\Component\ClassLoader\Psr4ClassLoader();
    $fedoraPsr4ClassLoader->register(true);
}

$fedoraPsr4ClassLoader->addPrefix('GuzzleHttp\\', __DIR__);

require_once __DIR__.'/functions_include.php';
require_once '%{phpdir}/GuzzleHttp/Promise/autoload.php';
require_once '%{phpdir}/GuzzleHttp/Psr7/autoload.php';
require_once '%{phpdir}/Psr/Log/autoload.php';
AUTOLOAD


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}/GuzzleHttp6
cp -pr src/* %{buildroot}%{phpdir}/GuzzleHttp6/


%check
%if %{with_tests}
: Create mock Composer autoloader
mkdir vendor
cat <<'AUTOLOAD' | tee vendor/autoload.php
<?php
require_once '%{buildroot}%{phpdir}/GuzzleHttp6/autoload.php';
$fedoraPsr4ClassLoader->addPrefix('GuzzleHttp\\Tests\\', __DIR__.'/tests');
AUTOLOAD

ret=0
run=0

if which php70; then
   php70 %{_bindir}/phpunit --verbose || ret=1
   run=1
fi
if which php70; then
   php70 %{_bindir}/phpunit --verbose || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
   %{_bindir}/phpunit --verbose || ret=1
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
%doc *.md
%doc composer.json
%{phpdir}/GuzzleHttp6


%changelog
* Fri Apr 08 2016 Shawn Iwinski <shawn@iwin.ski> - 6.2.0-2
- Prepend PSR-4 autoloader (fixes dual-install issue with
  php-guzzlehttp-guzzle when other packages register PSR-0
  autoloader first usually with include path failover)

* Sun Mar 27 2016 Shawn Iwinski <shawn@iwin.ski> - 6.2.0-1
- Updated to 6.2.0 (RHBZ #1319960)

* Sun Jan 31 2016 Remi Collet <remi@remirepo.net> - 6.1.1-2
- backport for remi repository

* Thu Jan 28 2016 Shawn Iwinski <shawn@iwin.ski> - 6.1.1-2
- Added min version of autoloader dependency
- Fix directory ownership

* Sun Dec 06 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 6.1.1-1
- Renamed from php-guzzlehttp-guzzle to php-guzzlehttp-guzzle6 for
  dual-install of version 5 and version 6
- Updated to 6.1.1

* Sun Jun 28 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 5.3.0-3
- Autoloader updates

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 14 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 5.3.0-1
- Updated to 5.3.0 (BZ #1140134)
- Added autoloader
- Re-added tests

* Sun Feb 08 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 5.1.0-1
- Updated to 5.1.0 (BZ #1140134)
- CA cert no longer bundled (see
  https://github.com/guzzle/guzzle/blob/5.1.0/docs/clients.rst#verify)
- No tests because dependency package does not provide required test file

* Mon Jan 12 2015 Remi Collet <remi@fedoraproject.org> - 4.1.8-3
- Upstream patch for PHP behavior change, thanks Koschei

* Tue Aug 26 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 4.1.8-2
- Fix test suite when previous version installed

* Sat Aug 23 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 4.1.8-1
- Updated to 4.1.8 (BZ #1126611)

* Wed Jul 30 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 4.1.4-1
- Updated to 4.1.4 (BZ #1124226)
- Added %%license usage

* Sun Jun 29 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 4.1.2-1
- Updated to 4.1.2

* Fri Jun 06 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 4.1.0-1
- Updated to 4.1.0
- Require php-composer virtual provides instead of direct pkgs
- Added php-PsrLog and nodejs build requires
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide
- Added option to build without tests

* Fri May 23 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 4.0.2-1
- Initial package
