# remirepo spec file for php-jsonlint, from:
#
# Fedora spec file for php-jsonlint
#
# Copyright (c) 2013-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#                         Remi Collet <remi@fedoraproject.org>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner   Seldaek
%global github_name    jsonlint
%global github_version 1.5.0
%global github_commit  19495c181d6d53a0a13414154e52817e3b504189

# "php": "^5.3 || ^7.0"
%global php_min_ver    5.3

# Build using "--without tests" to disable tests
%global with_tests     %{?_without_tests:0}%{!?_without_tests:1}

Name:          php-%{github_name}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       JSON Lint for PHP

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

# Autoloader
Source1:        %{name}-autoload.php

# Bin usage without Composer autoloader
Patch0:        %{name}-bin-without-composer-autoloader.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
%if %{with_tests}
# For tests: composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
# For tests: phpcompatinfo (computed from version 1.5.0)
BuildRequires: php-json
BuildRequires: php-pcre
# For autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.5.0)
Requires:      php-cli
Requires:      php-pcre
# For autoloader
Requires:      php-composer(fedora/autoloader)

Provides:      php-composer(seld/jsonlint) = %{version}


%description
%{summary}.

This library is a port of the JavaScript jsonlint
(https://github.com/zaach/jsonlint) library.

To use this library, you just have to add, in your project:
  require_once '%{_datadir}/php/Seld/JsonLint/autoload.php';


%prep
%setup -q -n %{github_name}-%{github_commit}

cp %{SOURCE1} src/Seld/JsonLint/autoload.php
%patch0 -p1


%build
# Empty build section, nothing to build


%install
# Lib
mkdir -p %{buildroot}%{_datadir}/php/Seld
cp -rp src/Seld/JsonLint %{buildroot}%{_datadir}/php/Seld/

# Bin
mkdir -p %{buildroot}%{_bindir}
install -pm 0755 bin/jsonlint %{buildroot}%{_bindir}/


%check
%if %{with_tests}

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap %{buildroot}%{_datadir}/php/Seld/JsonLint/autoload.php || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap %{buildroot}%{_datadir}/php/Seld/JsonLint/autoload.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit \
  --bootstrap %{buildroot}%{_datadir}/php/Seld/JsonLint/autoload.php \
  --verbose
# remirepo:2
fi
exit $ret
%else
: Tests skipped
%endif


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.mdown composer.json
%dir %{_datadir}/php/Seld
     %{_datadir}/php/Seld/JsonLint
%{_bindir}/jsonlint


%changelog
* Tue Nov 15 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- update to 1.5.0

* Mon Nov 14 2016 Remi Collet <remi@fedoraproject.org> - 1.4.1-3
- add patch for PHP 7.1
  open https://github.com/Seldaek/jsonlint/pull/37

* Fri Oct 21 2016 Remi Collet <remi@fedoraproject.org> - 1.4.1-2
- switch from symfony/class-loader to fedora/autoloader

* Thu Sep 15 2016 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- Updated to 1.4.1

* Thu Nov 26 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- Updated to 1.4.0
- run test suite with both PHP 5 and 7 when available

* Wed Oct 14 2015 Remi Collet <remi@fedoraproject.org> - 1.3.1-3
- add autoloader

* Mon Jan  5 2015 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Updated to 1.3.1

* Thu Sep 11 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.0-1
- Updated to 1.3.0 (BZ #1138911)

* Sat Aug 23 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.0-2
- %%license usage

* Wed Aug 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.0-1
- Updated to 1.2.0 (BZ #1124228)
- Added option to build without tests ("--without tests")
- Added bin

* Mon Jun  9 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-2
- fix FTBFS, include path during test
- upstream patch for latest PHPUnit
- provides php-composer(seld/jsonlint)

* Sat Nov 16 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.1.2-1
- backport 1.1.2 for remi repo

* Fri Nov 15 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.2-1
- Updated to upstream version 1.1.2
- php-common => php(language)

* Wed Feb 13 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.1.1-1
- backport 1.1.1 for remi repo

* Tue Feb 12 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.1-1
- Updated to upstream version 1.1.1
- Updates per new Fedora packaging guidelines for Git repos

* Wed Jan  9 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.1.0-1
- backport for remi repo

* Mon Jan 07 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-1
- Initial package
