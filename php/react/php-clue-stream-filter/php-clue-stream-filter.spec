#
# Fedora spec file for php-clue-stream-filter
#
# Copyright (c) 2017 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     clue
%global github_name      php-stream-filter
%global github_version   1.3.0
%global github_commit    e3bf9415da163d9ad6701dccb407ed501ae69785

%global composer_vendor  clue
%global composer_project stream-filter

# "php": ">=5.3"
%global php_min_ver 5.3

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       A simple and modern approach to stream filtering in PHP

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
## phpcompatinfo (computed from version 1.3.0)
BuildRequires: php-reflection
BuildRequires: php-spl
BuildRequires: php-zlib
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.3.0)
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.

Autoloader: %{phpdir}/Clue/StreamFilter/autoload.php


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

\Fedora\Autoloader\Autoload::addPsr4('Clue\\StreamFilter\\', __DIR__);

\Fedora\Autoloader\Dependencies::required(array(
    __DIR__.'/functions.php',
));
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}/Clue
cp -rp src %{buildroot}%{phpdir}/Clue/StreamFilter


%check
%if %{with_tests}
BOOTSTRAP=%{buildroot}%{phpdir}/Clue/StreamFilter/autoload.php

: Upstream tests
%{_bindir}/phpunit --verbose --bootstrap $BOOTSTRAP

: Upstream tests with SCLs if available
SCL_RETURN_CODE=0
for SCL in %{?rhel:php54 php55} php56 php70 php71; do
    if which $SCL; then
        $SCL %{_bindir}/phpunit --verbose --bootstrap $BOOTSTRAP || SCL_RETURN_CODE=1
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
     %{phpdir}/Clue/StreamFilter


%changelog
* Mon Jan 23 2017 Shawn Iwinski <shawn@iwin.ski> - 1.3.0-2
- Minor update to SCL tests (only php54 and php55 if rhel)

* Tue Jan 17 2017 Shawn Iwinski <shawn@iwin.ski> - 1.3.0-1
- Initial package
