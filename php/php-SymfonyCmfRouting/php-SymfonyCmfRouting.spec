%global github_owner    symfony-cmf
%global github_name     Routing
%global github_version  1.1.0
%global github_commit   9f8607950cbf888ec678713a35f3d0088857c85f

%global php_min_ver     5.3.3

%global symfony_min_ver 2.2
%global symfony_max_ver 3.0

%global psr_log_min_ver 1.0
%global psr_log_max_ver 2.0

# Tests are only run with rpmbuild --with tests
# Need to investigate errors
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:          php-SymfonyCmfRouting
Version:       %{github_version}
Release:       1%{?dist}.1
Summary:       Extends the Symfony2 routing component for dynamic routes and chaining

Group:         Development/Libraries
License:       MIT
URL:           http://symfony.com/doc/master/cmf/components/routing/index.html
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
%if %{with_tests}
# For tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
BuildRequires: php-pear(pear.symfony.com/Config) >= %{symfony_min_ver}
BuildRequires: php-pear(pear.symfony.com/Config) <  %{symfony_max_ver}
BuildRequires: php-pear(pear.symfony.com/DependencyInjection) >= %{symfony_min_ver}
BuildRequires: php-pear(pear.symfony.com/DependencyInjection) <  %{symfony_max_ver}
BuildRequires: php-pear(pear.symfony.com/EventDispatcher) >= %{symfony_min_ver}
BuildRequires: php-pear(pear.symfony.com/EventDispatcher) <  %{symfony_max_ver}
BuildRequires: php-pear(pear.symfony.com/HttpKernel) >= %{symfony_min_ver}
BuildRequires: php-pear(pear.symfony.com/HttpKernel) <  %{symfony_max_ver}
BuildRequires: php-pear(pear.symfony.com/Routing) >= %{symfony_min_ver}
BuildRequires: php-pear(pear.symfony.com/Routing) <  %{symfony_max_ver}
BuildRequires: php-PsrLog >= %{psr_log_min_ver}
BuildRequires: php-PsrLog <  %{psr_log_max_ver}
# For tests: phpcompatinfo
BuildRequires: php-pcre
BuildRequires: php-spl
%endif

Requires:      php(language) >= %{php_min_ver}
Requires:      php-pear(pear.symfony.com/HttpKernel) >= %{symfony_min_ver}
Requires:      php-pear(pear.symfony.com/HttpKernel) <  %{symfony_max_ver}
Requires:      php-pear(pear.symfony.com/Routing) >= %{symfony_min_ver}
Requires:      php-pear(pear.symfony.com/Routing) <  %{symfony_max_ver}
Requires:      php-PsrLog >= %{psr_log_min_ver}
Requires:      php-PsrLog <  %{psr_log_max_ver}
# Optional
Requires:      php-pear(pear.symfony.com/EventDispatcher) >= %{symfony_min_ver}
Requires:      php-pear(pear.symfony.com/EventDispatcher) <  %{symfony_max_ver}
# phpcompatinfo
Requires:      php-pcre
Requires:      php-spl

%description
The Symfony CMF Routing component extends the Symfony2 core routing component
to allow more flexibility. The most important difference is that the CMF
Routing component can load routing information from a database.


%prep
%setup -q -n %{github_name}-%{github_commit}

# Overwrite Tests/bootstrap.php (which uses Composer autoloader)
# with a simple spl autoloader
( cat <<'AUTOLOAD'
<?php
spl_autoload_register(function ($class) {
    $src = str_replace(array('\\', '_'), '/', $class).'.php';
    @include_once $src;
});
AUTOLOAD
) > Tests/bootstrap.php


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php/Symfony/Cmf/Component/Routing
cp -rp * %{buildroot}%{_datadir}/php/Symfony/Cmf/Component/Routing/


%check
%if %{with_tests}
%{_bindir}/phpunit \
    -d include_path="%{buildroot}%{_datadir}/php:%{pear_phpdir}" \
    -c phpunit.xml.dist
%else
: Tests skipped, missing '--with tests' option
%endif


%files
%defattr(-,root,root,-)
%doc LICENSE README.md composer.json
%dir %{_datadir}/php/Symfony/Cmf
%dir %{_datadir}/php/Symfony/Cmf/Component
     %{_datadir}/php/Symfony/Cmf/Component/Routing
%exclude %{_datadir}/php/Symfony/Cmf/Component/Routing/LICENSE
%exclude %{_datadir}/php/Symfony/Cmf/Component/Routing/README.md
%exclude %{_datadir}/php/Symfony/Cmf/Component/Routing/composer.json
%exclude %{_datadir}/php/Symfony/Cmf/Component/Routing/phpunit.xml.dist
%exclude %{_datadir}/php/Symfony/Cmf/Component/Routing/Test
%exclude %{_datadir}/php/Symfony/Cmf/Component/Routing/Tests


%changelog
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
