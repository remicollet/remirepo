# remirepo spec file for php-react-stream, from:
#
# Fedora spec file for php-react-stream
#
# Copyright (c) 2017 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     reactphp
%global github_name      stream
%global github_version   0.4.6
%global github_commit    44dc7f51ea48624110136b535b9ba44fd7d0c1ee

%global composer_vendor  react
%global composer_project stream

# "php": ">=5.3.8"
%global php_min_ver 5.3.8
# "clue/stream-filter": "~1.2"
%global clue_stream_filter_min_ver 1.2
%global clue_stream_filter_max_ver 2.0
# "evenement/evenement": "^2.0|^1.0"
#     NOTE: Min version not 1.0 to restrict to one major version
%global evenement_min_ver 2.0
%global evenement_max_ver 3.0
# "react/event-loop": "^0.4" (suggest)
# "react/event-loop": "^0.4|^0.3" (require-dev)
%global react_event_loop_min_ver 0.4
%global react_event_loop_max_ver 1.0
# "react/promise": "^2.0" (suggest)
# "react/promise": "^2.0|^1.0" (require-dev)
%global react_promise_min_ver 2.0
%global react_promise_max_ver 3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Basic readable and writable stream interfaces that support piping

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
BuildRequires: php-composer(clue/stream-filter) <  %{clue_stream_filter_max_ver}
BuildRequires: php-composer(clue/stream-filter) >= %{clue_stream_filter_min_ver}
BuildRequires: php-composer(evenement/evenement) <  %{evenement_max_ver}
BuildRequires: php-composer(evenement/evenement) >= %{evenement_min_ver}
BuildRequires: php-composer(react/event-loop) <  %{react_event_loop_max_ver}
BuildRequires: php-composer(react/event-loop) >= %{react_event_loop_min_ver}
BuildRequires: php-composer(react/promise) <  %{react_promise_max_ver}
BuildRequires: php-composer(react/promise) >= %{react_promise_min_ver}
## phpcompatinfo (computed from version 0.4.6)
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(evenement/evenement) <  %{evenement_max_ver}
Requires:      php-composer(evenement/evenement) >= %{evenement_min_ver}
# phpcompatinfo (computed from version 0.4.6)
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Weak dependencies
%if 0%{?fedora} >= 21
Suggests:      php-composer(react/event-loop)
Suggests:      php-composer(react/promise)
%endif

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Basic readable and writable stream interfaces that support piping.

In order to make the event loop easier to use, this component introduces the
concept of streams. They are very similar to the streams found in PHP itself,
but have an interface more suited for async I/O.

Mainly it provides interfaces for readable and writable streams, plus a file
descriptor based implementation with an in-memory write buffer.

This component depends on événement, which is an implementation of the
EventEmitter.

Autoloader: %{phpdir}/React/Stream/autoload.php


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

\Fedora\Autoloader\Autoload::addPsr4('React\\Stream\\', __DIR__);

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/Evenement/autoload.php',
));

\Fedora\Autoloader\Dependencies::optional(array(
    '%{phpdir}/React/EventLoop/autoload.php',
    '%{phpdir}/React/Promise/autoload.php',
));
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}/React
cp -rp src %{buildroot}%{phpdir}/React/Stream


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require '%{buildroot}%{phpdir}/React/Stream/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('React\\Tests\\Stream\\', __DIR__.'/tests');

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/Clue/StreamFilter/autoload.php',
));
BOOTSTRAP

: Skip tests requiring stream_socket_server tcp://localhost:0
sed \
    -e 's/function testDoesNotWriteDataIfClientSideHasBeenClosed/function SKIP_testDoesNotWriteDataIfClientSideHasBeenClosed/' \
    -e 's/function testDoesNotWriteDataIfServerSideHasBeenClosed/function SKIP_testDoesNotWriteDataIfServerSideHasBeenClosed/' \
    -i tests/StreamIntegrationTest.php


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
%{phpdir}/React/Stream


%changelog
%changelog
* Thu Jan 26 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.6-1
- Update to 0.4.6 (RHBZ #1416595)

* Tue Jan 24 2017 Remi Collet <remi@remirepo.net> - 0.4.5-2
- backport for remi repo

* Tue Jan 24 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.5-2
- Retrict evenement/evenement dependency to one major version
- Minor update to SCL tests (only php54 and php55 if rhel)

* Tue Jan 17 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.5-1
- Initial package
