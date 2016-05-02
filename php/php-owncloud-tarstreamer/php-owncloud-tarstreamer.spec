# remirepo/fedora spec file for php-owncloud-tarstreamer
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    859a0170de120c66b042e6c0dbc1a9979c74669b
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     owncloud
%global gh_project   TarStreamer
%global with_tests   0%{!?_without_tests:1}
%global ns_vendor    ownCloud
%global ns_project   TarStreamer

Name:           php-owncloud-tarstreamer
Version:        0.1.0
Release:        1%{?dist}
Summary:        Streaming dynamic tar files

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?prever}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-composer(theseer/autoload)
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.8
BuildRequires:  php-date
BuildRequires:  php-spl
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  php-pear(Archive_Tar)
BuildRequires:  php-pecl(Xdebug)
%endif

# From composer.json
#      "php": ">=5.3.8"
Requires:       php(language) >= 5.3.8
# From phpcompatinfo report for version 0.1beta3
Requires:       php-date
Requires:       php-spl

Provides:       php-composer(owncloud/tarstreamer) = %{version}%{?prever}


%description
A library for dynamically streaming dynamic tar files without
the need to have the complete file stored on the server.

Autoloader: %{_datadir}/php/%{ns_vendor}/%{ns_project}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate a simple autoloader
%{_bindir}/phpab -o src/autoload.php src


%install
rm -rf     %{buildroot}
: Create a PSR-0 tree
mkdir -p   %{buildroot}%{_datadir}/php/%{ns_vendor}
cp -pr src %{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_project}


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_project}/autoload.php';
require_once '/usr/share/pear/Archive/Tar.php';
EOF

: Run test suite
cd tests
%{_bindir}/phpunit

if which php70; then
  : Run test suite with PHP 7.0 SCL
  php70 %{_bindir}/phpunit
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
%{_datadir}/php/%{ns_vendor}


%changelog
* Mon May  2 2016 Remi Collet <remi@fedoraproject.org> - 0.1.0-1
- update to 0.1.0

* Fri Jan  8 2016 Remi Collet <remi@fedoraproject.org> - 0.1-0.1.beta3
- initial package
