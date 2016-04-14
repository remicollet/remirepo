# remirepo spec file for php-guzzle-Guzzle, from Fedora:
#
# Fedora spec file for php-guzzle-Guzzle
#
# Copyright (c) 2012-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%if 0%{?rhel} == 5
%global with_cacert 0
%else
%global with_cacert 1
%endif

%global github_owner     guzzle
%global github_name      guzzle3
%global github_version   3.9.3
%global github_commit    0645b70d953bc1c067bbc8d5bc53194706b628d9

%global composer_vendor  guzzle
%global composer_project guzzle

%global pear_channel     guzzlephp.org/pear
%global pear_name        Guzzle

# "php": ">=5.3.3"
%global php_min_ver 5.3.3
# "doctrine/cache": "~1.4,>=1.4.3"
%global doctrine_cache_min_ver 1.4.3
%global doctrine_cache_max_ver 2.0
# "monolog/monolog": "~1.0"
#     NOTE: Min version not 1.0 because autoloader required
%global monolog_min_ver 1.15.0
%global monolog_max_ver 2.0
# "psr/log": "~1.0"
#     NOTE: Min version not 1.0 because autoloader required
%global psr_log_min_ver 1.0.0-8
%global psr_log_max_ver 2.0
# "symfony/class-loader": "~2.1"
# "symfony/event-dispatcher": "~2.1"
%global symfony_min_ver 2.7.1
%global symfony_max_ver 3.0
# "zendframework/zend-cache": "2.*,<2.3",
# "zendframework/zend-log": "2.*,<2.3"
#     NOTE: Min version not 2.0 because autoloader required
#     NOTE: Max version 3 instead of 2.3 because tests pass
%global zend_min_ver 2.4.7
%global zend_max_ver 3

%if 0%{?fedora} < 18 && 0%{?rhel} < 6
# Missing nodejs
%global with_tests 0
%else
# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}
%endif

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-guzzle-%{pear_name}
Version:       %{github_version}
Release:       9%{?dist}
Summary:       PHP HTTP client library and framework for building RESTful web service clients

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

# Update tests to allow for Doctrine Cache >= 1.6.0 internal changes
# https://github.com/guzzle/guzzle3/pull/77
Patch0:        %{name}-doctrine-cache-gte-1-6-0.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: nodejs
## composer.json
BuildRequires: php(language)                          >= %{php_min_ver}
BuildRequires: php-composer(doctrine/cache)           >= %{doctrine_cache_min_ver}
BuildRequires: php-composer(monolog/monolog)          >= %{monolog_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
#BuildRequires: php-composer(psr/log)                  >= %%{psr_log_min_ver}
BuildRequires: php-PsrLog                             >= %{psr_log_min_ver}
BuildRequires: php-composer(symfony/class-loader)     >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/event-dispatcher) >= %{symfony_min_ver}
BuildRequires: php-composer(zendframework/zend-cache) >= %{zend_min_ver}
BuildRequires: php-composer(zendframework/zend-log)   >= %{zend_min_ver}
BuildRequires: php-curl
## phpcompatinfo (computed from version 3.9.3)
BuildRequires: php-ctype
BuildRequires: php-date
BuildRequires: php-filter
BuildRequires: php-hash
BuildRequires: php-intl
BuildRequires: php-json
BuildRequires: php-libxml
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-simplexml
BuildRequires: php-spl
BuildRequires: php-xmlwriter
BuildRequires: php-zlib
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                          >= %{php_min_ver}
Requires:      php-composer(symfony/event-dispatcher) >= %{symfony_min_ver}
Requires:      php-composer(symfony/event-dispatcher) <  %{symfony_max_ver}
Requires:      php-curl
# phpcompatinfo (computed from version 3.9.3)
Requires:      php-ctype
Requires:      php-date
Requires:      php-filter
Requires:      php-hash
Requires:      php-json
Requires:      php-libxml
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-simplexml
Requires:      php-spl
Requires:      php-xmlwriter
%if %{with_cacert}
# Unbundled CA certificate
Requires:      ca-certificates
%endif
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming
Provides:      php-%{composer_vendor}-%{composer_project}             = %{version}-%{release}
Provides:      php-%{composer_project}                                = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project})   = %{version}
## Sub-packages
Provides:      php-composer(%{composer_vendor}/batch)                 = %{version}
Provides:      php-composer(%{composer_vendor}/cache)                 = %{version}
Provides:      php-composer(%{composer_vendor}/common)                = %{version}
Provides:      php-composer(%{composer_vendor}/http)                  = %{version}
Provides:      php-composer(%{composer_vendor}/inflection)            = %{version}
Provides:      php-composer(%{composer_vendor}/iterator)              = %{version}
Provides:      php-composer(%{composer_vendor}/log)                   = %{version}
Provides:      php-composer(%{composer_vendor}/parser)                = %{version}
Provides:      php-composer(%{composer_vendor}/plugin)                = %{version}
Provides:      php-composer(%{composer_vendor}/plugin-async)          = %{version}
Provides:      php-composer(%{composer_vendor}/plugin-backoff)        = %{version}
Provides:      php-composer(%{composer_vendor}/plugin-cache)          = %{version}
Provides:      php-composer(%{composer_vendor}/plugin-cookie)         = %{version}
Provides:      php-composer(%{composer_vendor}/plugin-curlauth)       = %{version}
Provides:      php-composer(%{composer_vendor}/plugin-error-response) = %{version}
Provides:      php-composer(%{composer_vendor}/plugin-history)        = %{version}
Provides:      php-composer(%{composer_vendor}/plugin-log)            = %{version}
Provides:      php-composer(%{composer_vendor}/plugin-md5)            = %{version}
Provides:      php-composer(%{composer_vendor}/plugin-mock)           = %{version}
Provides:      php-composer(%{composer_vendor}/plugin-oauth)          = %{version}
Provides:      php-composer(%{composer_vendor}/service)               = %{version}
Provides:      php-composer(%{composer_vendor}/stream)                = %{version}
# PEAR
Provides:      php-pear(%{pear_channel}/%{pear_name})                 = %{version}

