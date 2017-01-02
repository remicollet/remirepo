# remirepo/fedora spec file for php-sabre-dav
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    b42593965211de1ce99f73bd3aede99c41258e08
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     fruux
%global gh_project   sabre-dav
%if 0%{?rhel} == 5
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_project}
Summary:        WebDAV Framework for PHP
Version:        3.0.9
Release:        3%{?dist}

URL:            https://github.com/%{gh_owner}/%{gh_project}
License:        BSD
Group:          Development/Libraries
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz
Source1:        %{name}-autoload.php

# replace composer autoloader
Patch0:         %{name}-autoload.patch
# upstream patch for 7.1
Patch1:         %{name}-php71.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.4.1
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  php-composer(sabre/vobject) >= 3.3.4
BuildRequires:  php-composer(sabre/event)   >= 2.0
BuildRequires:  php-composer(sabre/xml)     >= 1.0
BuildRequires:  php-composer(sabre/http)    >= 4.0
BuildRequires:  php-composer(sabre/uri)     >= 1.0
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
BuildRequires:  php-composer(fedora/autoloader)
BuildRequires:  php-pdo_sqlite
%endif

# From composer.json,    "require": {
#        "php": ">=5.4.1",
#        "sabre/vobject": "^3.3.4",
#        "sabre/event" : "~2.0",
#        "sabre/xml"  : "~1.0",
#        "sabre/http" : "~4.0",
#        "sabre/uri" : "~1.0",
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
Requires:       php-composer(sabre/event)   >= 2.0
Requires:       php-composer(sabre/event)   <  3
Requires:       php-composer(sabre/xml)     >= 1.0
Requires:       php-composer(sabre/xml)     <  2
Requires:       php-composer(sabre/http)    >= 4.0
Requires:       php-composer(sabre/http)    <  5
Requires:       php-composer(sabre/uri)     >= 1.0
Requires:       php-composer(sabre/uri)     <  2
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
Requires:       php-composer(fedora/autoloader)

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

Autoloader: %{_datadir}/php/Sabre/DAV/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p0
%patch1 -p1
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
%endif

: Fix bootstrap
cd tests
sed -e 's:@BUILDROOT@:%{buildroot}:' -i bootstrap.php

: Run upstream test suite against installed library
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose
# remirepo:2
fi
exit $ret
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
* Wed Nov 23 2016 Remi Collet <remi@fedoraproject.org> - 3.0.9-3
- add upstream patch to fix FTBFS with php 7.1

* Sat Oct 29 2016 Remi Collet <remi@fedoraproject.org> - 3.0.9-2
- switch from symfony/class-loader to fedora/autoloader

* Thu Apr  7 2016 Remi Collet <remi@fedoraproject.org> - 3.0.9-1
- update to 3.0.9
- add dependency on sabre/xml
- add dependency on sabre/uri
- raise dependency on sabre/http >= 4

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
