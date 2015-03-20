# spec file for php-ircmaxell-security-lib
#
# Copyright (c) 2014-2015 Remi Collet
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
Release:        1%{?dist}
Summary:        A Base Security Library

Group:          Development/Libraries
# See class headers
# LICENSE file will be in next version
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.2
BuildRequires:  php-bcmath
BuildRequires:  php-hash
BuildRequires:  %{_bindir}/phpab
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-theseer-autoload
#      "mikey179/vfsStream": "1.1.*", ignore max version on purpose
BuildRequires:  php-composer(mikey179/vfsStream) >= 1.1
%endif

# From composer.json
#      "php": ">=5.3.2"
Requires:       php(language) >= 5.3.2
# From phpcompatinfo report for version 1.0.0
Requires:       php-hash
Requires:       php-reflection
Requires:       php-spl
# optional php-bcmath or php-gmp

Provides:       php-composer(ircmaxell/security-lib) = %{version}


%description
This is a base set of libraries used in other projects.
This isn't useful on its own...

Optional dependency: php-gmp or php-bcmath


%prep
%setup -q -n %{gh_project}-%{gh_commit}

rm lib/SecurityLib/composer.json


%build
# Nothing


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{_datadir}/php
cp -pr lib/* %{buildroot}%{_datadir}/php


%check
%if %{with_tests}
if %{_bindir}/php -m | grep gmp; then
  : Skip test with GMP load, BCMath expected
else
  : Generate autoloader
  %{_bindir}/php -d date.timezone=UTC \
  %{_bindir}/phpab \
    --basedir $PWD \
    --output autoload.php \
    lib test %{_datadir}/php/org/bovigo/vfs

  : Run test suite
  %{_bindir}/phpunit \
    --bootstrap autoload.php \
    -d date.timezone=UTC
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
* Fri Mar 20 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0
- add LICENSE file

* Wed Aug 13 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- drop composer.json from library path

* Wed Aug 13 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package