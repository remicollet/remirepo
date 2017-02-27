# remirepo spec file for php-paragonie-random-compat, from
#
# Fedora spec file for php-paragonie-random-compat
#
# Copyright (c) 2015-2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     paragonie
%global github_name      random_compat
%global github_version   2.0.5
%global github_commit    411e7526015651c64887eb0bfe5d56f528a7c7e1
%global github_short     %(c=%{github_commit}; echo ${c:0:7})

%global composer_vendor  paragonie
%global composer_project random_compat

# "php": ">=5.2.0"
%global php_min_ver 5.2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-random-compat
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       PHP 5.x polyfill for random_bytes() and random_int() from PHP 7

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}

# GitHub export does not include tests.
# Run makesrc.sh to create full source.
Source0:       %{name}-%{version}-%{github_short}.tgz
Source1:       makesrc.sh

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
## phpcompatinfo (computed from version 2.0.4)
BuildRequires: php-pcre
BuildRequires: php-zlib
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 2.0.4)
Requires:      php-pcre
# Weak dependencies
%if 0%{?fedora} >= 21
Suggests:      php-mbstring
Suggests:      php-openssl
Suggests:      php-pecl(libsodium)
%endif

# php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}
Provides:      php-%{composer_vendor}-%{composer_project} = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.

Autoloader: %{phpdir}/random_compat/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Autoloader compat
ln -s random.php lib/autoload.php


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}/random_compat
cp -rp lib/* %{buildroot}%{phpdir}/random_compat/


%check
%if %{with_tests}
BOOTSTRAP=%{buildroot}%{phpdir}/random_compat/autoload.php

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
%{phpdir}/random_compat


%changelog
* Mon Feb 27 2017 Remi Collet <remi@remirepo.net> - 2.0.5-1
- update to 2.0.5

* Thu Dec 29 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.0.4-1
- Updated to 2.0.4 (RHBZ #1385987)
- Run upstream tests with SCLs if they are available

* Mon Apr 04 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.4.1-1
- Updated to 1.4.1 (RHBZ #1318836)

* Sat Mar 12 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.2-1
- Updated to 1.2.2 (RHBZ #1317102)

* Sat Mar 12 2016 Remi Collet <remi@remirepo.net> - 1.2.2-1
- update to 1.2.2

* Fri Mar 11 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.1-1
- Updated to 1.2.1 (RHBZ #1296738)

* Thu Mar  3 2016 Remi Collet <remi@remirepo.net> - 1.2.1-1
- update to 1.2.1
- sources from git snapshot ro retrive tests

* Fri Jan  8 2016 Remi Collet <remi@remirepo.net> - 1.1.5-1
- update to 1.1.5

* Sun Jan 03 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.4-1
- Updated to 1.1.4 (RHBZ #1290629)

* Thu Dec  3 2015 Remi Collet <remi@remirepo.net> - 1.1.0-2
- backport for remi repository
- run test suite with both php 5 and 7 when available

* Tue Dec 01 2015 Shawn Iwinski <shawn@iwin.ski> - 1.1.0-2
- Renamed from "php-paragonie-random_compat" ("_" => "-")
- Removed php-mcrypt suggest
- Added php-pecl(libsodium) suggest

* Wed Nov 25 2015 Shawn Iwinski <shawn@iwin.ski> - 1.1.0-1
- Initial package
