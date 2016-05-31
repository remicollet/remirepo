# remirepo/fedora spec file for php-sabre-http
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    2e93bc8321524c67be4ca5b8415daebd4c8bf85e
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     fruux
%global gh_project   sabre-http
#global prever       alpha6
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-%{gh_project}
Summary:        Library for dealing with http requests and responses
Version:        4.2.1
Release:        1%{?dist}

URL:            https://github.com/%{gh_owner}/%{gh_project}
License:        BSD
Group:          Development/Libraries
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz
Source1:        %{name}-autoload-dev.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) > 5.4
BuildRequires:  php-mbstring
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  php-composer(sabre/event) >= 1.0.0
BuildRequires:  php-composer(sabre/uri)   >= 1.0
BuildRequires:  php-ctype
BuildRequires:  php-curl
BuildRequires:  php-date
BuildRequires:  php-hash
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-xml
# Autoloader
BuildRequires:  php-composer(symfony/class-loader)
BuildRequires:  php-composer(sabre/event) >= 2.0.2
%endif

# From composer.json, "require" : {
#        "php"          : ">=5.4",
#        "ext-mbstring" : "*",
#        "sabre/event"  : ">=1.0.0,<4.0.0",
#        "sabre/uri"    : "~1.0"
Requires:       php(language) > 5.4
Requires:       php-mbstring
Requires:       php-composer(sabre/event) >= 1.0.0
Requires:       php-composer(sabre/event) <  4
Requires:       php-composer(sabre/uri)   >= 1.0
Requires:       php-composer(sabre/uri)   <  2
# From composer.json, "suggest" : {
#        "ext-curl" : " to make http requests with the Client class"
Requires:       php-curl
# From phpcompatinfo report for version 3.0.5
Requires:       php-ctype
Requires:       php-date
Requires:       php-hash
Requires:       php-pcre
Requires:       php-spl
Requires:       php-xml
# Autoloader
Requires:       php-composer(symfony/class-loader)
Requires:       php-composer(sabre/event) >= 2.0.2

# Was split from php-sabre-dav in version 1.9
Conflicts:      php-sabre-dav < 1.9

Provides:       php-composer(sabre/http) = %{version}


%description
This library provides a toolkit to make working with the HTTP protocol easier.

Most PHP scripts run within a HTTP request but accessing information about
the HTTP request is cumbersome at least, mainly do to superglobals and the
CGI standard.

There's bad practices, inconsistencies and confusion.
This library is effectively a wrapper around the following PHP constructs:

For Input:
    $_GET
    $_POST
    $_SERVER
    php://input or $HTTP_RAW_POST_DATA.

For output:
    php://output or echo.
    header()

What this library provides, is a Request object, and a Response object.
The objects are extendable and easily mockable.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE1} lib/autoload.php


%build
# nothing to build


%install
rm -rf %{buildroot}

# Install as a PSR-0 library
mkdir -p %{buildroot}%{_datadir}/php/Sabre
cp -pr lib %{buildroot}%{_datadir}/php/Sabre/HTTP


%check
%if %{with_tests}
: Run upstream test suite against installed library
cd tests
%{_bindir}/phpunit \
  --bootstrap=%{buildroot}%{_datadir}/php/Sabre/HTTP/autoload.php \
  --verbose

if which php70; then
  php70 %{_bindir}/phpunit \
    --bootstrap=%{buildroot}%{_datadir}/php/Sabre/HTTP/autoload.php \
    --verbose
fi
%else
: Skip upstream test suite
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *md
%doc composer.json
%{_datadir}/php/Sabre/HTTP


%changelog
* Fri Mar 11 2016 Remi Collet <remi@fedoraproject.org> - 4.2.1-1
- update to 4.2.1
- add dependency on sabre/uri
- run test suite with both PHP 5 and 7 when available

* Mon Jul 20 2015 Remi Collet <remi@fedoraproject.org> - 3.0.5-1
- update to 3.0.5
- add autoloader

* Wed Jul 16 2014 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- update to 2.0.4
- composer dependencies

* Tue May  6 2014 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- update to 2.0.3

* Tue Feb 11 2014 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- update to 2.0.2

* Sat Jan 11 2014 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1

* Tue Jan  7 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.2.alpha6
- update to 2.0.0alpha6
- add explicit conflicts with php-sabre-dav < 1.9

* Tue Dec 31 2013 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.alpha5
- Initial packaging
