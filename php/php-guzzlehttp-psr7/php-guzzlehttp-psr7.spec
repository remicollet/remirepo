# remirepo spec file for php-guzzlehttp-psr7, from
#
# Fedora spec file for php-guzzlehttp-psr7
#
# Copyright (c) 2015-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     guzzle
%global github_name      psr7
%global github_version   1.3.0
%global github_commit    31382fef2889136415751badebbd1cb022a4ed72

%global composer_vendor  guzzlehttp
%global composer_project psr7

# "php": ">=5.4.0"
%global php_min_ver 5.4.0
# "psr/http-message": "~1.0"
%global psr_http_message_min_ver 1.0
%global psr_http_message_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       PSR-7 message implementation

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language)                  >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(psr/http-message) >= %{psr_http_message_min_ver}
## phpcompatinfo (computed from version 1.3.0)
BuildRequires: php-hash
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
BuildRequires: php-zlib
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                  >= %{php_min_ver}
Requires:      php-composer(psr/http-message) >= %{psr_http_message_min_ver}
Requires:      php-composer(psr/http-message) <  %{psr_http_message_max_ver}
# phpcompatinfo (computed from version 1.3.0)
Requires:      php-hash
Requires:      php-pcre
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}
Provides:      php-composer(psr/http-message-implementation)        = 1.0

%description
PSR-7 message implementation, several stream decorators, and some helpful
functionality like query string parsing.


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee src/autoload.php
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

$fedoraClassLoader->addPrefix('GuzzleHttp\\Psr7\\', dirname(dirname(__DIR__)));

require_once __DIR__ . '/functions_include.php';
require_once '%{phpdir}/Psr/Http/Message/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}/GuzzleHttp/Psr7
cp -rp src/* %{buildroot}%{phpdir}/GuzzleHttp/Psr7/


%check
%if %{with_tests}
sed "s#require.*autoload.*#require '%{buildroot}%{phpdir}/GuzzleHttp/Psr7/autoload.php';#" \
    -i tests/bootstrap.php

%{_bindir}/phpunit --verbose

if which php70; then
   php70 %{_bindir}/phpunit --verbose
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
%doc *.md
%doc composer.json
%dir %{phpdir}/GuzzleHttp
     %{phpdir}/GuzzleHttp/Psr7


%changelog
* Sun May 29 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.0-1
- Updated to 1.3.0 (RHBZ #1326975)

* Fri Mar 11 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.3-1
- Updated to 1.2.3 (RHBZ #1301276)

* Wed Nov 04 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.1-1
- Updated to 1.2.1 (RHBZ #1277467)

* Sun Aug 16 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.0-1
- Updated to 1.2.0 (RHBZ #1253997)
- Updated autoloader to load dependencies after self registration

* Mon Jul 20 2015 Remi Collet <remi@remirepo.net> - 1.1.0-3
- add EL-5 stuff, backport for #remirepo

* Sun Jul 19 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.0-3
- Use full paths in autoloader

* Wed Jul 08 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.0-2
- Add autoloader dependencies
- Modify autoloader

* Mon Jul 06 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.0-1
- Initial package
