#
# Fedora spec file for php-react-http
#
# Copyright (c) 2017 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     reactphp
%global github_name      http
%global github_version   0.4.2
%global github_commit    abedac54967d7ea237ad104cff8274e2c4077cf4

%global composer_vendor  react
%global composer_project http

# "php": ">= 5.4.0"
%global php_min_ver 5.4.0
# "evenement/evenement": "^2.0"
%global evenement_min_ver 2.0
%global evenement_max_ver 3.0
# "guzzlehttp/psr7": "^1.0"
%global guzzlehttp_psr7_min_ver 1.0
%global guzzlehttp_psr7_max_ver 2.0
# "react/socket": "^0.4"
%global react_socket_min_ver 0.4
%global react_socket_max_ver 1.0
# "react/stream": "^0.4"
%global react_stream_min_ver 0.4
%global react_stream_max_ver 1.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       Library for building an evented http server

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(evenement/evenement) <  %{evenement_max_ver}
BuildRequires: php-composer(evenement/evenement) >= %{evenement_min_ver}
BuildRequires: php-composer(guzzlehttp/psr7) <  %{guzzlehttp_psr7_max_ver}
BuildRequires: php-composer(guzzlehttp/psr7) >= %{guzzlehttp_psr7_min_ver}
BuildRequires: php-composer(react/socket) <  %{react_socket_max_ver}
BuildRequires: php-composer(react/socket) >= %{react_socket_min_ver}
BuildRequires: php-composer(react/stream) <  %{react_stream_max_ver}
BuildRequires: php-composer(react/stream) >= %{react_stream_min_ver}
## phpcompatinfo (computed from version 0.4.2)
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(evenement/evenement) <  %{evenement_max_ver}
Requires:      php-composer(evenement/evenement) >= %{evenement_min_ver}
Requires:      php-composer(guzzlehttp/psr7) <  %{guzzlehttp_psr7_max_ver}
Requires:      php-composer(guzzlehttp/psr7) >= %{guzzlehttp_psr7_min_ver}
Requires:      php-composer(react/socket) <  %{react_socket_max_ver}
Requires:      php-composer(react/socket) >= %{react_socket_min_ver}
Requires:      php-composer(react/stream) <  %{react_stream_max_ver}
Requires:      php-composer(react/stream) >= %{react_stream_min_ver}
# phpcompatinfo (computed from version 0.4.2)
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Library for building an evented http server.

This component builds on top of the Socket component to implement HTTP. Here
are the main concepts:

* Server: Attaches itself to an instance of React\Socket\ServerInterface,
      parses any incoming data as HTTP, emits a request event for each request.
* Request: A ReadableStream which streams the request body and contains meta
      data which was parsed from the request header.
* Response A WritableStream which streams the response body. You can set the
      status code and response headers via the writeHead() method.

Autoloader: %{phpdir}/React/Http/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 */
require_once '%{phpdir}/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('React\\Http\\', __DIR__);

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/Evenement/autoload.php',
    '%{phpdir}/GuzzleHttp/Psr7/autoload.php',
    '%{phpdir}/React/Socket/autoload.php',
    '%{phpdir}/React/Stream/autoload.php',
));
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}/React
cp -rp src %{buildroot}%{phpdir}/React/Http


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require '%{buildroot}%{phpdir}/React/Http/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('React\\Tests\\Http\\', __DIR__.'/tests');
BOOTSTRAP

: Upstream tests
%{_bindir}/phpunit --verbose --bootstrap bootstrap.php

: Upstream tests with SCLs if available
SCL_RETURN_CODE=0
for SCL in %{?rhel:php55} php56 php70 php71; do
    if which $SCL; then
        $SCL %{_bindir}/phpunit --verbose --bootstrap bootstrap.php || SCL_RETURN_CODE=1
    fi
done
exit $SCL_RETURN_CODE
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{phpdir}/React/Http


%changelog
* Tue Jan 24 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.2-2
- Minor update to SCL tests (only php55 if rhel)

* Tue Jan 17 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.2-1
- Initial package
