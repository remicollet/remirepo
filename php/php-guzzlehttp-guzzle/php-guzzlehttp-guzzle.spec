#
# RPM spec file for php-guzzlehttp-guzzle
#
# Copyright (c) 2014 Shawn Iwinski <shawn.iwinski@gmail.com>
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
%global github_name      guzzle
%global github_version   4.1.8
%global github_commit    e196b8f44f9492a11261ea8f7b9724613a198daf

%global composer_vendor  guzzlehttp
%global composer_project guzzle

# "php": ">=5.4.0"
%global php_min_ver      5.4.0
# "guzzlehttp/streams": "~1.4"
%global streams_min_ver  1.4
%global streams_max_ver  2.0
# "psr/log": "~1.0"
%global psr_log_min_ver  1.0
%global psr_log_max_ver  2.0

%if 0%{?fedora} < 18 && 0%{?rhel} < 6
# Missing nodejs
%global with_tests 0
%else
# Build using "--without tests" to disable tests
%global with_tests       %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       PHP HTTP client and webservice framework

Group:         Development/Libraries
License:       MIT
URL:           http://guzzlephp.org
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
%if %{with_tests}
# For tests
BuildRequires: nodejs
# For tests: composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(guzzlehttp/streams) >= %{streams_min_ver}
BuildRequires: php-composer(guzzlehttp/streams) <  %{streams_max_ver}
BuildRequires: php-composer(psr/log) >= %{psr_log_min_ver}
BuildRequires: php-composer(psr/log) <  %{psr_log_max_ver}
BuildRequires: php-phpunit-PHPUnit
BuildRequires: php-curl
BuildRequires: php-json
# For tests: phpcompatinfo (computed from version 4.1.8)
BuildRequires: php-date
BuildRequires: php-filter
BuildRequires: php-libxml
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-simplexml
BuildRequires: php-spl
%endif

%if %{with_cacert}
Requires:      ca-certificates
%endif
# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(guzzlehttp/streams) >= %{streams_min_ver}
Requires:      php-composer(guzzlehttp/streams) <  %{streams_max_ver}
Requires:      php-json
# composer.json: optional
Requires:      php-curl
# phpcompatinfo (computed from version 4.1.8)
Requires:      php-date
Requires:      php-filter
Requires:      php-libxml
Requires:      php-pcre
Requires:      php-simplexml
Requires:      php-spl

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

%if %{with_cacert}
# Remove bundled cert
rm -f src/cacert.pem
sed "s#__DIR__ . '/cacert.pem'#'%{_sysconfdir}/pki/tls/cert.pem'#" \
    -i src/Client.php
sed "s#cacert.pem#%{_sysconfdir}/pki/tls/cert.pem#" \
    -i tests/ClientTest.php
sed "s#__DIR__ . '/../../src/cacert.pem'#'%{_sysconfdir}/pki/tls/cert.pem'#" \
    -i tests/Adapter/StreamAdapterTest.php
%endif


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -pm 0755 %{buildroot}%{_datadir}/php/GuzzleHttp
cp -pr src/* %{buildroot}%{_datadir}/php/GuzzleHttp/


%check
%if %{with_tests}
# Ensure no bundled cert
for DIR in src tests
do
    find $DIR | grep 'cacert.pem' && exit 1
    grep -r 'cacert.pem' $DIR && exit 1
done

# Create autoloader
mkdir vendor
cat > vendor/autoload.php <<'AUTOLOAD'
<?php

spl_autoload_register(function ($class) {
    $src = str_replace(array('\\', '_'), '/', $class).'.php';
    @include_once $src;
});

require_once '%{_datadir}/php/GuzzleHttp/Stream/functions.php';
require_once __DIR__ . '/../src/functions.php';
AUTOLOAD

# Create PHPUnit config w/ colors turned off
sed 's/colors\s*=\s*"true"/colors="false"/' phpunit.xml.dist > phpunit.xml

%{_bindir}/phpunit --include-path="%{buildroot}%{_datadir}/php" -d date.timezone="UTC"
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md composer.json
%{_datadir}/php/GuzzleHttp/*


%changelog
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