# This pkg was the only one in this channel so the channel is no longer needed
Obsoletes: php-channel-guzzle

# Weak dependencies
%if 0%{?fedora} >= 21
Suggests:      php-composer(doctrine/cache)
Suggests:      php-composer(monolog/monolog)
Suggests:      php-composer(zendframework/zend-cache)
Suggests:      php-composer(zendframework/zend-log)
%endif
Conflicts:     php-composer(doctrine/cache)           <  %{doctrine_cache_min_ver}
Conflicts:     php-composer(doctrine/cache)           >= %{doctrine_cache_max_ver}
Conflicts:     php-composer(monolog/monolog)          <  %{monolog_min_ver}
Conflicts:     php-composer(monolog/monolog)          >= %{monolog_max_ver}
Conflicts:     php-composer(zendframework/zend-cache) <  %{zend_min_ver}
Conflicts:     php-composer(zendframework/zend-cache) >= %{zend_max_ver}
Conflicts:     php-composer(zendframework/zend-log)   <  %{zend_min_ver}
Conflicts:     php-composer(zendframework/zend-log)   >= %{zend_max_ver}

%description
Guzzle takes the pain out of sending HTTP requests and the redundancy out
of creating web service clients.

Guzzle is a framework that includes the tools needed to create a robust web
service client, including: Service descriptions for defining the inputs and
outputs of an API, resource iterators for traversing paginated resources,
batching for sending a large number of requests as efficiently as possible.

* All the power of cURL with a simple interface
* Persistent connections and parallel requests
* Streams request and response bodies
* Service descriptions for quickly building clients
* Powered by the Symfony2 EventDispatcher
* Use all of the code or only specific components
* Plugins for caching, logging, OAuth, mocks, and more

Optional dependencies:
* Doctrine Cache (%{doctrine_cache_min_ver} <= php-doctrine-cache < %{doctrine_cache_max_ver})
* Monolog (%{monolog_min_ver} <= php-Monolog < %{monolog_max_ver})
* Zend Framework 2 Cache (%{zend_min_ver} <= php-ZendFramework2-Cache < %{zend_max_ver})
* Zend Framework 2 Log (%{zend_min_ver} <= php-ZendFramework2-Log < %{zend_max_ver})

***** EOL NOTICE *****

This package is for Guzzle 3.x. Guzzle 5.x+, the new versions of Guzzle, has
been released and is available as the package "php-guzzlehttp-guzzle". The
documentation for Guzzle version 5+ can be found at http://guzzlephp.org.

Guzzle 3 is only maintained for bug and security fixes. Guzzle 3 will be EOL at
some point in late 2015.

**********************


%prep
%setup -qn %{github_name}-%{github_commit}

: Update tests to allow for Doctrine Cache >= 1.6.0 internal changes
%patch0 -p1

%if %{with_cacert}
: Unbundle CA certificate
sed -e "s#__DIR__\s*.\s*'/Resources/cacert.pem'#'%{_sysconfdir}/pki/tls/cert.pem'#" \
    -e 's#$expectedMd5\s*=\s*.*#$expectedMd5 = $actualMd5;  // RPM NOTE: cacert.pem is managed by the ca-certificates package#' \
    -i src/Guzzle/Http/Client.php
