# remirepo/fedora spec file for php-sabre-dav
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    9f8c1939a3f66eb7170489fc48579ffd1461af62
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     fruux
%global gh_project   sabre-dav
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-%{gh_project}
Summary:        WebDAV Framework for PHP
Version:        2.1.10
Release:        1%{?dist}

URL:            https://github.com/%{gh_owner}/%{gh_project}
License:        BSD
Group:          Development/Libraries
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz
Source1:        %{name}-autoload.php

# replace composer autoloader
Patch0:         %{name}-autoload.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.4.1
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  php-composer(sabre/vobject) >= 3.3.4
BuildRequires:  php-composer(sabre/event)   >= 2.0.0
BuildRequires:  php-composer(sabre/http)    >= 3.0.0
BuildRequires:  php-dom
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-simplexml
BuildRequires:  php-mbstring
BuildRequires:  php-ctype
BuildRequires:  php-date
BuildRequires:  php-iconv
BuildRequires:  php-libxml
BuildRequires:  php-curl
BuildRequires:  php-pdo
# Autoloader
BuildRequires:  php-composer(symfony/class-loader)
BuildRequires:  php-pdo_sqlite
%endif

# From composer.json,    "require": {
#        "php": ">=5.4.1",
#        "sabre/vobject": "^3.3.4",
#        "sabre/event" : "^2.0.0",
#        "sabre/http" : "^3.0.0",
#        "ext-dom": "*",
#        "ext-pcre": "*",
#        "ext-spl": "*",
#        "ext-simplexml": "*",
#        "ext-mbstring" : "*",
#        "ext-ctype" : "*",
#        "ext-date" : "*",
#        "ext-iconv" : "*",
#        "ext-libxml" : "*"
Requires:       php(language) >= 5.4.1
Requires:       php-composer(sabre/vobject) >= 3.3.4
Requires:       php-composer(sabre/vobject) <  4
Requires:       php-composer(sabre/event)   >= 2.0.0
Requires:       php-composer(sabre/event)   <  2.1
Requires:       php-composer(sabre/http)    >= 3.0.0
Requires:       php-composer(sabre/http)    <  3.1
Requires:       php-dom
Requires:       php-pcre
Requires:       php-spl
Requires:       php-simplexml
Requires:       php-mbstring
Requires:       php-ctype
Requires:       php-date
Requires:       php-iconv
Requires:       php-libxml
# From composer.json, "suggest" : {
#        "ext-curl" : "*",
#        "ext-pdo" : "*"
Requires:       php-curl
Requires:       php-pdo
# Autoloader
Requires:       php-composer(symfony/class-loader)

Provides:       php-composer(sabre/dav) = %{version}


%description
What is SabreDAV

SabreDAV allows you to easily add WebDAV support to a PHP application.
SabreDAV is meant to cover the entire standard, and attempts to allow
integration using an easy to understand API.

Feature list:
* Fully WebDAV compliant
* Supports Windows XP, Windows Vista, Mac OS/X, DavFSv2, Cadaver, Netdrive,
  Open Office, and probably more.
* Passing all Litmus tests.
* Supporting class 1, 2 and 3 Webdav servers.
* Locking support.
* Custom property support.
* CalDAV (tested with Evolution, iCal, iPhone and Lightning).
* CardDAV (tested with OS/X addressbook, the iOS addressbook and Evolution).
* Over 97% unittest code coverage.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p0
cp %{SOURCE1} lib/DAV/autoload.php

# drop executable as only provided as doc
chmod -x bin/*


%build
# nothing to build


%install
# Install as a PSR-0 library
mkdir -p %{buildroot}%{_datadir}/php
cp -pr lib %{buildroot}%{_datadir}/php/Sabre



%check
%if %{with_tests}
%if 0%{?rhel} == 5
sed -e 's/testMove/SKIP_testMove/' \
    -i tests/Sabre/DAV/PropertyStorage/Backend/AbstractPDOTest.php
sed -e 's/testCalendarQueryReportWindowsPhone/SKIP_testCalendarQueryReportWindowsPhone/' \
    -i tests/Sabre/CalDAV/PluginTest.php
%endif

: Fix bootstrap
cd tests
sed -e 's:@BUILDROOT@:%{buildroot}:' -i bootstrap.php

: Run upstream test suite against installed library
%{_bindir}/phpunit --verbose

if which php70; then
   php70 %{_bindir}/phpunit --verbose || : ignore test results
fi
%else
: Skip upstream test suite
%endif


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *md
%doc composer.json
%doc examples bin
%{_datadir}/php/Sabre/DAV
%{_datadir}/php/Sabre/DAVACL
%{_datadir}/php/Sabre/CalDAV
%{_datadir}/php/Sabre/CardDAV


%changelog
* Tue Mar 22 2016 Remi Collet <remi@fedoraproject.org> - 2.1.10-1
- update to 2.1.10

* Mon Mar 21 2016 Remi Collet <remi@fedoraproject.org> - 2.1.6-2
- provide missing php-composer(sabre/dav)

* Wed Feb 24 2016 James Hogarth <james.hogarth@gmail.com> - 2.1.6-1
- update to 2.1.6

* Wed Feb 24 2016 Remi Collet <remi@fedoraproject.org> - 2.1.5-1
- update to 2.1.5

* Fri Mar 06 2015 Adam Williamson <awilliam@redhat.com> - 1.8.12-1
- update to 1.8.12 (bugfix release, no bc breaks)

* Thu May 22 2014 Remi Collet <remi@fedoraproject.org> - 1.8.10-1
- update to 1.8.10

* Sun Mar  2 2014 Remi Collet <remi@fedoraproject.org> - 1.8.9-1
- update to 1.8.9

* Thu Feb 20 2014 Remi Collet <remi@fedoraproject.org> - 1.8.8-2
- drop max version for VObject

* Tue Feb 11 2014 Remi Collet <remi@fedoraproject.org> - 1.8.8-1
- update to 1.8.8

* Tue Dec 31 2013 Remi Collet <remi@fedoraproject.org> - 1.8.7-1
- Initial packaging
