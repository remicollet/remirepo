%global	handlebars_git df077dd262eea766648af0b6efd8a22e44c78178
%global	mustache_git 83b0721610a4e11832e83df19c73ace3289972b9

Name:		php-zordius-lightncandy
Version:	0.22
Release:	1%{?dist}
Summary:	An extremely fast PHP implementation of handlebars and mustache

License:	MIT
URL:		https://github.com/zordius/lightncandy
Source0:	https://github.com/zordius/lightncandy/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Tests require data from third-party repositories
Source1:	https://github.com/kasperisager/handlebars-spec/archive/%{handlebars_git}.tar.gz#/%{name}-handlebars.tar.gz
Source2:	https://github.com/mustache/spec/archive/%{mustache_git}.tar.gz#/%{name}-mustache.tar.gz

BuildArch:	noarch

BuildRequires:	php-phpunit-PHPUnit
BuildRequires:	php-theseer-autoload

Requires:	php(language) >= 5.3.0
Requires:	php-pcre
Requires:	php-reflection
Requires:	php-spl

Provides:	php-composer(zordius/lightncandy) = %{version}

%description
An extremely fast PHP implementation of handlebars ( http://handlebarsjs.com/ )
and mustache ( http://mustache.github.io/ ).


%prep
%setup -qn lightncandy-%{version}
tar zxf %{SOURCE1}
cp -rp handlebars-spec-%{handlebars_git}/spec specs/handlebars/
tar zxf %{SOURCE2}
cp -rp spec-%{mustache_git}/specs specs/mustache/


%build
phpab --output src/autoload.php src


%install
mkdir -pm 0755 %{buildroot}%{_datadir}/php/zordius/lightncandy
cp -p src/autoload.php %{buildroot}%{_datadir}/php/zordius/lightncandy
cp -p src/lightncandy.php %{buildroot}%{_datadir}/php/zordius/lightncandy


%check
phpunit -v --filter test


%files
%license LICENSE.txt
%doc composer.json CONTRIBUTING.md HISTORY.md README.md UPGRADE.md
%{_datadir}/php/zordius


%changelog
* Fri Oct 09 2015 Michael Cronenworth <mike@cchtml.com> - 0.22-1
- Initial package

