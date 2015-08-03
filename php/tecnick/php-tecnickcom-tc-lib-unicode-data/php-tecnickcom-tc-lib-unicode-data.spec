# remirepo/fedora spec file for php-tecnickcom-tc-lib-unicode-data
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    d638e699520881b1b866a5e4486e26c4ea3f325a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global c_vendor     tecnick.com
%global gh_owner     tecnickcom
%global gh_project   tc-lib-unicode-data
%global php_project  %{_datadir}/php/Com/Tecnick/Unicode/Data
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.2.0
Release:        1%{?dist}
Summary:        PHP library containing UTF-8 font definitions

Group:          Development/Libraries
License:        LGPLv3+
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{?gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# For tests
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php(language) >= 5.3.3
%endif

# From composer.json, "require": {
#        "php": ">=5.3.3"
Requires:       php(language) >= 5.3.3
# From phpcompatinfo report for version 1.1.1
# Only Core

# Library renamed (not provided as not compatible)
Obsoletes:      php-tecnickcom-tc-lib-pdf-font-data < 1.2
# Composer
Provides:       php-composer(%{c_vendor}/%{gh_project}) = %{version}
# Upstream package name
Provides:       php-%{gh_project} = %{version}


%description
PHP library containing UTF-8 font definitions.

The initial source code has been extracted from TCPDF (http://www.tcpdf.org).


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
EOF

%{_bindir}/phpunit --verbose
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.TXT
%doc composer.json
%doc README.md
%dir %{_datadir}/php/Com
%dir %{_datadir}/php/Com/Tecnick
%dir %{_datadir}/php/Com/Tecnick/Unicode
%{php_project}


%changelog
* Mon Aug  3 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- renamed from pdf-font-data to unicode-data

* Mon Aug  3 2015 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- update to 1.1.4

* Fri Jul 24 2015 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- update to 1.1.3 (no change)

* Thu Jul  2 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- initial package, version 1.1.1