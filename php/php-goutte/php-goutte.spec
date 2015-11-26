# remirepo spec file for php-goutte, from:
#
# Fedora spec file for php-goutte
#
# Copyright (c) 2014-2015 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner    FriendsOfPHP
%global github_name     Goutte
%global github_version  1.0.7
%global github_commit   794b196e76bdd37b5155cdecbad311f0a3b07625

%global composer_vendor  fabpot
%global composer_project goutte

# "php": ">=5.3.0"
%global php_min_ver     5.3.0
# "guzzle/http": "~3.1"
# "guzzle/plugin-history": "~3.1"
# "guzzle/plugin-mock": "~3.1"
%global guzzle_min_ver  3.1
%global guzzle_max_ver  4.0
# "symfony/browser-kit": "~2.1"
# "symfony/css-selector": "~2.1"
# "symfony/dom-crawler": "~2.1"
# "symfony/finder": "~2.1"
# "symfony/process": "~2.1"
#     NOTE: Min version not 2.1 because autoloader required
%global symfony_min_ver 2.7.1
%global symfony_max_ver 3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%global phpdir   %{_datadir}/php

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
BuildRequires: php(language)                       >= %{php_min_ver}
BuildRequires: php-composer(guzzle/http)           >= %{guzzle_min_ver}
BuildRequires: php-composer(guzzle/plugin-history) >= %{guzzle_min_ver}
BuildRequires: php-composer(guzzle/plugin-mock)    >= %{guzzle_min_ver}
BuildRequires: php-composer(symfony/browser-kit)   >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/css-selector)  >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/dom-crawler)   >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/finder)        >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/process)       >= %{symfony_min_ver}
BuildRequires: php-curl
## phpcompatinfo (computed from version 1.7.0)
# <none>
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                      >= %{php_min_ver}
Requires:      php-composer(guzzle/http)          >= %{guzzle_min_ver}
Requires:      php-composer(guzzle/http)          <  %{guzzle_max_ver}
Requires:      php-composer(symfony/browser-kit)  >= %{symfony_min_ver}
Requires:      php-composer(symfony/browser-kit)  <  %{symfony_max_ver}
Requires:      php-composer(symfony/css-selector) >= %{symfony_min_ver}
Requires:      php-composer(symfony/css-selector) <  %{symfony_max_ver}
Requires:      php-composer(symfony/dom-crawler)  >= %{symfony_min_ver}
Requires:      php-composer(symfony/dom-crawler)  <  %{symfony_max_ver}
Requires:      php-composer(symfony/finder)       >= %{symfony_min_ver}
Requires:      php-composer(symfony/finder)       <  %{symfony_max_ver}
Requires:      php-composer(symfony/process)      >= %{symfony_min_ver}
Requires:      php-composer(symfony/process)      <  %{symfony_max_ver}
Requires:      php-curl
# phpcompatinfo (computed from version 1.7.0)
# <none>

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Goutte is a screen scraping and web crawling library for PHP.

Goutte provides a nice API to crawl websites and extract data
from the HTML/XML responses.

Autoloader: %{phpdir}/Goutte/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee Goutte/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Goutte\\', dirname(__DIR__));

require_once '%{phpdir}/Guzzle/autoload.php';
require_once '%{phpdir}/Symfony/Component/BrowserKit/autoload.php';
require_once '%{phpdir}/Symfony/Component/CssSelector/autoload.php';
require_once '%{phpdir}/Symfony/Component/DomCrawler/autoload.php';
require_once '%{phpdir}/Symfony/Component/Finder/autoload.php';
require_once '%{phpdir}/Symfony/Component/Process/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{phpdir}/Goutte
cp -p Goutte/{autoload,Client}.php %{buildroot}/%{phpdir}/Goutte/


%check
%if %{with_tests}
%{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}/%{phpdir}/Goutte/autoload.php

if which php70; then
  php70 %{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}/%{phpdir}/Goutte/autoload.php
fi
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
