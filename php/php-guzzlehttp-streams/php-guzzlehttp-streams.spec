#
# RPM spec file for php-guzzlehttp-streams
#
# Copyright (c) 2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     guzzle
%global github_name      streams
%global github_version   1.5.1
%global github_commit    fb0d1ee29987c2bdc59867bffaade6fc88c2675f

%global composer_vendor  guzzlehttp
%global composer_project streams

# "php": ">=5.4.0"
%global php_min_ver      5.4.0

# Build using "--without tests" to disable tests
%global with_tests       %{?_without_tests:0}%{!?_without_tests:1}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Provides a simple abstraction over streams of data

Group:         Development/Libraries
License:       MIT
URL:           http://docs.guzzlephp.org/en/latest/streams.html
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
%if %{with_tests}
# For tests: composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-phpunit-PHPUnit
# For tests: phpcompatinfo (computed from version 1.5.1)
BuildRequires: php-hash
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.5.1)
Requires:      php-hash
Requires:      php-spl

Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Provides a simple abstraction over streams of data.

This library is used in Guzzle and is an implementation of the proposed
PSR-7 stream interface [1].

[1] https://github.com/php-fig/fig-standards/blob/master/proposed/http-message.md#34-psrhttpstreaminterface


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing required


%install
mkdir -pm 0755 %{buildroot}%{_datadir}/php/GuzzleHttp/Stream
cp -pr src/* %{buildroot}%{_datadir}/php/GuzzleHttp/Stream/


%check
%if %{with_tests}
# Create autoloader
mkdir vendor
cat > vendor/autoload.php <<'AUTOLOAD'
<?php

require_once __DIR__ . '/../src/functions.php';

spl_autoload_register(function ($class) {
    $src = str_replace(array('\\', '_'), '/', $class).'.php';
    if (!@include_once $src) {
        $psr4_class = preg_replace('#^GuzzleHttp\\\Stream\\\?#', '', $class);
        $psr4_src = str_replace(array('\\', '_'), '/', $psr4_class).'.php';
        @include_once $psr4_src;
    }
});
AUTOLOAD

# Create PHPUnit config w/ colors turned off
sed 's/colors\s*=\s*"true"/colors="false"/' phpunit.xml.dist > phpunit.xml

%{_bindir}/phpunit --include-path="./src:./tests" -d date.timezone="UTC"
%else
: Tests skipped
%endif


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.rst composer.json
%dir %{_datadir}/php/GuzzleHttp
     %{_datadir}/php/GuzzleHttp/Stream


%changelog
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
