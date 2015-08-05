# remirepo spec file for php-symfony-psr-http-message-bridge, from:
#
#
# Fedora spec file for php-symfony-psr-http-message-bridge
#
# Copyright (c) 2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     symfony
%global github_name      psr-http-message-bridge
%global github_version   0.2
%global github_commit    dc7e308e1dc2898a46776e2221a643cb08315453

%global composer_vendor  symfony
%global composer_project psr-http-message-bridge

# "php": ">=5.3.3",
%global php_min_ver 5.3.3
# "psr/http-message": "~1.0"
%global psr_http_message_min_ver 1.0
%global psr_http_message_max_ver 2.0
# "symfony/http-foundation": "~2.3|~3.0"
%global symfony_min_ver %{?el6:2.3.31}%{!?el6:2.7.3}
%global symfony_max_ver 4.0

%global with_zend_diactoros 0%{!?el6:1}

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       Symfony PSR HTTP message bridge

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
%if %{with_zend_diactoros}
BuildRequires: php-composer(zendframework/zend-diactoros)
%endif
BuildRequires: %{_bindir}/phpunit
## composer.json
BuildRequires: php(language)                         >= %{php_min_ver}
BuildRequires: php-composer(psr/http-message)        >= %{psr_http_message_min_ver}
BuildRequires: php-composer(symfony/http-foundation) >= %{symfony_min_ver}
## phpcompatinfo (computed from version 0.2)
BuildRequires: php-date
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                         >= %{php_min_ver}
Requires:      php-composer(psr/http-message)        >= %{psr_http_message_min_ver}
Requires:      php-composer(psr/http-message)        <  %{psr_http_message_max_ver}
Requires:      php-composer(symfony/http-foundation) >= %{symfony_min_ver}
Requires:      php-composer(symfony/http-foundation) <  %{symfony_max_ver}
# phpcompatinfo (computed from version 0.2)
Requires:      php-date
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Provides integration for PSR7.
%if %{with_zend_diactoros}
Optional:
* php-zendframework-zend-diactoros: To use the Zend Diactoros factory
%endif


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee autoload.php
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

$fedoraClassLoader->addPrefix('Symfony\\Bridge\\PsrHttpMessage\\', dirname(dirname(dirname(__DIR__))));

require_once '%{phpdir}/Psr/Http/Message/autoload.php';
require_once '%{phpdir}/Symfony/Component/HttpFoundation/autoload.php';
%if %{with_zend_diactoros}

if (file_exists('%{phpdir}/Zend/Diactoros/autoload.php')) {
    require_once '%{phpdir}/Zend/Diactoros/autoload.php';
}
%endif

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}/Symfony/Bridge/PsrHttpMessage
cp -rp *.php Factory Tests %{buildroot}%{phpdir}/Symfony/Bridge/PsrHttpMessage/


%check
%if %{with_tests}
: Run tests
%{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}%{phpdir}/Symfony/Bridge/PsrHttpMessage/autoload.php
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
%{phpdir}/Symfony/Bridge/PsrHttpMessage
%exclude %{phpdir}/Symfony/Bridge/PsrHttpMessage/Tests


%changelog
* Wed Aug  5 2015 Remi Collet <remi@remirepo.net> - 0.2-2
- backport for #remirepo

* Sun Aug 02 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.2-2
- Fixed dependency versions
- Added php-composer(zendframework/zend-diactoros) build dependency for tests
  (excluding el6)
- Autoloader update
- Fixed %%files

* Wed Jul 08 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.2-1
- Initial package
