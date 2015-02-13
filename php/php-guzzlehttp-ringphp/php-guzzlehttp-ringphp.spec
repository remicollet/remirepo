#
# RPM spec file for php-guzzlehttp-ringphp
#
# Copyright (c) 2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     guzzle
%global github_name      RingPHP
%global github_version   1.0.5
%global github_commit    a903f51b692427318bc813217c0e6505287e79a4

%global composer_vendor  guzzlehttp
%global composer_project ringphp

# "php": ">=5.4.0"
%global php_min_ver      5.4.0
# "guzzlehttp/streams": "~3.0"
%global streams_min_ver  3.0
%global streams_max_ver  4.0
# "react/promise": "~2.0"
%global promise_min_ver  2.0
%global promise_max_ver  3.0

# Build using "--without tests" to disable tests
%global with_tests %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:     %global phpdir     %{_datadir}/php}
%{!?__phpunit:  %global __phpunit  %{_bindir}/phpunit}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Simple handler system used to power clients and servers in PHP

Group:         Development/Libraries
License:       MIT
URL:           http://ringphp.readthedocs.org
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
%if %{with_tests}
BuildRequires: nodejs
BuildRequires: php-phpunit-PHPUnit
# composer.json
BuildRequires: php(language)                    >= %{php_min_ver}
BuildRequires: php-composer(guzzlehttp/streams) >= %{streams_min_ver}
BuildRequires: php-composer(guzzlehttp/streams) <  %{streams_max_ver}
BuildRequires: php-composer(react/promise)      >= %{promise_min_ver}
BuildRequires: php-composer(react/promise)      <  %{promise_max_ver}
BuildRequires: php-curl
# phpcompatinfo (computed from version 1.0.5)
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
BuildRequires: php-zlib
%endif

# composer.json
Requires:      php(language)                    >= %{php_min_ver}
Requires:      php-composer(guzzlehttp/streams) >= %{streams_min_ver}
Requires:      php-composer(guzzlehttp/streams) <  %{streams_max_ver}
Requires:      php-composer(react/promise)      >= %{promise_min_ver}
Requires:      php-composer(react/promise)      <  %{promise_max_ver}
# composer.json: optional
Requires:      php-curl
# phpcompatinfo (computed from version 1.0.5)
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Provides low level APIs used to power HTTP clients and servers through a simple,
PHP callable that accepts a request hash and returns a future response hash.
RingPHP supports both synchronous and asynchronous workflows by utilizing both
futures and promises [1].

RingPHP is inspired by Clojure's Ring [2], but has been modified to accommodate
clients and servers for both blocking and non-blocking requests.

[1] https://github.com/reactphp/promise
[2] https://github.com/ring-clojure/ring


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -pm 0755 %{buildroot}%{phpdir}/GuzzleHttp/Ring
cp -rp src/* %{buildroot}%{phpdir}/GuzzleHttp/Ring/


%check
%if %{with_tests}
# Create autoloader
mkdir vendor
cat > vendor/autoload.php <<'AUTOLOAD'
<?php

spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', $class) . '.php';

    if (!@include_once $src) {
        $psr4_class = str_replace('GuzzleHttp\\Tests\\Ring\\', '', $class);
        $psr4_src = str_replace('\\', '/', $psr4_class) . '.php';

        @include_once $psr4_src;
    }
});

require_once '%{phpdir}/React/Promise/functions.php';
AUTOLOAD

%{__phpunit} --include-path %{buildroot}%{phpdir}:./tests
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.rst *.md composer.json
%{phpdir}/GuzzleHttp/Ring


%changelog
* Fri Feb 13 2015 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- backport for remi repository

* Sun Dec 28 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.5-1
- Updated to 1.0.5

* Thu Nov 13 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.3-1
- Updated to 1.0.3
- Removed color turn off and default timezone for phpunit

* Mon Oct 27 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.1-1
- Initial package
