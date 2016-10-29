# remirepo/fedora spec file for php-sabre-event
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    337b6f5e10ea6e0b21e22c7e5788dd3883ae73ff
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     fruux
%global gh_project   sabre-event
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-%{gh_project}
Summary:        Lightweight library for event-based programming
Version:        2.0.2
Release:        3%{?dist}

URL:            http://sabre.io/event
License:        BSD
Group:          Development/Libraries
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz
Source1:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.4.1
BuildRequires:  php-composer(phpunit/phpunit)
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)
%endif

# From composer.json, "require": {
#        "php": ">=5.4.1"
Requires:       php(language) >= 5.4.1
# From phpcompatinfo report for version 2.0.2
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(sabre/event) = %{version}


%description
A lightweight library for event management in PHP.
It's design is inspired by Node.js's EventEmitter. sabre/event requires PHP 5.4.

Autoloader: %{_datadir}/php/Sabre/Event/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE1} lib/autoload.php


%build
# nothing to build


%install
rm -rf %{buildroot}

# Install as a PSR-0 library
mkdir -p %{buildroot}%{_datadir}/php/Sabre
cp -pr lib %{buildroot}%{_datadir}/php/Sabre/Event


%check
%if %{with_tests}
: Run upstream test suite against installed library
# remirepo:11
ret=0
run=0
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap=%{buildroot}%{_datadir}/php/Sabre/Event/autoload.php || ret=1
   run=1
fi
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap=%{buildroot}%{_datadir}/php/Sabre/Event/autoload.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit \
  --bootstrap=%{buildroot}%{_datadir}/php/Sabre/Event/autoload.php \
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
%{_datadir}/php/Sabre


%changelog
* Sat Oct 29 2016 Remi Collet <remi@fedoraproject.org> - 2.0.2-3
- switch from symfony/class-loader to fedora/autoloader

* Mon Jul 20 2015 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- update to 2.0.2
- add autoloader

* Fri Jun 13 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- add provides php-composer(sabre/event)
- change url to http://sabre.io/event

* Tue Dec 31 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- Initial packaging
