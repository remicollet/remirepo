# remirepo spec file for php-stack-builder, from Fedora:
#
# Fedora spec file for php-stack-builder
#
# Copyright (c) 2015-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     stackphp
%global github_name      builder
%global github_version   1.0.4
%global github_commit    59fcc9b448a8ce5e338a04c4e2e4aca893e83425

%global composer_vendor  stack
%global composer_project builder

# "php": ">=5.3.0"
%global php_min_ver      5.3.0
# "silex/silex": "~1.0"
%global silex_min_ver    1.0
%global silex_max_ver    2.0
# "symfony/http-foundation": "~2.1|~3.0"
# "symfony/http-kernel": "~2.1|~3.0"
#     NOTE: Min version not 2.1 because autoloader required
%global symfony_min_ver  2.7.1
%global symfony_max_ver  4.0

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
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Autoloader
BuildRequires: %{_bindir}/phpab
# Tests
%if %{with_tests}
BuildRequires: php-composer(phpunit/phpunit)
## composer.json
BuildRequires: php(language)                         >= %{php_min_ver}
BuildRequires: php-composer(silex/silex)             >= %{silex_min_ver}
BuildRequires: php-composer(symfony/http-foundation) >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/http-foundation) <  %{symfony_max_ver}
BuildRequires: php-composer(symfony/http-kernel)     >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/http-kernel)     <  %{symfony_max_ver}
## phpcompatinfo (computed from version 1.0.4)
BuildRequires: php-reflection
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language)                         >= %{php_min_ver}
Requires:      php-composer(symfony/http-foundation) >= %{symfony_min_ver}
Requires:      php-composer(symfony/http-foundation) <  %{symfony_max_ver}
Requires:      php-composer(symfony/http-kernel)     >= %{symfony_min_ver}
Requires:      php-composer(symfony/http-kernel)     <  %{symfony_max_ver}
# phpcompatinfo (computed from version 1.0.4)
Requires:      php-reflection
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Builder for stack middlewares based on HttpKernelInterface.

Stack/Builder is a small library that helps you construct a nested
HttpKernelInterface decorator tree. It models it as a stack of middlewares.

Autoloader: %{phpdir}/Stack/autoload-builder.php


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Generate autoloader
%{_bindir}/phpab --nolower --output src/Stack/autoload-builder.php src/Stack

cat <<'AUTOLOAD' | tee -a src/Stack/autoload-builder.php

// Required dependencies
require_once '%{phpdir}/Symfony/Component/HttpFoundation/autoload.php';
require_once '%{phpdir}/Symfony/Component/HttpKernel/autoload.php';
AUTOLOAD


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require_once '%{buildroot}%{phpdir}/Stack/autoload-builder.php';
require_once '%{phpdir}/Silex/autoload.php';
BOOTSTRAP

run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap bootstrap.php || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap bootstrap.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --bootstrap bootstrap.php
fi
exit $ret
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
%dir %{_datadir}/php/Stack
     %{_datadir}/php/Stack/Builder.php
     %{_datadir}/php/Stack/StackedHttpKernel.php
     %{_datadir}/php/Stack/autoload-builder.php


%changelog
* Sun Jul 24 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.4-1
- Update to 1.0.4 (RHBZ #1342093)
- Update autoloader to use dependencies' autoloaders

* Wed Jun 17 2015 Remi Collet <remi@remirepo.net> - 1.0.3-1
- add backport stuff for remirepo

* Sat May 16 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.3-1
- Initial package
