Name:       php-maennchen-zipstream-php
Version:    0.4.1
Release:    2%{?dist}
BuildArch:  noarch

License:    MIT
Summary:    A fast and simple streaming zip file downloader for PHP
URL:        https://github.com/maennchen/ZipStream-PHP
Source0:    %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: php-composer(fedora/autoloader)
BuildRequires: php-fedora-autoloader-devel
BuildRequires: php-zip
BuildRequires: phpunit 

Requires:   php(language) >= 5.6.0
Requires:   php-date
Requires:   php-hash
Requires:   php-mbstring
Requires:   php-pcre
Requires:   php-reflection
Requires:   php-spl
Requires:   php-zip
Requires:   php-zlib

Requires:   php-composer(fedora/autoloader)
Provides:   php-composer(maennchen/zipstream-php) = %{version}


%description
A fork of pablotron's zip streaming library, a fast and simple streaming
zip file downloader for PHP.


%prep
%autosetup -n ZipStream-PHP-%{version}


%build
%{_bindir}/phpab --format fedora --output src/autoload.php src


%install
install -d -p -m 0755 %{buildroot}/%{_datadir}/php
install -d -p -m 0755 %{buildroot}/%{_datadir}/php/ZipStream

cp -ar src/* %{buildroot}/%{_datadir}/php/ZipStream


%check
sed -i "s:require.*:require('%{buildroot}/%{_datadir}/php/ZipStream/autoload.php');:" test/bootstrap.php

phpunit --no-coverage


%files
%license LICENSE.md
%doc composer.json
%doc README.md
%{_datadir}/php/ZipStream


%changelog
* Mon Feb 20 2017 Randy Barlow <bowlofeggs@fedoraproject.org> - 0.4.1-2
- Use ZipStream instead of maennchen/zipstream-php for the package location.
- Use --no-coverage on phpunit and drop --bootstrap.

* Sat Feb 18 2017 Randy Barlow <bowlofeggs@fedoraproject.org> - 0.4.1-1
- Initial release.
