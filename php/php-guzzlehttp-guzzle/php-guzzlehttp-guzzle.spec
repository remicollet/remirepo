#
# RPM spec file for php-guzzlehttp-guzzle
#
# Copyright (c) 2014-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     guzzle
%global github_name      guzzle
%global github_version   5.1.0
%global github_commit    f1085bb4e023766a66b7b051914ec73bdf7202b5

%global composer_vendor  guzzlehttp
%global composer_project guzzle

# "php": ">=5.4.0"
%global php_min_ver      5.4.0
# "guzzlehttp/ringphp": "~1.0"
%global ring_min_ver     1.0
%global ring_max_ver     2.0
# "psr/log": "~1.0"
%global psr_log_min_ver  1.0
%global psr_log_max_ver  2.0

%{!?phpdir:     %global phpdir     %{_datadir}/php}
%{!?__phpunit:  %global __phpunit  %{_bindir}/phpunit}

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

Requires:      ca-certificates
# composer.json
Requires:      php(language)                    >= %{php_min_ver}
Requires:      php-composer(guzzlehttp/ringphp) >= %{ring_min_ver}
Requires:      php-composer(guzzlehttp/ringphp) <  %{ring_max_ver}
# phpcompatinfo (computed from version 5.1.0)
Requires:      php-curl
Requires:      php-date
Requires:      php-filter
Requires:      php-json
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


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}/GuzzleHttp
cp -pr src/* %{buildroot}%{phpdir}/GuzzleHttp/


%check
# Cannot run tests because RingPHP package does not provide tests
# (tests/bootstrap.php requires GuzzleHttp\Tests\Ring\Client\Server)


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
