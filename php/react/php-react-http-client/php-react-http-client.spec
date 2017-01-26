#
# Fedora spec file for php-react-http-client
#
# Copyright (c) 2017 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     reactphp
%global github_name      http-client
%global github_version   0.4.15
%global github_commit    01e919008363622334f91419a9908b3a51754ccd

%global composer_vendor  react
%global composer_project http-client

# "php": ">= 5.4.0"
%global php_min_ver 5.4.0
# "evenement/evenement": "~2.0"
%global evenement_min_ver 2.0
%global evenement_max_ver 3.0
# "guzzlehttp/psr7": "^1.0"
%global guzzlehttp_psr7_min_ver 1.0
%global guzzlehttp_psr7_max_ver 2.0
# "react/dns": "0.4.*"
%global react_dns_min_ver 0.4.0
%global react_dns_max_ver 0.5.0
# "react/event-loop": "0.4.*"
%global react_event_loop_min_ver 0.4.0
%global react_event_loop_max_ver 0.5.0
# "react/promise": "~2.2"
%global react_promise_min_ver 2.2
%global react_promise_max_ver 3.0
# "react/socket-client": "^0.5 || ^0.4 || ^0.3"
%global react_socket_client_min_ver 0.3
%global react_socket_client_max_ver 1.0
# "react/stream": "0.4.*"
%global react_stream_min_ver 0.4.0
%global react_stream_max_ver 0.5.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       Asynchronous HTTP client library

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
Requires:      php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(evenement/evenement) <  %{evenement_max_ver}
BuildRequires: php-composer(evenement/evenement) >= %{evenement_min_ver}
BuildRequires: php-composer(guzzlehttp/psr7) <  %{guzzlehttp_psr7_max_ver}
BuildRequires: php-composer(guzzlehttp/psr7) >= %{guzzlehttp_psr7_min_ver}
BuildRequires: php-composer(react/dns) <  %{react_dns_max_ver}
BuildRequires: php-composer(react/dns) >= %{react_dns_min_ver}
BuildRequires: php-composer(react/event-loop) <  %{react_event_loop_max_ver}
BuildRequires: php-composer(react/event-loop) >= %{react_event_loop_min_ver}
BuildRequires: php-composer(react/promise) <  %{react_promise_max_ver}
BuildRequires: php-composer(react/promise) >= %{react_promise_min_ver}
BuildRequires: php-composer(react/socket-client) <  %{react_socket_client_max_ver}
BuildRequires: php-composer(react/socket-client) >= %{react_socket_client_min_ver}
BuildRequires: php-composer(react/stream) <  %{react_stream_max_ver}
BuildRequires: php-composer(react/stream) >= %{react_stream_min_ver}
## phpcompatinfo (computed from version 0.4.15)
BuildRequires: php-json
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
Requires:      php-composer(react/dns) <  %{react_dns_max_ver}
Requires:      php-composer(react/dns) >= %{react_dns_min_ver}
Requires:      php-composer(react/event-loop) <  %{react_event_loop_max_ver}
Requires:      php-composer(react/event-loop) >= %{react_event_loop_min_ver}
Requires:      php-composer(react/promise) <  %{react_promise_max_ver}
Requires:      php-composer(react/promise) >= %{react_promise_min_ver}
Requires:      php-composer(react/socket-client) <  %{react_socket_client_max_ver}
Requires:      php-composer(react/socket-client) >= %{react_socket_client_min_ver}
Requires:      php-composer(react/stream) <  %{react_stream_max_ver}
Requires:      php-composer(react/stream) >= %{react_stream_min_ver}
# phpcompatinfo (computed from version 0.4.15)
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.

Autoloader: %{phpdir}/React/HttpClient/autoload.php


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

\Fedora\Autoloader\Autoload::addPsr4('React\\HttpClient\\', __DIR__);

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/Evenement/autoload.php',
    '%{phpdir}/GuzzleHttp/Psr7/autoload.php',
    '%{phpdir}/React/Dns/autoload.php',
    '%{phpdir}/React/EventLoop/autoload.php',
    '%{phpdir}/React/Promise/autoload.php',
    '%{phpdir}/React/SocketClient/autoload.php',
    '%{phpdir}/React/Stream/autoload.php',
));
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}/React
cp -rp src %{buildroot}%{phpdir}/React/HttpClient


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require '%{buildroot}%{phpdir}/React/HttpClient/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('React\\Tests\\HttpClient\\', __DIR__.'/tests');
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
%{phpdir}/React/HttpClient/


%changelog
* Wed Jan 25 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.15-2
- Minor update to SCL tests (only php55 if rhel)

* Tue Jan 17 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.15-1
- Initial package
