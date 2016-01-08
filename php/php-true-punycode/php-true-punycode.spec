# remirepo/fedora spec file for php-true-punycode
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    74fa01d4de396c40e239794123b3874cb594a30c
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     true
%global gh_project   php-punycode
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

# Notice: single file / class, so no need to provide an autoloader for now

Name:           php-true-punycode
Version:        2.0.2
Release:        1%{?dist}
Summary:        A Bootstring encoding of Unicode for IDNA

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-mbstring
BuildRequires:  %{_bindir}/phpunit

# From composer.json
#      "php": ">=5.3.0"
#      "ext-mbstring": "*"
Requires:       php(language) >= 5.3.3
Requires:       php-mbstring

Provides:       php-composer(true/punycode) = %{version}


%description
A Bootstring encoding of Unicode for Internationalized Domain Names
in Applications (IDNA).


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Nothing


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{_datadir}/php
cp -pr src %{buildroot}%{_datadir}/php/TrueBV


%check
%if %{with_tests}
: Run test suite
%{_bindir}/phpunit --bootstrap src/Punycode.php

if which php70; then
   php70 %{_bindir}/phpunit --bootstrap src/Punycode.php
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
%{_datadir}/php/TrueBV


%changelog
* Fri Jan  8 2016 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- update to version 2.0.2
- run test suite with both PHP 5 and 7 when available

* Wed Sep  2 2015 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to version 2.0.1 (no change)

* Sun Aug  9 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to version 2.0.0

* Mon May 18 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to version 1.1.0

* Wed Jan  7 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- initial package