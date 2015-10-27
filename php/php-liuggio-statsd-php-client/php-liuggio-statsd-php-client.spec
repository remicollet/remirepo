# remirepo spec file for php-liuggio-statsd-php-client, from Fedora
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
Name:		php-liuggio-statsd-php-client
Version:	1.0.18
Release:	1%{?dist}
Summary:	Object Oriented Client for etsy/statsd written in php
Group:		Development/Libraries

License:	MIT
URL:		https://github.com/liuggio/statsd-php-client
Source0:	https://github.com/liuggio/statsd-php-client/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:	%{name}-autoload.php

BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# For tests
BuildRequires:	php-composer(phpunit/phpunit) >= 4.7
BuildRequires:	php-composer(symfony/class-loader)
BuildRequires:	php-composer(monolog/monolog) >= 1.2.0

# From composer.json
Requires:	php(language) >= 5.3.2
# From phpcompatinfo report for 1.0.16
Requires:	php-pcre
Requires:	php-sockets
Requires:	php-spl
# For our autoloader
Requires:	php-composer(symfony/class-loader)

Provides:	php-composer(liuggio/statsd-php-client) = %{version}


%description
statsd-php-client is an Open Source, and Object Oriented Client for etsy/statsd
written in php.


%prep
%setup -qn statsd-php-client-%{version}


%build


%install
rm -rf %{buildroot}

mkdir -pm 0755 %{buildroot}%{_datadir}/php/Liuggio/StatsdClient
cp -rp src/Liuggio/StatsdClient/* %{buildroot}%{_datadir}/php/Liuggio/StatsdClient
cp -p %{SOURCE1} %{buildroot}%{_datadir}/php/Liuggio/StatsdClient/autoload.php


%check
phpunit -v \
    --bootstrap=%{buildroot}%{_datadir}/php/Liuggio/StatsdClient/autoload.php


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGELOG.md composer.json README.md
%{_datadir}/php/Liuggio


%changelog
* Sat Oct 24 2015 Michael Cronenworth <mike@cchtml.com> - 1.0.18-1
- version update

* Mon Aug 10 2015 Remi Collet <remi@remirepo.net> - 1.0.18-1
- update to 1.0.18

* Tue Jun 23 2015 Michael Cronenworth <mike@cchtml.com> - 1.0.16-3
- Fix Requires, install autoloader

* Tue Jun 16 2015 Remi Collet <remi@remirepo.net> - 1.0.16-1
- add backport stuff for remirepo
- run test suite during build
- add missing dependencies
- add autoloader

* Mon Jun 15 2015 Michael Cronenworth <mike@cchtml.com> - 1.0.16-1
- Initial package

