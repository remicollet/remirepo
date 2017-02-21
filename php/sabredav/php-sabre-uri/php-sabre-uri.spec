# remirepo/fedora spec file for php-sabre-uri
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    ada354d83579565949d80b2e15593c2371225e61
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     fruux
%global gh_project   sabre-uri
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_project}
Summary:        Functions for making sense out of URIs
Version:        1.2.1
Release:        1%{?dist}

URL:            https://github.com/%{gh_owner}/%{gh_project}
License:        BSD
Group:          Development/Libraries
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz
Source1:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) > 5.4.7
# From composer.json, "require-dev": {
#        "sabre/cs": "~1.0.0",
#        "phpunit/phpunit" : ">=4.0,<6.0"
BuildRequires:  php-pcre
BuildRequires:  php-composer(phpunit/phpunit)
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)
%endif

# From composer.json, "require" : {
#        "php": ">=5.4.7"
Requires:       php(language) > 5.4.7
# From phpcompatinfo report for version 1.1.0
Requires:       php-pcre
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(sabre/uri) = %{version}


%description
sabre/uri is a lightweight library that provides several functions for
working with URIs, staying true to the rules of RFC3986.

Partially inspired by Node.js URL library, and created to solve real
problems in PHP applications. 100% unitested and many tests are based
on examples from RFC3986.

The library provides the following functions:
* resolve to resolve relative urls.
* normalize to aid in comparing urls.
* parse, which works like PHP's parse_url.
* build to do the exact opposite of parse.
* split to easily get the 'dirname' and 'basename' of a URL without
  all the problems those two functions have.

Autoloader: %{_datadir}/php/Sabre/Uri/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE1} lib/autoload.php


%build
# nothing to build


%install
rm -rf %{buildroot}

# Install as a PSR-0 library
mkdir -p %{buildroot}%{_datadir}/php/Sabre
cp -pr lib %{buildroot}%{_datadir}/php/Sabre/Uri


%check
%if %{with_tests}
: Run upstream test suite against installed library
cd tests
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap=%{buildroot}%{_datadir}/php/Sabre/Uri/autoload.php || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap=%{buildroot}%{_datadir}/php/Sabre/Uri/autoload.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit \
  --bootstrap=%{buildroot}%{_datadir}/php/Sabre/Uri/autoload.php \
  --verbose
# remirepo:2
fi
exit $ret
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
%dir %{_datadir}/php/Sabre
     %{_datadir}/php/Sabre/Uri


%changelog
* Tue Feb 21 2017 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- update to 1.2.1

* Sat Oct 29 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-2
- switch from symfony/class-loader to fedora/autoloader

* Thu Oct 27 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1

* Fri Mar 11 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Initial packaging

