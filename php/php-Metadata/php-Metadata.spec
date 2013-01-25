%global github_owner   schmittjoh
%global github_name    metadata
%global github_version 1.1.1
%global github_commit  84088bc4f6e2387ec8b549bffc1e037107572f5a

%global lib_name       Metadata
%global php_min_ver    5.3.0

Name:          php-%{lib_name}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       Class/method/property metadata management in PHP

Group:         Development/Libraries
License:       ASL 2.0
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# Test build requires
BuildRequires: php-common >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
# Test build requires: phpci
BuildRequires: php-date
BuildRequires: php-reflection
BuildRequires: php-spl

Requires:      php-common >= %{php_min_ver}
Requires:      php-pear(pear.symfony.com/DependencyInjection)
# phpci requires
Requires:      php-date
Requires:      php-reflection
Requires:      php-spl

%description
This library provides some commonly needed base classes for managing metadata
for classes, methods and properties. The metadata can come from many different
sources (annotations, YAML/XML/PHP configuration files).

The metadata classes are used to abstract away that source and provide a common
interface for all of them.


%package tests
Summary:  Test suite for %{name}
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description tests
%{summary}.


%prep
%setup -q -n %{github_name}-%{github_commit}

# PHPUnit config
sed 's:\(\./\)\?tests/:./:' -i phpunit.xml.dist
mv phpunit.xml.dist tests/

# Rewrite tests' bootstrap (which uses Composer autoloader) with simple
# autoloader that uses include path
mv tests/bootstrap.php tests/bootstrap.php.dist
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

mkdir -p -m 755 %{buildroot}%{_datadir}/tests/%{name}
cp -rp tests/* %{buildroot}%{_datadir}/tests/%{name}/


%check
%{_bindir}/phpunit \
    -d include_path="./src:./tests:.:%{pear_phpdir}:%{_datadir}/php" \
    -c tests/phpunit.xml.dist


%files
%doc LICENSE README.rst CHANGELOG.md composer.json
%{_datadir}/php/%{lib_name}

%files tests
%dir %{_datadir}/tests
     %{_datadir}/tests/%{name}


%changelog
* Wed Jan 23 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.1-1
- Initial package
