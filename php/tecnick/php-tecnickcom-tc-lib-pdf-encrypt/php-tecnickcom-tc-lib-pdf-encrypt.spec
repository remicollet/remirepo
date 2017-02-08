# remirepo/fedora spec file for php-tecnickcom-tc-lib-pdf-encrypt
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    66db26ddb3d1a0204b9113dbc594750f4d5448ae
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global c_vendor     tecnickcom
%global gh_owner     tecnickcom
%global gh_project   tc-lib-pdf-encrypt
%global php_project  %{_datadir}/php/Com/Tecnick/Pdf/Encrypt
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.5.0
Release:        1%{?dist}
Summary:        PHP library to encrypt data for PDF

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
BuildRequires:  php-date
BuildRequires:  php-hash
BuildRequires:  php-openssl
BuildRequires:  php-pcre
BuildRequires:  php-posix
%endif

# From composer.json, "require": {
#        "php": ">=5.4",
#        "ext-date": "*",
#        "ext-hash": "*",
#        "ext-openssl": "*",
#        "ext-pcre": "*",
#        "ext-posix": "*"
Requires:       php(language) >= 5.4
Requires:       php-date
Requires:       php-hash
Requires:       php-openssl
Requires:       php-pcre
Requires:       php-posix
# From phpcompatinfo report for version 1.5.0
# none

# Composer
Provides:       php-composer(%{c_vendor}/%{gh_project}) = %{version}
# Upstream package name
Provides:       php-%{gh_project} = %{version}


%description
PHP library to encrypt data for PDF.

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
date_default_timezone_set("UTC");
require '%{buildroot}%{php_project}/autoload.php';
EOF

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
%dir %{_datadir}/php/Com/Tecnick/Pdf
%{php_project}


%changelog
* Wed Feb  8 2017 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- update to 1.5.0
- drop dependency on php-mcrypt

* Mon Feb  6 2017 Remi Collet <remi@fedoraproject.org> - 1.4.4-1
- update to 1.4.4 (no change)
- open https://github.com/tecnickcom/tc-lib-pdf-encrypt/issues/4 - 7.1 failure
- open https://github.com/tecnickcom/tc-lib-pdf-encrypt/pull/5 add 7.1 to travis
- open https://github.com/tecnickcom/tc-lib-pdf-encrypt/pull/6 better exception

* Fri Sep  2 2016 Remi Collet <remi@fedoraproject.org> - 1.4.3-1
- update to 1.4.3

* Tue Jun 14 2016 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- update to 1.4.0 (no change)

* Fri Mar  4 2016 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- update to 1.3.2 (no change)

* Fri Jan 15 2016 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- initial package, version 1.3.0

