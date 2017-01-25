#
# Fedora spec file for php-clue-block-react
#
# Copyright (c) 2017 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     clue
%global github_name      php-block-react
%global github_version   1.1.0
%global github_commit    ed70f8d497dd265e30bc7dd19cf86b2e149b1ecf

%global composer_vendor  clue
%global composer_project block-react

# "php": ">=5.3"
%global php_min_ver 5.3
# "react/event-loop": "0.4.*|0.3.*"
%global react_event_loop_min_ver 0.3
%global react_event_loop_max_ver 0.5
# "react/promise-timer": "~1.0"
%global react_promise_timer_min_ver 1.0
%global react_promise_timer_max_ver 2.0
# "react/promise": "~2.1|~1.2"
#     NOTE: Min version not 1.2 to restrict to one major version
%global react_promise_min_ver 2.1
%global react_promise_max_ver 3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       Integrate async React PHP components into your blocking environment

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
BuildRequires: php-composer(react/event-loop) <  %{react_event_loop_max_ver}
BuildRequires: php-composer(react/event-loop) >= %{react_event_loop_min_ver}
BuildRequires: php-composer(react/promise-timer) <  %{react_promise_timer_max_ver}
BuildRequires: php-composer(react/promise-timer) >= %{react_promise_timer_min_ver}
BuildRequires: php-composer(react/promise) <  %{react_promise_max_ver}
BuildRequires: php-composer(react/promise) >= %{react_promise_min_ver}
## phpcompatinfo (computed from version 1.1.0)
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(react/event-loop) <  %{react_event_loop_max_ver}
Requires:      php-composer(react/event-loop) >= %{react_event_loop_min_ver}
Requires:      php-composer(react/promise-timer) <  %{react_promise_timer_max_ver}
Requires:      php-composer(react/promise-timer) >= %{react_promise_timer_min_ver}
Requires:      php-composer(react/promise) <  %{react_promise_max_ver}
Requires:      php-composer(react/promise) >= %{react_promise_min_ver}
# phpcompatinfo (computed from version 1.1.0)
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Lightweight library that eases integrating async components built for
React PHP [1] in a traditional, blocking environment.

Autoloader: %{phpdir}/Clue/React/Block/autoload.php

[1] http://reactphp.org/


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

\Fedora\Autoloader\Dependencies::required(array(
    __DIR__.'/functions.php',
    '%{phpdir}/React/EventLoop/autoload.php',
    '%{phpdir}/React/Promise/autoload.php',
    '%{phpdir}/React/Promise/Timer/autoload.php',
));
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}/Clue/React
cp -rp src %{buildroot}%{phpdir}/Clue/React/Block


%check
%if %{with_tests}
: Mock Composer autoloader
mkdir vendor
ln -s %{buildroot}%{phpdir}/Clue/React/Block/autoload.php vendor/autoload.php

: Upstream tests
%{_bindir}/phpunit --verbose

: Upstream tests with SCLs if available
SCL_RETURN_CODE=0
for SCL in %{?rhel:php54 php55} php56 php70 php71; do
    if which $SCL; then
        $SCL %{_bindir}/phpunit --verbose || SCL_RETURN_CODE=1
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
%dir %{phpdir}/Clue
%dir %{phpdir}/Clue/React
     %{phpdir}/Clue/React/Block


%changelog
* Fri Jan 20 2017 Shawn Iwinski <shawn@iwin.ski> - 1.1.0-2
- Add missing BuildRequires and Requires
- Retrict react/promise dependency to one major version
- Minor update to SCL tests (only php54 and php55 if rhel)

* Tue Jan 17 2017 Shawn Iwinski <shawn@iwin.ski> - 1.1.0-1
- Initial package
