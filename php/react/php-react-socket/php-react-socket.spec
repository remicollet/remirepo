# remirepo spec file for php-react-socket, from:
#
# Fedora spec file for php-react-socket
#
# Copyright (c) 2017 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     reactphp
%global github_name      socket
%global github_version   0.4.5
%global github_commit    32385d71f84c4a26ea577cb91f1220decb440dce

%global composer_vendor  react
%global composer_project socket

# "php": ">= 5.3.0"
%global php_min_ver 5.3.0
# "clue/block-react": "^1.1"
%global clue_block_react_min_ver 1.1
%global clue_block_react_max_ver 2.0
# "evenement/evenement": "~2.0|~1.0"
#     NOTE: Min version not 1.0 to restrict to one major version
%global evenement_min_ver 2.0
%global evenement_max_ver 3.0
# "react/event-loop": "0.4.*|0.3.*"
%global react_event_loop_min_ver 0.3.0
%global react_event_loop_max_ver 0.5.0
# "react/promise": "^2.0 || ^1.1"
#     NOTE: Min version not 1.1 to restrict to one major version
%global react_promise_min_ver 2.0
%global react_promise_max_ver 3.0
# "react/socket-client": "^0.5.1"
%global react_socket_client_min_ver 0.5.1
%global react_socket_client_max_ver 1.0
# "react/stream": "^0.4.5"
%global react_stream_min_ver 0.4.5
%global react_stream_max_ver 1.0

# Allow bootstrapped build because:
# - Circular build dependency with "react/socket-client" and "react/dns"
# - Requires "react/socket-client" >= 0.5.1 but 0.4 will be packaged
%global bootstrap 1

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       Async, streaming plaintext TCP/IP and secure TLS socket server

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
BuildRequires: php-composer(clue/block-react) <  %{clue_block_react_max_ver}
BuildRequires: php-composer(clue/block-react) >= %{clue_block_react_min_ver}
BuildRequires: php-composer(evenement/evenement) <  %{evenement_max_ver}
BuildRequires: php-composer(evenement/evenement) >= %{evenement_min_ver}
BuildRequires: php-composer(react/event-loop) <  %{react_event_loop_max_ver}
BuildRequires: php-composer(react/event-loop) >= %{react_event_loop_min_ver}
BuildRequires: php-composer(react/promise) <  %{react_promise_max_ver}
BuildRequires: php-composer(react/promise) >= %{react_promise_min_ver}
BuildRequires: php-composer(react/stream) <  %{react_stream_max_ver}
BuildRequires: php-composer(react/stream) >= %{react_stream_min_ver}
%if !%{bootstrap}
BuildRequires: php-composer(react/socket-client) <  %{react_socket_client_max_ver}
BuildRequires: php-composer(react/socket-client) >= %{react_socket_client_min_ver}
%endif
## phpcompatinfo (computed from version 0.4.5)
BuildRequires: php-openssl
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(evenement/evenement) <  %{evenement_max_ver}
Requires:      php-composer(evenement/evenement) >= %{evenement_min_ver}
Requires:      php-composer(react/event-loop) <  %{react_event_loop_max_ver}
Requires:      php-composer(react/event-loop) >= %{react_event_loop_min_ver}
Requires:      php-composer(react/promise) <  %{react_promise_max_ver}
Requires:      php-composer(react/promise) >= %{react_promise_min_ver}
Requires:      php-composer(react/stream) <  %{react_stream_max_ver}
Requires:      php-composer(react/stream) >= %{react_stream_min_ver}
# phpcompatinfo (computed from version 0.4.5)
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Async, streaming plaintext TCP/IP and secure TLS socket server for React PHP.

The socket component provides a more usable interface for a socket-layer server
based on the EventLoop and Stream components.

Autoloader: %{phpdir}/React/Socket/autoload.php


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

\Fedora\Autoloader\Autoload::addPsr4('React\\Socket\\', __DIR__);

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/Evenement/autoload.php',
    '%{phpdir}/React/EventLoop/autoload.php',
    '%{phpdir}/React/Promise/autoload.php',
    '%{phpdir}/React/Stream/autoload.php',
));
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}/React
cp -rp src %{buildroot}%{phpdir}/React/Socket


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require '%{buildroot}%{phpdir}/React/Socket/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('React\\Tests\\Socket\\\\', __DIR__.'/tests');

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/Clue/React/Block/autoload.php',
%if !%{bootstrap}
    '%{phpdir}/React/SocketClient/autoload.php',
%endif
));
BOOTSTRAP

%if %{bootstrap}
: Skip tests requiring react/socket-client
rm -f \
    tests/FunctionalSecureServerTest.php \
    tests/FunctionalServerTest.php
%endif

: Upstream tests
%{_bindir}/phpunit --verbose --bootstrap bootstrap.php

: Upstream tests with SCLs if available
SCL_RETURN_CODE=0
for SCL in %{?rhel:php54 php55} php56 php70 php71; do
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
%{phpdir}/React/Socket


%changelog
* Wed Jan 25 2017 Remi Collet <remi@remirepo.net> - 0.4.5-2
- backport for remi repo

* Tue Jan 24 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.5-2
- Restrict evenement/evenement and react/promise dependencies to one major version
- Minor update to SCL tests (only php54 and php55 if rhel)

* Tue Jan 17 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.5-1
- Initial package
