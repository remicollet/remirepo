# remimrepo spec file for php-SymfonyCmfRouting, from:
#
# Fedora spec file for php-SymfonyCmfRouting
#
# Copyright (c) 2013-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     symfony-cmf
%global github_name      routing
%global github_version   1.4.0
%global github_commit    b93704ca098334f56e9b317932f21a4362e620db

%global composer_vendor  symfony-cmf
%global composer_project routing

# "php": "^5.3.9|^7.0"
%global php_min_ver     5.3.9
# "symfony/config": "^2.2|3.*"
# "symfony/dependency-injection": "^2.0.5|3.*"
# "symfony/event-dispatcher": "^2.1|3.*"
# "symfony/http-kernel": "^2.2|3.*"
# "symfony/routing": "^2.2|3.*"
## NOTE: Min version not 2.2 because autoloaders required
## NOTE: Max version not 4.0 to force version 2
%global symfony_min_ver 2.7.1
%global symfony_max_ver 3.0
# "psr/log": "1.*"
## NOTE: Min version not 1.0 because autoloader required
%global psr_log_min_ver 1.0.1
%global psr_log_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests  0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-SymfonyCmfRouting
Version:       %{github_version}
Release:       1%{?dist}
Summary:       Extends the Symfony2 routing component for dynamic routes and chaining

Group:         Development/Libraries
License:       MIT
URL:           http://symfony.com/doc/master/cmf/book/routing.html
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: php-composer(phpunit/phpunit)
## composer.json
BuildRequires: php(language)                              >= %{php_min_ver}
BuildRequires: php-composer(psr/log)                      >= %{psr_log_min_ver}
BuildRequires: php-composer(symfony/config)               >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/dependency-injection) >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/event-dispatcher)     >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/http-kernel)          >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/routing)              >= %{symfony_min_ver}
## phpcompatinfo (computed from version 1.4.0)
BuildRequires: php-pcre
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                     >= %{php_min_ver}
Requires:      php-composer(psr/log)             >= %{psr_log_min_ver}
Requires:      php-composer(psr/log)             <  %{psr_log_max_ver}
Requires:      php-composer(symfony/http-kernel) >= %{symfony_min_ver}
Requires:      php-composer(symfony/http-kernel) <  %{symfony_max_ver}
Requires:      php-composer(symfony/routing)     >= %{symfony_min_ver}
Requires:      php-composer(symfony/routing)     <  %{symfony_max_ver}
# phpcompatinfo (computed from version 1.4.0)
Requires:      php-pcre
Requires:      php-spl
# composer.json: optional
%if 0%{?fedora} > 21
Suggests:      php-composer(symfony/event-dispatcher)
%endif

# php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}
Provides:      php-%{composer_vendor}-%{composer_project}           = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
The Symfony CMF Routing component extends the Symfony2 core routing component.
It provides:
* A ChainRouter to run several routers in parallel
* A DynamicRouter that can load routes from any database and can generate
      additional information in the route match

Even though it has Symfony in its name, the Routing component does not need the
full Symfony2 Framework and can be used in standalone projects.


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Create autoloader
cat <<'AUTOLOAD' | tee autoload.php
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

$fedoraClassLoader->addPrefix(
    'Symfony\\Cmf\\Component\\Routing\\',
    dirname(dirname(dirname(dirname(__DIR__))))
);

// Required dependencies
require_once '%{phpdir}/Psr/Log/autoload.php';
require_once '%{phpdir}/Symfony/Component/HttpKernel/autoload.php';
require_once '%{phpdir}/Symfony/Component/Routing/autoload.php';

// Optional dependency
if (file_exists('%{phpdir}/Symfony/Component/EventDispatcher/autoload.php')) {
    require_once '%{phpdir}/Symfony/Component/EventDispatcher/autoload.php';
}

return $fedoraClassLoader;
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}/Symfony/Cmf/Component/Routing
cp -rp * %{buildroot}%{phpdir}/Symfony/Cmf/Component/Routing/


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
$fedoraClassLoader =
    require_once '%{buildroot}%{phpdir}/Symfony/Cmf/Component/Routing/autoload.php';

$fedoraClassLoader->addPrefix(
    'Symfony\\Cmf\\Component\\Routing\\Test\\',
    '%{buildroot}%{phpdir}'
);

$fedoraClassLoader->addPrefix(
    'Symfony\\Cmf\\Component\\Routing\\Tests\\',
    '%{buildroot}%{phpdir}'
);

require_once '%{phpdir}/Symfony/Component/Config/autoload.php';
require_once '%{phpdir}/Symfony/Component/DependencyInjection/autoload.php';
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
%{_bindir}/phpunit --verbose --bootstrap bootstrap.php
fi
exit $ret
%else
: Tests skipped
%endif


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGELOG.md
%doc README.md
%doc composer.json
%dir %{phpdir}/Symfony/Cmf
%dir %{phpdir}/Symfony/Cmf/Component
     %{phpdir}/Symfony/Cmf/Component/Routing
%exclude %{phpdir}/Symfony/Cmf/Component/Routing/LICENSE
%exclude %{phpdir}/Symfony/Cmf/Component/Routing/*.md
%exclude %{phpdir}/Symfony/Cmf/Component/Routing/composer.json
%exclude %{phpdir}/Symfony/Cmf/Component/Routing/phpunit.xml.dist
%exclude %{phpdir}/Symfony/Cmf/Component/Routing/Test*


%changelog
* Thu Nov 03 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.4.0-1
- Updated to 1.4.0 (RHBZ #1297159)

* Thu Jan 21 2016 Remi Collet <remi@fedoraproject.org> - 1.3.0-4
- sync with Fedora
- run test suite with both PHP 5 and 7 when available

* Wed Jan 20 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.0-4
- Added autoloader dependency to build requires

* Wed Jan 20 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.0-3
- php-composer(*) virtual provide dependencies instead of direct package names
- Dropped max version build dependencies
- Increased Symfony min version from 2.2 to 2.3.31/2.7.3 for autoloaders
- Added "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" ("php-symfony-cmf-routing")
  virtual provide
- Suggest php-composer(symfony/event-dispatcher) instead of require
- Added autoloader

* Thu Nov 13 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.0-1
- Updated to 1.3.0 (BZ #1096125)

* Mon Oct 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.0-1
- Updated to 1.2.0 (BZ #1096125)
- Enabled tests by default
- Updated URL, description, dependencies, %%check, and %%files
- Added "php-composer(symfony-cmf/routing)" virtual provide
- %%license usage

* Sat Nov 16 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-1.1
- backport 1.1.0 for remi repo.

* Wed Oct 30 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-1
- Updated to 1.1.0
- Updated required pkg versions, required pkgs, summary, URL, and description
- php-common -> php(language)

* Thu May 16 2013 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- backport 1.0.1 for remi repo.

* Wed May 08 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.1-1
- Updated to version 1.0.1
- Added php-pear(pear.symfony.com/HttpFoundation) require
- Only run tests with "--with tests" option
- Remove phpunit.xml.dist from packaging since tests themselves are not included

* Mon Mar 11 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3.alpha4.20130306git4706313
- backport for remi repo.

* Sat Mar 09 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-0.3.alpha4.20130306git4706313
- Added additional commits (snapshot) beyond tagged version 1.0.0-alpha4 which
  include several Symfony 2.2 fixes

* Tue Mar 05 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-0.2.alpha4.20130121git92ee467
- Added globals symfony_min_ver and symfony_max_ver
- Removed tests sub-package

* Thu Jan 31 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-0.1.alpha4.20130121git92ee467
- Initial package
