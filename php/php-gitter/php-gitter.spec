# remirepo spec file for php-gitter, from Fedora:
#
# RPM spec file for php-gitter
#
# Copyright (c) 2014-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     klaussilveira
%global github_name      gitter
%global github_version   0.3.0
%global github_commit    6eff42830c336ee9b8b8b9d2f69b62bd9bcbaf3b

%global composer_vendor  klaussilveira
%global composer_project gitter

# "php": ">=5.3.0"
%global php_min_ver      5.3.0
# "symfony/*": ">=2.2"
%global symfony_min_ver  2.2

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_project}
Version:       %{github_version}
Release:       5%{?github_release}%{?dist}
Summary:       Object oriented interaction with Git repositories

Group:         Development/Libraries
License:       BSD
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

# fix for git 2.4.x
# https://github.com/klaussilveira/gitter/pull/47
Patch0:        %{name}-pr47.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: git
## composer.json
BuildRequires: %{_bindir}/phpunit
BuildRequires: php(language)                    >= %{php_min_ver}
BuildRequires: php-composer(symfony/filesystem) >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/process)    >= %{symfony_min_ver}
BuildRequires: php-deepend-Mockery
## phpcompatinfo (computed from version 0.3.0)
BuildRequires: php-date
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

Requires:      git
# composer.json
Requires:      php(language)                 >= %{php_min_ver}
Requires:      php-composer(symfony/process) >= %{symfony_min_ver}
# phpcompatinfo (computed from version 0.3.0)
Requires:      php-date
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming
Provides:      php-%{composer_vendor}-%{composer_project} = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Gitter allows you to interact in an object oriented manner with Git repositories
via PHP. The main goal of the library is not to replace the system git command,
but provide a coherent, stable and performatic object oriented interface.

Most commands are sent to the system's git command, parsed and then interpreted
by Gitter. Everything is transparent to you, so you don't have to worry about a
thing.


%prep
%setup -qn %{github_name}-%{github_commit}

: fix for git 2.4.x
: https://github.com/klaussilveira/gitter/pull/47
%patch0 -p1

: Create autoloader
cat <<'AUTOLOAD' | tee lib/Gitter/autoload.php
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

$fedoraClassLoader->addPrefix('Gitter\\', dirname(__DIR__));

// Not all dependency autoloaders exist or are in every dist yet so fallback
// to using include path for dependencies for now
$fedoraClassLoader->setUseIncludePath(true);

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{phpdir}
cp -rp lib/* %{buildroot}/%{phpdir}/


%check
%if %{with_tests}
: Always run all tests
sed '/stopOnFailure/d' phpunit.xml.dist > phpunit.xml

: Run tests
%{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}/%{phpdir}/Gitter/autoload.php
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
%{phpdir}/Gitter


%changelog
* Sat Jul 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.3.0-5
- Use full require paths in autoloader

* Sat Jul 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.3.0-4
- Added autoloader
- Added standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming provides

* Sun May 24 2015 Remi Collet <remi@fedoraproject.org> - 0.3.0-2
- add patch for git 2.4 (FTBFS detected by Koschei)

* Sat Jul 19 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.3.0-1
- Updated to 0.3.0 (BZ #1101229)
- Added "php-composer(klaussilveira/gitter)" virtual provide
- Added option to build without tests ("--without tests")

* Fri Feb 21 2014 Remi Collet <remi@fedoraproject.org> 0.2.0-2.20131206git786e86a
- backport for remi repo

* Thu Feb 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 0.2.0-2.20131206git786e86a
- Conditional release dist

* Mon Jan 27 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 0.2.0-1.20131206git786e86a
- Initial package
