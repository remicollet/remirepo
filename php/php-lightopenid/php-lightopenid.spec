Name:           php-lightopenid
Version:        0.6
Release:        2%{?dist}
Summary:        PHP OpenID library

License:        MIT
URL:            http://code.google.com/p/lightopenid/
Source0:        http://lightopenid.googlecode.com/files/lightopenid-%{version}.tgz

Requires:       php-curl
Requires:       php-pcre
BuildArch:      noarch

%description
Lightweight OpenID library.

%prep
%setup -q -n lightopenid

%build
# Nothing to build

%install
mkdir -p %{buildroot}%{_datadir}/php/lightopenid
cp -p openid.php %{buildroot}%{_datadir}/php/lightopenid/openid.php

%files
%doc example.php example-google.php
%{_datadir}/php/lightopenid


%changelog
* Mon Oct 14 2013 Patrick Uiterwijk <puiterwijk@gmail.com> - 0.6-2
- Fixed package guidelines issues

* Tue Oct 01 2013 Patrick Uiterwijk <patrick@puiterwijk.org> - 0.6-1
- Initial packaging
