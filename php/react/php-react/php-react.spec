#
# Fedora spec file for php-react
#
# Copyright (c) 2017 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     reactphp
%global github_name      react
%global github_version   0.4.2
%global github_commit    457b6b8a16a37c11278cac0870d6d2ff911c5765

%global composer_vendor  react
%global composer_project react

# "php": ">= 5.4.0"
%global php_min_ver 5.4.0
# "react/cache": "0.4.*"
%global react_cache_min_ver 0.4.0
%global react_cache_max_ver 0.5.0
# "react/child-process": "0.4.*"
%global react_child_process_min_ver 0.4.0
%global react_child_process_max_ver 0.5.0
# "react/dns": "0.4.*"
%global react_dns_min_ver 0.4.0
%global react_dns_max_ver 0.5.0
# "react/event-loop": "0.4.*"
%global react_event_loop_min_ver 0.4.0
%global react_event_loop_max_ver 0.5.0
# "react/http-client": "0.4.*"
%global react_http_client_min_ver 0.4.0
%global react_http_client_max_ver 0.5.0
# "react/http": "0.4.*"
%global react_http_min_ver 0.4.0
%global react_http_max_ver 0.5.0
# "react/promise": "~2.1"
%global react_promise_min_ver 2.1
%global react_promise_max_ver 3.0
# "react/socket-client": "0.4.*"
%global react_socket_client_min_ver 0.4.0
%global react_socket_client_max_ver 0.5.0
# "react/socket": "0.4.*"
%global react_socket_min_ver 0.4.0
%global react_socket_max_ver 0.5.0
# "react/stream": "0.4.*"
%global react_stream_min_ver 0.4.0
%global react_stream_max_ver 0.5.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       Event-driven, non-blocking I/O with PHP

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: php-cli
## Minimal autoloader test
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(react/cache) <  %{react_cache_max_ver}
BuildRequires: php-composer(react/cache) >= %{react_cache_min_ver}
BuildRequires: php-composer(react/child-process) <  %{react_child_process_max_ver}
BuildRequires: php-composer(react/child-process) >= %{react_child_process_min_ver}
BuildRequires: php-composer(react/dns) <  %{react_dns_max_ver}
BuildRequires: php-composer(react/dns) >= %{react_dns_min_ver}
BuildRequires: php-composer(react/event-loop) <  %{react_event_loop_max_ver}
BuildRequires: php-composer(react/event-loop) >= %{react_event_loop_min_ver}
BuildRequires: php-composer(react/http-client) <  %{react_http_client_max_ver}
BuildRequires: php-composer(react/http-client) >= %{react_http_client_min_ver}
BuildRequires: php-composer(react/http) <  %{react_http_max_ver}
BuildRequires: php-composer(react/http) >= %{react_http_min_ver}
BuildRequires: php-composer(react/promise) <  %{react_promise_max_ver}
BuildRequires: php-composer(react/promise) >= %{react_promise_min_ver}
BuildRequires: php-composer(react/socket-client) <  %{react_socket_client_max_ver}
BuildRequires: php-composer(react/socket-client) >= %{react_socket_client_min_ver}
BuildRequires: php-composer(react/socket) <  %{react_socket_max_ver}
BuildRequires: php-composer(react/socket) >= %{react_socket_min_ver}
BuildRequires: php-composer(react/stream) <  %{react_stream_max_ver}
BuildRequires: php-composer(react/stream) >= %{react_stream_min_ver}
## phpcompatinfo (computed from version 0.4.2)
##     <none>
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(react/cache) <  %{react_cache_max_ver}
Requires:      php-composer(react/cache) >= %{react_cache_min_ver}
Requires:      php-composer(react/child-process) <  %{react_child_process_max_ver}
Requires:      php-composer(react/child-process) >= %{react_child_process_min_ver}
Requires:      php-composer(react/dns) <  %{react_dns_max_ver}
Requires:      php-composer(react/dns) >= %{react_dns_min_ver}
Requires:      php-composer(react/event-loop) <  %{react_event_loop_max_ver}
Requires:      php-composer(react/event-loop) >= %{react_event_loop_min_ver}
Requires:      php-composer(react/http-client) <  %{react_http_client_max_ver}
Requires:      php-composer(react/http-client) >= %{react_http_client_min_ver}
Requires:      php-composer(react/http) <  %{react_http_max_ver}
Requires:      php-composer(react/http) >= %{react_http_min_ver}
Requires:      php-composer(react/promise) <  %{react_promise_max_ver}
Requires:      php-composer(react/promise) >= %{react_promise_min_ver}
Requires:      php-composer(react/socket-client) <  %{react_socket_client_max_ver}
Requires:      php-composer(react/socket-client) >= %{react_socket_client_min_ver}
Requires:      php-composer(react/socket) <  %{react_socket_max_ver}
Requires:      php-composer(react/socket) >= %{react_socket_min_ver}
Requires:      php-composer(react/stream) <  %{react_stream_max_ver}
Requires:      php-composer(react/stream) >= %{react_stream_min_ver}
# phpcompatinfo (computed from version 0.4.2)
#     <none>
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}"
Provides:      php-%{composer_vendor}-%{composer_project} = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.

Autoloader: %{phpdir}/React/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Update autoloader require in examples
sed '/require.*autoload\.php/s#.*#require "%{phpdir}/React/autoload.php";#' -i examples/*


%build
: Create autoloader
cat <<'AUTOLOAD' | tee autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 */
require_once '%{phpdir}/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/React/Cache/autoload.php',
    '%{phpdir}/React/ChildProcess/autoload.php',
    '%{phpdir}/React/Dns/autoload.php',
    '%{phpdir}/React/EventLoop/autoload.php',
    '%{phpdir}/React/Http/autoload.php',
    '%{phpdir}/React/HttpClient/autoload.php',
    '%{phpdir}/React/Promise/autoload.php',
    '%{phpdir}/React/Socket/autoload.php',
    '%{phpdir}/React/SocketClient/autoload.php',
    '%{phpdir}/React/Stream/autoload.php',
));
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}/React
cp -p autoload.php %{buildroot}%{phpdir}/React/


%check
%if %{with_tests}
: Minimal autoloader test
%{_bindir}/php -r 'require "%{buildroot}%{phpdir}/React/autoload.php";'
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc examples
%doc composer.json
%{phpdir}/React/autoload.php


%changelog
* Wed Jan 25 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.2-2
- Add missing php-cli BuildRequires

* Tue Jan 17 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.2-1
- Initial package
