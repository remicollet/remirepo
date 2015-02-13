# spec file for php-doctrine-instantiator
#
# Copyright (c) 2014-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#

# bootstrap needed when rebuilding PHPUnit for new major version
%global bootstrap    0
%global gh_commit    f976e5de371104877ebc89bd8fecb0019ed9c119
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     doctrine
%global gh_project   instantiator
%if %{bootstrap}
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-doctrine-instantiator
Version:        1.0.4
Release:        2%{?dist}
Summary:        Instantiate objects in PHP without invoking their constructors

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
BuildRequires:  php(language) >= 5.3
BuildRequires:  php-phar
BuildRequires:  php-pdo
BuildRequires:  php-reflection
BuildRequires:  %{_bindir}/phpunit
%endif

# From composer.json
#        "php": "~5.3"
Requires:       php(language) >= 5.3
# From phpcompatinfo report for version 1.0.0
Requires:       php-reflection

Provides:       php-composer(doctrine/instantiator) = %{version}


%description
This library provides a way of avoiding usage of constructors when
instantiating PHP classes.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate a simple autoloader
%{_bindir}/phpab \
    --output src/Doctrine/Instantiator/autoload.php \
    src/Doctrine/Instantiator


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{_datadir}/php
cp -pr src/* %{buildroot}%{_datadir}/php


%check
%if %{with_tests}
: Generate autoloader
%{_bindir}/phpab \
    --basedir $PWD \
    --output autoload.php \
    src tests

if [ -d /usr/share/php/PHPUnit ] \
   && grep -q Doctrine /usr/share/php/PHPUnit/Autoload.php
then
  # Hack PHPUnit >= 4.3 autoloader to not use system Instantiator
  mkdir PHPUnit
  sed -e '/Doctrine\\\\Instantiator/d' \
    -e 's:dirname(__FILE__):"/usr/share/php/PHPUnit":' \
    /usr/share/php/PHPUnit/Autoload.php \
    >PHPUnit/Autoload.php
fi

sed -e '/log/d' phpunit.xml.dist >phpunit.xml

: Run test suite
%{_bindir}/phpunit \
    --bootstrap autoload.php
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md composer.json
%dir %{_datadir}/php/Doctrine
%{_datadir}/php/Doctrine/Instantiator


%changelog
* Fri Feb 13 2015 Remi Collet <remi@fedoraproject.org> - 1.0.4-2
- add autoloader

* Mon Oct 13 2014 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- update to 1.0.4 (no change)

* Sun Oct  5 2014 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- update to 1.0.3

* Mon Aug 25 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- initial package, version 1.0.2