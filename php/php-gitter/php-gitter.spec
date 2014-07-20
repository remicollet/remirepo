#
# RPM spec file for php-gitter
#
# Copyright (c) 2014 Shawn Iwinski <shawn.iwinski@gmail.com>
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

%global lib_name         Gitter

# "php": ">=5.3.0"
%global php_min_ver      5.3.0
# "phpunit/phpunit": ">=3.7.1"
%global phpunit_min_ver  3.7.1
# "symfony/*": ">=2.2"
%global symfony_min_ver  2.2

# Build using "--without tests" to disable tests
%global with_tests       %{?_without_tests:0}%{!?_without_tests:1}

%{!?__phpunit: %global __phpunit %{_bindir}/phpunit}

Name:          php-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Object oriented interaction with Git repositories

Group:         Development/Libraries
License:       BSD
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
%if %{with_tests}
# For tests
BuildRequires: git
# For tests: composer.json
BuildRequires: php(language)          >= %{php_min_ver}
BuildRequires: php-deepend-Mockery
BuildRequires: php-phpunit-PHPUnit    >= %{phpunit_min_ver}
BuildRequires: php-symfony-process    >= %{symfony_min_ver}
BuildRequires: php-symfony-filesystem >= %{symfony_min_ver}
# For tests: phpcompatinfo (computed from version 0.3.0)
BuildRequires: php-date
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
%endif

Requires:      git
# composer.json
Requires:      php(language)       >= %{php_min_ver}
Requires:      php-symfony-process >= %{symfony_min_ver}
# phpcompatinfo (computed from version 0.3.0)
Requires:      php-date
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl

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


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/php
cp -rp lib/%{lib_name} %{buildroot}/%{_datadir}/php/


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

# Create PHPUnit config w/ colors turned off
sed 's/colors="true"/colors="false"/' phpunit.xml.dist > phpunit.xml

%{__phpunit} --include-path="./lib:./tests" -d date.timezone="UTC"
%else
: Tests skipped
%endif

%clean
rm -rf %{buildroot}

%{!?_licensedir:%global license %%doc}

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.md composer.json
%{_datadir}/php/%{lib_name}


%changelog
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
