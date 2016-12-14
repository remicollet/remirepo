# remirepo/fedora spec file for php-fig-http-message-util
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit    70899e53776d4d65fec9f90f0f88ba6c4d0f7b88
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     php-fig
%global gh_project   http-message-util
%global pk_owner     fig
%global pk_project   %{gh_project}

Name:           php-%{pk_owner}-%{pk_project}
Version:        1.1.0
Release:        1%{?dist}
Summary:        PSR Http Message Util

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
#        "php": "^5.3 || ^7.0",
#        "psr/http-message": "^1.0"
Requires:       php(language) > 5.3
Requires:       php-composer(psr/http-message) >= 1.0
Requires:       php-composer(psr/http-message) <  2
# From phpcompatinfo: none
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_owner}/%{pk_project}) = %{version}


%description
This library holds utility classes and constants to facilitate common
operations of PSR-7; the primary purpose is to provide constants for
referring to request methods, response status codes and messages, and
potentially common headers.

Autoloader: %{_datadir}/php/Fig/Http/Message/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}



%build
cat << 'AUTOLOAD' | tee src/autoload.php
<?php
/* Autoloader for %{pk_owner}/%{pk_project} and its dependencies */

require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('Fig\\Http\\Message\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
    '%{_datadir}/php/Psr/Http/Message/autoload.php',
));
AUTOLOAD


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{_datadir}/php/Fig/Http
cp -pr src %{buildroot}%{_datadir}/php/Fig/Http/Message


%check
php -r '
require "%{buildroot}%{_datadir}/php/Fig/Http/Message/autoload.php";
$ok = interface_exists("Fig\\Http\\Message\\StatusCodeInterface");
echo "Autoload " . ($ok ? "Ok\n" : "fails\n");
exit ($ok ? 0 : 1);
'


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%dir %{_datadir}/php/Fig
%dir %{_datadir}/php/Fig/Http
     %{_datadir}/php/Fig/Http/Message


%changelog
* Wed Dec 14 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- initial package