rm src/Guzzle/Http/Resources/cacert.pem
%endif

: Create autoloader
cat <<'AUTOLOAD' | tee src/Guzzle/autoload.php
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

$fedoraClassLoader->addPrefix('Guzzle\\', dirname(__DIR__));

// Dependencies (autoloader => required)
foreach(array(
    '%{phpdir}/Doctrine/Common/Cache/autoload.php'             => false,
    '%{phpdir}/Monolog/autoload.php'                           => false,
    '%{phpdir}/Symfony/Component/EventDispatcher/autoload.php' => true,
    '%{phpdir}/Zend/autoload.php'                              => false,
) as $dependencyAutoloader => $required) {
    if ($required || file_exists($dependencyAutoloader)) {
        require_once $dependencyAutoloader;
    }
}

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create tests autoloader
cat <<'AUTOLOAD' | tee tests/autoload.php
<?php

$fedoraClassLoader =
    require_once '%{buildroot}%{phpdir}/Guzzle/autoload.php';

$fedoraClassLoader->addPrefix('Guzzle\\Tests', __DIR__);

require_once '%{phpdir}/Symfony/Component/ClassLoader/autoload.php';
AUTOLOAD

: Modify tests bootstrap
sed "s#require.*autoload.*#require __DIR__ . '/autoload.php';#" \
    -i tests/bootstrap.php

: Skip tests known to fail
#sed 's/function testPurgeRemovesAllMethodCaches/function SKIP_testPurgeRemovesAllMethodCaches/' \
#    -i tests/Guzzle/Tests/Plugin/Cache/DefaultCacheStorageTest.php
sed 's/function testAddsBody/function SKIP_testAddsBody/' \
    -i tests/Guzzle/Tests/Stream/PhpStreamRequestFactoryTest.php
%if 0%{?rhel} == 6 || 0%{?rhel} == 5
rm -f tests/Guzzle/Tests/Http/RedirectPluginTest.php
sed 's/function testCanCreateStreamsUsingDefaultFactory/function SKIP_testCanCreateStreamsUsingDefaultFactory/' \
    -i tests/Guzzle/Tests/Http/StaticClientTest.php
sed -e 's/function testOpensValidStreamByCreatingContext/function SKIP_testOpensValidStreamByCreatingContext/' \
    -e 's/function testAddsPostFields/function SKIP_testAddsPostFields/' \
    -e 's/function testAddsBody/function SKIP_testAddsBody/' \
    -i tests/Guzzle/Tests/Stream/PhpStreamRequestFactoryTest.php
sed 's/function testSendsPostRequestsWithFiles/function SKIP_testSendsPostRequestsWithFiles/' \
    -i tests/Guzzle/Tests/Http/Curl/CurlHandleTest.php
sed 's/function testSetPostFiles/function SKIP_testSetPostFiles/' \
    -i tests/Guzzle/Tests/Http/Message/EntityEnclosingRequestTest.php
sed -e 's/function testThrowsExceptionWithStrictMode/function SKIP_testThrowsExceptionWithStrictMode/' \
    -e 's/function testValidatesCookies/function SKIP_testValidatesCookies/' \
    -i tests/Guzzle/Tests/Plugin/Cookie/CookieTest.php
sed 's/function testThrowsExceptionWithStrictMode/function SKIP_testThrowsExceptionWithStrictMode/' \
    -i tests/Guzzle/Tests/Plugin/Cookie/CookieJar/ArrayCookieJarTest.php
sed 's/function testMustReturnRequest/function SKIP_testMustReturnRequest/' \
    -i tests/Guzzle/Tests/Service/Command/ClosureCommandTest.php
%endif

%{_bindir}/phpunit --verbose

if which php70; then
   %{_bindir}/phpunit --verbose
fi
%else
: Tests skipped
%endif

%if %{with_cacert}
# Ensure bundled CA cert is not referenced
grep -r "'/Resources/cacert.pem'" \
    %{buildroot}%{_datadir}/php/Guzzle \
    && exit 1
%endif


%clean
rm -rf %{buildroot}


%post
# Unregister PEAR pkg (ignore errors if it was not registered)
if [ -x %{_bindir}/pear ]; then
    %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{phpdir}/Guzzle
%exclude %{phpdir}/Guzzle/*/composer.json
%exclude %{phpdir}/Guzzle/*/*/composer.json

%changelog
* Wed Apr 13 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.9.3-9
- Re-rolled patch
- Updated autoloader dependency loading

