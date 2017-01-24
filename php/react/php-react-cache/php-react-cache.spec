#
# Fedora spec file for php-react-cache
#
# Copyright (c) 2017 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     reactphp
%global github_name      cache
%global github_version   0.4.1
%global github_commit    558f614891341b1d817a8cdf9a358948ec49638f

%global composer_vendor  react
%global composer_project cache

# "php": ">=5.3.0",
%global php_min_ver 5.3.0
# "react/promise": "~2.0|~1.1"
#     NOTE: Min version not 1.1 to restrict to one major version
%global react_promise_min_ver 2.0
%global react_promise_max_ver 3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       Async caching

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
BuildRequires: php-composer(react/promise) <  %{react_promise_max_ver}
BuildRequires: php-composer(react/promise) >= %{react_promise_min_ver}
## phpcompatinfo (computed from version 0.4.1)
#     <none>
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(react/promise) <  %{react_promise_max_ver}
Requires:      php-composer(react/promise) >= %{react_promise_min_ver}
# phpcompatinfo (computed from version 0.4.1)
#     <none>
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Promised cache interface.

The cache component provides a promise-based cache interface and an in-memory
ArrayCache implementation of that. This allows consumers to type hint against
the interface and third parties to provide alternate implementations.

Autoloader: %{phpdir}/React/Cache/autoload.php


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

\Fedora\Autoloader\Autoload::addPsr4('React\\Cache\\', __DIR__);

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/React/Promise/autoload.php',
));
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}/React
cp -rp src %{buildroot}%{phpdir}/React/Cache


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require '%{buildroot}%{phpdir}/React/Cache/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('React\\Tests\\Cache\\', __DIR__.'/tests');
BOOTSTRAP

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
%{phpdir}/React/Cache


%changelog
* Mon Jan 23 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.1-2
- Retrict react/promise dependency to one major version
- Minor update to SCL tests (only php54 and php55 if rhel)

* Tue Jan 17 2017 Shawn Iwinski <shawn@iwin.ski> - 0.4.1-1
- Initial package
