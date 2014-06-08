#
# RPM spec file for php-Raven
#
# Copyright (c) 2013-2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve the changelog entries
#
%global github_owner    getsentry
%global github_name     raven-php
%global github_version  0.9.0
%global github_commit   1177f1c51110454f3a5bcca88aec3fa30e40e277

%global lib_name        Raven

# "php": ">=5.2.4"
%global php_min_ver     5.2.4
# "phpunit/phpunit": "3.7.*"
#     Note: Max version ignored on purpose
%global phpunit_min_ver 3.7.0

# Build using "--without tests" to disable tests
%global with_tests      %{?_without_tests:0}%{!?_without_tests:1}

Name:          php-%{lib_name}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       A PHP client for Sentry

Group:         Development/Libraries
License:       BSD
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_commit}.tar.gz
# Fix Raven_Tests_ClientTest::testGetAuthHeader
# https://github.com/getsentry/raven-php/pull/155
Patch0:        %{url}/pull/155.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
%if %{with_tests}
# For tests: composer.json
BuildRequires: php(language)       >= %{php_min_ver}
BuildRequires: php-phpunit-PHPUnit >= %{phpunit_min_ver}
# For tests: phpcompatinfo (computed from version 0.9.0)
BuildRequires: php-curl
BuildRequires: php-date
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-session
BuildRequires: php-sockets
BuildRequires: php-spl
BuildRequires: php-zlib
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 0.9.0)
Requires:      php-curl
Requires:      php-date
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-session
Requires:      php-sockets
Requires:      php-spl
Requires:      php-zlib

Provides:      php-composer(raven/raven) = %{version}

%description
%{summary} (http://getsentry.com).


%prep
%setup -qn %{github_name}-%{github_commit}

%patch0 -p1

# Update autoloader require in bin and test bootstrap
sed "/require.*Autoloader/s:.*:require_once 'Raven/Autoloader.php';:" \
    -i bin/raven \
    -i test/bootstrap.php


%build
# Empty build section, nothing to build


%install
mkdir -p %{buildroot}%{_datadir}/php
cp -rp lib/* %{buildroot}%{_datadir}/php/

mkdir -p %{buildroot}%{_bindir}
install -pm 755 bin/raven %{buildroot}%{_bindir}/


%check
%if %{with_tests}
# Create PHPUnit config w/ colors turned off
sed 's/colors\s*=\s*"true"/colors="false"/' phpunit.xml.dist > phpunit.xml

%{_bindir}/phpunit --include-path ./lib:./test
%else
: Tests skipped
%endif


%files
%defattr(-,root,root,-)
%doc LICENSE AUTHORS *.rst composer.json
%{_datadir}/php/%{lib_name}
%{_bindir}/raven


%changelog
* Sun Jun  8 2014 Remi Collet <remi@fedoraproject.org> 0.9.0-1
- backport 0.9.0 for remi repo

* Sat Jun 07 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.9.0-1
- Updated to 0.9.0 (BZ #1104557)
- Added php-composer(raven/raven) virtual provide
- Added option to build without tests

* Mon Jun  2 2014 Remi Collet <remi@fedoraproject.org> 0.8.0-2.20131209gitdac9333
- merge rawhide changes

* Fri May 30 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.8.0-3.20140519git2351d97
- Updated to latest snapshot
- Removed max PHPUnit dependency

* Mon Dec 30 2013 Remi Collet <remi@fedoraproject.org> 0.8.0-2.20131209gitdac9333
- backport 0.8.0 for remi repo.

* Mon Dec 30 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.8.0-2.20131209gitdac9333
- Updated to latest snapshot

* Sun Dec 29 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.8.0-1
- Updated to 0.8.0 (BZ #1037543)
- Spec cleanup

* Thu Oct  3 2013 Remi Collet <remi@fedoraproject.org> 0.7.1-1
- backport 0.7.1 for remi repo.

* Wed Oct 02 2013 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.7.1-1
- Updated to 0.7.1

* Mon Jul  8 2013 Remi Collet <remi@fedoraproject.org> 0.6.1-1
- backport 0.6.1 for remi repo.

* Fri Jul 05 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.6.1-1
- Updated to 0.6.1 (BZ #981406)

* Fri Jun 07 2013 Remi Collet <remi@fedoraproject.org> 0.6.0-1
- backport 0.6.0 for remi repo.

* Fri Jun 07 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.6.0-1
- Updated to 0.6.0
- Removed tests sub-package

* Tue Feb 26 2013 Remi Collet <remi@fedoraproject.org> 0.5.1-1
- backport 0.5.1 for remi repo.

* Sun Feb 24 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.5.1-1
- Updated to upstream version 0.5.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 23 2013 Remi Collet <remi@fedoraproject.org> 0.4.0-2
- backport 0.4.0 for remi repo.

* Tue Jan 22 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.4.0-2
- Updated bin install from "install" to "install -pm 755"

* Mon Jan 21 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.4.0-1
- Updated to upstream version 0.4.0
- Fixed license
- Fixed build requires

* Fri Jan 18 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.3.1-1.20130117git60e91ac
- Initial package
