# remirepo/fedora spec file for php-league-flysystem
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
# Github
%global gh_commit    521a233642773505222a5dd53231ccf5b0607d5a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     thephpleague
%global gh_project   flysystem
# Packagist
%global pk_vendor    league
%global pk_name      flysystem
# PSR-0 namespace
%global ns_vendor    League
%global ns_project   Flysystem

Name:           php-%{pk_vendor}-%{pk_name}
Version:        1.0.31
Release:        1%{?dist}
Summary:        Filesystem abstraction: Many filesystems, one API

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
# Create git snapshot as tests are excluded from official tarball
Source1:        makesrc.sh
# Autoloader
Source2:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.5.9
BuildRequires:  php-date
BuildRequires:  php-fileinfo
BuildRequires:  php-ftp
BuildRequires:  php-hash
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
BuildRequires:  php-spl
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "~4.8 || ~5.0",
#        "mockery/mockery": "~0.9",
#        "phpspec/phpspec": "^2.2"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.0
BuildRequires:  php-composer(mockery/mockery) >= 0.9
BuildRequires:  php-composer(phpspec/phpspec) >= 2.2
# Autoloader
BuildRequires:  php-composer(symfony/class-loader)

# From composer.json, "require": {
Requires:       php(language) >= 5.5.9
# From phpcompatifo report for 1.0.29
Requires:       php-date
Requires:       php-fileinfo
Requires:       php-ftp
Requires:       php-hash
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-spl
# Autoloader
Requires:       php-composer(symfony/class-loader)

Provides:       php-composer(%{pk_vendor}/%{pk_name}) = %{version}


%description
Flysystem is a filesystem abstraction which allows you to easily swap out
a local filesystem for a remote one.

Autoloader: %{_datadir}/php/%{ns_vendor}/%{ns_project}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

install -pm 644 %{SOURCE2} src/autoload.php


%build
# Nothing


%install
rm -rf     %{buildroot}

# Restore PSR-0 tree
mkdir -p   %{buildroot}%{_datadir}/php/%{ns_vendor}
cp -pr src %{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_project}


%check
: Generate a simple autoloader
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
// Installed library
require '%{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_project}/autoload.php';

// Dependency
require_once '%{_datadir}/php/Mockery/autoload.php';

// Test suite
require_once '%{_datadir}/php/Symfony/Component/ClassLoader/Psr4ClassLoader.php';
$Loader = new \Symfony\Component\ClassLoader\Psr4ClassLoader();
$Loader->addPrefix("League\\Flysystem\\Stub\\", dirname(__DIR__).'/stub');
$Loader->register();
EOF

: Fix bootstraping
sed -e 's/file="[^"]*"//' -i phpunit.xml
echo 'bootstrap: vendor/autoload.php' >>phpspec.yml

PHPSPECVER=$(%{_bindir}/phpspec --version | sed 's/.* //;s/\..*//')
if [ "$PHPSPECVER" -ge 3 ]
then PHPSPEC=/dev/null
else PHPSPEC=%{_bindir}/phpspec
fi

# remirepo:15
run=0
ret=0
if which php56; then
   : Run upstream test suite with PHP 5
   php56 $PHPSPEC run || ret=1
   php56 %{_bindir}/phpunit --verbose || ret=1
   run=1
fi
if which php71; then
   : Run upstream test suite with PHP 7
   php71 $PHPSPEC run || ret=1
   php71 %{_bindir}/phpunit --verbose || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
: Run upstream test suite
%{_bindir}/php $PHPSPEC run
%{_bindir}/phpunit --verbose
# remirepo:2
fi
exit $ret


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{_datadir}/php/%{ns_vendor}


%changelog
* Wed Oct 19 2016 Remi Collet <remi@fedoraproject.org> - 1.0.30-1
- update to 1.0.30

* Wed Oct 19 2016 Remi Collet <remi@fedoraproject.org> - 1.0.30-1
- update to 1.0.30 (no change)
- lower dependency on PHP 5.5.9

* Tue Oct 18 2016 Remi Collet <remi@fedoraproject.org> - 1.0.29-1
- update to 1.0.29
- raise dependency on PHP 5.6

* Fri Oct  7 2016 Remi Collet <remi@fedoraproject.org> - 1.0.28-1
- update to 1.0.28

* Wed Aug 10 2016 Remi Collet <remi@fedoraproject.org> - 1.0.27-1
- update to 1.0.27

* Wed Aug  3 2016 Remi Collet <remi@fedoraproject.org> - 1.0.26-1
- update to 1.0.26

* Mon Jul 18 2016 Remi Collet <remi@fedoraproject.org> - 1.0.25-1
- update to 1.0.25
- disable spec test suite with phpspec 3

* Sat Jun  4 2016 Remi Collet <remi@fedoraproject.org> - 1.0.24-1
- update to 1.0.24

* Thu Apr 28 2016 Remi Collet <remi@fedoraproject.org> - 1.0.22-1
- update to 1.0.22

* Fri Apr 22 2016 Remi Collet <remi@fedoraproject.org> - 1.0.21-1
- update to 1.0.21

* Tue Mar 15 2016 Remi Collet <remi@fedoraproject.org> - 1.0.20-1
- update to 1.0.20

* Tue Mar  8 2016 Remi Collet <remi@fedoraproject.org> - 1.0.18-1
- update to 1.0.18

* Sat Feb 20 2016 Remi Collet <remi@fedoraproject.org> - 1.0.17-1
- update to 1.0.17

* Thu Jan 14 2016 Remi Collet <remi@fedoraproject.org> - 1.0.16-1
- initial package
- open https://github.com/thephpleague/flysystem/pull/592 - PHPUnit

