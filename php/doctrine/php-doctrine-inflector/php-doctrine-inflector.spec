#
# RPM spec file for php-doctrine-inflector
#
# Copyright (c) 2013-2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      inflector
%global github_version   1.0.1
%global github_commit    0bcb2e79d8571787f18b7eb036ed3d004908e604

%global composer_vendor  doctrine
%global composer_project inflector

# "php": ">=5.3.2"
%global php_min_ver      5.3.2

# Build using "--without tests" to disable tests
%global with_tests       %{?_without_tests:0}%{!?_without_tests:1}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       Common string manipulations with regard to casing and singular/plural rules

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
%if %{with_tests}
# For tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-phpunit-PHPUnit
# For tests: phpcompatinfo (computed from version 1.0.1)
BuildRequires: php-pcre
BuildRequires: php-spl
%endif

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.0.1)
Requires:      php-pcre

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Doctrine Inflector is a small library that can perform string manipulations
with regard to upper-/lowercase and singular/plural forms of words.


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/php
cp -rp lib/* %{buildroot}/%{_datadir}/php/


%check
%if %{with_tests}
%{_bindir}/phpunit
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md composer.json
%dir %{_datadir}/php/Doctrine
%dir %{_datadir}/php/Doctrine/Common
     %{_datadir}/php/Doctrine/Common/Inflector


%changelog
* Sun Dec 28 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.1-2
- %%license usage

* Sun Dec 28 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.1-1
- Updated to 1.0.1 (BZ #1176943)

* Fri Jun 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0-4.20131221gita81c334
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide
- Added option to build without tests ("--without tests")

* Sat Jan 11 2014 Remi Collet <rpms@famillecollet.com> 1.0-2.20131221gita81c334
- backport for remi repo

* Mon Jan 06 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0-2.20131221gita81c334
- Conditional %%{?dist}

* Mon Dec 23 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0-1.20131221gita81c334
- Initial package
