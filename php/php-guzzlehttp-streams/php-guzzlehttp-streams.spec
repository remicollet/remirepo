# remirepo spec file for php-guzzlehttp-streams, from Fedora:
#
# Fedora spec file for php-guzzlehttp-streams
#
# Copyright (c) 2014-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     guzzle
%global github_name      streams
%global github_version   3.0.0
%global github_commit    47aaa48e27dae43d39fc1cea0ccf0d84ac1a2ba5

%global composer_vendor  guzzlehttp
%global composer_project streams

# "php": ">=5.4.0"
%global php_min_ver      5.4.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       6%{?github_release}%{?dist}
Summary:       Provides a simple abstraction over streams of data

Group:         Development/Libraries
License:       MIT
URL:           http://docs.guzzlephp.org/en/guzzle4/streams.html
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

# Test suite start failing with upcoming 5.5.21RC1 / 5.6.5RC1
# https://github.com/guzzle/streams/issues/29
# https://github.com/guzzle/streams/commit/ad4c07ea55d02789a65ae75f6e4a9ee2cb9dab3f.patch
Patch0:        %{name}-ad4c07ea55d02789a65ae75f6e4a9ee2cb9dab3f.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: %{_bindir}/phpunit
BuildRequires: php(language) >= %{php_min_ver}
## phpcompatinfo (computed from version 3.0.0)
BuildRequires: php-hash
BuildRequires: php-spl
BuildRequires: php-zlib
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 3.0.0)
Requires:      php-hash
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.


%prep
%setup -qn %{github_name}-%{github_commit}

%patch0 -p1 -b .ad4c07ea55d02789a65ae75f6e4a9ee2cb9dab3f

: Create autoloader
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 *
 * Created by %{name}-%{version}-%{release}
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

$fedoraClassLoader->addPrefix('GuzzleHttp\\Stream\\', dirname(dirname(__DIR__)));

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p  %{buildroot}%{phpdir}/GuzzleHttp/Stream
cp -pr src/* %{buildroot}%{phpdir}/GuzzleHttp/Stream/


%check
%if %{with_tests}
%{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}%{phpdir}/GuzzleHttp/Stream/autoload.php
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
%dir %{phpdir}/GuzzleHttp
     %{phpdir}/GuzzleHttp/Stream


%changelog
* Tue Sep 22 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.0.0-6
- Minor cleanups

* Sun Jun 28 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.0.0-5
- Autoloader updates

* Fri Jun 12 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.0.0-3
- Use new $fedoraClassLoader concept in autoloader

* Mon Jun 01 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.0.0-2
- Added autoloader

* Sun Feb 08 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.0.0-1
- Updated to 3.0.0 (BZ #1131103)

* Thu Jan 22 2015 Remi Collet <remi@fedoraproject.org> - 1.5.1-3
- add upstream patch for test suite against latest PHP
  see https://github.com/guzzle/streams/issues/29, thank Koschei

* Tue Aug 26 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.5.1-2
- Updated URL and description per upstream
- Fix test suite when previous version installed

* Sun Aug 17 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.5.1-1
- Updated to 1.5.1 (BZ #1128102)

* Fri Jun 06 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.4.0-1
- Updated to 1.4.0 (BZ #1124227)
- Added option to build without tests ("--without tests")
- Added %%license usage

* Fri Jun 06 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.0-2
- Updated URL
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide

* Fri May 23 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.0-1
- Initial package
