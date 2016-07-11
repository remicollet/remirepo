# remirepo/fedora spec file for php-tecnickcom-tc-lib-barcode
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    220728e5f659b935348442e8d1d3e46fd5f9e178
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global c_vendor     tecnickcom
%global gh_owner     tecnickcom
%global gh_project   tc-lib-barcode
%global php_project  %{_datadir}/php/Com/Tecnick/Barcode
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.9.2
Release:        1%{?dist}
Summary:        PHP library to generate linear and bidimensional barcodes

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
BuildRequires:  php-composer(%{c_vendor}/tc-lib-color) >= 1.10.0
BuildRequires:  php-bcmath
BuildRequires:  php-date
BuildRequires:  php-gd
BuildRequires:  php-pcre
# Optional but required for test
BuildRequires:  php-pecl-imagick
%endif

# From composer.json, "require": {
#        "php": ">=5.4"
#        "tecnickcom/tc-lib-color": "^1.11.0"
Requires:       php(language) >= 5.4
Requires:       php-composer(%{c_vendor}/tc-lib-color) >= 1.11.0
Requires:       php-composer(%{c_vendor}/tc-lib-color) <  2
# From phpcompatinfo report for version 1.1.2
Requires:       php-bcmath
Requires:       php-date
Requires:       php-gd
Requires:       php-pcre

# Composer
Provides:       php-composer(%{c_vendor}/%{gh_project}) = %{version}
# Upstream package name
Provides:       php-%{gh_project} = %{version}


%description
Provides tc-lib-barcode: PHP classes to generate linear and bidimensional
barcodes: CODE 39, ANSI MH10.8M-1983, USD-3, 3 of 9, CODE 93, USS-93,
Standard 2 of 5, Interleaved 2 of 5, CODE 128 A/B/C, 2 and 5 Digits
UPC-Based Extension, EAN 8, EAN 13, UPC-A, UPC-E, MSI, POSTNET, PLANET,
RMS4CC (Royal Mail 4-state Customer Code), CBC (Customer Bar Code),
KIX (Klant index - Customer index), Intelligent Mail Barcode, Onecode,
USPS-B-3200, CODABAR, CODE 11, PHARMACODE, PHARMACODE TWO-TRACKS, Datamatrix
ECC200, QR-Code, PDF417.

Optional dependency: php-pecl-imagick


%prep
%setup -q -n %{gh_project}-%{gh_commit}

: Sanity check
grep -q '^%{version}$' VERSION

: Fix the examples
sed -e 's:^require:////require:' \
    -e 's:^//require:require:'   \
    -i example/*php


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
require '%{php_project}/../Color/autoload.php';
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
%doc README.md example
%{php_project}


%changelog
* Mon Jul 11 2016 Remi Collet <remi@fedoraproject.org> - 1.9.2-1
- update to 1.9.2

* Tue Jun 14 2016 Remi Collet <remi@fedoraproject.org> - 1.9.0-1
- update to 1.9.0 (no change)

* Thu Mar 10 2016 Remi Collet <remi@fedoraproject.org> - 1.8.0-1
- update to 1.8.0
- raise dependency on tecnickcom/tc-lib-color >= 1.10.0

* Fri Mar  4 2016 Remi Collet <remi@fedoraproject.org> - 1.7.3-1
- update to 1.7.3

* Mon Feb 29 2016 Remi Collet <remi@fedoraproject.org> - 1.7.2-1
- update to 1.7.2

* Tue Dec 15 2015 Remi Collet <remi@fedoraproject.org> - 1.7.1-1
- update to 1.7.1 (no change)

* Fri Dec 11 2015 Remi Collet <remi@fedoraproject.org> - 1.7.0-1
- update to 1.7.0 (no change)
- raise dependency on php >= 5.4
- raise dependency on tecnickcom/tc-lib-color ^1.8.0

* Fri Dec 11 2015 Remi Collet <remi@fedoraproject.org> - 1.6.8-1
- update to 1.6.8 (no change)

* Tue Dec  8 2015 Remi Collet <remi@fedoraproject.org> - 1.6.6-1
- update to 1.6.6 (no change)

* Mon Dec  7 2015 Remi Collet <remi@fedoraproject.org> - 1.6.5-1
- update to 1.6.5 (no change)

* Thu Dec  3 2015 Remi Collet <remi@fedoraproject.org> - 1.6.3-1
- update to 1.6.3 (no change)

* Fri Nov 27 2015 Remi Collet <remi@fedoraproject.org> - 1.6.1-1
- update to 1.6.1 (no change)

* Wed Nov 25 2015 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- update to 1.6.0

* Fri Nov 20 2015 Remi Collet <remi@fedoraproject.org> - 1.5.6-1
- update to 1.5.6 (no change)

* Fri Nov 20 2015 Remi Collet <remi@fedoraproject.org> - 1.5.4-1
- update to 1.5.4 (no change)

* Wed Nov 18 2015 Remi Collet <remi@fedoraproject.org> - 1.5.2-1
- update to 1.5.2 (no change)
- run test suite with both PHP 5 and 7 when available

* Wed Nov  4 2015 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- update to 1.5.0

* Tue Oct 20 2015 Remi Collet <remi@fedoraproject.org> - 1.4.7-1
- update to 1.4.7 (no change)

* Fri Sep 25 2015 Remi Collet <remi@fedoraproject.org> - 1.4.6-1
- update to 1.4.6 (no change)

* Sun Sep 13 2015 Remi Collet <remi@fedoraproject.org> - 1.4.3-1
- update to 1.4.3
- provide php-composer(tecnickcom/tc-lib-barcode)

* Thu Aug 27 2015 Remi Collet <remi@fedoraproject.org> - 1.4.2-1
- update to 1.4.2

* Tue Aug 25 2015 Remi Collet <remi@fedoraproject.org> - 1.4.1-3
- add patch for PHP 5.3
  https://github.com/tecnickcom/tc-lib-barcode/pull/7

* Wed Aug 12 2015 Remi Collet <remi@fedoraproject.org> - 1.4.1-2
- fix package summary

* Tue Aug 11 2015 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- update to 1.4.1

* Tue Aug 11 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- update to 1.4.0

* Sat Aug  8 2015 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- update to 1.3.1

* Thu Aug  6 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- update to 1.3.0

* Fri Jul 24 2015 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- update to 1.2.1 (no change)

* Thu Jul  2 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0

* Wed Jul  1 2015 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- update to 1.1.3
- drop patch merged upstream

* Wed Jul  1 2015 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- initial package, version 1.1.2
- open https://github.com/tecnickcom/tc-lib-barcode/pull/2
  PHP < 5.5 compatibility
