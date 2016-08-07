# remirepo spec file for php-psr-cache, from:
#
# Fedora spec file for php-psr-cache
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     php-fig
%global github_name      cache
%global github_version   1.0.1
%global github_commit    d11b50ad223250cf17b86e38383413f5a6764bf8

%global composer_vendor  psr
%global composer_project cache

# "php": ">=5.3.0"
%global php_min_ver 5.3.0

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:      php-%{composer_vendor}-%{composer_project}
Version:   %{github_version}
Release:   1%{?github_release}%{?dist}
Summary:   PSR Cache: Common interface for caching libraries

Group:     Development/Libraries
License:   MIT
URL:       https://github.com/%{github_owner}/%{github_name}
Source0:   %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
# For tests
BuildRequires: php-cli
BuildRequires: php-composer(symfony/class-loader)

# composer.json
Requires:  php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.0.0)
#     <none>
# Autoloader
Requires:  php-composer(symfony/class-loader)

# Composer
Provides:  php-composer(%{composer_vendor}/%{composer_project}) = %{version}


%description
This package holds all interfaces defined by PSR-6 [1].

Note that this is not a Cache implementation of its own. It is merely an
interface that describes a Cache implementation. See the specification for
more details.

Autoloader: %{phpdir}/Psr/Cache/autoload.php

[1] http://www.php-fig.org/psr/psr-6/


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

$fedoraClassLoader->addPrefix('Psr\\Cache\\', dirname(dirname(__DIR__)));

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing to build


%install
rm -rf   %{buildroot}
mkdir -p %{buildroot}%{phpdir}/Psr/Cache
cp -rp src/* %{buildroot}%{phpdir}/Psr/Cache/


%check
: Test autoloader
php -r '
require "%{buildroot}%{phpdir}/Psr/Cache/autoload.php";
exit (interface_exists("Psr\\Cache\\CacheItemInterface") ? 0 : 1);
'


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc *.md
%doc composer.json
%dir %{phpdir}/Psr
     %{phpdir}/Psr/Cache


%changelog
* Sun Aug  7 2016 Remi Collet <remi@remirepo.net> - 1.0.1-1
- update to 1.0.1 (only comments)
- add check for autoloader

* Mon Jan  4 2016 Remi Collet <remi@remirepo.net> - 1.0.0-1
- backport for #remirepo

* Sun Jan 03 2016 Shawn Iwinski <shawn@iwin.ski> - 1.0.0-1
- Initial package
