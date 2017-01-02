# remirepo/fedora spec file for php-ircmaxell-random-lib
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    e9e0204f40e49fa4419946c677eccd3fa25b8cf4
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     ircmaxell
%global gh_project   RandomLib
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-ircmaxell-random-lib
Version:        1.2.0
Release:        1%{?dist}
Summary:        A Library For Generating Secure Random Numbers

Group:          Development/Libraries
# See class headers
# LICENSE file will be in next version
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  %{_bindir}/phpab
BuildRequires:  php(language) >= 5.3.2
BuildRequires:  php-hash
BuildRequires:  php-openssl
BuildRequires:  php-posix
BuildRequires:  php-spl
BuildRequires:  php-composer(ircmaxell/security-lib) >= 1.0
#        "mikey179/vfsStream": "^1.6",
#        "friendsofphp/php-cs-fixer": "^1.11",
#        "phpunit/phpunit": "^4.8|^5.0"
BuildRequires:  php-composer(mikey179/vfsStream) >= 1.6
BuildRequires:  php-composer(phpunit/phpunit) >= 4.8
# For autoloader
BuildRequires:  php-mikey179-vfsstream >= 1.6.0
BuildRequires:  php-ircmaxell-security-lib >= 1.1.0-3
%endif

# From composer.json
#        "ircmaxell/security-lib": "^1.1",
#        "php": ">=5.3.2"
Requires:       php(language) >= 5.3.2
Requires:       php-composer(ircmaxell/security-lib) >= 1.1
# From phpcompatinfo report for version 1.2.0
Requires:       php-hash
Requires:       php-openssl
Requires:       php-posix
Requires:       php-spl
# For autoloader
Requires:       php-ircmaxell-security-lib >= 1.1.0-3

Provides:       php-composer(ircmaxell/random-lib) = %{version}


%description
A library for generating random numbers and strings of various strengths.

This library is useful in security contexts.

Autoloader: %{_datadir}/php/RandomLib/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

chmod -x lib/RandomLib/Generator.php


%build
: Generate library autoloader
%{_bindir}/phpab --output lib/RandomLib/autoload.php lib

cat << EOF | tee -a lib/RandomLib/autoload.php
// Dependency
require_once '%{_datadir}/php/SecurityLib/autoload.php';
EOF


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{_datadir}/php
cp -pr lib/* %{buildroot}%{_datadir}/php


%check
%if %{with_tests}
: Generate test suite autoloader
%{_bindir}/phpab --output test/autoload.php test

mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once __DIR__ . '/../test/autoload.php';
require_once '%{_datadir}/php/org/bovigo/vfs/autoload.php';
require_once '%{buildroot}%{_datadir}/php/RandomLib/autoload.php';
EOF

: Run test suite
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --verbose
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --verbose
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
%doc *.md
%doc composer.json
%{_datadir}/php/RandomLib


%changelog
* Thu Sep  8 2016 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0

* Thu Jan 14 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-3
- add autoloader

* Fri Jan 16 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0

* Wed Aug 13 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
