# remirepo spec file for php-Raven, from:
#
# Fedora spec file for php-Raven
#
# Copyright (c) 2013-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve the changelog entries
#
%global github_owner     getsentry
%global github_name      raven-php
%global github_version   0.13.0
%global github_commit    1d5be07afc001df98a3528d1f928eeb2241afce6

%global composer_vendor  raven
%global composer_project raven

%global lib_name         Raven

# "php": ">=5.2.4"
%global php_min_ver      5.2.4

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{lib_name}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}.1
Summary:       A PHP client for Sentry

Group:         Development/Libraries
License:       BSD
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Library version value check
BuildRequires: php-cli
# Tests
%if %{with_tests}
## composer.json
BuildRequires: %{_bindir}/phpunit
BuildRequires: php(language) >= %{php_min_ver}
## phpcompatinfo (computed from version 0.13.0)
BuildRequires: php-curl
BuildRequires: php-date
BuildRequires: php-hash
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-session
BuildRequires: php-spl
BuildRequires: php-zlib
%endif

# use path as ca-certificates doesn't exists on EL-5
Requires:      /etc/pki/tls/cert.pem
# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 0.13.0)
Requires:      php-curl
Requires:      php-date
Requires:      php-hash
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-session
Requires:      php-spl
Requires:      php-zlib

# Standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming
Provides:      php-%{composer_vendor}-%{composer_project} = %{version}-%{release}
Provides:      php-%{composer_project} = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary} (http://getsentry.com).


%prep
%setup -qn %{github_name}-%{github_commit}

: Remove bundled cert
rm -rf lib/Raven/data
sed "/return.*cacert\.pem/s#.*#        return '%{_sysconfdir}/pki/tls/cert.pem';#" \
    -i lib/Raven/Client.php

: Create autoloader
cat <<'AUTOLOAD' | tee lib/Raven/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 *
 * Created by %{name}-%{version}-%{release}
 */

require_once dirname(__FILE__) . '/Autoloader.php';
Raven_Autoloader::register();
AUTOLOAD

: Update autoloader require in bin
sed "/require.*Autoloader/s:.*:require_once '%{phpdir}/Raven/Autoloader.php';:" \
    -i bin/raven


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}
cp -rp lib/* %{buildroot}%{phpdir}/

mkdir -p %{buildroot}%{_bindir}
install -pm 0755 bin/raven %{buildroot}%{_bindir}/


%check
: Library version value check
%{_bindir}/php -r 'require_once "%{buildroot}%{phpdir}/Raven/autoload.php";
    exit(version_compare("%{version}", Raven_Client::VERSION, "=") ? 0 : 1);'

%if %{with_tests}
: Update tests autoloader require
sed "/require.*Autoloader/s:.*:require_once '%{buildroot}%{phpdir}/Raven/Autoloader.php';:" \
    -i test/bootstrap.php

: Run tests
%{_bindir}/phpunit --verbose
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.rst
%doc AUTHORS
%doc CHANGES
%doc composer.json
%{phpdir}/%{lib_name}
%{_bindir}/raven


%changelog
* Fri Apr 15 2016 Remi Collet <remi@remirepo.net> - 0.13.0-1.1
- fix dep. on EL-5

* Sun Sep 20 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.13.0-1
- Updated to 0.13.0 (RHBZ #1261679)
- Always run library version value check

* Fri Aug 28 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.12.1-1
- Updated to 0.12.1 (RHBZ #1256982)
- Added standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming provides
- Added library version value check

* Sat Jun 27 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.12.0-1
- Updated to 0.12.0 (RHBZ #1224010)
- Added autoloader

* Sun Apr 12 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.11.0-1
- Updated to 0.11.0 (BZ #1205685)

* Thu Sep 11 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.10.0-1
- Updated to 0.10.0 (BZ #1138284)

* Sun Aug 31 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.9.1-1
- Updated to 0.9.1 (BZ #1134284)
- %%license usage

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
