# remirepo/fedora spec file for php-http-interop-http-middleware
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit    ff545c87e97bf4d88f0cb7eb3e89f99aaa53d7a9
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     http-interop
%global gh_project   http-middleware

Name:           php-%{gh_owner}-%{gh_project}
Version:        0.2.0
Release:        1%{?dist}
Summary:        Common interface for HTTP middleware

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-cli
BuildRequires:  php-composer(psr/http-message) >= 1.0
BuildRequires:  php-composer(fedora/autoloader)

# From composer.json, "require": {
#        "php": ">=5.3.0",
#        "psr/http-message": "^1.0"
Requires:       php(language) > 5.3
Requires:       php-composer(psr/http-message) >= 1.0
Requires:       php-composer(psr/http-message) <  2
# From phpcompatinfo: none
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
PSR-15 interfaces for HTTP middleware.

Autoloader: %{_datadir}/php/Interop/Http/Middleware/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}



%build
cat << 'AUTOLOAD' | tee src/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 */
require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Interop\\Http\\Middleware\\', __DIR__);

\Fedora\Autoloader\Dependencies::required(array(
    '%{_datadir}/php/Psr/Http/Message/autoload.php',
));
AUTOLOAD


%install
rm -rf   %{buildroot}
mkdir -p %{buildroot}%{_datadir}/php/Interop/Http
cp -pr src %{buildroot}%{_datadir}/php/Interop/Http/Middleware


%check
php -r '
require "%{buildroot}%{_datadir}/php/Interop/Http/Middleware/autoload.php";
if (interface_exists("Interop\\Http\\Middleware\\ServerMiddlewareInterface")) {
   echo "Autoload OK\n";
   exit (0);
} else {
   echo "Autoload fails\n";
   exit (1);
}'


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%dir %{_datadir}/php/Interop
%dir %{_datadir}/php/Interop/Http
     %{_datadir}/php/Interop/Http/Middleware


%changelog
* Thu Nov 10 2016 Remi Collet <remi@fedoraproject.org> - 0.2.0-1
- initial package
