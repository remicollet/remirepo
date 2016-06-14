# remirepo/fedora spec file for php-tecnickcom-tc-lib-unicode
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    363376cb4a340dc6d6060aff312ca45d7d0ee77a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global c_vendor     tecnickcom
%global gh_owner     tecnickcom
%global gh_project   tc-lib-unicode
%global php_project  %{_datadir}/php/Com/Tecnick/Unicode
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.3.0
Release:        1%{?dist}
Summary:        PHP library containing Unicode methods

Group:          Development/Libraries
License:        LGPLv3+
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{?gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# For tests
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  php(language) >= 5.4
BuildRequires:  php-composer(%{c_vendor}/tc-lib-unicode-data) >= 1.5.0
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
%endif

# From composer.json, "require": {
#        "php": ">=5.4"
#        "tecnickcom/tc-lib-unicode-data": "^1.6.0"
Requires:       php(language) >= 5.4
Requires:       php-composer(%{c_vendor}/tc-lib-unicode-data) >= 1.6.0
Requires:       php-composer(%{c_vendor}/tc-lib-unicode-data) <  2
# From phpcompatinfo report for version 1.2.1
Requires:       php-mbstring
Requires:       php-pcre

# Composer
Provides:       php-composer(%{c_vendor}/%{gh_project}) = %{version}
# Upstream package name
Provides:       php-%{gh_project} = %{version}


%description
PHP library containing Unicode and UTF-8 methods, including the
Unicode Bidirectional Algorithm.

The initial source code has been derived from TCPDF (http://www.tcpdf.org/).


%prep
%setup -q -n %{gh_project}-%{gh_commit}

: Sanity check
grep -q '^%{version}$' VERSION


%build
# Empty build section, most likely nothing required.


%install
rm -rf     %{buildroot}
mkdir -p   $(dirname %{buildroot}%{php_project})
cp -pr src %{buildroot}%{php_project}
cp -p  resources/autoload.php \
           %{buildroot}%{php_project}/autoload.php


%check
%if %{with_tests}
mkdir vendor
cat <<EOF | tee vendor/autoload.php
<?php
require '%{buildroot}%{php_project}/autoload.php';
require '%{php_project}/Data/autoload.php';
EOF

%{_bindir}/phpunit --verbose

if which php70; then
   php70 %{_bindir}/phpunit --verbose
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
%doc composer.json
%doc README.md
%{php_project}/*


%changelog
* Tue Jun 14 2016 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- update to 1.3.0 (no change)

* Fri Mar  4 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- update to 1.2.2 (no change)

* Fri Jan 15 2016 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- initial package, version 1.2.1

