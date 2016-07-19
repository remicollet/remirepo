# remirepo spec file for php-guzzlehttp-guzzle, from:
#
# Fedora spec file for php-guzzlehttp-guzzle
#
# Copyright (c) 2014-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     guzzle
%global github_name      guzzle
%global github_version   5.3.1
%global github_commit    70f1fa53b71c4647bf2762c09068a95f77e12fb8

%global composer_vendor  guzzlehttp
%global composer_project guzzle

# "php": ">=5.4.0"
%global php_min_ver      5.4.0
# "guzzlehttp/ringphp": "^1.1"
#     Note: Min version not "1.1" because autoloader required
%global ring_min_ver     1.1.0-6
%global ring_max_ver     2.0
# "psr/log": "^1.0"
%global psr_log_min_ver  1.0
%global psr_log_max_ver  2.0

%if 0%{?rhel} == 5
# no nodejs available in RHEL-5
%global with_tests %{?_with_tests:1}%{!?_with_tests:0}
%else
# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}
%endif

%{!?phpdir:    %global phpdir    %{_datadir}/php}
%{!?testsdir:  %global testsdir  %{_datadir}/tests}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       PHP HTTP client and webservice framework

Group:         Development/Libraries
License:       MIT
URL:           http://guzzlephp.org

# GitHub export does not include tests.
# Run php-guzzlehttp-guzzle.sh to create full source.
Source0:       %{name}-%{github_version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: nodejs
BuildRequires: %{_bindir}/phpunit
BuildRequires: php-guzzlehttp-ringphp-tests
## composer.json
BuildRequires: php(language)                    >= %{php_min_ver}
#BuildRequires: php-composer(guzzlehttp/ringphp) >= %%{ring_min_ver}
BuildRequires: php-guzzlehttp-ringphp           >= %{ring_min_ver}
## phpcompatinfo (computed from version 5.3.1)
BuildRequires: php-curl
BuildRequires: php-date
BuildRequires: php-filter
BuildRequires: php-json
BuildRequires: php-libxml
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-simplexml
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# use path as ca-certificates doesn't exists on EL-5
Requires:      /etc/pki/tls/certs/ca-bundle.crt
# composer.json
Requires:      php(language)                    >= %{php_min_ver}
#Requires:      php-composer(guzzlehttp/ringphp) >= %%{ring_min_ver}
Requires:      php-guzzlehttp-ringphp           >= %{ring_min_ver}
Requires:      php-composer(guzzlehttp/ringphp) <  %{ring_max_ver}
# phpcompatinfo (computed from version 5.3.1)
Requires:      php-curl
Requires:      php-date
Requires:      php-filter
Requires:      php-json
Requires:      php-libxml
Requires:      php-pcre
Requires:      php-simplexml
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Guzzle is a PHP HTTP client that makes it easy to work with HTTP/1.1 and takes
the pain out of consuming web services.

* Pluggable HTTP adapters that can send requests serially or in parallel
* Doesn't require cURL, but uses cURL by default
* Streams data for both uploads and downloads
* Provides event hooks & plugins for cookies, caching, logging, OAuth, mocks,
  etc
* Keep-Alive & connection pooling
* SSL Verification
* Automatic decompression of response bodies
* Streaming multipart file uploads
* Connection timeouts


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

$fedoraClassLoader->addPrefix('GuzzleHttp\\', dirname(__DIR__));

// Required dependency
require_once '%{phpdir}/GuzzleHttp/Ring/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}/GuzzleHttp
cp -pr src/* %{buildroot}%{phpdir}/GuzzleHttp/


%check
%if %{with_tests}
: Create tests autoloader
cat <<'AUTOLOAD' | tee tests/autoload.php
<?php

$fedoraClassLoader = require '%{buildroot}%{phpdir}/GuzzleHttp/autoload.php';
$fedoraClassLoader->addPrefix('GuzzleHttp\\Tests', __DIR__);
AUTOLOAD

: Modify tests bootstrap
sed -e "s#.*require.*autoload.*#require __DIR__ . '/autoload.php';#" \
    -e "s#.*require.*Server.php.*#require '%{testsdir}/php-guzzlehttp-ringphp/autoload.php';#" \
    -i tests/bootstrap.php

: Mock tests PSR-0
mkdir tests/GuzzleHttp
ln -s .. tests/GuzzleHttp/Tests

run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit
   run=1
fi

%if 1
: Skip allowed failures
: https://github.com/guzzle/guzzle/blob/5.3.1/.travis.yml
: https://travis-ci.org/guzzle/guzzle/builds/145548161
sed -e 's/function testLoadsFromFileFile/function SKIP_testLoadsFromFileFile/' \
    -e 's/function testPersistsToFileFile/function SKIP_testPersistsToFileFile/' \
    -i tests/Cookie/FileCookieJarTest.php
sed -e 's/function testLoadsFromSession/function SKIP_testLoadsFromSession/' \
    -e 's/function testPersistsToSession/function SKIP_testPersistsToSession/' \
    -i tests/Cookie/SessionCookieJarTest.php
sed -e 's/function testParsesJsonResponses/function SKIP_testParsesJsonResponses/' \
    -e 's/function testThrowsExceptionWhenFailsToParseJsonResponse/function SKIP_testThrowsExceptionWhenFailsToParseJsonResponse/' \
    -i tests/Message/ResponseTest.php
sed 's/function testEnsuresResponseIsPresentAfterSending/function SKIP_testEnsuresResponseIsPresentAfterSending/' \
    -i tests/ClientTest.php
%endif

if which php71; then
   php71 %{_bindir}/phpunit || ret=1
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
%{phpdir}/GuzzleHttp/*


%changelog
* Tue Jul 19 2016 Remi Collet <remi@remirepo.net> - 5.3.1-1
- update to 5.3.1 (bacported from Fedora)
- run test suite with both PHP 5 and 7 when available

* Mon Jul 18 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 5.3.1-1
- Update to 5.3.1 (RHBZ #1350616 / RHBZ #1357580 / CVE-2016-5385)
- Add "get source" script

* Fri Apr 15 2016 Remi Collet <remi@remirepo.net> - 5.3.0-4.1
- fix dep. on EL-5

* Tue Sep 22 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 5.3.0-4
- Updated autoloader to load dependencies after self registration
- Minor cleanups

* Sun Jun 28 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 5.3.0-3
- Autoloader updates

* Sun Jun 14 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 5.3.0-1
- Updated to 5.3.0 (BZ #1140134)
- Added autoloader
- Re-added tests

* Sun Feb 08 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 5.1.0-1
- Updated to 5.1.0 (BZ #1140134)
- CA cert no longer bundled (see
  https://github.com/guzzle/guzzle/blob/5.1.0/docs/clients.rst#verify)
- No tests because dependency package does not provide required test file

* Sat Aug 23 2014 Remi Collet <remi@fedoraproject.org> - 4.1.8-1
- backport for remi repository

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
