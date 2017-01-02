# remirepo/fedora spec file for php-seld-phar-utils
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    7009b5139491975ef6486545a39f3e6dad5ac30a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     Seldaek
%global gh_project   phar-utils

Name:           php-seld-phar-utils
Version:        1.0.1
Release:        2%{?dist}
Summary:        PHAR file format utilities

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# Autoloader
Source1:        %{gh_project}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3
# For test
BuildRequires:  php-cli
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)

# From composer.json
#       "php": ">=5.3.0",
Requires:       php(language) >= 5.3.0
# From phpcompatifo report for 1.0.1
Requires:       php-date
Requires:       php-hash
Requires:       php-pcre
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(seld/phar-utils) = %{version}


%description
PHAR file format utilities, for when PHP phars you up.

To use this library, you just have to add, in your project:
  require_once '%{_datadir}/php/Seld/PharUtils/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE1} src/autoload.php


%build
# Nothing


%install
rm -rf       %{buildroot}
# Restore PSR-0 tree
mkdir -p     %{buildroot}%{_datadir}/php/Seld/PharUtils/
cp -pr src/* %{buildroot}%{_datadir}/php/Seld/PharUtils/


%check
: Check if our autoloader works
php -r '
require "%{buildroot}%{_datadir}/php/Seld/PharUtils/autoload.php";
$a = new \Seld\PharUtils\Timestamps("%{SOURCE1}");
echo "Ok\n";
exit(0);
'


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%doc composer.json
%{_datadir}/php/Seld


%changelog
* Fri Oct 21 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-2
- switch from symfony/class-loader to fedora/autoloader

* Wed Oct 14 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- add autoloader

* Mon May  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
