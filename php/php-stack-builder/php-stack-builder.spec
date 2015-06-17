#
# RPM spec file for php-stack-builder
#
# Copyright (c) 2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     stackphp
%global github_name      builder
%global github_version   1.0.3
%global github_commit    c1f8a4693b55c563405024f708a76ef576c3b276

%global composer_vendor  stack
%global composer_project builder

# "php": ">= 5.3.0"
%global php_min_ver      5.3.3
# "silex/silex": "~1.0"
%global silex_min_ver    1.0
%global silex_max_ver    2.0
# "symfony/*": "~2.1"
%global symfony_min_ver  2.1
%global symfony_max_ver  3.0

# Build using "--without tests" to disable tests
%global with_tests  %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Builder for stack middlewares based on HttpKernelInterface

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# For autoload generation
BuildRequires: %{_bindir}/phpab
# For tests
%if %{with_tests}
BuildRequires: %{_bindir}/phpunit
## composer.json
BuildRequires: php(language)                         >= %{php_min_ver}
BuildRequires: php-composer(silex/silex)             >= %{silex_min_ver}
BuildRequires: php-composer(silex/silex)             <  %{silex_max_ver}
BuildRequires: php-composer(symfony/http-foundation) >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/http-foundation) <  %{symfony_max_ver}
BuildRequires: php-composer(symfony/http-kernel)     >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/http-kernel)     <  %{symfony_max_ver}
## phpcompatinfo (computed from version 1.0.3)
BuildRequires: php-reflection
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language)                         >= %{php_min_ver}
Requires:      php-composer(symfony/http-foundation) >= %{symfony_min_ver}
Requires:      php-composer(symfony/http-foundation) <  %{symfony_max_ver}
Requires:      php-composer(symfony/http-kernel)     >= %{symfony_min_ver}
Requires:      php-composer(symfony/http-kernel)     <  %{symfony_max_ver}
# phpcompatinfo (computed from version 1.0.3)
Requires:      php-reflection
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Builder for stack middlewares based on HttpKernelInterface.

Stack/Builder is a small library that helps you construct a nested
HttpKernelInterface decorator tree. It models it as a stack of middlewares.


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Generate autoloader
%{_bindir}/phpab --nolower --output src/Stack/autoload-builder.php src/Stack

cat >> src/Stack/autoload-builder.php <<'AUTOLOAD'

// TODO: Add Symfony autoloaders from their packages when they are available
spl_autoload_register(function ($class) {
    if (0 === strpos($class, 'Symfony\\')) {
        $src = str_replace('\\', '/',  $class) . '.php';
        @include_once $src;
    }
});
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
# Create bootstrap
cat > bootstrap.php <<'BOOTSTRAP'
<?php
require '%{buildroot}%{phpdir}/Stack/autoload-builder.php';
require '%{phpdir}/Silex/autoload.php';
BOOTSTRAP

%{_bindir}/phpunit --bootstrap bootstrap.php
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%dir %{_datadir}/php/Stack
     %{_datadir}/php/Stack/Builder.php
     %{_datadir}/php/Stack/StackedHttpKernel.php
     %{_datadir}/php/Stack/autoload-builder.php


%changelog
* Sat May 16 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.3-1
- Initial package
