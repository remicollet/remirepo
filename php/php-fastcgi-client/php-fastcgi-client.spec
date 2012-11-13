Name:           php-fastcgi-client
Summary:        Template/Presentation Framework for PHP
Version:        1.0
Release:        1%{?dist}

URL:            https://github.com/adoy/PHP-FastCGI-Client
License:        LGPLv2+
Group:          Development/Libraries
# https://github.com/adoy/PHP-FastCGI-Client/archive/master.tar.gz
Source0:        PHP-FastCGI-Client-master.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       php-cli
Requires:       php-spl


%description
This PHP class handles the communication with a FastCGI (FCGI) application
using the FastCGI protocol.

The package provides a simple command line test command: fcgiget.


%prep
%setup -qn PHP-FastCGI-Client-master

# Fix include path
sed -e '/^require/s:fastcgi.php:PHP-FastCGI-Client/fastcgi.php:' \
    -i fcgiget.php


%build
# empty build section, nothing required


%install
rm -rf %{buildroot}

# install the class
install -Dpm 644 fastcgi.php %{buildroot}%{_datadir}/php/PHP-FastCGI-Client/fastcgi.php

# install the command
install -Dpm 755 fcgiget.php %{buildroot}%{_bindir}/fcgiget


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE
%{_bindir}/fcgiget
%{_datadir}/php/PHP-FastCGI-Client


%changelog
* Tue Oct 13 2012 Remi Collet <remi@fedoraproject.org> - 1.0-1
- Initial package
