# Spec file for php-sabre-http
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    1edcd387535d10a5a5c0e0fd2f3192d1e3156970
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     fruux
%global gh_project   sabre-http
%global prever       alpha6
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-%{gh_project}
Summary:        Library for dealing with http requests and responses
Version:        2.0.0
Release:        0.2.%{prever}%{?dist}

URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?prever}.tar.gz
License:        BSD
Group:          Development/Libraries

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) > 5.4
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit)
BuildRequires:  php-sabre-event >= 1.0.0
BuildRequires:  php-sabre-event <  1.1
%endif

# From composer.json
Requires:       php(language) > 5.4
Requires:       php-curl
Requires:       php-mbstring
Requires:       php-sabre-event >= 1.0.0
Requires:       php-sabre-event <  1.1
# From phpcompatinfo report for version 1.0.0alpha5
Requires:       php-ctype
Requires:       php-date
Requires:       php-pcre
Requires:       php-spl
Requires:       php-xml
# Was split from php-sabre-dav in version 1.9
Conflicts:      php-sabre-dav < 1.9


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

: Create trivial PSR0 autoloader
cat <<EOF | tee psr0.php
<?php
spl_autoload_register(function (\$class) {
    \$file = str_replace('\\\\', '/', \$class).'.php';
    @include \$file;
});
EOF


%build
# nothing to build


%install
# Install as a PSR-0 library
mkdir -p %{buildroot}%{_datadir}/php
cp -pr lib/Sabre %{buildroot}%{_datadir}/php/Sabre


%check
%if %{with_tests}
: Run upstream test suite against installed library
cd tests
phpunit \
  --bootstrap=../psr0.php \
  --include-path=%{buildroot}%{_datadir}/php \
  -d date.timezone=UTC
%else
: Skip upstream test suite
%endif


%files
%defattr(-,root,root,-)
%doc ChangeLog composer.json LICENSE README.md
%{_datadir}/php/Sabre/HTTP


%changelog
* Tue Jan  7 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.2.alpha6
- update to 2.0.0alpha6
- add explicit conflicts with php-sabre-dav < 1.9

* Tue Dec 31 2013 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.alpha5
- Initial packaging