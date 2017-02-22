# remirepo spec file for php-maennchen-zipstream-php, from
#
# Fedora spec file for php-maennchen-zipstream-php
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
Name:       php-maennchen-zipstream-php
Version:    0.4.1
Release:    2%{?dist}
BuildArch:  noarch

License:    MIT
Group:      Development/Libraries
Summary:    A fast and simple streaming zip file downloader for PHP
URL:        https://github.com/maennchen/ZipStream-PHP
Source0:    %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
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
%setup -n ZipStream-PHP-%{version}


%build
%{_bindir}/phpab --format fedora --output src/autoload.php src


%install
rm -rf %{buildroot}

install -d -p -m 0755 %{buildroot}/%{_datadir}/php
install -d -p -m 0755 %{buildroot}/%{_datadir}/php/ZipStream

cp -ar src/* %{buildroot}/%{_datadir}/php/ZipStream


%check
sed -i "s:require.*:require('%{buildroot}/%{_datadir}/php/ZipStream/autoload.php');:" test/bootstrap.php

ret=0
for cmd in php56 php70 php71 php; do
  if which $cmd; then
    $cmd %{_bindir}/phpunit --no-coverage
  fi
done


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc composer.json
%doc README.md
%{_datadir}/php/ZipStream


%changelog
* Wed Feb 22 2017 Remi Collet <remi@remirepo.net> - 0.4.1-2
- backport for remi repository

* Mon Feb 20 2017 Randy Barlow <bowlofeggs@fedoraproject.org> - 0.4.1-2
- Use ZipStream instead of maennchen/zipstream-php for the package location.
- Use --no-coverage on phpunit and drop --bootstrap.

* Sat Feb 18 2017 Randy Barlow <bowlofeggs@fedoraproject.org> - 0.4.1-1
- Initial release.
