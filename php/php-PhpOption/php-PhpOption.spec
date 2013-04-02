%global github_owner   schmittjoh
%global github_name    php-option
%global github_version 1.2.0
%global github_commit  24e55357ced5bb041da1416711737b9e144505b4

%global lib_name       PhpOption
%global php_min_ver    5.3.0

Name:          php-%{lib_name}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       Option type for PHP

Group:         Development/Libraries
License:       ASL 2.0
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# For tests
BuildRequires: php-common >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
# For tests: phpci
BuildRequires: php-spl

Requires:      php-common >= %{php_min_ver}
# phpci
Requires:      php-spl

%description
This package adds an Option type for PHP.

The Option type is intended for cases where you sometimes might return a value
(typically an object), and sometimes you might return no value (typically null)
depending on arguments, or other runtime factors.

Often times, you forget to handle the case where no value is returned. Not
intentionally of course, but maybe you did not account for all possible states
of the system; or maybe you indeed covered all cases, then time goes on, code
is refactored, some of these your checks might become invalid, or incomplete.
Suddenly, without noticing, the no value case is not handled anymore. As a
result, you might sometimes get fatal PHP errors telling you that you called a
method on a non-object; users might see blank pages, or worse.

On one hand, the Option type forces a developer to consciously think about both
cases (returning a value, or returning no value). That in itself will already
make your code more robust. On the other hand, the Option type also allows the
API developer to provide more concise API methods, and empowers the API user in
how he consumes these methods.


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
%doc LICENSE README.md composer.json
%{_datadir}/php/%{lib_name}

%changelog
* Tue Apr  2 2013 Remi Collet <RPMS@famillecollet.com> 1.2.0-1
- backport 1.2.0 for remi repo

* Sat Mar 30 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.2.0-1
- Updated to version 1.2.0
- Removed tests sub-package

* Fri Jan 25 2013 Remi Collet <RPMS@famillecollet.com> 1.1.0-1
- backport 1.1.0 for remi repo

* Tue Jan 22 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-1
- Initial package
