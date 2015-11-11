# remirepo spec file for php-zordius-lightncandy, from
#
# Fedora spec file for php-zordius-lightncandy
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global	handlebars_git df077dd262eea766648af0b6efd8a22e44c78178
%global	mustache_git 83b0721610a4e11832e83df19c73ace3289972b9

Name:		php-zordius-lightncandy
Version:	0.23
Release:	1%{?dist}
Summary:	An extremely fast PHP implementation of handlebars and mustache
Group:		Development/Libraries

License:	MIT
URL:		https://github.com/zordius/lightncandy
Source0:	https://github.com/zordius/lightncandy/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Tests require data from third-party repositories
Source1:	https://github.com/kasperisager/handlebars-spec/archive/%{handlebars_git}.tar.gz#/%{name}-handlebars.tar.gz
Source2:	https://github.com/mustache/spec/archive/%{mustache_git}.tar.gz#/%{name}-mustache.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
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
rm -rf %{buildroot}

mkdir -pm 0755 %{buildroot}%{_datadir}/php/zordius/lightncandy
cp -p src/autoload.php %{buildroot}%{_datadir}/php/zordius/lightncandy
cp -p src/lightncandy.php %{buildroot}%{_datadir}/php/zordius/lightncandy


%check
%{_bindir}/phpunit -v --filter test

if which php70; then
  php70 %{_bindir}/phpunit -v --filter test || exit 0
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc composer.json CONTRIBUTING.md HISTORY.md README.md UPGRADE.md
%{_datadir}/php/zordius


%changelog
* Wed Nov 11 2015 Remi Collet <remi@remirepo.net> - 0.23-1
- update to 0.23 (backported from Fedora)
- run test suite against PHP 7 (broken for now)

* Wed Nov 11 2015 Michael Cronenworth <mike@cchtml.com> - 0.23-1
- version update

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 0.22-1
- backport for remi repo, add EL-5 stuff

* Fri Oct 09 2015 Michael Cronenworth <mike@cchtml.com> - 0.22-1
- Initial package

