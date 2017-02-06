# remirepo/fedora spec file for php-tecnickcom-tc-lib-file
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    25883874ca399300d2b631034c6a89817204631d
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global c_vendor     tecnickcom
%global gh_owner     tecnickcom
%global gh_project   tc-lib-file
%global php_project  %{_datadir}/php/Com/Tecnick/File
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.6.4
Release:        1%{?dist}
Summary:        PHP library to read byte-level data from files

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
BuildRequires:  php-curl
BuildRequires:  php-pcre
%endif

# From composer.json, "require": {
#        "php": ">=5.4",
#        "ext-curl": "*",
#        "ext-pcre": "*"
Requires:       php(language) >= 5.4
Requires:       php-curl
Requires:       php-pcre
# From phpcompatinfo report for version 1.6.4
# none

# Composer
Provides:       php-composer(%{c_vendor}/%{gh_project}) = %{version}
# Upstream package name
Provides:       php-%{gh_project} = %{version}


%description
This library includes utility classes to read byte-level data.

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

sed -i 's:src:File:g' -i test/DirTest.php

ret=0
for cmd in php56 php70 php71 php; do
   if which $cmd; then
      $cmd %{_bindir}/phpunit --verbose || ret=1
   fi
done
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
%{php_project}


%changelog
* Mon Feb  6 2017 Remi Collet <remi@remirepo.net> - 1.6.4-1
- update to 1.6.4 (no change)

* Fri Sep  2 2016 Remi Collet <remi@fedoraproject.org> - 1.6.3-1
- update to 1.6.3 (no change)

* Tue Jun 14 2016 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- update to 1.6.0 (no change)

* Tue Mar  8 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- update to 1.5.0

* Fri Mar  4 2016 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- update to 1.3.1 (no change)

* Sat Jan 23 2016 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- update to 1.3.0

* Fri Jan 15 2016 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- initial package, version 1.2.0

