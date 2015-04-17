# spec file for php-adoy-fastcgi-client
#
# Copyright (c) 2012-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    c332dfc8d3f96e47022170f169de73cf8d8d4f0a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_date      20150417
%global gh_owner     adoy
%global gh_project   PHP-FastCGI-Client
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-adoy-fastcgi-client
Summary:        Client for communication with a FastCGI application
Version:        1.0
Release:        0.1.%{gh_date}git%{gh_short}%{?dist}

URL:            https://github.com/adoy/PHP-FastCGI-Client
License:        LGPLv2+
Group:          Development/Libraries
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       php(language) > 5.3
Requires:       php-cli
Requires:       php-pcre

Obsoletes:      php-fastcgi-client <= 1.0
Provides:       php-composer(adoy/fastcgi-client) = %{version}

%description
This PHP class handles the communication with a FastCGI (FCGI) application
using the FastCGI protocol.

The package provides a simple command line test command: fcgiget.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

# Fix include path
sed -e '/^require/s:src/::' \
    -i fcgiget.php


%build
# empty build section, nothing required


%install
rm -rf %{buildroot}

# install the class
mkdir -p %{buildroot}%{_datadir}/php
cp -pr src/Adoy %{buildroot}%{_datadir}/php/Adoy

# install the command
install -Dpm 755 fcgiget.php %{buildroot}%{_bindir}/fcgiget


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README
%doc composer.json
%{_bindir}/fcgiget
%{_datadir}/php/Adoy


%changelog
* Fri Apr 17 2015 Remi Collet <remi@fedoraproject.org> - 1.0-0.1.20150417gitc332dfc
- rename to php-adoy-fastcgi-client
- PSR-0 tree

* Sat Oct 13 2012 Remi Collet <remi@fedoraproject.org> - 1.0-1
- Initial package