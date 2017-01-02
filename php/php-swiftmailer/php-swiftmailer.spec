# remirepo/fedora spec file for php-swiftmailer
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please preserve changelog entries
#
%global gh_commit    cd142238a339459b10da3d8234220963f392540c
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     swiftmailer
%global gh_project   swiftmailer
%global with_tests   0%{!?_without_tests:1}
%global php_home     %{_datadir}/php

Name:           php-%{gh_project}
Version:        5.4.5
Release:        1%{?dist}
Summary:        Free Feature-rich PHP Mailer

Group:          Development/Libraries
License:        MIT
URL:            http://www.swiftmailer.org/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  php-fedora-autoloader-devel
# From composer.json, "require-dev": {
#        "mockery/mockery": "~0.9.1",
#        "symfony/phpunit-bridge": "~3.2"
BuildRequires:  php-composer(mockery/mockery) >= 0.9.1
BuildRequires:  php-composer(symfony/phpunit-bridge) >= 0.9.1
%endif

# From composer.json, "require": {
#        "php": ">=5.3.3"
Requires:       php(language) >= 5.3.3
# from phpcompatinfo report on version 5.4.1
Requires:       php-bcmath
Requires:       php-ctype
Requires:       php-date
Requires:       php-hash
Requires:       php-iconv
Requires:       php-mbstring
Requires:       php-mcrypt
Requires:       php-mhash
Requires:       php-openssl
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-simplexml
Requires:       php-spl

# Removed from official repo in Fedora 25
%if 1
Obsoletes:      php-swift-Swift   <= 5.4.1
# Single package in this channel
Obsoletes:      php-channel-swift <= 1.3
Provides:       php-pear(pear.swiftmailer.org/Swift) = %{version}
%endif

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Swift Mailer integrates into any web app written in PHP, offering a 
flexible and elegant object-oriented approach to sending emails with 
a multitude of features.

Autoloader: %{php_home}/Swift/swift_required.php



%prep
%setup -q -n %{gh_project}-%{gh_commit}

# Install using the same layout than the old PEAR package
mv lib/swift_required_pear.php lib/swift_required.php
rm lib/swiftmailer_generate_mimes_config.php


%build
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

mkdir -p                   %{buildroot}/%{php_home}/Swift
cp -p lib/*.php            %{buildroot}/%{php_home}/Swift/
cp -pr lib/classes/*       %{buildroot}/%{php_home}/Swift/
cp -pr lib/dependency_maps %{buildroot}/%{php_home}/Swift/


%check
%if %{with_tests}
: Use installed tree and autoloader
mkdir vendor
%{_bindir}/phpab --format fedora --output vendor/autoload.php tests
cat << 'EOF' | tee -a vendor/autoload.php
require_once '%{buildroot}/%{php_home}/Swift/swift_required.php';
require_once '%{php_home}/Mockery/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('Symfony\\Bridge\\PhpUnit\\', '%{php_home}/Symfony/Bridge/PhpUnit');
EOF

TMPDIR=$(mktemp -d $PWD/rpmtests-XXXXXXXX)
cat << EOF | tee tests/acceptance.conf.php
<?php
define('SWIFT_TMP_DIR', '$TMPDIR');
EOF

: Run upstream test suite
ret=0
# remirepo:10
run=0
if which php56; then
   php56 %{_bindir}/phpunit --exclude smoke --verbose || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --exclude smoke --verbose || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --exclude smoke --verbose || ret=1
# remirepo:1
fi

# Cleanup
rm -r $TMPDIR
exit $ret
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGES README
%doc doc
%doc composer.json
%{php_home}/Swift


%changelog
* Thu Dec 29 2016 Remi Collet <remi@fedoraproject.org> - 5.4.5-1
- update to 5.4.5
- fix Remote Code Execution CVE-2016-10074

* Thu Nov 24 2016 Remi Collet <remi@fedoraproject.org> - 5.4.4-1
- update to 5.4.4

* Fri Jul  8 2016 Remi Collet <remi@fedoraproject.org> - 5.4.3-1
- update to 5.4.3
- drop patch merged upstream

* Tue Jun 14 2016 Remi Collet <remi@fedoraproject.org> - 5.4.2-2
- add patch to allow mockery 0.9.x
  open https://github.com/swiftmailer/swiftmailer/pull/769

* Mon May  2 2016 Remi Collet <remi@fedoraproject.org> - 5.4.2-1
- update to 5.4.2

* Fri Mar 25 2016 Remi Collet <remi@fedoraproject.org> - 5.4.1-2
- rebuild for remi repository

* Fri Oct 16 2015 Remi Collet <remi@fedoraproject.org> - 5.4.1-1
- initial rpm, version 5.4.1
- sources from github, pear channel is dead

