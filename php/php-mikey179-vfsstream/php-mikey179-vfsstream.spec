# spec file for php-mikey179-vfsstream
#
# Copyright (c) 2012-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    063fb10633f10c5ccbcac26227e94f46d9336f90
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     mikey179
%global gh_project   vfsStream
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-mikey179-vfsstream
Version:        1.2.0
Release:        1%{?dist}
Summary:        PHP stream wrapper for a virtual file system

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
%endif

# From composer.json
Requires:       php(language) >= 5.3
# From phpcompatifo report for 1.2.0
Requires:       php-date
Requires:       php-posix
Requires:       php-spl


%description
vfsStream is a PHP stream wrapper for a virtual file system that may be
helpful in unit tests to mock the real file system.

It can be used with any unit test framework, like PHPUnit or SimpleTest.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Nothing


%install
rm -rf                  %{buildroot}
mkdir -p                %{buildroot}%{_datadir}/php
cp -pr src/main/php/org %{buildroot}%{_datadir}/php/org


%if %{with_tests}
%check
: generate the bootstrap/autoloader
phpab --output src/main/php/bs.php src/main/php

: run test suite
phpunit \
  --bootstrap src/main/php/bs.php \
  -d date.timezone=UTC
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE
%doc CHANGES composer.json

%dir %{_datadir}/php/org
%dir %{_datadir}/php/org/bovigo
     %{_datadir}/php/org/bovigo/vfs


%changelog
* Tue May 13 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- initial package