# remirepo spec file for php-Monolog, from
#
# Fedora spec file for php-Monolog
#
# Copyright (c) 2012-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     Seldaek
%global github_name      monolog
%global github_version   1.18.1
%global github_commit    a5f2734e8c16f3aa21b3da09715d10e15b4d2d45

%global composer_vendor  monolog
%global composer_project monolog

# "php": ">=5.3.0"
%global php_min_ver     5.3.0
# "psr/log": "~1.0"
#     NOTE: Min version not 1.0 because autoloader required
%global psrlog_min_ver  1.0.0-8
%global psrlog_max_ver  2.0
# "raven/raven": "^0.13"
%global raven_min_ver   0.13
%global raven_max_ver   1.0
# "aws/aws-sdk-php": "^2.4.9"
#     NOTE: Min version not 2.4.9 because autoloader required
%global aws_min_ver     2.8.13
%global aws_max_ver     3.0
# "swiftmailer/swiftmailer": "~5.3"
%global swift_min_ver   5.3
%global swift_max_ver   6

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:      php-Monolog
Version:   %{github_version}
Release:   2%{?dist}
Summary:   Sends your logs to files, sockets, inboxes, databases and various web services

Group:     Development/Libraries
License:   MIT
URL:       https://github.com/%{github_owner}/%{github_name}
Source0:   %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

# missing property
# https://github.com/Seldaek/monolog/pull/757
Patch0:    %{name}-pr756.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language)                         >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
#BuildRequires: php-composer(psr/log)                 >= %%{psrlog_min_ver}
BuildRequires: php-PsrLog                            >= %{psrlog_min_ver}
BuildRequires: php-composer(psr/log)                 <  %{psrlog_max_ver}
## optional
BuildRequires: php-composer(swiftmailer/swiftmailer) >= %{swift_min_ver}
BuildRequires: php-composer(raven/raven)             >= %{raven_min_ver}
BuildRequires: php-composer(aws/aws-sdk-php)         >= %{aws_min_ver}
## phpcompatinfo (computed from version 1.18.1)
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
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)         >= %{php_min_ver}
#Requires:      php-composer(psr/log) >= %%{psrlog_min_ver}
Requires:      php-PsrLog            >= %{psrlog_min_ver}
Requires:      php-composer(psr/log) <  %{psrlog_max_ver}
# phpcompatinfo (computed from version 1.18.1)
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
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming
Provides:      php-%{composer_vendor}-%{composer_project} = %{version}-%{release}
Provides:      php-%{composer_vendor} = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}
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

# Weak dependencies
%if 0%{?fedora} >= 21
Suggests:      php-composer(aws/aws-sdk-php)
Suggests:      php-composer(raven/raven)
Suggests:      php-composer(swiftmailer/swiftmailer)
%endif
Conflicts:     php-aws-sdk     <  %{aws_min_ver}
Conflicts:     php-aws-sdk     >= %{aws_max_ver}
Conflicts:     php-Raven       <  %{raven_min_ver}
Conflicts:     php-Raven       >= %{raven_max_ver}
Conflicts:     php-swiftmailer <  %{swift_min_ver}
Conflicts:     php-swiftmailer >= %{swift_max_ver}

%description
Monolog sends your logs to files, sockets, inboxes, databases and various web
services. Special handlers allow you to build advanced logging strategies.

This library implements the PSR-3 [1] interface that you can type-hint against
in your own libraries to keep a maximum of interoperability. You can also use it
in your applications to make sure you can always use another compatible logger
at a later time.

[1] http://www.php-fig.org/psr/psr-3/


%prep
%setup -qn %{github_name}-%{github_commit}

%patch0 -p1

: Create autoloader
cat <<'AUTOLOAD' | tee src/Monolog/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Monolog\\', dirname(__DIR__));

// Required dependency
require_once '%{phpdir}/Psr/Log/autoload.php';

// Optional dependencies
@include_once '%{phpdir}/Aws/autoload.php';
@include_once '%{phpdir}/Raven/autoload.php';
@include_once '%{phpdir}/Swift/swift_required.php';

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}
cp -pr src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php

$fedoraClassLoader = require_once '%{buildroot}%{phpdir}/Monolog/autoload.php';
$fedoraClassLoader->addPrefix(false, __DIR__.'/tests');
BOOTSTRAP

: Remove MongoDBHandlerTest because it requires a running MongoDB server
rm -f tests/Monolog/Handler/MongoDBHandlerTest.php

: Remove GitProcessorTest because it requires a git repo
rm -f tests/Monolog/Processor/GitProcessorTest.php

: Skip tests known to fail
%if 0%{?rhel} > 0
sed 's/function testThrowsOnInvalidEncoding/function SKIP_testThrowsOnInvalidEncoding/' \
    -i tests/Monolog/Formatter/NormalizerFormatterTest.php
%endif

ret=0
run=0
if which php70; then
   php70 %{_bindir}/phpunit --verbose --bootstrap bootstrap.php || ret=1
   run=1
fi
if which php56; then
   php56 %{_bindir}/phpunit --verbose --bootstrap bootstrap.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
   %{_bindir}/phpunit --verbose --bootstrap bootstrap.php || ret =1
fi

exit $ret;
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.mdown
%doc doc
%doc composer.json
%{phpdir}/Monolog


%changelog
* Fri Apr 01 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.18.1-2
- Increased PSR log min version for autoloader
- Updated autoloader
- Added weak dependencies

* Fri Mar 25 2016 Remi Collet <remi@remirepo.net> - 1.18.1-1
- update to 1.18.1
- use php-swiftmailer instead of old php-swift-Swift
- install optional dependencies during the build for tests
- add patch for missing property, breaking test suite
  open https://github.com/Seldaek/monolog/pull/757

* Thu Oct 15 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.17.2-1
- Updated to 1.17.2 (RHBZ #1271882)

* Thu Oct 15 2015 Remi Collet <remi@remirepo.net> - 1.17.2-1
- update to 1.17.2

* Sun Sep 13 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.17.1-1
- Updated to 1.17.1 (RHBZ #1258230)

* Tue Aug 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.16.0-1
- Updated to 1.16.0 (RHBZ #1251783)
- Updated autoloader to load dependencies after self registration

* Mon Aug 10 2015 Remi Collet <remi@remirepo.net> - 1.16.0-1
- update to 1.16.0

* Mon Jul 20 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.15.0-2
- Fix autoloader

* Sun Jul 19 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.15.0-1
- Updated to 1.15.0 (RHBZ #1199105)
- Added autoloader

* Sun Jan 04 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.12.0-1
- Updated to 1.12.0 (BZ #1178410)

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
