%global github_owner   schmittjoh
%global github_name    php-option
%global github_version 1.4.0
%global github_commit  5d099bcf0393908bf4ad69cc47dafb785d51f7f5

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
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
# For tests: phpcompatinfo (computed from 1.4.0)
BuildRequires: php-spl

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from 1.4.0)
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
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing to build


%install
mkdir -pm 0755 %{buildroot}%{_datadir}/php
cp -rp src/%{lib_name} %{buildroot}%{_datadir}/php/


%check
# Rewrite tests' bootstrap
cat > tests/bootstrap.php <<'BOOTSTRAP'
<?php
spl_autoload_register(function ($class) {
    $src = str_replace(array('\\', '_'), '/', $class).'.php';
    @include_once $src;
});
BOOTSTRAP

# Create PHPUnit config w/ colors turned off
sed 's/colors="true"/colors="false"/' phpunit.xml.dist > phpunit.xml

%{_bindir}/phpunit --include-path ./src:./tests -d date.timezone="UTC"


%files
%defattr(-,root,root,-)
%doc LICENSE README.md composer.json
%{_datadir}/php/%{lib_name}

%changelog
* Mon Feb 17 2014 Remi Collet <RPMS@famillecollet.com> 1.4.0-1
- backport 1.4.0 for remi repo

* Wed Feb 12 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.4.0-1
- Updated to 1.4.0 (BZ #1055299)

* Sun Sep 29 2013 Remi Collet <RPMS@famillecollet.com> 1.3.0-1
- backport 1.3.0 for remi repo

* Sat Sep 28 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.0-1
- Updated to 1.3.0
- Other minor updates

* Tue Apr  2 2013 Remi Collet <RPMS@famillecollet.com> 1.2.0-1
- backport 1.2.0 for remi repo

* Sat Mar 30 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.2.0-1
- Updated to version 1.2.0
- Removed tests sub-package

* Fri Jan 25 2013 Remi Collet <RPMS@famillecollet.com> 1.1.0-1
- backport 1.1.0 for remi repo

* Tue Jan 22 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-1
- Initial package
