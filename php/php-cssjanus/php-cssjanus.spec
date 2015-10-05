Name:		php-cssjanus
Version:	1.1.1
Release:	1%{?dist}
Summary:	Convert CSS stylesheets between left-to-right and right-to-left

License:	ASL 2.0
URL:		https://github.com/cssjanus/php-cssjanus
Source0:	https://github.com/cssjanus/php-cssjanus/archive/v%{version}.tar.gz#/php-cssjanus-%{version}.tar.gz
Source1:	https://github.com/cssjanus/cssjanus/raw/v%{version}/test/data.json#/php-cssjanus-data.json

BuildArch:	noarch

BuildRequires:	php-phpunit-PHPUnit

Requires:	php(language) >= 5.3.3
Requires:	php-pcre

Provides:	php-composer(cssjanus/cssjanus) = %{version}


%description
Convert CSS stylesheets between left-to-right and right-to-left.


%prep
%setup -qn php-cssjanus-%{version}
cp -p %{SOURCE1} test/data-v%{version}.json


%build


%install
mkdir -pm 0755 %{buildroot}%{_datadir}/php/cssjanus
cp -p src/CSSJanus.php %{buildroot}%{_datadir}/php/cssjanus


%check
phpunit --bootstrap src/CSSJanus.php test/


%files
%license APACHE-LICENSE-2.0.txt
%doc README.md
%{_datadir}/php/cssjanus


%changelog
* Wed Sep 30 2015 Michael Cronenworth <mike@cchtml.com> - 1.1.1-1
- Initial package

