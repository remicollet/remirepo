%global libname Monolog

Name:      php-%{libname}
Version:   1.2.1
Release:   1%{?dist}
Summary:   Logging for PHP 5.3

Group:     Development/Libraries
License:   MIT
URL:       https://github.com/Seldaek/monolog
Source0:   %{url}/archive/%{version}.tar.gz

BuildArch: noarch

Requires:  php-common >= 5.3.0
Requires:  php-pear(pear.swiftmailer.org/Swift)
# phpci requires
Requires:  php-curl
Requires:  php-date
Requires:  php-json
Requires:  php-libxml
Requires:  php-pcre
Requires:  php-sockets
Requires:  php-spl
# phpci dist specific requires
%{?fedora:Requires: php-filter}

%description
%{summary}.

Optional packages:
* php-%{libname}-amqp
      Allow sending log messages to an AMQP server (1.0+ required)
* php-%{libname}-mongo
      Allow sending log messages to a MongoDB server
* https://github.com/mlehner/gelf-php
      Allow sending log messages to a GrayLog2 server


%package amqp
Summary:  Monolog AMQP handler
Requires: php-%{libname} = %{version}-%{release}
Requires: php-pecl(amqp)

%description amqp
Allow sending log messages to an AMQP server (1.0+ required).


%package mongo
Summary:  Monolog MongoDB handler
Requires: php-%{libname} = %{version}-%{release}
Requires: php-pecl(mongo)

%description mongo
Allow sending log messages to a MongoDB server.


%prep
%setup -q -n monolog-%{version}


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php/%{libname}
cp -pr src/%{libname} %{buildroot}%{_datadir}/php/


%files
%doc LICENSE *.mdown doc composer.json
%{_datadir}/php/%{libname}
%exclude %{_datadir}/php/%{libname}/Handler/MongoDBHandler.php
%exclude %{_datadir}/php/%{libname}/Handler/AmqpHandler.php

%files amqp
%{_datadir}/php/%{libname}/Handler/AmqpHandler.php

%files mongo
%{_datadir}/php/%{libname}/Handler/MongoDBHandler.php


%changelog
* Sat Nov 17 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.2.1-1
- Updated to upstream version 1.2.1
- Changed %%{libname} from monolog to Monolog
- Fixed license
- GitHub archive source
- Added php-pear(pear.swiftmailer.org/Swift), php-curl, and php-sockets requires
- Added optional packages note in %%{description}
- Simplified %%prep
- Added subpackages for AMQP and MongoDB handlers
- Changed RPM_BUILD_ROOT to %%{buildroot}

* Sun Jul 22 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-1
- Initial package
