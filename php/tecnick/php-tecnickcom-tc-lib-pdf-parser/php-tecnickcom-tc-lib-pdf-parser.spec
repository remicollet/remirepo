# remirepo/fedora spec file for php-tecnickcom-tc-lib-pdf-parser
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    4d1ecdecd96dc6e770351cfca1aeaed72893bbfc
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global c_vendor     tecnickcom
%global gh_owner     tecnickcom
%global gh_project   tc-lib-pdf-parser
%global php_project  %{_datadir}/php/Com/Tecnick/Pdf/Parser
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.3.0
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
BuildRequires:  php(language) >= 5.4
BuildRequires:  php-composer(%{c_vendor}/tc-lib-pdf-filter) >= 1.2.0
BuildRequires:  php-pcre
%endif

# From composer.json, "require": {
#        "php": ">=5.4"
#        "tecnick.com/tc-lib-pdf-filter": "^1.3.0"
Requires:       php(language) >= 5.4
Requires:       php-composer(%{c_vendor}/tc-lib-pdf-filter) >= 1.3.0
Requires:       php-composer(%{c_vendor}/tc-lib-pdf-filter) <  2
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
%license LICENSE
%doc composer.json
%doc README.md example
%{php_project}


%changelog
* Tue Jun 14 2016 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- update to 2.3.0 (no change)

* Fri Mar  4 2016 Remi Collet <remi@fedoraproject.org> - 2.2.3-1
- update to 2.2.3 (no change)

* Tue Jan 12 2016 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- update to 2.2.2

* Tue Dec 15 2015 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- update to 2.2.1 (no change)

* Fri Dec 11 2015 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- update to 2.2.0 (no change)
- raise dependency on php >= 5.4
- raise dependency on tecnickcom/tc-lib-pdf-filter ^1.2.0

* Fri Dec 11 2015 Remi Collet <remi@fedoraproject.org> - 2.1.22-1
- update to 2.1.22 (no change)

* Mon Dec  7 2015 Remi Collet <remi@fedoraproject.org> - 2.1.20-1
- update to 2.1.20 (no change)

* Thu Dec  3 2015 Remi Collet <remi@fedoraproject.org> - 2.1.18-1
- update to 2.1.18 (no change)

* Fri Nov 27 2015 Remi Collet <remi@fedoraproject.org> - 2.1.17-1
- update to 2.1.17 (no change)

* Wed Nov 25 2015 Remi Collet <remi@fedoraproject.org> - 2.1.16-1
- update to 2.1.16 (no change)

* Fri Nov 20 2015 Remi Collet <remi@fedoraproject.org> - 2.1.12-1
- update to 2.1.12 (no change)

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

