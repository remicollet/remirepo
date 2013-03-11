%global github_owner    symfony-cmf
%global github_name     Routing
%global github_version  1.0.0
%global github_commit   4706313dc7708633cfb1228c8b44e807aa44b6bf
%global github_date     20130306

%global github_release  alpha4.%{github_date}git%(c=%{github_commit}; echo ${c:0:7})

%global php_min_ver     5.3.2

%global symfony_min_ver 2.1.0
%global symfony_max_ver 2.3.0

Name:          php-SymfonyCmfRouting
Version:       %{github_version}
Release:       0.3.%{github_release}%{?dist}
Summary:       Extends the Symfony2 routing component

Group:         Development/Libraries
License:       MIT
URL:           http://symfony.com/doc/master/cmf/components/routing.html
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# For tests
BuildRequires: php-common >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
BuildRequires: php-pear(pear.symfony.com/Routing) >= %{symfony_min_ver}
BuildRequires: php-pear(pear.symfony.com/Routing) <  %{symfony_max_ver}
BuildRequires: php-pear(pear.symfony.com/HttpKernel) >= %{symfony_min_ver}
BuildRequires: php-pear(pear.symfony.com/HttpKernel) <  %{symfony_max_ver}
# For tests: phpci
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl

Requires:      php-common >= %{php_min_ver}
Requires:      php-pear(pear.symfony.com/Routing) >= %{symfony_min_ver}
Requires:      php-pear(pear.symfony.com/Routing) <  %{symfony_max_ver}
Requires:      php-pear(pear.symfony.com/HttpKernel) >= %{symfony_min_ver}
Requires:      php-pear(pear.symfony.com/HttpKernel) <  %{symfony_max_ver}
# phpci
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl

%description
The Symfony CMF Routing component library extends the Symfony2 core routing
component. Even though it has Symfony in its name, it does not need the full
Symfony2 framework and can be used in standalone projects. For integration
with Symfony we provide RoutingExtraBundle.

At the core of the Symfony CMF Routing component is the ChainRouter, that is
used instead of the Symfony2's default routing system. The ChainRouter can
chain several RouterInterface implementations, one after the other, to determine
what should handle each request. The default Symfony2 router can be added to
this chain, so the standard routing mechanism can still be used.

Additionally, this component is meant to provide useful implementations of the
routing interfaces. Currently, it provides the DynamicRouter, which uses a
RequestMatcherInterface to dynamically load Routes, and can apply
RouteEnhancerInterface strategies in order to manipulate them. The provided
NestedMatcher can dynamically retrieve Symfony2 Route objects from a
RouteProviderInterface. This interfaces abstracts a collection of Routes,
that can be stored in a database, like Doctrine PHPCR-ODM or Doctrine ORM.
The DynamicRouter also uses a UrlGenerator instance to generate Routes and
an implementation is provided under ProviderBasedGenerator that can generate
routes loaded from a RouteProviderInterface instance, and the
ContentAwareGenerator on top of it to determine the route object from a
content object.


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
%{_bindir}/phpunit \
    -d include_path="%{buildroot}%{_datadir}/php:%{pear_phpdir}" \
    -c phpunit.xml.dist


%files
%doc LICENSE README.md composer.json
%dir %{_datadir}/php/Symfony/Cmf
%dir %{_datadir}/php/Symfony/Cmf/Component
     %{_datadir}/php/Symfony/Cmf/Component/Routing
%exclude %{_datadir}/php/Symfony/Cmf/Component/Routing/LICENSE
%exclude %{_datadir}/php/Symfony/Cmf/Component/Routing/README.md
%exclude %{_datadir}/php/Symfony/Cmf/Component/Routing/composer.json
%exclude %{_datadir}/php/Symfony/Cmf/Component/Routing/Test
%exclude %{_datadir}/php/Symfony/Cmf/Component/Routing/Tests


%changelog
* Sat Mar 09 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-0.3.alpha4.20130306git4706313
- Added additional commits (snapshot) beyond tagged version 1.0.0-alpha4 which
  include several Symfony 2.2 fixes

* Tue Mar 05 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-0.2.alpha4.20130121git92ee467
- Added globals symfony_min_ver and symfony_max_ver
- Removed tests sub-package

* Thu Jan 31 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-0.1.alpha4.20130121git92ee467
- Initial package
