# remirepo/fedora spec file for php-ircmaxell-security-lib
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    f3db6de12c20c9bcd1aa3db4353a1bbe0e44e1b5
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     ircmaxell
%global gh_project   SecurityLib
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-ircmaxell-security-lib
Version:        1.1.0
Release:        4%{?dist}
Summary:        A Base Security Library

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

# Upstream patches
Patch0:         %{name}-upstream.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.2
BuildRequires:  php-bcmath
BuildRequires:  php-gmp
BuildRequires:  php-hash
BuildRequires:  %{_bindir}/phpab
BuildRequires:  %{_bindir}/phpunit
#      "mikey179/vfsStream": "1.1.*", ignore max version on purpose
# 1.6.0 is first version with autoloader
BuildRequires:  php-composer(mikey179/vfsStream) >= 1.6
%endif

# From composer.json
#      "php": ">=5.3.2"
Requires:       php(language) >= 5.3.2
# From phpcompatinfo report for version 1.0.0
Requires:       php-hash
Requires:       php-reflection
Requires:       php-spl
%if 0%{?fedora} > 21
Suggests:       php-bcmath
Suggests:       php-gmp
%endif

Provides:       php-composer(ircmaxell/security-lib) = %{version}


%description
This is a base set of libraries used in other projects.
This isn't useful on its own...

Optional dependency: php-gmp or php-bcmath

Autoloader: %{_datadir}/php/SecurityLib/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}
%patch0 -p1

rm lib/SecurityLib/composer.json


%build
: Generate library autoloader
%{_bindir}/phpab \
    --output lib/SecurityLib/autoload.php \
    lib/SecurityLib


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{_datadir}/php
cp -pr lib/* %{buildroot}%{_datadir}/php


%check
%if %{with_tests}
: Generate test suite autoloader
%{_bindir}/phpab \
    --output test/autoload.php \
    test

mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once __DIR__ . '/../test/autoload.php';
require_once '%{_datadir}/php/org/bovigo/vfs/autoload.php';
require_once '%{buildroot}%{_datadir}/php/SecurityLib/autoload.php';
EOF

: Run test suite
%{_bindir}/phpunit --verbose

if which php70; then
   php70 %{_bindir}/phpunit --verbose
fi
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{_datadir}/php/SecurityLib


%changelog
* Thu Jan 14 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-4
- add upstream patches to fix test suite

* Thu Jan 14 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-3
- add autoloader

* Fri Mar 20 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0
- add LICENSE file

* Wed Aug 13 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- drop composer.json from library path

* Wed Aug 13 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
