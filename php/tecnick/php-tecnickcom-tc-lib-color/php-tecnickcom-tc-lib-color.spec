# remirepo/fedora spec file for php-tecnickcom-tc-lib-color
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    6a000b658758e271bf4c41bbc1ce4c685d8a7160
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global c_vendor     tecnickcom
%global gh_owner     tecnickcom
%global gh_project   tc-lib-color
%global php_project  %{_datadir}/php/Com/Tecnick/Color
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.11.0
Release:        1%{?dist}
Summary:        PHP library to manipulate various color representations

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
Requires:       php-pcre
%endif

# From composer.json, "require": {
#        "php": ">=5.4"
Requires:       php(language) >= 5.4
# From phpcompatinfo report for version 1.4.5
Requires:       php-pcre

# Composer
Provides:       php-composer(%{c_vendor}/%{gh_project}) = %{version}
# Upstream package name
Provides:       php-%{gh_project} = %{version}


%description
Provides tc-lib-color: PHP library to manipulate various color
representations (GRAY, RGB, HSL, CMYK) and parse Web colors.

The initial source code has been extracted from TCPDF (http://www.tcpdf.org).


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
%dir %{_datadir}/php/Com
%dir %{_datadir}/php/Com/Tecnick
%{php_project}


%changelog
* Tue Jun 14 2016 Remi Collet <remi@fedoraproject.org> - 1.11.0-1
- update to 1.11.0 (no change)

* Thu Mar 10 2016 Remi Collet <remi@fedoraproject.org> - 1.10.3-1
- update to 1.10.3 (no change)

* Fri Mar  4 2016 Remi Collet <remi@fedoraproject.org> - 1.10.2-1
- update to 1.10.2 (no change)

* Wed Dec 16 2015 Remi Collet <remi@fedoraproject.org> - 1.10.0-1
- update to 1.10.0

* Fri Dec 11 2015 Remi Collet <remi@fedoraproject.org> - 1.8.0-1
- update to 1.8.0 (no change)
- raise dependency on php >= 5.4

* Fri Dec 11 2015 Remi Collet <remi@fedoraproject.org> - 1.7.2-1
- update to 1.7.2

* Mon Dec  7 2015 Remi Collet <remi@fedoraproject.org> - 1.6.18-1
- update to 1.6.18 (no change)

* Thu Dec  3 2015 Remi Collet <remi@fedoraproject.org> - 1.6.16-1
- update to 1.6.16 (no change)

* Fri Nov 27 2015 Remi Collet <remi@fedoraproject.org> - 1.6.15-1
- update to 1.6.15 (no change)

* Wed Nov 25 2015 Remi Collet <remi@fedoraproject.org> - 1.6.14-1
- update to 1.6.14 (no change)

* Fri Nov 20 2015 Remi Collet <remi@fedoraproject.org> - 1.6.10-1
- update to 1.6.10 (no change)

* Fri Nov 20 2015 Remi Collet <remi@fedoraproject.org> - 1.6.8-1
- update to 1.6.8 (no change)

* Wed Nov 18 2015 Remi Collet <remi@fedoraproject.org> - 1.6.5-1
- update to 1.6.5 (no change)
- run test suite with both PHP 5 and 7 when available

* Mon Oct 19 2015 Remi Collet <remi@fedoraproject.org> - 1.6.2-1
- update to 1.6.2

* Fri Sep 25 2015 Remi Collet <remi@fedoraproject.org> - 1.5.4-1
- update to 1.5.4 (no change)

* Sun Sep 13 2015 Remi Collet <remi@fedoraproject.org> - 1.5.2-1
- update to 1.5.2
- provide php-composer(tecnickcom/tc-lib-color)

* Fri Jul 24 2015 Remi Collet <remi@fedoraproject.org> - 1.5.1-1
- update to 1.5.1 (no change)

* Thu Jul  2 2015 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- update to 1.5.0

* Wed Jul  1 2015 Remi Collet <remi@fedoraproject.org> - 1.4.5-1
- initial package, version 1.4.5

