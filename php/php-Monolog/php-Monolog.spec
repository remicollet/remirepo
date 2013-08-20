%global github_owner   Seldaek
%global github_name    monolog
%global github_version 1.6.0
%global github_commit  f72392d0e6eb855118f5a84e89ac2d257c704abd

%global lib_name       Monolog

%global php_min_ver    5.3.0
%global psrlog_min_ver 1.0
%global psrlog_max_ver 2.0
%global raven_min_ver  0.5.0
#%%global raven_max_ver  0.6.0

Name:      php-%{lib_name}
Version:   %{github_version}
Release:   1%{?dist}
Summary:   Sends your logs to files, sockets, inboxes, databases and various web services

Group:     Development/Libraries
License:   MIT
URL:       https://github.com/%{github_owner}/%{github_name}
Source0:   %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# For tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
BuildRequires: php-PsrLog >= %{psrlog_min_ver}
BuildRequires: php-PsrLog <  %{psrlog_max_ver}
# For tests: phpcompatinfo
BuildRequires: php-curl
BuildRequires: php-date
BuildRequires: php-filter
BuildRequires: php-hash
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-sockets
BuildRequires: php-spl
BuildRequires: php-xml

Requires:      php(language) >= %{php_min_ver}
Requires:      php-PsrLog >= %{psrlog_min_ver}
Requires:      php-PsrLog <  %{psrlog_max_ver}
Requires:      php-pear(pear.swiftmailer.org/Swift)
# phpcompatinfo
Requires:      php-curl
Requires:      php-date
Requires:      php-filter
Requires:      php-hash
Requires:      php-json
Requires:      php-pcre
Requires:      php-sockets
Requires:      php-spl
Requires:      php-xml

%description
Monolog sends your logs to files, sockets, inboxes, databases and various web
services. Special handlers allow you to build advanced logging strategies.

This library implements the PSR-3 [1] interface that you can type-hint against
in your own libraries to keep a maximum of interoperability. You can also use it
in your applications to make sure you can always use another compatible logger
at a later time.

Optional packages:
* %{name}-amqp
      Allow sending log messages to an AMQP server (1.0+ required)
* %{name}-mongo
      Allow sending log messages to a MongoDB server
* %{name}-raven
      Allow sending log messages to a Sentry server
* https://github.com/doctrine/couchdb-client
      Allow sending log messages to a CouchDB server
* https://github.com/mlehner/gelf-php
      Allow sending log messages to a GrayLog2 server

[1] https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-3-logger-interface.md


%package amqp
Summary:  Monolog AMQP handler
Group:    Development/Libraries
Requires: php-%{lib_name} = %{version}-%{release}
Requires: php-pecl(amqp)

%description amqp
Allow sending log messages to an AMQP server (1.0+ required).


%package mongo
Summary:  Monolog MongoDB handler
Group:    Development/Libraries
Requires: php-%{lib_name} = %{version}-%{release}
Requires: php-pecl(mongo)

%description mongo
Allow sending log messages to a MongoDB server.


%package raven
Summary:  Monolog Sentry handler
Group:    Development/Libraries
Requires: php-%{lib_name} = %{version}-%{release}
Requires: php-Raven >= %{raven_min_ver}
%{?raven_max_ver:Requires: php-Raven < %{raven_max_ver}}
Provides: %{name}-Raven = %{version}-%{release}

%description raven
Allow sending log messages to a Sentry server.


%prep
%setup -q -n %{github_name}-%{github_commit}

# Rewrite tests' bootstrap
( cat <<'AUTOLOAD'
<?php
set_include_path(get_include_path() . PATH_SEPARATOR . __DIR__);

spl_autoload_register(function ($class) {
    $src = str_replace(array('\\', '_'), '/', $class).'.php';
    @include_once $src;
});
AUTOLOAD
) > ./tests/bootstrap.php


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php/%{lib_name}
cp -pr ./src/%{lib_name} %{buildroot}%{_datadir}/php/


%check
# Remove MongoDBHandlerTest because it requires a running MongoDB server
rm -f tests/Monolog/Handler/MongoDBHandlerTest.php

%{_bindir}/phpunit \
    -d include_path="./src:./tests:.:%{_datadir}/php:%{pear_phpdir}" \
    -d date.timezone="UTC" \
    -c ./phpunit.xml.dist


%files
%defattr(-,root,root,-)
%doc LICENSE *.mdown doc composer.json
%{_datadir}/php/%{lib_name}
%exclude %{_datadir}/php/%{lib_name}/Handler/AmqpHandler.php
%exclude %{_datadir}/php/%{lib_name}/Handler/MongoDBHandler.php
%exclude %{_datadir}/php/%{lib_name}/Handler/RavenHandler.php

%files amqp
%defattr(-,root,root,-)
%{_datadir}/php/%{lib_name}/Handler/AmqpHandler.php

%files mongo
%defattr(-,root,root,-)
%{_datadir}/php/%{lib_name}/Handler/MongoDBHandler.php

%files raven
%defattr(-,root,root,-)
%{_datadir}/php/%{lib_name}/Handler/RavenHandler.php


%changelog
* Tue Aug 20 2013 Remi Collet <RPMS@famillecollet.com> 1.6.0-1
- backport 1.6.0 for remi repo

* Sat Aug 17 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.6.0-1
- Updated to version 1.6.0
- Added phpcompatinfo build requires
- php-common -> php(language)
- No conditional php-filter require
- Added php-hash require
- Global raven min and max versions
- Removed MongoDBHandlerTest because it requires a running MongoDB server

* Tue Apr  2 2013 Remi Collet <RPMS@famillecollet.com> 1.4.1-1
- backport 1.4.1 for remi repo

* Mon Apr 01 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.4.1-1
- Updated to version 1.4.1
- Updates for "new" Fedora GitHub guidelines
- Updated summary and description
- Added php-PsrLog require
- Added tests (%%check)
- Removed tests sub-package
- Added raven sub-package

* Sun Nov 25 2012 Remi Collet <RPMS@famillecollet.com> 1.2.1-1
- backport 1.2.1 for remi repo

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
