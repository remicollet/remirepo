# spec file for php-ircmaxell-random-lib
#
# Copyright (c) 2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    0eaad991c1756842f26dfbcbc6effcabb5003d0a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     ircmaxell
%global gh_project   RandomLib
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-ircmaxell-random-lib
Version:        1.0.0
Release:        1%{?dist}
Summary:        A Library For Generating Secure Random Numbers

Group:          Development/Libraries
# See class headers
# LICENSE file will be in next version
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  %{_bindir}/phpab
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php(language) >= 5.3.2
BuildRequires:  php-hash
BuildRequires:  php-openssl
BuildRequires:  php-posix
BuildRequires:  php-spl
BuildRequires:  php-composer(ircmaxell/security-lib) >= 1.0
#      "mikey179/vfsStream": "1.1.*", ignore max version on purpose
BuildRequires:  php-composer(mikey179/vfsStream) >= 1.1
%endif

# From composer.json
#      "php": ">=5.3.2"
#      "ircmaxell/security-lib": "1.0.*@dev",
Requires:       php(language) >= 5.3.2
Requires:       php-composer(ircmaxell/security-lib) >= 1.0
# From phpcompatinfo report for version 1.0.0
Requires:       php-hash
Requires:       php-openssl
Requires:       php-posix
Requires:       php-spl
# optional php-bcmath or php-gmp

Provides:       php-composer(ircmaxell/random-lib) = %{version}


%description
A library for generating random numbers and strings of various strengths.

This library is useful in security contexts.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Nothing


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{_datadir}/php
cp -pr lib/* %{buildroot}%{_datadir}/php


%check
%if %{with_tests}
: Generate autoloader
%{_bindir}/php -d date.timezone=UTC \
%{_bindir}/phpab \
    --basedir $PWD \
    --output autoload.php \
    %{_datadir}/php/org/bovigo/vfs \
    %{_datadir}/php/SecurityLib \
    lib test

: Run test suite
%{_bindir}/phpunit \
    --bootstrap autoload.php \
    -d date.timezone=UTC
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
%{_datadir}/php/RandomLib


%changelog
* Wed Aug 13 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package