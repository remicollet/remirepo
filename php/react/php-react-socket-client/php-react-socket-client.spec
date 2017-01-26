# remirepo spec file for php-react-socket-client, from:
#
# Fedora spec file for php-react-socket-client
#
# Copyright (c) 2017 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     reactphp
%global github_name      socket-client
%global github_version   0.4.6
%global github_commit    49e730523b73d912e56f7a41f53ed3fc083ae167

%global composer_vendor  react
%global composer_project socket-client

# "php": ">= 5.4.0"
%global php_min_ver 5.4.0
# "react/dns": "0.4.*"
%global react_dns_min_ver 0.4.0
%global react_dns_max_ver 0.5.0
# "react/event-loop": "0.4.*"
%global react_event_loop_min_ver 0.4.0
%global react_event_loop_max_ver 0.5.0
# "react/promise": "~2.0"
%global react_promise_min_ver 2.0
%global react_promise_max_ver 3.0
# "react/stream": "0.4.*"
%global react_stream_min_ver 0.4.0
%global react_stream_max_ver 0.5.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       3%{?github_release}%{?dist}
Summary:       Async connector to open TCP/IP and SSL/TLS based connections

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
BuildRequires: php-composer(react/dns) <  %{react_dns_max_ver}
BuildRequires: php-composer(react/dns) >= %{react_dns_min_ver}
BuildRequires: php-composer(react/event-loop) <  %{react_event_loop_max_ver}
BuildRequires: php-composer(react/event-loop) >= %{react_event_loop_min_ver}
BuildRequires: php-composer(react/promise) <  %{react_promise_max_ver}
BuildRequires: php-composer(react/promise) >= %{react_promise_min_ver}
BuildRequires: php-composer(react/stream) <  %{react_stream_max_ver}
BuildRequires: php-composer(react/stream) >= %{react_stream_min_ver}
## phpcompatinfo (computed from version 0.4.6)
BuildRequires: php-filter
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(react/dns) <  %{react_dns_max_ver}
Requires:      php-composer(react/dns) >= %{react_dns_min_ver}
Requires:      php-composer(react/event-loop) <  %{react_event_loop_max_ver}
Requires:      php-composer(react/event-loop) >= %{react_event_loop_min_ver}
Requires:      php-composer(react/promise) <  %{react_promise_max_ver}
Requires:      php-composer(react/promise) >= %{react_promise_min_ver}
Requires:      php-composer(react/stream) <  %{react_stream_max_ver}
Requires:      php-composer(react/stream) >= %{react_stream_min_ver}
# phpcompatinfo (computed from version 0.4.6)
Requires:      php-filter
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.

Autoloader: %{phpdir}/React/SocketClient/autoload.php


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

\Fedora\Autoloader\Autoload::addPsr4('React\\SocketClient\\', __DIR__);

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/React/Dns/autoload.php',
    '%{phpdir}/React/EventLoop/autoload.php',
    '%{phpdir}/React/Promise/autoload.php',
    '%{phpdir}/React/Stream/autoload.php',
));
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}/React
cp -rp src %{buildroot}%{phpdir}/React/SocketClient


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require '%{buildroot}%{phpdir}/React/SocketClient/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('React\\Tests\\SocketClient\\', __DIR__.'/tests');
BOOTSTRAP

: Skip tests requiring network access
rm -f tests/IntegrationTest.php

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
%{phpdir}/React/SocketClient


%changelog
* Thu Jan 26 2017 Remi Collet <remi@remirepo.net> - 0.4.6-3
- backport

* Wed Jan 25 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.6-3
- Skip tests requiring network access

* Wed Jan 25 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.6-2
- Minor update to SCL tests (only php55 if rhel)

* Tue Jan 17 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.6-1
- Initial package
