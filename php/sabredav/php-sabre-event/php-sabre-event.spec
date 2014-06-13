# Spec file for php-sabre-event
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    5ee3adf5441c2fe53b8ceacff6db81e621ee884c
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     fruux
%global gh_project   sabre-event
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-%{gh_project}
Summary:        Lightweight library for event-based programming
Version:        1.0.1
Release:        1%{?dist}

URL:            http://sabre.io/event
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz
License:        BSD
Group:          Development/Libraries

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.4.1
BuildRequires:  php-phpunit-PHPUnit
%endif

# From composer.json
Requires:       php(language) >= 5.4.1
# From phpcompatinfo report: nothing else

Provides:       php-composer(sabre/event) = %{version}


%description
A lightweight library for event management in PHP.
It's design is inspired by Node.js's EventEmitter. sabre/event requires PHP 5.4.


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
%{_datadir}/php/Sabre


%changelog
* Fri Jun 13 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- add provides php-composer(sabre/event)
- change url to http://sabre.io/event

* Tue Dec 31 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- Initial packaging
