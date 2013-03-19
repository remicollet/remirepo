%global github_owner      schmittjoh
%global github_name       php-collection
%global github_version    0.2.0
%global github_commit     acb02a921bb364f360ce786b13455345063c4a07

%global lib_name          PhpCollection

%global php_min_ver       5.3.0
%global phpoption_min_ver 1.0
%global phpoption_max_ver 2.0

Name:          php-%{lib_name}
Version:       %{github_version}
Release:       2%{?dist}
Summary:       General purpose collection library for PHP

Group:         Development/Libraries
License:       ASL 2.0
URL:           http://jmsyst.com/libs/%{github_name}
# To create source:
# wget https://github.com/schmittjoh/php-collection/archive/%%{github_commit}.tar.gz
# php-PhpCollection-strip.sh %%{github_version} %%{github_commit}
Source0:       %{name}-%{github_version}-%{github_commit}.tar.gz
Source1:       %{name}-strip.sh

BuildArch:     noarch
# Test build requires
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
BuildRequires: php-PhpOption >= %{phpoption_min_ver}
BuildRequires: php-PhpOption <  %{phpoption_max_ver}
# Test build requires:phpci
BuildRequires: php-spl

Requires:      php(language) >= %{php_min_ver}
Requires:      php-PhpOption >= %{phpoption_min_ver}
Requires:      php-PhpOption <  %{phpoption_max_ver}
# phpci requires
Requires:      php-spl

%description
This library adds basic collections for PHP.

Collections can be seen as more specialized arrays for which certain contracts
are guaranteed.

Supported Collections:
* Sequences
** Keys: numerical, consequentially increasing, no gaps
** Values: anything, duplicates allowed
** Classes: Sequence, SortedSequence
* Maps
** Keys: strings or objects, duplicate keys not allowed
** Values: anything, duplicates allowed
** Classes: Map, ObjectMap (not yet implemented)
* Sets (not yet implemented)
** Keys: not meaningful
** Values: anything, each value must be unique (===)
** Classes: Set

General Characteristics:
* Collections are mutable (new elements may be added, existing elements may be
  modified or removed). Specialized immutable versions may be added in the
  future though.
* Equality comparison between elements are always performed using the shallow
  comparison operator (===).
* Sorting algorithms are unstable, that means the order for equal elements is
  undefined (the default, and only PHP behavior).


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
%{_bindir}/phpunit \
    -d include_path="./src:./tests:.:%{pear_phpdir}:%{_datadir}/php" \
    -c phpunit.xml.dist


%files
%doc LICENSE README.md composer.json
%{_datadir}/php/%{lib_name}


%changelog
* Mon Mar 18 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.2.0-2
- Added %%{name}-strip.sh as Source1

* Sat Mar 16 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.2.0-1
- Updated to version 0.2.0
- Added phpoption_max_ver global
- Bad licensed files stripped from source
- php-common => php(language)
- Removed tests sub-package

* Wed Jan 23 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.1.0-1
- Initial package
