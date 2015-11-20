# remirepo/fedora spec file for php-tecnickcom-tc-lib-pdf-parser
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    c1d0a6109e325429cef4fa508af82d828f3b943f
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global c_vendor     tecnickcom
%global gh_owner     tecnickcom
%global gh_project   tc-lib-pdf-parser
%global php_project  %{_datadir}/php/Com/Tecnick/Pdf/Parser
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.1.10
Release:        1%{?dist}
Summary:        PHP library to parse PDF documents

Group:          Development/Libraries
License:        LGPLv3+
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{?gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# For tests
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-composer(%{c_vendor}/tc-lib-pdf-filter)
BuildRequires:  php-pcre
%endif

# From composer.json, "require": {
#        "php": ">=5.3.3"
#        "tecnick.com/tc-lib-pdf-filter": "dev-master"
Requires:       php(language) >= 5.3.3
Requires:       php-composer(%{c_vendor}/tc-lib-pdf-filter)
# From phpcompatinfo report for version 2.1.0
Requires:       php-pcre

# Composer
Provides:       php-composer(%{c_vendor}/%{gh_project}) = %{version}
# Upstream package name
Provides:       php-%{gh_project} = %{version}


%description
PHP library to parse PDF documents.

The initial source code has been extracted from TCPDF (http://www.tcpdf.org).


%prep
%setup -q -n %{gh_project}-%{gh_commit}

: Sanity check
grep -q '^%{version}$' VERSION

: Fix the examples
sed -e 's:^require:////require:' \
    -e 's:^//require:require:'   \
    -e 's:../resources/test/::'  \
    -i example/*php
ln resources/test/example_036.pdf example


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
require '%{php_project}/../Filter/autoload.php';
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
%license LICENSE.TXT
%doc composer.json
%doc README.md example
%{php_project}


%changelog
* Fri Nov 20 2015 Remi Collet <remi@fedoraproject.org> - 2.1.10-1
- update to 2.1.10 (no change)

* Wed Nov 18 2015 Remi Collet <remi@fedoraproject.org> - 2.1.8-1
- update to 2.1.8 (no change)
- run test suite with both PHP 5 and 7 when available

* Tue Oct 20 2015 Remi Collet <remi@fedoraproject.org> - 2.1.7-1
- update to 2.1.7 (no change)

* Fri Sep 25 2015 Remi Collet <remi@fedoraproject.org> - 2.1.6-1
- update to 2.1.6 (no change)

* Sun Sep 13 2015 Remi Collet <remi@fedoraproject.org> - 2.1.4-1
- update to 2.1.4
- provide php-composer(tecnickcom/tc-lib-pdf-parser)

* Fri Jul 24 2015 Remi Collet <remi@fedoraproject.org> - 2.1.3-1
- update to 2.1.3 (no change)

* Thu Jul  2 2015 Remi Collet <remi@fedoraproject.org> - 2.1.2-1
- update to 2.1.2
- drop patches merged/fixed upstream

* Thu Jul  2 2015 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- initial package, version 2.1.0
- open https://github.com/tecnickcom/tc-lib-pdf-parser/pull/1
  fix autoloader
- open https://github.com/tecnickcom/tc-lib-pdf-parser/pull/2
  php < 5.5 compatibility
