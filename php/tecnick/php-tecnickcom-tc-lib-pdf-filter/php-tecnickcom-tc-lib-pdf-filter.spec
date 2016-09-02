# remirepo/fedora spec file for php-tecnickcom-tc-lib-pdf-filter
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    b26d5e06b8bd7bef836b0c18530b971839eee664
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global c_vendor     tecnickcom
%global gh_owner     tecnickcom
%global gh_project   tc-lib-pdf-filter
%global php_project  %{_datadir}/php/Com/Tecnick/Pdf/Filter
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.3.3
Release:        1%{?dist}
Summary:        PHP library to decode PDF compression and encryption filters

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
Requires:       php-zlib
%endif

# From composer.json, "require": {
#        "php": ">=5.4"
Requires:       php(language) >= 5.4
# From phpcompatinfo report for version 1.1.0
Requires:       php-pcre
Requires:       php-zlib

# Composer
Provides:       php-composer(%{c_vendor}/%{gh_project}) = %{version}
# Upstream package name
Provides:       php-%{gh_project} = %{version}


%description
PHP library to decode PDF compression and encryption filters.

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
%dir %{_datadir}/php/Com
%dir %{_datadir}/php/Com/Tecnick
%dir %{_datadir}/php/Com/Tecnick/Pdf
%{php_project}


%changelog
* Fri Sep  2 2016 Remi Collet <remi@fedoraproject.org> - 1.3.3-1
- update to 1.3.3 (no change)

* Tue Jun 14 2016 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- update to 1.3.0 (no change)

* Fri Mar  4 2016 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- update to 1.2.1 (no change)

* Fri Dec 11 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0 (no change)
- raise dependency on php >= 5.4

* Fri Dec 11 2015 Remi Collet <remi@fedoraproject.org> - 1.1.24-1
- update to 1.1.24 (no change)

* Mon Dec  7 2015 Remi Collet <remi@fedoraproject.org> - 1.1.22-1
- update to 1.1.22 (no change)

* Thu Dec  3 2015 Remi Collet <remi@fedoraproject.org> - 1.1.20-1
- update to 1.1.20 (no change)

* Fri Nov 27 2015 Remi Collet <remi@fedoraproject.org> - 1.1.19-1
- update to 1.1.19 (no change)

* Wed Nov 25 2015 Remi Collet <remi@fedoraproject.org> - 1.1.18-1
- update to 1.1.18 (no change)

* Fri Nov 20 2015 Remi Collet <remi@fedoraproject.org> - 1.1.14-1
- update to 1.1.14 (no change)

* Fri Nov 20 2015 Remi Collet <remi@fedoraproject.org> - 1.1.12-1
- update to 1.1.12 (no change)

* Wed Nov 18 2015 Remi Collet <remi@fedoraproject.org> - 1.1.9-1
- update to 1.1.9 (no change)
- run test suite with both PHP 5 and 7 when available

* Tue Oct 20 2015 Remi Collet <remi@fedoraproject.org> - 1.1.8-1
- update to 1.1.8 (no change)

* Fri Sep 25 2015 Remi Collet <remi@fedoraproject.org> - 1.1.7-1
- update to 1.1.7 (no change)

* Sun Sep 13 2015 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- update to 1.1.4
- provide php-composer(tecnickcom/tc-lib-pdf-filter)

* Fri Jul 24 2015 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- update to 1.1.3 (no change)

* Thu Jul  2 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1
- drop patch merged upstream

* Thu Jul  2 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- initial package, version 1.1.0
- open https://github.com/tecnickcom/tc-lib-pdf-filter/pull/1
  fix autoloader

