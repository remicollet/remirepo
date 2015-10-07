%global git_tag_rev 3c2dd6706546fe616e6ceba02044e64dce4fc9be

Name:		php-wikimedia-ip-set
Version:	0
Release:	0.1.20150917git%{?dist}
Summary:	Library to match IP addresses against CIDR specifications

License:	GPLv2+
URL:		http://www.mediawiki.org/wiki/IPSet
Source0:	http://git.wikimedia.org/zip/?r=IPSet.git&format=xz&h=%{git_tag_rev}#/%{name}-%{version}.tar.xz

BuildArch:	noarch

BuildRequires:	php-phpunit-PHPUnit
BuildRequires:	php-theseer-autoload

Requires:	php(language) >= 5.3.0
Requires:	php-ctype
Requires:	php-spl

Provides:	php-composer(wikimedia/ip-set) = %{version}


%description
IPSet is a PHP library to match IPs against CIDR specs.


%prep
%setup -qc %{name}-%{version}


%build
phpab --output src/autoload.php src


%install
mkdir -pm 0755 %{buildroot}%{_datadir}/php/IPSet
cp -rp src/* %{buildroot}%{_datadir}/php/IPSet


%check
phpunit -v --bootstrap %{buildroot}%{_datadir}/php/IPSet/autoload.php


%files
%license COPYING
%doc composer.json README.md
%{_datadir}/php/IPSet


%changelog
* Thu Sep 17 2015 Michael Cronenworth <mike@cchtml.com> - 0-0.1.20150917git
- Initial package

