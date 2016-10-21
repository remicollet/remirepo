#
# Fedora spec file for php-asm89-stack-cors
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     asm89
%global github_name      stack-cors
%global github_version   1.0.0
%global github_commit    3ae8ef219bb4c9a6caf857421719aa07fa7776cc

%global composer_vendor  asm89
%global composer_project stack-cors

# "php": ">=5.3.2"
%global php_min_ver 5.3.2
# "symfony/http-foundation": "~2.1|~3.0"
# "symfony/http-kernel": "~2.1|~3.0"
#     NOTE: Min version not 2.1 because autoloader required
%global symfony_min_ver %{?el6:2.3.31}%{!?el6:2.7.1}
%global symfony_max_ver 4.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Cross-origin resource sharing library and stack middleware

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

# Add LICENSE file
# https://github.com/asm89/stack-cors/pull/32
Patch0:        %{name}-pull-request-32-add-license-file.patch

BuildArch:     noarch
# Autoloader
BuildRequires: %{_bindir}/phpab
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(symfony/http-foundation) >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/http-kernel) >= %{symfony_min_ver}
## phpcompatinfo (computed from version 1.0.0)
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(symfony/http-foundation) >= %{symfony_min_ver}
Requires:      php-composer(symfony/http-foundation) <  %{symfony_max_ver}
Requires:      php-composer(symfony/http-kernel) >= %{symfony_min_ver}
Requires:      php-composer(symfony/http-kernel) <  %{symfony_max_ver}
# phpcompatinfo (computed from version 1.0.0)
#     <none>

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Library and middleware enabling cross-origin resource sharing for your
http-{foundation,kernel} using application. It attempts to implement the
W3C Candidate Recommendation [1] for cross-origin resource sharing.

Autoloader: %{phpdir}/Asm89/Stack/autoload-cors.php

[1] http://www.w3.org/TR/cors/


%prep
%setup -qn %{github_name}-%{github_commit}

: Remove executable bits from non-executable files
: https://github.com/asm89/stack-cors/pull/31
find . -type f -executable -name '*.php' -print0 | xargs -0 chmod a-x

: Add LICENSE file
: https://github.com/asm89/stack-cors/pull/32
%patch0 -p1


%build
: Create autoloader
%{_bindir}/phpab --output src/Asm89/Stack/autoload-cors.php src/

cat <<'AUTOLOAD' | tee -a src/Asm89/Stack/autoload-cors.php

// Required dependencies
require_once '%{phpdir}/Symfony/Component/HttpFoundation/autoload.php';
require_once '%{phpdir}/Symfony/Component/HttpKernel/autoload.php';
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
%{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}%{phpdir}/Asm89/Stack/autoload-cors.php
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%dir %{phpdir}/Asm89
%dir %{phpdir}/Asm89/Stack
     %{phpdir}/Asm89/Stack/autoload-cors.php
     %{phpdir}/Asm89/Stack/Cors.php
     %{phpdir}/Asm89/Stack/CorsService.php


%changelog
* Sun Oct 09 2016 Shawn Iwinski <shawn@iwin.ski> - 1.0.0-1
- Initial package
