# spec file for php-andrewsville-php-token-reflection
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    e6d0ac2baf66cdf154be34c3d2a2aa1bd4b426ee
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     Andrewsville
%global gh_project   PHP-Token-Reflection
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-andrewsville-php-token-reflection
Version:        1.4.0
Release:        1%{?dist}
Summary:        Library emulating the PHP internal reflection

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
# https://github.com/Andrewsville/PHP-Token-Reflection/issues/68
# run mksrc.sh to create the tarball from a git snapshot
Source0:        %{name}-%{version}-%{gh_short}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3
%if %{with_tests}
BuildRequires:  %{_bindir}/phpab
BuildRequires:  %{_bindir}/phpunit
%endif

# From composer.json
#       "php": ">=5.3.0",
#       "ext-tokenizer": "*"
Requires:       php(language) >= 5.3
Requires:       php-tokenizer
# From phpcompatifo report for 1.4.0
Requires:       php-pcre
Requires:       php-phar
Requires:       php-reflection
Requires:       php-spl

Provides:       php-composer(andrewsville/php-token-reflection) = %{version}


%description
This library emulates the PHP reflection model using the tokenized PHP source.

%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Nothing


%install
rm -rf                 %{buildroot}
mkdir -p               %{buildroot}%{_datadir}/php
cp -pr TokenReflection %{buildroot}%{_datadir}/php/TokenReflection


%if %{with_tests}
%check
: generate the bootstrap/autoloader
%{_bindir}/phpab --output TokenReflection/bs.php TokenReflection

: run test suite
%{_bindir}/phpunit --bootstrap TokenReflection/bs.php \
  tests || : results ignored for now, known upstream issues
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc README.md composer.json
%{_datadir}/php/TokenReflection


%changelog
* Tue Mar 31 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- initial package