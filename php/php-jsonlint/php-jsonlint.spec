%global libname     jsonlint
%global php_min_ver 5.3.0

Name:          php-%{libname}
Version:       1.1.0
Release:       1%{?dist}
Summary:       JSON Lint for PHP

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/Seldaek/%{libname}
Source0:       %{url}/archive/%{version}.tar.gz

BuildArch:     noarch
# Test build requires
BuildRequires: php-common >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
# Test build requires: phpci
BuildRequires: php-pcre

Requires:      php-common >= %{php_min_ver}
# phpci requires
Requires:      php-pcre

%description
%{summary}.

This library is a port of the JavaScript jsonlint
(https://github.com/zaach/jsonlint) library.


%prep
%setup -q -n %{libname}-%{version}

# Create PSR-0 autoloader for tests
( cat <<'AUTOLOAD'
<?php
spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', $class).'.php';
    require_once $src;
});
AUTOLOAD
) > autoload.php


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php/Seld
cp -rp src/Seld/JsonLint %{buildroot}%{_datadir}/php/Seld/


%check
%{_bindir}/phpunit --bootstrap=autoload.php \
    -d include_path="src:tests:.:/usr/share/pear" .


%files
%doc LICENSE README.mdown composer.json
%dir %{_datadir}/php/Seld
     %{_datadir}/php/Seld/JsonLint


%changelog
* Mon Jan  7 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-1
- Initial package
