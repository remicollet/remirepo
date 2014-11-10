#
# RPM spec file for php-Monolog
#
# Copyright (c) 2012-2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner    Seldaek
%global github_name     monolog
%global github_version  1.11.0
%global github_commit   ec3961874c43840e96da3a8a1ed20d8c73d7e5aa

%global lib_name        Monolog

# "php": ">=5.3.0"
%global php_min_ver     5.3.0
# "phpunit/phpunit": "~3.7.0"
#     Note: Max version ignored on purpose
%global phpunit_min_ver 3.7.0
# "psr/log": "~1.0"
%global psrlog_min_ver  1.0
%global psrlog_max_ver  2.0
# "raven/raven": "~0.5"
%global raven_min_ver   0.5
%global raven_max_ver   1.0
# "aws/aws-sdk-php": "~2.4, >2.4.8"
%global aws_min_ver     2.4.9
%global aws_max_ver     3.0

# Build using "--without tests" to disable tests
%global with_tests      %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:     %global phpdir     %{_datadir}/php}
%{!?__phpunit:  %global __phpunit  %{_bindir}/phpunit}

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
%if %{with_tests}
# composer.json
BuildRequires: php(language)         >= %{php_min_ver}
BuildRequires: php-composer(psr/log) >= %{psrlog_min_ver}
BuildRequires: php-composer(psr/log) <  %{psrlog_max_ver}
BuildRequires: php-phpunit-PHPUnit   >= %{phpunit_min_ver}
# phpcompatinfo (computed from version 1.11.0)
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
%endif

Requires:      php-swift-Swift
# composer.json
Requires:      php(language)         >= %{php_min_ver}
Requires:      php-composer(psr/log) >= %{psrlog_min_ver}
Requires:      php-composer(psr/log) <  %{psrlog_max_ver}
# phpcompatinfo (computed from version 1.11.0)
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

# Composer
Provides:      php-composer(monolog/monolog) = %{version}
Provides:      php-composer(psr/log-implementation) = 1.0.0

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
      Allow sending log messages to AWS services like DynamoDB
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
* https://github.com/videlalvaro/php-amqplib
      Allow sending log messages to an AMQP server using php-amqplib

[1] https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-3-logger-interface.md


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing to build


%install
mkdir -pm 0755 %{buildroot}%{phpdir}
cp -pr ./src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
# Rewrite tests' bootstrap
cat > tests/bootstrap.php <<'BOOTSTRAP'
<?php
spl_autoload_register(function ($class) {
    $src = str_replace(array('\\', '_'), '/', $class).'.php';
    @include_once $src;
});
BOOTSTRAP

# Remove MongoDBHandlerTest because it requires a running MongoDB server
rm -f tests/Monolog/Handler/MongoDBHandlerTest.php

# Remove GitProcessorTest because it requires a git repo
rm -f tests/Monolog/Processor/GitProcessorTest.php

%{__phpunit} \
    --include-path="%{buildroot}%{phpdir}:./tests" \
    -d date.timezone="UTC"
%endif


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.mdown doc composer.json
%{phpdir}/%{lib_name}


%changelog
* Sun Nov  9 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.11.0-1
- Updated to 1.11.0 (BZ #1148336)
- Added php-composer(psr/log-implementation) virtual provide
- %%license usage

* Sun Jun  8 2014 Remi Collet <RPMS@famillecollet.com> 1.10.0-1
- backport 1.10.0 for remi repo

* Sat Jun 07 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.10.0-1
- Updated to 1.10.0 (BZ #1105816)
- Removed max PHPUnit dependency
- Added php-composer(monolog/monolog) virtual provide

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
