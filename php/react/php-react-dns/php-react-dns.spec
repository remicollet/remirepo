#
# Fedora spec file for php-react-dns
#
# Copyright (c) 2017 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     reactphp
%global github_name      dns
%global github_version   0.4.3
%global github_commit    751b3129556e04944f164e3556a20ca6e201e459

%global composer_vendor  react
%global composer_project dns

# "php": ">= 5.3.0"
%global php_min_ver 5.3.0
# "react/cache": "~0.4.0|~0.3.0"
%global react_cache_min_ver 0.3.0
%global react_cache_max_ver 0.5.0
# "react/promise": "~2.1|~1.2"
#     NOTE: Min version not 1.2 to restrict to one major version
%global react_promise_min_ver 2.1
%global react_promise_max_ver 3.0
# "react/socket": "~0.4.0|~0.3.0"
%global react_socket_min_ver 0.3.0
%global react_socket_max_ver 0.5.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       3%{?github_release}%{?dist}
Summary:       Async DNS resolver

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
BuildRequires: php-composer(react/cache) <  %{react_cache_max_ver}
BuildRequires: php-composer(react/cache) >= %{react_cache_min_ver}
BuildRequires: php-composer(react/promise) <  %{react_promise_max_ver}
BuildRequires: php-composer(react/promise) >= %{react_promise_min_ver}
BuildRequires: php-composer(react/socket) <  %{react_socket_max_ver}
BuildRequires: php-composer(react/socket) >= %{react_socket_min_ver}
## phpcompatinfo (computed from version 0.4.3)
BuildRequires: php-date
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(react/cache) <  %{react_cache_max_ver}
Requires:      php-composer(react/cache) >= %{react_cache_min_ver}
Requires:      php-composer(react/promise) <  %{react_promise_max_ver}
Requires:      php-composer(react/promise) >= %{react_promise_min_ver}
Requires:      php-composer(react/socket) <  %{react_socket_max_ver}
Requires:      php-composer(react/socket) >= %{react_socket_min_ver}
# phpcompatinfo (computed from version 0.4.3)
Requires:      php-date
Requires:      php-pcre
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Async DNS resolver.

The main point of the DNS component is to provide async DNS resolution.
However, it is really a toolkit for working with DNS messages, and could
easily be used to create a DNS server.

Autoloader: %{phpdir}/React/Dns/autoload.php


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

\Fedora\Autoloader\Autoload::addPsr4('React\\Dns\\', __DIR__);

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/React/Cache/autoload.php',
    '%{phpdir}/React/Promise/autoload.php',
    '%{phpdir}/React/Socket/autoload.php',
));
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}/React
cp -rp src %{buildroot}%{phpdir}/React/Dns


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require '%{buildroot}%{phpdir}/React/Dns/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('React\\Tests\\Dns\\', __DIR__.'/tests');
BOOTSTRAP

: Skip test requiring network access
sed 's/function testResolveGoogleResolves/function SKIP_testResolveGoogleResolves/' \
    -i tests/FunctionalResolverTest.php

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
%{phpdir}/React/Dns


%changelog
* Wed Jan 25 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.3-3
- Skip test requiring network access

* Tue Jan 24 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.3-2
- Restrict react/promise dependency to one major version
- Minor update to SCL tests (only php54 and php55 if rhel)

* Tue Jan 17 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.3-1
- Initial package
