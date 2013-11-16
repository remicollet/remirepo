%global github_owner    schmittjoh
%global github_name     metadata
%global github_version  1.5.0
%global github_commit   88ffa28bc987e4c26229fc84a2e541b6ed4e1459

%global lib_name        Metadata
%global php_min_ver     5.3.0

Name:          php-%{lib_name}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       A library for class/method/property metadata management in PHP

Group:         Development/Libraries
License:       ASL 2.0
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# For tests
BuildRequires: php-common >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
BuildRequires: php-pear(pear.doctrine-project.org/DoctrineCommon) >= 2.0
BuildRequires: php-pear(pear.doctrine-project.org/DoctrineCommon) <  2.4
# For tests: phpcompatinfo
BuildRequires: php-date
BuildRequires: php-reflection
BuildRequires: php-spl

Requires:      php-common >= %{php_min_ver}
Requires:      php-pear(pear.symfony.com/DependencyInjection)
# phpcompatinfo requires
Requires:      php-date
Requires:      php-reflection
Requires:      php-spl

%description
This library provides some commonly needed base classes for managing metadata
for classes, methods and properties. The metadata can come from many different
sources (annotations, YAML/XML/PHP configuration files).

The metadata classes are used to abstract away that source and provide a common
interface for all of them.


%prep
%setup -q -n %{github_name}-%{github_commit}

# Rewrite tests' bootstrap (which uses Composer autoloader) with simple
# autoloader that uses include path
( cat <<'AUTOLOAD'
<?php
spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', str_replace('_', '/', $class)).'.php';
    @include_once $src;
});
AUTOLOAD
) > tests/bootstrap.php


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php
cp -rp src/%{lib_name} %{buildroot}%{_datadir}/php/


%check
%{_bindir}/phpunit -d include_path="./src:./tests:.:%{pear_phpdir}"


%files
%defattr(-,root,root,-)
%doc LICENSE README.rst CHANGELOG.md composer.json
%{_datadir}/php/%{lib_name}


%changelog
* Sat Nov 16 2013 Remi Collet <RPMS@famillecollet.com> 1.5.0-1
- backport 1.5.0 for remi repo

* Fri Nov 15 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.5.0-1
- Updated to 1.5.0

* Tue Apr  2 2013 Remi Collet <RPMS@famillecollet.com> 1.3.0-1
- backport 1.3.0 for remi repo

* Sat Mar 30 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.0-1
- Updated to version 1.3.0
- Removed tests sub-package

* Fri Jan 25 2013 Remi Collet <RPMS@famillecollet.com> 1.1.1-1
- backport 1.1.1 for remi repo

* Wed Jan 23 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.1-1
- Initial package
