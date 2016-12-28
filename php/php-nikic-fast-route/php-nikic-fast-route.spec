# remirepo spec file for php-nikic-fast-route, from
#
# Fedora spec file for php-nikic-fast-route
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries

%global gh_commit    f3dcf5130e634b6123d40727d612ec6aa4f61fb3
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nikic
%global gh_project   FastRoute
%global pk_project   fast-route
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{pk_project}
Version:        1.1.0
Release:        1%{?dist}
Summary:        Fast implementation of a regular expression based router

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source:         https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz
Source1:        php-%{gh_owner}-%{pk_project}-tests-autoloader.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# For tests
BuildRequires:  php(language) >= 5.4
BuildRequires:  php-pcre
BuildRequires:  php-spl
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "~4.0"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.0
%endif

# From composer.json, "require": {
#        "php": ">=5.4",
Requires:       php(language) >= 5.4
# From phpcompatinfo 5.0.0 report for version 1.0.0
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(%{gh_owner}/%{pk_project}) = %{version}


%description
Fast implementation of a regular expression based router.

Documentation:
http://nikic.github.io/2014/02/18/Fast-request-routing-using-regular-expressions.html

Autoloader: %{php_home}/%{gh_project}/bootstrap.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
#Nothing to build


%install
rm -rf %{buildroot}

#: Library
mkdir -p                %{buildroot}%{php_home}
cp -pr src              %{buildroot}%{php_home}/%{gh_project}


%check
%if %{with_tests}
#ensure tests are not ran against local sources
rm -rf src
cp %{SOURCE1}       test/bootstrap.php
sed -e "s|BUILDROOT_PATH|%{buildroot}/%{php_home}/%{gh_project}|" -i test/bootstrap.php

: Run upstream test suite
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
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json
%doc *.md
%{php_home}/%{gh_project}


%changelog
* Sat Jun 25 2016 Johan Cwiklinski <johan AT x-tnd DOT be> - 1.0.1-1
- Last upstream release

* Fri May 06 2016 Johan Cwiklinski <johan AT x-tnd DOT be> - 1.0.0-2
- Fix package name

* Fri May 06 2016 Johan Cwiklinski <johan AT x-tnd DOT be> - 1.0.0-1
- Initial packaging
