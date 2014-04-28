%global github_owner    Seldaek
%global github_name     monolog
%global github_version  1.9.1
%global github_commit   65026b610f8c19e61d7242f600530677b0466aac

%global lib_name        Monolog

# "php": ">=5.3.0"
%global php_min_ver     5.3.0
# "phpunit/phpunit": "~3.7.0"
%global phpunit_min_ver 3.7.0
%global phpunit_max_ver 3.8.0
# "psr/log": "~1.0"
%global psrlog_min_ver  1.0
%global psrlog_max_ver  2.0
# "raven/raven": "~0.5"
%global raven_min_ver   0.5
%global raven_max_ver   1.0
# "aws/aws-sdk-php": "~2.4, >2.4.8"
%global aws_min_ver     2.4.9
%global aws_max_ver     3.0

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
BuildRequires: php-PsrLog    >= %{psrlog_min_ver}
BuildRequires: php-PsrLog    <  %{psrlog_max_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit) >= %{phpunit_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit) <  %{phpunit_max_ver}
# For tests: phpcompatinfo (computed from 1.9.1)
BuildRequires: php-curl
BuildRequires: php-date
BuildRequires: php-filter
BuildRequires: php-hash
BuildRequires: php-json
BuildRequires: php-mbstring
BuildRequires: php-openssl
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-sockets
BuildRequires: php-spl
BuildRequires: php-xml

Requires:      php(language) >= %{php_min_ver}
Requires:      php-PsrLog    >= %{psrlog_min_ver}
Requires:      php-PsrLog    <  %{psrlog_max_ver}
Requires:      php-pear(pear.swiftmailer.org/Swift)
# phpcompatinfo (computed from 1.9.1)
Requires:      php-curl
Requires:      php-date
Requires:      php-filter
Requires:      php-hash
Requires:      php-json
Requires:      php-mbstring
Requires:      php-openssl
Requires:      php-pcre
Requires:      php-sockets
Requires:      php-spl
Requires:      php-xml

# Removed sub-packages
Obsoletes:     %{name}-amqp   < %{version}-%{release}
Provides:      %{name}-amqp   = %{version}-%{release}
Obsoletes:     %{name}-dynamo < %{version}-%{release}
Provides:      %{name}-dynamo = %{version}-%{release}
Obsoletes:     %{name}-mongo  < %{version}-%{release}
Provides:      %{name}-mongo  = %{version}-%{release}
Obsoletes:     %{name}-raven  < %{version}-%{release}
Provides:      %{name}-raven  = %{version}-%{release}

# Optional dependencies, but need this to enforce versions
Conflicts:     php-aws-sdk <  %{aws_min_ver}
Conflicts:     php-aws-sdk >= %{aws_max_ver}
Conflicts:     php-Raven   <  %{raven_min_ver}
Conflicts:     php-Raven   >= %{raven_max_ver}

%description
Monolog sends your logs to files, sockets, inboxes, databases and various web
services. Special handlers allow you to build advanced logging strategies.

This library implements the PSR-3 [1] interface that you can type-hint against
in your own libraries to keep a maximum of interoperability. You can also use it
in your applications to make sure you can always use another compatible logger
at a later time.

Optional:
* php-aws-sdk (>= %{aws_min_ver}, < %{aws_max_ver})
      Allow sending log messages to AWS DynamoDB
* php-pecl-amqp
      Allow sending log messages to an AMQP server (1.0+ required)
* php-pecl-mongo
      Allow sending log messages to a MongoDB server
* php-Raven (>= %{raven_min_ver}, < %{raven_max_ver})
      Allow sending log messages to a Sentry server
* https://github.com/doctrine/couchdb-client
      Allow sending log messages to a CouchDB server
* https://github.com/Graylog2/gelf-php
      Allow sending log messages to a GrayLog2 server
* https://docs.newrelic.com/docs/php/new-relic-for-php
      Allow sending log messages to a New Relic application
* https://github.com/rollbar/rollbar-php
      Allow sending log messages to Rollbar
* https://github.com/ruflin/Elastica
      Allow sending log messages to an Elastic Search server

[1] https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-3-logger-interface.md


%prep
%setup -q -n %{github_name}-%{github_commit}


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php
cp -pr ./src/* %{buildroot}%{_datadir}/php/


%check
# Rewrite tests' bootstrap
( cat <<'BOOTSTRAP'
<?php
spl_autoload_register(function ($class) {
    $src = str_replace(array('\\', '_'), '/', $class).'.php';
    @include_once $src;
});
BOOTSTRAP
) > ./tests/bootstrap.php

# Create PHPUnit config w/ colors turned off
sed 's/colors\s*=\s*"true"/colors="false"/' phpunit.xml.dist > phpunit.xml

# Remove MongoDBHandlerTest because it requires a running MongoDB server
rm -f tests/Monolog/Handler/MongoDBHandlerTest.php

# Remove GitProcessorTest because it requires a git repo
rm -f tests/Monolog/Processor/GitProcessorTest.php

%{_bindir}/phpunit --include-path="./src:./tests" -d date.timezone="UTC"


%files
%defattr(-,root,root,-)
%doc LICENSE *.mdown doc composer.json
%{_datadir}/php/%{lib_name}


%changelog
* Mon Apr 28 2014 Remi Collet <RPMS@famillecollet.com> 1.9.1-1
- backport 1.9.1 for remi repo

* Fri Apr 25 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.9.1-1
- Updated to 1.9.1 (BZ #1080872)
- Added option to build without tests ("--without tests")

* Thu Jan 16 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.7.0-3
- Properly obsolete sub-packages

* Wed Jan 15 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.7.0-2
- Removed sub-packages (optional dependencies note in description instead)

* Mon Dec 30 2013 Remi Collet <RPMS@famillecollet.com> 1.7.0-1
- backport 1.7.0 for remi repo

* Mon Dec 30 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.7.0-1
- Updated to 1.7.0 (BZ #1030923)
- Added dynamo sub-package
- Spec cleanup

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
