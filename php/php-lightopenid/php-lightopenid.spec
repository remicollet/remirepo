Name:           php-lightopenid
Version:        0.6
Release:        2%{?dist}
Summary:        PHP OpenID library

Group:          Development/Libraries
License:        MIT
URL:            http://code.google.com/p/lightopenid/
Source0:        http://lightopenid.googlecode.com/files/lightopenid-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       php-curl
Requires:       php-pcre

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
%defattr(-,root,root,-)
%doc example.php example-google.php
%{_datadir}/php/lightopenid


%changelog
* Sun Oct 20 2013 Remi Collet <remi@fedoraproject.org> - 0.6-2
- bacport 0.6 for remi repo

* Mon Oct 14 2013 Patrick Uiterwijk <puiterwijk@gmail.com> - 0.6-2
- Fixed package guidelines issues

* Tue Oct 01 2013 Patrick Uiterwijk <patrick@puiterwijk.org> - 0.6-1
- Initial packaging
