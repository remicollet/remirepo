Name:		php-wikimedia-assert
Version:	0.2.2
Release:	1%{?dist}
Summary:	An alternative to PHP's assert

License:	MIT
URL:		https://github.com/wmde/Assert
Source0:	https://github.com/wmde/Assert/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

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
mkdir -pm 0755 %{buildroot}%{_datadir}/php/Wikimedia/Assert
cp -rp src/* %{buildroot}%{_datadir}/php/Wikimedia/Assert


%check
phpunit -v --bootstrap %{buildroot}%{_datadir}/php/Wikimedia/Assert/autoload.php


%files
%license COPYING
%doc composer.json README.md
%{_datadir}/php/Wikimedia


%changelog
* Mon Oct 05 2015 Michael Cronenworth <mike@cchtml.com> - 0.2.2-1
- Initial package

