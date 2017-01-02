# remirepo/fedora spec file for php-zetacomponents-base
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit    f20df24e8de3e48b6b69b2503f917e457281e687
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zetacomponents
%global gh_project   Base
%global cname        base
%global ezcdir       %{_datadir}/php/ezc
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{cname}
Version:        1.9
Release:        2%{?dist}
Summary:        Zeta Base Component

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://zetacomponents.org/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# Use old PEAR layout
Patch0:         %{name}-layout.patch
# Upstream
Patch1:         %{name}-upstream.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  %{_bindir}/convert
BuildRequires:  php-composer(%{gh_owner}/unit-test)
BuildRequires:  php-posix
%endif

# From phpcompatinfo report for 1.9
Requires:       php(language) > 5.3
Requires:       php-pcre
Requires:       php-posix
Requires:       php-simplexml
Requires:       php-spl

Provides:       php-composer(%{gh_owner}/%{cname}) = %{version}


%description
This is the base package of the Zeta components, offering the basic
support that all Components need. In the first version this will be the
autoload support.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p0
%patch1 -p1


%build
: Generate a simple autoloader
%{_bindir}/phpab \
   --output src/autoloader.php \
   src


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
: Ignore test relying on composer layout
rm tests/file_find_recursive_test.php

: Create test autoloader
mkdir vendor
cat <<EOF | tee vendor/autoload.php
<?php
require '%{ezcdir}/UnitTest/autoloader.php';
require '$PWD/src/autoloader.php';
EOF

: Run test test suite
%{_bindir}/phpunit
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
%doc docs design
%dir %{ezcdir}
%dir %{ezcdir}/autoload
     %{ezcdir}/autoload/*_autoload.php
     %{ezcdir}/%{gh_project}


%changelog
* Thu Jun  4 2015 Remi Collet <remi@fedoraproject.org> - 1.9-2
- add upstream patch for LICENSE file

* Wed Jun  3 2015 Remi Collet <remi@fedoraproject.org> - 1.9-1
- initial package
- open https://github.com/zetacomponents/UnitTest/issues/4 License