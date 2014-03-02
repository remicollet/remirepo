# Spec file for php-sabre-dav
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    25e095469e44d195cd255bdce55ce473224558bc
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     fruux
%global gh_project   sabre-dav
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-%{gh_project}
Summary:        WebDAV Framework for PHP
Version:        1.8.9
Release:        1%{?dist}

URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz
License:        BSD
Group:          Development/Libraries

# replace composer autoloader with trivial PSR-0 one
Patch0:         %{gh_project}-autoload.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.1
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit) > 3.7
BuildRequires:  php-sabre-vobject > 2.1
Requires:       php-pdo
%endif

# From composer.json
Requires:       php(language) >= 5.3.1
Requires:       php-ctype
Requires:       php-date
Requires:       php-dom
Requires:       php-iconv
Requires:       php-libxml
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-simplexml
Requires:       php-spl
Requires:       php-sabre-vobject > 2.1
# From phpcompatinfo report for version 1.8.7
Requires:       php-curl
Requires:       php-pdo
Requires:       php-xml


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

: Create trivial PSR0 autoloader for tests
cat <<EOF | tee psr0.php
<?php
define('SABRE_HASSQLITE', 1);
define('SABRE_HASMYSQL', 0);
define("SABRE_TEMPDIR", __DIR__ . '/temp/');

spl_autoload_register(function (\$class) {
    \$file = str_replace('\\\\', '/', \$class).'.php';
    @include \$file;
});
EOF

# drop executable as only provided as doc
chmod -x bin/*


%build
# nothing to build


%install
# Install as a PSR-0 library
mkdir -p %{buildroot}%{_datadir}/php
cp -pr lib/Sabre %{buildroot}%{_datadir}/php/Sabre



%check
: Check that our autoloader is working
php -d include_path=%{buildroot}%{_datadir}/php \
    -r 'include "Sabre/autoload.php"; echo Sabre\DAV\Version::VERSION."\n";' \
    | grep %{version}

%if %{with_tests}
: Run upstream test suite against installed library
mkdir temp
cd tests
phpunit \
  --bootstrap=../psr0.php \
  --include-path=%{buildroot}%{_datadir}/php \
  -d date.timezone=GMT
%else
: Skip upstream test suite
%endif


%files
%defattr(-,root,root,-)
%doc ChangeLog composer.json LICENSE README.md
%doc docs examples bin
%{_datadir}/php/Sabre


%changelog
* Sun Mar  2 2014 Remi Collet <remi@fedoraproject.org> - 1.8.9-1
- update to 1.8.9

* Thu Feb 20 2014 Remi Collet <remi@fedoraproject.org> - 1.8.8-2
- drop max version for VObject

* Tue Feb 11 2014 Remi Collet <remi@fedoraproject.org> - 1.8.8-1
- update to 1.8.8

* Tue Dec 31 2013 Remi Collet <remi@fedoraproject.org> - 1.8.7-1
- Initial packaging