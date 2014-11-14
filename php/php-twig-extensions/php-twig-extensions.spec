#
# RPM spec file for php-twig-extensions
#
# Copyright (c) 2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     twigphp
%global github_name      Twig-extensions
%global github_version   1.2.0
%global github_commit    8cf4b9fe04077bd54fc73f4fde83347040c3b8cd

%global composer_vendor  twig
%global composer_project extensions

# "symfony/translation": "~2.3"
%global symfony_min_ver  2.3
%global symfony_max_ver  3.0
# "twig/twig": "~1.12"
%global twig_min_ver     1.12
%global twig_max_ver     2.0

# Build using "--without tests" to disable tests
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:     %global phpdir     %{_datadir}/php}
%{!?__phpunit:  %global __phpunit  %{_bindir}/phpunit}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       2%{?dist}
Summary:       Twig extensions

Group:         Development/Libraries
License:       MIT
URL:           http://twig.sensiolabs.org/doc/extensions/index.html
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
%if %{with_tests}
BuildRequires: php-phpunit-PHPUnit
# composer.json
BuildRequires: php-composer(symfony/translation) >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/translation) <  %{symfony_max_ver}
BuildRequires: php-composer(twig/twig)           >= %{twig_min_ver}
BuildRequires: php-composer(twig/twig)           <  %{twig_max_ver}
# phpcompatinfo (computed from version 1.2.0)
BuildRequires: php-date
BuildRequires: php-intl
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-spl
%endif

# composer.json
Requires:      php-composer(twig/twig)           >= %{twig_min_ver}
Requires:      php-composer(twig/twig)           <  %{twig_max_ver}
# composer.json: optional
Requires:      php-composer(symfony/translation) >= %{symfony_min_ver}
Requires:      php-composer(symfony/translation) <  %{symfony_max_ver}
# phpcompatinfo (computed from version 1.2.0)
Requires:      php-intl
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Common additional features for Twig that do not directly belong in core Twig.


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -pm 0755 %{buildroot}%{phpdir}
cp -rp lib/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
# Create tests' bootstrap
mkdir vendor
cat > vendor/autoload.php <<'AUTOLOAD'
<?php
spl_autoload_register(function ($class) {
    $src = str_replace(array('\\', '_'), '/', $class) . '.php';
    @include_once $src;
});
AUTOLOAD

%{__phpunit} --include-path %{buildroot}%{phpdir}
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.rst composer.json doc
%{phpdir}/Twig/Extensions


%changelog
* Fri Nov 14 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-2
- backport for remi repo, add EL-5 stuff

* Thu Nov 13 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.0-2
- Conditional %%{?dist}
- Removed color turn off and default timezone for phpunit
- Removed "%%dir %%{phpdir}/Twig" from %%files

* Sun Nov 02 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.0-1
- Initial package
