# remirepo/fedora spec file for php-composer-ca-bundle
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    a795611394b3c05164fd0eb291b492b39339cba4
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     composer
%global gh_project   ca-bundle
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-composer-ca-bundle
Version:        1.0.6
Release:        1%{?dist}
Summary:        Lets you find a path to the system CA

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
# git snapshot to get everything, despite .gitattributes
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh
Source2:        %{name}-autoload.php

# Never bundle a CA file
Patch0:         %{name}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# For tests
BuildRequires:  php(language) >= 5.3.2
BuildRequires:  php-openssl
BuildRequires:  php-pcre
BuildRequires:  php-cli
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)
# ca-certificates
BuildRequires:  %{_sysconfdir}/pki/tls/certs/ca-bundle.crt
%endif

# From composer.json, "require": {
#        "ext-openssl": "*",
#        "ext-pcre": "*",
#        "php": "^5.3.2 || ^7.0"
Requires:       php(language) >= 5.3.2
Requires:       php-openssl
Requires:       php-pcre
# From phpcompatinfo report for version 1.0.3
#nothing
# Autoloader
Requires:       php-composer(fedora/autoloader)
# ca-certificates
Requires:       %{_sysconfdir}/pki/tls/certs/ca-bundle.crt

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Small utility library that lets you find a path to the system CA bundle.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE2} src/autoload.php
%patch0 -p0 -b .rpm

find src -name \*.rpm -exec rm {} \;


%build
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

: Library
mkdir -p   %{buildroot}%{php_home}/Composer/
cp -pr src %{buildroot}%{php_home}/Composer/CaBundle


%check
%if %{with_tests}
php -r '
use Composer\CaBundle\CaBundle as CA;
require "%{buildroot}%{php_home}/Composer/CaBundle/autoload.php";
$file = CA::getSystemCaRootBundlePath();
if ($file != "/etc/pki/tls/certs/ca-bundle.crt") {
    echo "Unexpected $file\n";
    exit(1);
}
if (!CA::validateCaFile($file)) {
    echo "Cannot validate $file\n";
    exit(1);
}
echo "OK\n";
'
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
%doc *.md
%dir %{php_home}/Composer
     %{php_home}/Composer/CaBundle


%changelog
* Thu Nov  3 2016 Remi Collet <remi@fedoraproject.org> - 1.0.6-1
- update to 1.0.6 (no change)

* Wed Nov  2 2016 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- update to 1.0.5 (no change)

* Thu Oct 20 2016 Remi Collet <remi@fedoraproject.org> - 1.0.4-2
- switch from symfony/class-loader to fedora/autoloader

* Mon Sep  5 2016 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- update to 1.0.4 (no change)

* Tue Jul 19 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- update to 1.0.3

* Sat Apr 30 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- initial package, version 1.0.2

