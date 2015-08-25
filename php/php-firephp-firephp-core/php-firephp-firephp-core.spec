#
# Fedora spec file for php-firephp-firephp-core
#
# Copyright (c) 2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     firephp
%global github_name      firephp-core
%global github_version   0.4.0
%global github_commit    fabad0f2503f9577fe8dd2cb1d1c7cd73ed2aacf

%global composer_vendor  firephp
%global composer_project firephp-core

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Traditional FirePHPCore library for sending PHP variables to the browser

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: %{_bindir}/phpunit
## phpcompatinfo (computed from version 0.4.0)
BuildRequires: php(language) >= 5.3.0
BuildRequires: php-json
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
BuildRequires: php-xml
%endif

# phpcompatinfo (computed from version 0.4.0)
Requires:      php(language) >= 5.3.0
Requires:      php-json
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-xml
# Autoloader
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
FirePHP is an advanced logging system that can display PHP variables in the
browser as an application is navigated. All communication is out of band to
the application meaning that the logging data will not interfere with the
normal functioning of the application.


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing to build


%install
: Lib
mkdir -p %{buildroot}%{phpdir}
cp -rp lib/* %{buildroot}%{phpdir}/

: Autoloader
ln -s fb.php %{buildroot}%{phpdir}/FirePHPCore/autoload.php


%check
%if %{with_tests}
pushd tests
    %{_bindir}/phpunit --verbose .
popd
%else
: Tests skipped
%endif


%files
# README re-used as license file since it has full license text
%{?_licensedir:%license README.md}
%doc *.md
%doc composer.json
%{phpdir}/FirePHPCore
%exclude %{phpdir}/FirePHPCore/*.php4


%changelog
* Tue Aug 18 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.4.0-1
- Initial package
