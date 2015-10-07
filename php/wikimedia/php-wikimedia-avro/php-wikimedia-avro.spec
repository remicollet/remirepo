%global git_tag_rev c8c12cb47e4ad9a534926d2ace5d8f64b319fa26

Name:		php-wikimedia-avro
Version:	1.7.7
Release:	1%{?dist}
Summary:	A library for using Avro with PHP

License:	ASL 2.0
URL:		https://avro.apache.org/
Source0:	http://git.wikimedia.org/zip/?r=avro-php.git&format=xz&h=%{git_tag_rev}#/%{name}-%{version}.tar.xz

BuildArch:	noarch

BuildRequires:  php-theseer-autoload

Requires:	php(language) >= 5.3.0
Requires:	php-date
Requires:	php-gmp
Requires:	php-json
Requires:	php-pcre
Requires:	php-spl

Provides:	php-composer(wikimedia/avro) = %{version}


%description
A library for using Apache Avro with PHP. Avro is a data serialization system.


%prep
%setup -qc %{name}-%{version}


%build
phpab --output lib/autoload.php lib


%install
mkdir -pm 0755 %{buildroot}%{_datadir}/php/avro
cp -rp lib/* %{buildroot}%{_datadir}/php/avro


%files
%license LICENSE.txt
%doc composer.json README.md NOTICE.txt
%{_datadir}/php/avro


%changelog
* Thu Sep 17 2015 Michael Cronenworth <mike@cchtml.com> - 1.7.7-1
- Initial package