* Thu Mar 24 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.9.3-8
- Add patches for tests
- Use actual dependency autoloaders instead of failover include path

* Sun Feb 28 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.9.3-7
- Skip additional tests known to fail (RHBZ #1307858)

* Thu Aug 13 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.9.3-5
- Added explicit autoloader build dependency
- Minor cleanups

* Wed Aug 12 2015 Remi Collet <remi@fedoraproject.org> - 3.9.3-4
- raise max version for Zend Framework

* Thu Aug  6 2015 Remi Collet <remi@fedoraproject.org> - 3.9.3-3.1
- ignore max ZF version

* Sat Jul 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.9.3-3
- Autoloader updates
- Added standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming provides

* Mon Jun 15 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.9.3-1
- Updated to 3.9.3
- Updated dependencies to use php-composer(*)
- Added composer sub-packages' provides
- Added optional dependency version conflicts
- Added EOL notice to %%description
- Added autoloader
- Excluded sub-packages' composer.json

* Sat Aug 23 2014 Remi Collet <remi@fedoraproject.org> - 3.9.2-2
- really drop bundled cacert

* Fri Aug 22 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.9.2-1
- Updated to 3.9.2 (BZ #1090936)
- PEAR install changed to Composer-ish install
- Obsoleted php-channel-guzzle
- Added tests

* Tue Apr 22 2014 Remi Collet <remi@fedoraproject.org> - 3.8.1-1
- backport 3.8.1 for remi repo

* Mon Apr 21 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.8.1-1
- Updated to 3.8.1 (BZ #1039260)

* Sun Feb 23 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.7.4-3
- Fixed unbundled cacert issue (Guzzle/Http/Client::preparePharCacert())
- Added test to ensure unbundled cacert is referenced

* Fri Feb 21 2014 Remi Collet <remi@fedoraproject.org> - 3.7.4-1.1
- EL-5 don't have ca-certificates

* Fri Nov 15 2013 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.7.4-2
- Updated PHP min version from 5.3.2 to 5.3.3
- php-common => php(language)

* Fri Nov 15 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 3.7.4-1
- Updated to 3.7.4
- Added php-libxml require

* Thu Oct 03 2013 Remi Collet <remi@fedoraproject.org> - 3.7.4-1
- Update to 3.7.4

* Mon Sep 16 2013 Remi Collet <remi@fedoraproject.org> - 3.7.3-1
- backport 3.7.3 for remi repo

* Sat Sep 14 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 3.7.3-1
- Updated to 3.7.3
- Added php-xmlwriter require

* Mon Aug 05 2013 Remi Collet <remi@fedoraproject.org> - 3.7.2-1
- Update to 3.7.2

* Mon Jul 08 2013 Remi Collet <remi@fedoraproject.org> - 3.7.1-1
- Update to 3.7.1

* Fri Jul 05 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 3.7.1-1
- Updated to 3.7.1

* Fri Jul 05 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 3.7.0-1
- Updated to 3.7.0 (BZ #973065)

* Wed Jun 12 2013 Remi Collet <remi@fedoraproject.org> - 3.7.0-1
- Update to 3.7.0

* Fri Jun 07 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 3.6.0-1
- Updated to 3.6.0

* Fri Jun 07 2013 Remi Collet <remi@fedoraproject.org> - 3.6.0-1
- Update to 3.6.0

* Wed May 08 2013 Remi Collet <remi@fedoraproject.org> - 3.4.3-1
- backport 3.3.0 for remi repo.

* Wed May 08 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 3.4.3-1
- Updated to version 3.4.3

* Tue Mar 12 2013 Remi Collet <remi@fedoraproject.org> - 3.3.1-1
- Update to 3.3.1

* Thu Mar 07 2013 Remi Collet <remi@fedoraproject.org> - 3.3.0-1
- backport 3.3.0 for remi repo.

* Mon Mar 04 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 3.3.0-1
- Updated to upstream version 3.3.0

* Tue Feb 26 2013 Remi Collet <remi@fedoraproject.org> - 3.2.0-1
- backport 3.2.0 for remi repo.

* Fri Feb 15 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 3.2.0-1
- Updated to upstream version 3.2.0

* Thu Feb  7 2013 Remi Collet <remi@fedoraproject.org> - 3.1.2-1
- backport 3.1.2 for remi repo.

* Mon Feb 04 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 3.1.2-1
- Updated to upstream version 3.1.2
- Removed bundled cert

* Sat Jan 26 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 3.1.1-1
- Updated to upstream version 3.1.1

* Sun Dec 16 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 3.0.6-1
- Updated to upstream version 3.0.6

* Sat Dec  8 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 3.0.5-1
- Initial package
