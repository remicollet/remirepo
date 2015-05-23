# remirepo spec file for php-pimple1, from:
#
# Fedora spec file for php-pimple1
#
# Copyright (c) 2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     silexphp
%global github_name      Pimple
%global github_version   1.1.1
%global github_commit    2019c145fe393923f3441b23f29bbdfaa5c58c4d

%global composer_vendor  pimple
%global composer_project pimple

# "php": ">=5.3.0"
%global php_min_ver 5.3.0

# Build using "--without tests" to disable tests
%global with_tests  %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_project}1
Version:       %{github_version}
Release:       4%{?dist}
Summary:       A simple dependency injection container for PHP

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}/tree/1.1
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Autoload generation
BuildRequires: %{_bindir}/phpab
# Tests
%if %{with_tests}
BuildRequires: %{_bindir}/phpunit
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
## phpcompatinfo (computed from version 1.1.1)
BuildRequires: php-spl
%endif

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.1.1)
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Pimple is a small dependency injection container for PHP that consists of
just one file and one class.


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Generate autoloader
%{_bindir}/phpab --nolower --output lib/autoload.php lib


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}/Pimple1
cp -pr lib/* %{buildroot}%{phpdir}/Pimple1/


%check
%if %{with_tests}
: Recreate test bootstrap
rm -f tests/bootstrap.php
%{_bindir}/phpab --nolower --output tests/bootstrap.php tests
cat >> tests/bootstrap.php <<'BOOTSTRAP'

require '%{buildroot}%{phpdir}/Pimple1/autoload.php';
BOOTSTRAP

: Run tests
%{_bindir}/phpunit
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.rst
%doc composer.json
%{phpdir}/Pimple1


%changelog
* Sat May 23 2015 Remi Collet <rpms@famillecollet.com> - 1.1.1-4
- add backport stuff for remi repo.

* Fri May 22 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.1-4
- Wrap tests' build requires in "%%if %%{with_tests}"

* Wed May 20 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.1-3
- No rename and no conflict because the lib directory was changed from
  "%%{phpdir}/Pimple" to "%%{phpdir}/Pimple1".  This is possible because
  this library is not PSR-0 compliant so we can define whatever lib directory
  we want.

* Sun May 17 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.1-2
- Add missing %%{_bindir}/phpab build dependency

* Sun May 17 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.1-1
- Rename of php-Pimple version 1 to php-pimple1
