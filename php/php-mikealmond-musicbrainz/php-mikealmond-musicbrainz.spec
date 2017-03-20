Name:       php-mikealmond-musicbrainz
Version:    0.2.2
Release:    1%{?dist}
BuildArch:  noarch

License:    MIT
Summary:    A PHP library to access MusicBrainz's Web Service v2
URL:        https://github.com/mikealmond/MusicBrainz
Source0:    %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: php-composer(fedora/autoloader)
BuildRequires: php-fedora-autoloader-devel
BuildRequires: phpunit 

Requires:   php(language) >= 5.3.8
Requires:   php-composer(fedora/autoloader)
Requires:   php-curl
Requires:   php-date
Requires:   php-filter
Requires:   php-json
Requires:   php-pcre
Requires:   php-spl

Provides:   php-composer(mikealmond/musicbrainz) = %{version}


%description
This PHP library that allows you to easily access the MusicBrainz Web
Service V2 API. Visit the MusicBrainz development page for more
information.

This project is a fork of https://github.com/chrisdawson/MusicBrainz and
takes some inspiration from the Python bindings.


%prep
%autosetup -n MusicBrainz-%{version}


%build
cat <<'AUTOLOAD' | tee src/MusicBrainz/autoload.php
<?php
require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('MusicBrainz', __DIR__);
AUTOLOAD


%install
install -d -p -m 0755 %{buildroot}/%{_datadir}/php
install -d -p -m 0755 %{buildroot}/%{_datadir}/php/MusicBrainz

cp -ar src/MusicBrainz/* %{buildroot}/%{_datadir}/php/MusicBrainz


%check
phpunit --no-coverage --bootstrap %{buildroot}/%{_datadir}/php/MusicBrainz/autoload.php


%files
%license LICENSE.md
%doc composer.json
%doc README.md
%{_datadir}/php/MusicBrainz


%changelog
* Sat Mar 04 2017 Randy Barlow <bowlofeggs@fedoraproject.org> - 0.2.2-1
- Initial release.
