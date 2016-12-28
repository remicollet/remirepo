# remirepo spec file for php-webmozart-assert, from
#
# Fedora spec file for php-webmozart-assert
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     webmozart
%global github_name      assert
%global github_version   1.2.0
%global github_commit    2db61e59ff05fe5126d152bd0655c9ea113e550f

%global composer_vendor  webmozart
%global composer_project assert

# "php": "^5.3.3 || ^7.0"
%global php_min_ver 5.3.3

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Assertions to validate method input/output with nice error messages

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
## phpcompatinfo (computed from version 1.2.0)
BuildRequires: php-ctype
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.2.0)
Requires:      php-ctype
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
This library contains efficient assertions to test the input and output of your
methods. With these assertions, you can greatly reduce the amount of coding
needed to write a safe implementation.

All assertions in the Assert class throw an \InvalidArgumentException if they
fail.

Autoloader: %{phpdir}/Webmozart/Assert/autoload.php


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

\Fedora\Autoloader\Autoload::addPsr4('Webmozart\\Assert\\', __DIR__);
AUTOLOAD


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}/Webmozart/Assert
cp -rp src/* %{buildroot}%{phpdir}/Webmozart/Assert/


%check
%if %{with_tests}
BOOTSTRAP=%{buildroot}%{phpdir}/Webmozart/Assert/autoload.php

: Upstream tests
%{_bindir}/phpunit --verbose --bootstrap $BOOTSTRAP

: Upstream tests with SCLs if available
SCL_RETURN_CODE=0
for SCL in php56 php70 php71; do
    if which $SCL; then
        $SCL %{_bindir}/phpunit --verbose --bootstrap $BOOTSTRAP || SCL_RETURN_CODE=1
    fi
done
exit $SCL_RETURN_CODE
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%dir %{phpdir}/Webmozart
     %{phpdir}/Webmozart/Assert


%changelog
* Tue Dec 27 2016 Shawn Iwinski <shawn@iwin.ski> - 1.2.0-1
- Update to 1.2.0 (RHBZ #1398043)
- Use php-composer(fedora/autoloader)
- Run upstream tests with SCLs if they are available

* Thu Oct  6 2016 Remi Collet <remi@remirepo.net> - 1.1.0-1
- backport for remi repo, add EL-5 stuff

* Wed Sep 28 2016 Shawn Iwinski <shawn@iwin.ski> - 1.1.0-1
- Initial package
