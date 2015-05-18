#
# RPM spec file for php-whitehat101-apr1-md5
#
# Copyright (c) 2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     whitehat101
%global github_name      apr1-md5
%global github_version   1.0.0
%global github_commit    8b261c9fc0481b4e9fa9d01c6ca70867b5d5e819

%global composer_vendor  whitehat101
%global composer_project apr1-md5

# "php": ">=5.3.0"
%global php_min_ver 5.3.0

# Build using "--without tests" to disable tests
%global with_tests %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Apache's APR1-MD5 algorithm in pure PHP

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# For autoload generation
BuildRequires: %{_bindir}/phpab
%if %{with_tests}
# For tests
## composer.json
BuildRequires: %{_bindir}/phpunit
BuildRequires: php(language) >= %{php_min_ver}
## phpcompatinfo (computed from version 1.0.0)
BuildRequires: php-openssl
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.0.0)
Requires:      php-openssl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
A tested, referenced, documented, and packaged implementation of Apache's APR1
MD5 Hashing Algorithm in pure PHP.


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Generate autoloader
%{_bindir}/phpab --nolower --output src/autoload.php src


%install
mkdir -p %{buildroot}%{phpdir}/WhiteHat101/Crypt
cp -rp src/* %{buildroot}%{phpdir}/WhiteHat101/Crypt/


%check
%if %{with_tests}
%{_bindir}/phpunit \
    --bootstrap %{buildroot}%{phpdir}/WhiteHat101/Crypt/autoload.php
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%doc composer.json
%dir %{phpdir}/WhiteHat101
     %{phpdir}/WhiteHat101/Crypt


%changelog
* Sat May 16 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.0-1
- Initial package
