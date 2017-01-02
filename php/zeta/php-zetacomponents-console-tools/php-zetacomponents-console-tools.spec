# remirepo/fedora spec file for php-zetacomponents-console-tools
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit    30d67e9d04f458ac8cae4c49e50f81061460ff2c
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zetacomponents
%global gh_project   ConsoleTools
%global cname        console-tools
%global ezcdir       %{_datadir}/php/ezc
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{cname}
Version:        1.7
Release:        3%{?dist}
Summary:        Zeta %{gh_project} Component

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://zetacomponents.org/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# Upstream patches
Patch0:         %{name}-upstream.patch
# https://github.com/zetacomponents/ConsoleTools/pull/8
Patch1:         %{name}-pr8.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-composer(%{gh_owner}/base) >= 1.8
BuildRequires:  php-composer(%{gh_owner}/unit-test)
%endif

# From composer.json, "require": {
#            "zetacomponents/base": "~1.8"
Requires:       php-composer(%{gh_owner}/base) >= 1.8
Requires:       php-composer(%{gh_owner}/base) <  2
# From phpcompatinfo report for 1.7
Requires:       php(language) > 5.3
Requires:       php-iconv
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(%{gh_owner}/%{cname}) = %{version}


%description
A set of classes to do different actions with the console, also called shell.
It can render a progress bar, tables and a status bar and contains a class for
parsing command line options.

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

: Drop assertion which rely on path in sources dir
sed -e '/realpath/d' -i tests/statusbar_test.php

: Run test test suite
%{_bindir}/phpunit --exclude-group interactive
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
* Mon Jul 13 2015 Remi Collet <remi@fedoraproject.org> - 1.7-3
- create subpackage for documentation
- minor improvments, from review #1228091 comments

* Thu Jun  4 2015 Remi Collet <remi@fedoraproject.org> - 1.7-2
- fix summary

* Wed Jun  3 2015 Remi Collet <remi@fedoraproject.org> - 1.7-1
- initial package
- open https://github.com/zetacomponents/ConsoleTools/pull/8 interactive