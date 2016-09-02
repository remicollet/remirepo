# remirepo/fedora spec file for php-tecnickcom-tc-lib-pdf-graph
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    00b479529d98adacbbb9cc3a7ef7d6d73eb9cd60
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global c_vendor     tecnickcom
%global gh_owner     tecnickcom
%global gh_project   tc-lib-pdf-graph
%global php_project  %{_datadir}/php/Com/Tecnick/Pdf/Graph
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.4.1
Release:        1%{?dist}
Summary:        PHP library containing PDF graphic and geometric methods

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
BuildRequires:  php-composer(%{c_vendor}/tc-lib-color) >= 1.12.1
BuildRequires:  php-composer(%{c_vendor}/tc-lib-pdf-encrypt) >= 1.4.3
%endif

# From composer.json, "require": {
#        "php": ">=5.4"
#        "tecnickcom/tc-lib-color": "^1.12.1",
#        "tecnickcom/tc-lib-pdf-encrypt": "^1.4.3"
Requires:       php(language) >= 5.4
Requires:       php-composer(%{c_vendor}/tc-lib-color) >= 1.12.1
Requires:       php-composer(%{c_vendor}/tc-lib-color) <  2
Requires:       php-composer(%{c_vendor}/tc-lib-pdf-encrypt) >= 1.4.3
Requires:       php-composer(%{c_vendor}/tc-lib-pdf-encrypt) <  2
# From phpcompatinfo report for version 1.4.1
Requires:       php-zlib

# Composer
Provides:       php-composer(%{c_vendor}/%{gh_project}) = %{version}
# Upstream package name
Provides:       php-%{gh_project} = %{version}


%description
PHP library containing PDF graphic and geometric methods.

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
require '%{php_project}/../../Color/autoload.php';
EOF

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose
# remirepo:2
fi
exit $ret
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
%dir %{_datadir}/php/Com/Tecnick/Pdf
%{php_project}


%changelog
* Fri Sep  2 2016 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- update to 1.4.1
- raise dependency on tecnickcom/tc-lib-color >= 1.12.1
- add dependency on tecnickcom/tc-lib-pdf-encrypt

* Tue Jun 14 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0 (no change)

* Fri Mar  4 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2 (no change)

* Fri Jan 15 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- initial package, version 1.0.1

