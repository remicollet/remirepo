# remirepo/fedora spec file for php-zetacomponents-graph
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit    7efda09f967b92fe38a1fbf0c2090fc4fedb0c73
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zetacomponents
%global gh_project   Graph
%global cname        graph
%global ezcdir       %{_datadir}/php/ezc
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{cname}
Version:        1.5.2
Release:        5%{?dist}
Summary:        Zeta Graph Component

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://zetacomponents.org/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# https://github.com/zetacomponents/Graph/pull/16
Patch0:         %{name}-pr16.patch
# Upstream
Patch1:         %{name}-upstream.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-gd
BuildRequires:  php-composer(%{gh_owner}/base) >= 1.8
BuildRequires:  php-composer(%{gh_owner}/unit-test)
%if 0%{?fedora} > 24
# Used for the test suite
BuildRequires:  glibc-langpack-en
BuildRequires:  glibc-langpack-de
%endif
%endif

# From composer.json, "require": {
#            "zetacomponents/base": "~1.8"
Requires:       php-composer(%{gh_owner}/base) >= 1.8
Requires:       php-composer(%{gh_owner}/base) <  2
# From composer.json, "suggest": {
#            "ext-gd": "Used by the GD driver, one of the choices for generating bitmap images."
Requires:       php-gd
# From phpcompatinfo report for 1.5.2
Requires:       php(language) > 5.3
Requires:       php-date
Requires:       php-dom
Requires:       php-gd
Requires:       php-pcre
Requires:       php-simplexml
Requires:       php-spl
Requires:       php-xml

Provides:       php-composer(%{gh_owner}/%{cname}) = %{version}


%description
A component for creating pie charts, line graphs and other kinds of diagrams.

Documentation is available in the %{name}-doc package.


%package doc
Summary:  Documentation for %{name}
Group:    Documentation
# For License
Requires: %{name} = %{version}-%{release}

%description doc
%{summary}.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1
%patch1 -p1

: Drop bundled fonts
rm docs/tutorial/tutorial_font.*
sed -e 's:tutorial_font.ttf:/usr/share/fonts/gnu-free/FreeSans.ttf:' \
    -i docs/tutorial/*php


%build
: Generate a simple autoloader
%{_bindir}/phpab \
   --output src/autoloader.php \
   src
cat <<EOF | tee -a  src/autoloader.php
# Dependencies
require_once '%{ezcdir}/Base/autoloader.php';
EOF


%install
rm -rf   %{buildroot}
mkdir -p %{buildroot}%{ezcdir}/autoload

: The library
cp -pr src \
       %{buildroot}%{ezcdir}/%{gh_project}
: For ezcBase autoloader
cp -pr src/*_autoload.php \
       %{buildroot}%{ezcdir}/autoload


%check
%if %{with_tests}
: Create test autoloader
mkdir vendor
cat <<EOF | tee vendor/autoload.php
<?php
require '%{ezcdir}/UnitTest/autoloader.php';
require '%{buildroot}%{ezcdir}/%{gh_project}/autoloader.php';
EOF

: Ignore test with erratic result
sed -e 's/testBarChartWithSingleDataPointNumericAxis/SKIP_testBarChartWithSingleDataPointNumericAxis/' \
    -i tests/chart_test.php

: Run test test suite
%{_bindir}/phpunit

if which php70; then
   php70 %{_bindir}/phpunit
fi
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE* CREDITS
%doc ChangeLog
%doc composer.json
%{ezcdir}/autoload/*
%{ezcdir}/%{gh_project}

%files doc
%defattr(-,root,root,-)
%doc docs design


%changelog
* Mon Feb 29 2016 Remi Collet <remi@fedoraproject.org> - 1.5.2-5
- add BR glibc-langpack-en, glibc-langpack-de for test suite
  FTBFS detected by Koschei
- ignore 1 test with erratic result

* Mon Jul 13 2015 Remi Collet <remi@fedoraproject.org> - 1.5.2-3
- create subpackage for documentation
- minor improvments, from review #1228090 comments

* Thu Jun  4 2015 Remi Collet <remi@fedoraproject.org> - 1.5.2-2
- add upstream patch for LICENSE file

* Wed Jun  3 2015 Remi Collet <remi@fedoraproject.org> - 1.5.2-1
- initial package
- open https://github.com/zetacomponents/Graph/pull/16
