#
# Fedora spec file for php-react-event-loop
#
# Copyright (c) 2017 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     reactphp
%global github_name      event-loop
%global github_version   0.4.2
%global github_commit    164799f73175e1c80bba92a220ea35df6ca371dd

%global composer_vendor  react
%global composer_project event-loop

# "php": ">=5.4.0"
%global php_min_ver 5.4.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       Event loop abstraction layer that libraries can use for evented I/O

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
## phpcompatinfo (computed from version 0.4.2)
BuildRequires: php-pcntl
BuildRequires: php-posix
BuildRequires: php-spl

## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 0.4.2)
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Event loop abstraction layer that libraries can use for evented I/O.

In order for async based libraries to be interoperable, they need to use
the same event loop. This component provides a common LoopInterface that
any library can target. This allows them to be used in the same loop, with
one single run call that is controlled by the user.

In addition to the interface there are some implementations provided:
* StreamSelectLoop: This is the only implementation which works out of the box
      with PHP. It does a simple select system call. It's not the most
      performant of loops, but still does the job quite well.
* LibEventLoop: This uses the libevent pecl extension. libevent itself supports
      a number of system-specific backends (epoll, kqueue).
* LibEvLoop: This uses the libev pecl extension (github). It supports the same
      backends as libevent.
* ExtEventLoop: This uses the event pecl extension. It supports the same
      backends as libevent.

All of the loops support these features:
* File descriptor polling
* One-off timers
* Periodic timers
* Deferred execution of callbacks

Autoloader: %{phpdir}/React/EventLoop/autoload.php


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

\Fedora\Autoloader\Autoload::addPsr4('React\\EventLoop\\', __DIR__);
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}/React
cp -rp src %{buildroot}%{phpdir}/React/EventLoop

find %{buildroot}%{phpdir}/React/EventLoop | sed 's#%{buildroot}##' | sort


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require '%{buildroot}%{phpdir}/React/EventLoop/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('React\\Tests\\EventLoop\\', __DIR__.'/tests');
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
%dir %{phpdir}/React
     %{phpdir}/React/EventLoop


%changelog
* Mon Jan 23 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.2-2
- Minor update to SCL tests (only php55 if rhel)

* Tue Jan 17 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.2-1
- Initial package
