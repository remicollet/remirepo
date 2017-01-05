# remirepo spec file for php-goutte, from:
#
# Fedora spec file for php-goutte
#
# Copyright (c) 2014-2017 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner    FriendsOfPHP
%global github_name     Goutte
%global github_version  3.2.1
%global github_commit   db5c28f4a010b4161d507d5304e28a7ebf211638

%global composer_vendor  fabpot
%global composer_project goutte

# "php": ">=5.5.0"
%global php_min_ver 5.5.0
# "guzzlehttp/guzzle": "^6.0"
%global guzzle_min_ver 6.0
%global guzzle_max_ver 7.0
# "symfony/browser-kit": "~2.1|~3.0"
# "symfony/css-selector": "~2.1|~3.0"
# "symfony/dom-crawler": "~2.1|~3.0"
#     NOTE: Min version not 2.1 because autoloader required
%global symfony_min_ver 2.7.1
%global symfony_max_ver 4.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-goutte
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       A simple PHP web scraper

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: php-composer(phpunit/phpunit)
## composer.json
BuildRequires: php(language)                      >= %{php_min_ver}
BuildRequires: php-composer(guzzlehttp/guzzle)    <  %{guzzle_max_ver}
BuildRequires: php-composer(guzzlehttp/guzzle)    >= %{guzzle_min_ver}
BuildRequires: php-composer(symfony/browser-kit)  >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/css-selector) >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/dom-crawler)  >= %{symfony_min_ver}
## phpcompatinfo (computed from version 3.2.0)
BuildRequires: php-reflection
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language)                      >= %{php_min_ver}
Requires:      php-composer(guzzlehttp/guzzle)    <  %{guzzle_max_ver}
Requires:      php-composer(guzzlehttp/guzzle)    >= %{guzzle_min_ver}
Requires:      php-composer(symfony/browser-kit)  <  %{symfony_max_ver}
Requires:      php-composer(symfony/browser-kit)  >= %{symfony_min_ver}
Requires:      php-composer(symfony/css-selector) <  %{symfony_max_ver}
Requires:      php-composer(symfony/css-selector) >= %{symfony_min_ver}
Requires:      php-composer(symfony/dom-crawler)  <  %{symfony_max_ver}
Requires:      php-composer(symfony/dom-crawler)  >= %{symfony_min_ver}
# phpcompatinfo (computed from version 3.2.0)
# <none>
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming
Provides:      php-%{composer_vendor}-%{composer_project} = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Goutte is a screen scraping and web crawling library for PHP.

Goutte provides a nice API to crawl websites and extract data
from the HTML/XML responses.

Autoloader: %{phpdir}/Goutte/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Create autoloader
cat <<'AUTOLOAD' | tee Goutte/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 */
require_once '%{phpdir}/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Goutte\\', __DIR__);

\Fedora\Autoloader\Dependencies::required([
    '%{phpdir}/GuzzleHttp6/autoload.php',
    '%{phpdir}/Symfony/Component/BrowserKit/autoload.php',
    '%{phpdir}/Symfony/Component/CssSelector/autoload.php',
    '%{phpdir}/Symfony/Component/DomCrawler/autoload.php',
]);
AUTOLOAD


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{phpdir}/Goutte
cp -p Goutte/{autoload,Client}.php %{buildroot}/%{phpdir}/Goutte/


%check
%if %{with_tests}
BOOTSTRAP=%{buildroot}/%{phpdir}/Goutte/autoload.php

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
%doc *.rst
%doc composer.json
%{phpdir}/Goutte


%changelog
* Thu Jan  5 2017 Remi Collet <remi@remirepo.net> - 3.2.1-1
- update to 3.2.1

* Fri Dec 30 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.2.0-1
- Updated to 3.2.0 (RHBZ #1395456)
- Use php-composer(fedora/autoloader)
- Run upstream tests with SCLs if they are available

* Sat Jul 09 2016 Shawn Iwinski <shawn@iwin.ski> - 3.1.2-1
- Update to 3.1.2 (RHBZ #1100719, 1289798)

* Sun Jun 12 2016 Shawn Iwinski <shawn@iwin.ski> - 2.0.4-1
- Update to 2.0.4

* Mon Mar 28 2016 Shawn Iwinski <shawn@iwin.ski> - 1.0.7-3
- Fixed Guzzle min version for autoloader
- Added "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" virtual provide
- Fixed \Goutte\Client::VERSION
- Added library version value and autoloader check

* Mon Nov 23 2015 Shawn Iwinski <shawn@iwin.ski> - 1.0.7-1
- Updated to 1.0.7
- Added spec file license header
- php-composer(*) dependencies
- Added php-composer(fabpot/goutte) virtual provide
- Added autoloader

* Sat May 17 2014 Remi Collet <remi@fedoraproject.org> 1.0.6-1
- backport 1.0.6 for remi repo

* Fri May 16 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.6-1
- Updated to 1.0.6

* Fri Feb 21 2014 Remi Collet <remi@fedoraproject.org> 1.0.5-1
- backport for remi repo

* Wed Feb 19 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.5-1
- Updated to 1.0.5
- Conditional release dist
- Fixed %%files

* Mon Jan 27 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.3-1.20140118gite83f8f9
- Initial package
