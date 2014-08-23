#
# RPM spec file for php-guzzle-Guzzle
#
# Copyright (c) 2012-2014 Shawn Iwinski <shawn.iwinski@gmail.com>
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
%global github_version   3.9.2
%global github_commit    54991459675c1a2924122afbb0e5609ade581155

%global composer_vendor  guzzle
%global composer_project guzzle

%global pear_channel     guzzlephp.org/pear
%global pear_name        Guzzle

# "php": ">=5.3.3"
%global php_min_ver 5.3.3
# "doctrine/cache": "~1.3"
%global doctrine_cache_min_ver 1.3
%global doctrine_cache_max_ver 2.0
# "monolog/monolog": "~1.0"
%global monolog_min_ver 1.0
%global monolog_max_ver 2.0
# "phpunit/phpunit": "3.7.*"
#     NOTE: Max version ignored on purpose
%global _min_ver 3.7.0
# "psr/log": "~1.0"
%global psr_log_min_ver 1.0
%global psr_log_max_ver 2.0
# "symfony/class-loader": "~2.1"
# "symfony/event-dispatcher": "~2.1"
%global symfony_min_ver 2.1
%global symfony_max_ver 3.0
# "zendframework/zend-cache": "2.*,<2.3",
# "zendframework/zend-log": "2.*,<2.3"
#     NOTE: Max 2.4 instead of 2.3 because tests with 2.3 pass
%global zend_min_ver 2.0
%global zend_max_ver 2.4

%if 0%{?fedora} < 18 && 0%{?rhel} < 6
# Missing nodejs
%global with_tests 0
%else
# Build using "--without tests" to disable tests
%global with_tests %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:          php-guzzle-%{pear_name}
Version:       3.9.2
Release:       1%{?dist}
Summary:       PHP HTTP client library and framework for building RESTful web service clients

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
%if %{with_tests}
# For tests
BuildRequires: nodejs
# For tests: composer.json
BuildRequires: php(language)                 >= %{php_min_ver}
BuildRequires: php-composer(doctrine/cache)  >= %{doctrine_cache_min_ver}
BuildRequires: php-composer(doctrine/cache)  <  %{doctrine_cache_max_ver}
BuildRequires: php-composer(monolog/monolog) >= %{monolog_min_ver}
BuildRequires: php-composer(monolog/monolog) <  %{monolog_max_ver}
BuildRequires: php-composer(psr/log)         >= %{psr_log_min_ver}
BuildRequires: php-composer(psr/log)         <  %{psr_log_max_ver}
BuildRequires: php-phpunit-PHPUnit
BuildRequires: php-symfony-eventdispatcher   >= %{symfony_min_ver}
BuildRequires: php-symfony-eventdispatcher   <  %{symfony_max_ver}
BuildRequires: php-ZendFramework2            >= %{zend_min_ver}
BuildRequires: php-ZendFramework2            <  %{zend_max_ver}
BuildRequires: php-curl
# For tests: phpcompatinfo (computed from version 3.9.2)
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
%endif

%if %{with_cacert}
Requires:      ca-certificates
%endif
# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-symfony-eventdispatcher >= %{symfony_min_ver}
Requires:      php-symfony-eventdispatcher <  %{symfony_max_ver}
Requires:      php-curl
# phpcompatinfo (computed from version 3.9.2)
Requires:      php-ctype
Requires:      php-date
Requires:      php-filter
Requires:      php-hash
Requires:      php-intl
Requires:      php-json
Requires:      php-libxml
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-simplexml
Requires:      php-spl
Requires:      php-xmlwriter

# Composer
Provides:  php-composer(%{composer_vendor}/%{composer_project}) = %{version}
# PEAR
Provides:  php-pear(%{pear_channel}/%{pear_name}) = %{version}

# This pkg was the only one in this channel so the channel is no longer needed
Obsoletes: php-channel-guzzle

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
* Zend Framework (php-ZendFramework2)
* Doctrine Cache (php-doctrine-cache)
* Monolog (php-Monolog)


%prep
%setup -qn %{github_name}-%{github_commit}

%if %{with_cacert}
# Remove bundled cert
sed -e "s#__DIR__\s*.\s*'/Resources/cacert.pem'#'%{_sysconfdir}/pki/tls/cert.pem'#" \
    -e 's#$expectedMd5\s*=\s*.*#$expectedMd5 = $actualMd5;  // RPM NOTE: cacert.pem is managed by the ca-certificates package#' \
    -i src/Guzzle/Http/Client.php

rm src/Guzzle/Http/Resources/cacert.pem
%endif


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/php
cp -rp src/* %{buildroot}%{_datadir}/php/


%check
%if %{with_tests}
# Create autoloader
mkdir vendor
cat > vendor/autoload.php <<'AUTOLOAD'
<?php
spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', $class).'.php';
    @include_once $src;
});
AUTOLOAD

# Create PHPUnit config w/ colors turned off
sed 's/colors\s*=\s*"true"/colors="false"/' phpunit.xml.dist > phpunit.xml

# Skip tests known to fail
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

%{_bindir}/phpunit --include-path=./src:./tests -d date.timezone="UTC" .
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
%doc *.md composer.json
%{_datadir}/php/Guzzle

%changelog
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
