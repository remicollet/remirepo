#
# RPM spec file for php-SymfonyCmfRouting
#
# Copyright (c) 2013-2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     symfony-cmf
%global github_name      Routing
%global github_version   1.3.0
%global github_commit    8e87981d72c6930a27585dcd3119f3199f6cb2a6

%global composer_vendor  symfony-cmf
%global composer_project routing

# "php": ">=5.3.3"
%global php_min_ver     5.3.3
# "symfony/*": "~2.2"
%global symfony_min_ver 2.2
%global symfony_max_ver 3.0
# "psr/log": "~1.0"
%global psr_log_min_ver 1.0
%global psr_log_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests  %{?_without_tests:0}%{!?_without_tests:1}

%{!?__phpunit:  %global __phpunit  %{_bindir}/phpunit}
%{!?phpdir:     %global phpdir     %{_datadir}/php}

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
%if %{with_tests}
# composer.json
BuildRequires: php(language)                   >= %{php_min_ver}
BuildRequires: php-composer(psr/log)           >= %{psr_log_min_ver}
BuildRequires: php-composer(psr/log)           <  %{psr_log_max_ver}
BuildRequires: php-phpunit-PHPUnit
BuildRequires: php-symfony-config              >= %{symfony_min_ver}
BuildRequires: php-symfony-config              <  %{symfony_max_ver}
BuildRequires: php-symfony-dependencyinjection >= %{symfony_min_ver}
BuildRequires: php-symfony-dependencyinjection <  %{symfony_max_ver}
BuildRequires: php-symfony-eventdispatcher     >= %{symfony_min_ver}
BuildRequires: php-symfony-eventdispatcher     <  %{symfony_max_ver}
BuildRequires: php-symfony-httpkernel          >= %{symfony_min_ver}
BuildRequires: php-symfony-httpkernel          <  %{symfony_max_ver}
BuildRequires: php-symfony-routing             >= %{symfony_min_ver}
BuildRequires: php-symfony-routing             <  %{symfony_max_ver}
# phpcompatinfo (computed from version 1.3.0)
BuildRequires: php-pcre
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language)               >= %{php_min_ver}
Requires:      php-composer(psr/log)       >= %{psr_log_min_ver}
Requires:      php-composer(psr/log)       <  %{psr_log_max_ver}
Requires:      php-symfony-httpkernel      >= %{symfony_min_ver}
Requires:      php-symfony-httpkernel      <  %{symfony_max_ver}
Requires:      php-symfony-routing         >= %{symfony_min_ver}
Requires:      php-symfony-routing         <  %{symfony_max_ver}
# composer.json: optional
Requires:      php-symfony-eventdispatcher >= %{symfony_min_ver}
Requires:      php-symfony-eventdispatcher <  %{symfony_max_ver}
# phpcompatinfo (computed from version 1.2.0)
Requires:      php-pcre
Requires:      php-spl

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
# Empty build section, nothing to build


%install
mkdir -pm 0755 %{buildroot}%{phpdir}/Symfony/Cmf/Component/Routing
cp -rp * %{buildroot}%{phpdir}/Symfony/Cmf/Component/Routing/


%check
%if %{with_tests}
# Create autoloader
mkdir vendor
cat > vendor/autoload.php <<'AUTOLOAD'
<?php

spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', $class).'.php';
    @include_once $src;
});
AUTOLOAD

%{__phpunit} --include-path %{buildroot}%{phpdir}
%else
: Tests skipped
%endif


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGELOG.md README.md composer.json
%dir %{phpdir}/Symfony/Cmf
%dir %{phpdir}/Symfony/Cmf/Component
     %{phpdir}/Symfony/Cmf/Component/Routing
%exclude %{phpdir}/Symfony/Cmf/Component/Routing/LICENSE
%exclude %{phpdir}/Symfony/Cmf/Component/Routing/*.md
%exclude %{phpdir}/Symfony/Cmf/Component/Routing/composer.json
%exclude %{phpdir}/Symfony/Cmf/Component/Routing/phpunit.xml.dist
%exclude %{phpdir}/Symfony/Cmf/Component/Routing/Test*


%changelog
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
