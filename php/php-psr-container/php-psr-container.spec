# remirepo/fedora spec file for php-psr-container
#
# Copyright (c) 2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit    b7ce3b176482dbbc1245ebf52b181af44c2cf55f
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     php-fig
%global gh_project   container

%global pk_vendor    psr
%global pk_project   container

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:      php-%{pk_vendor}-%{pk_project}
Version:   1.0.0
Release:   1%{?dist}
Summary:   Common Container Interface

Group:     Development/Libraries
License:   MIT
URL:       https://github.com/%{gh_owner}/%{gh_project}
Source0:   %{url}/archive/%{gh_commit}/%{name}-%{version}-%{gh_commit}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
# For tests
BuildRequires: php(language) >= 5.3.0
BuildRequires: php-cli
BuildRequires: php-composer(fedora/autoloader)

# From composer.json,    "require": {
#        "php": ">=5.3.0"
Requires:  php(language) >= 5.3.0
# phpcompatinfo (computed from version 1.0.0)
#     <none>
# Autoloader
Requires:  php-composer(fedora/autoloader)

# Composer
Provides:  php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
This repository holds all interfaces/classes/traits related to PSR-11.

Note that this is not a container implementation of its own. 

Autoloader: %{_datadir}/php/Psr/Container/autoload.php


%prep
%setup -qn %{gh_project}-%{gh_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
/* Autoloader for %{pk_vendor}/%{pk_project} and its dependencies */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Psr\\Container\\', __DIR__);
AUTOLOAD


%build
# Empty build section, nothing to build


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{_datadir}/php/Psr
cp -rp src %{buildroot}%{_datadir}/php/Psr/Container


%check
: Test autoloader
php -r '
require "%{buildroot}%{_datadir}/php/Psr/Container/autoload.php";
exit (interface_exists("Psr\\Container\\ContainerInterface") ? 0 : 1);
'


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%dir %{_datadir}/php/Psr
     %{_datadir}/php/Psr/Container


%changelog
* Mon Feb 27 2017 Remi Collet <remi@remirepo.net> - 1.0.0-1
- Initial package, version 1.0.0

