# remirepo spec file for php-react-child-process, from:
#
# Fedora spec file for php-react-child-process
#
# Copyright (c) 2017 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     reactphp
%global github_name      child-process
%global github_version   0.4.1
%global github_commit    3ab4f83c6f6c5862f7ca28d999a92d327472a671

%global composer_vendor  react
%global composer_project child-process

# "php": ">=5.4.0"
%global php_min_ver 5.4.0
# "evenement/evenement": "~2.0"
%global evenement_min_ver 2.0
%global evenement_max_ver 3.0
# "react/event-loop": "0.4.*"
%global react_event_loop_min_ver 0.4.0
%global react_event_loop_max_ver 0.5.0
# "react/stream": "~0.4.2"
%global react_stream_min_ver 0.4.2
%global react_stream_max_ver 0.5.0
# "sebastian/environment": "~1.0"
%if 0
%global sebastian_environment_min_ver 1.0
%global sebastian_environment_max_ver 2.0
%else
#     NOTE: Max version not 2.0 because:
#         - only v2 is provided in F24+
#         - upstream tests pass
#         - only a build (i.e. not runtime) dependency
%global sebastian_environment_min_ver 2.0
%global sebastian_environment_max_ver 3.0
%endif

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       Library for executing child processes

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
BuildRequires: php-composer(react/event-loop) <  %{react_event_loop_max_ver}
BuildRequires: php-composer(react/event-loop) >= %{react_event_loop_min_ver}
BuildRequires: php-composer(react/stream) <  %{react_stream_max_ver}
BuildRequires: php-composer(react/stream) >= %{react_stream_min_ver}
BuildRequires: php-composer(sebastian/environment) <  %{sebastian_environment_max_ver}
BuildRequires: php-composer(sebastian/environment) >= %{sebastian_environment_min_ver}
## phpcompatinfo (computed from version 0.4.1)
BuildRequires: php-pcntl
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
Requires:      php-composer(react/stream) <  %{react_stream_max_ver}
Requires:      php-composer(react/stream) >= %{react_stream_min_ver}
# phpcompatinfo (computed from version 0.4.1)
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.

Autoloader: %{phpdir}/React/ChildProcess/autoload.php


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

\Fedora\Autoloader\Autoload::addPsr4('React\\ChildProcess\\', __DIR__);

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/Evenement/autoload.php',
    '%{phpdir}/React/EventLoop/autoload.php',
    '%{phpdir}/React/Stream/autoload.php',
));
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}/React
cp -rp src %{buildroot}%{phpdir}/React/ChildProcess


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require '%{buildroot}%{phpdir}/React/ChildProcess/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('React\\Tests\\ChildProcess\\', __DIR__.'/tests');

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/SebastianBergmann/Environment/autoload.php',
));
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
%{phpdir}/React/ChildProcess


%changelog
* Wed Jan 25 2017 Remi Collet <remi@remirepo.net> - 0.4.1-2
- backport for remi repo

* Tue Jan 24 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.1-2
- Retrict sebastian/environment dependency to one major version
- Minor update to SCL tests (only php55 if rhel)

* Tue Jan 17 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.1-1
- Initial package
