# remirepo spec file for php-liuggio-statsd-php-client, from Fedora
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
Name:		php-liuggio-statsd-php-client
Version:	1.0.16
Release:	1%{?dist}
Summary:	Object Oriented Client for etsy/statsd written in php
Group:		Development/Libraries

License:	MIT
URL:		https://github.com/liuggio/statsd-php-client
Source0:	https://github.com/liuggio/statsd-php-client/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

Buildarch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	php(language) >= 5.3.2

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


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGELOG.md composer.json README.md
%{_datadir}/php/Liuggio


%changelog
* Tue Jun 16 2015 Remi Collet <remi@remirepo.net> - 1.0.16-1
- add backport stuff for remirepo

* Mon Jun 15 2015 Michael Cronenworth <mike@cchtml.com> - 1.0.16-1
- Initial package

