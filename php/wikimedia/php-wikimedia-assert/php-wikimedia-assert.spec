# remirepo spec file for php-wikimedia-utfnormal, from Fedora
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
Name:		php-wikimedia-assert
Version:	0.2.2
Release:	1%{?dist}
Summary:	An alternative to PHP's assert
Group:		Development/Libraries

License:	MIT
URL:		https://github.com/wmde/Assert
Source0:	https://github.com/wmde/Assert/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

BuildRequires:	php-phpunit-PHPUnit
BuildRequires:	php-theseer-autoload

Requires:	php(language) >= 5.3.0
Requires:	php-spl

Provides:	php-composer(wikimedia/assert) = %{version}


%description
This package provides an alternative to PHP's assert() that allows for a
simple and reliable way to check preconditions and postconditions in PHP
code. It was proposed as a MediaWiki RFC, but is completely generic and
can be used by any PHP program or library.


%prep
%setup -qn Assert-%{version}


%build
phpab --output src/autoload.php src


%install
rm -rf %{buildroot}

mkdir -pm 0755 %{buildroot}%{_datadir}/php/Wikimedia/Assert
cp -rp src/* %{buildroot}%{_datadir}/php/Wikimedia/Assert


%check
phpunit -v --bootstrap %{buildroot}%{_datadir}/php/Wikimedia/Assert/autoload.php


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc composer.json README.md
%{_datadir}/php/Wikimedia


%changelog
* Fri Oct  9 2015 Remi Collet <remi@remirepo.net> - 0.2.2-1
- add backport stuff for remirepo

* Mon Oct 05 2015 Michael Cronenworth <mike@cchtml.com> - 0.2.2-1
- Initial package

