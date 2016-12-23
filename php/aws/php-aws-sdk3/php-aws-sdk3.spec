# remirepo spec file for php-aws-sdk3, from
#
# Fedora spec file for php-aws-sdk3
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     aws
%global github_name      aws-sdk-php
%global github_version   3.20.11
%global github_commit    39d122b903813da2f53312fd3146acaa83a6d9f6

%global composer_vendor  aws
%global composer_project aws-sdk-php

# "php": ">=5.5"
%global php_min_ver 5.5
# "andrewsville/php-token-reflection": "^1.4"
%global tokenreflection_min_ver 1.4
%global tokenreflection_max_ver 2.0
# "aws/aws-php-sns-message-validator": "~1.0"
%global aws_sns_message_validator_min_ver 1.0
%global aws_sns_message_validator_max_ver 2.0
# "doctrine/cache": "~1.4"
#     NOTE: Min version not 1.4 because autoloader required
%global doctrine_cache_min_ver 1.4.1
%global doctrine_cache_max_ver 2.0
# "guzzlehttp/guzzle": "^5.3.1|^6.2.1"
%global guzzle_min_ver 5.3.1
%global guzzle_max_ver 7.0
# "guzzlehttp/promises": "~1.0"
%global guzzle_promises_min_ver 1.0
%global guzzle_promises_max_ver 2.0
# "guzzlehttp/psr7": "~1.3.1"
#     NOTE: Keeping previous max of 2.0 instead of changing to 1.4
%global guzzle_psr7_min_ver 1.3.1
%global guzzle_psr7_max_ver 2.0
# "mtdowling/jmespath.php": "~2.2"
%global jmespath_min_ver 2.2
%global jmespath_max_ver 3.0
# "nette/neon": "^2.3"
%global nette_neon_min_ver 2.3
%global nette_neon_max_ver 3.0
# "psr/cache": "^1.0"
%global psr_cache_min_ver 1.0
%global psr_cache_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-aws-sdk3
Version:       %{github_version}
Release:       1%{?dist}
Summary:       Amazon Web Services framework for PHP

Group:         Development/Libraries
License:       ASL 2.0
URL:           http://aws.amazon.com/sdkforphp

# GitHub export does not include tests.
# Run php-aws-sdk3-get-source.sh to create full source.
Source0:       %{name}-%{github_version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Library version value and autoloader check
BuildRequires: php-cli                              >= %{php_min_ver}
BuildRequires: php-composer(guzzlehttp/guzzle)      >= %{guzzle_min_ver}
BuildRequires: php-composer(guzzlehttp/promises)    >= %{guzzle_promises_min_ver}
BuildRequires: php-composer(guzzlehttp/psr7)        >= %{guzzle_psr7_min_ver}
BuildRequires: php-composer(mtdowling/jmespath.php) >= %{jmespath_min_ver}
BuildRequires: php-composer(fedora/autoloader)
# Tests
%if %{with_tests}
## Classmap
BuildRequires: php-composer(theseer/autoload)
## composer.json
BuildRequires: php-composer(andrewsville/php-token-reflection) >= %{tokenreflection_min_ver}
BuildRequires: php-composer(aws/aws-php-sns-message-validator) >= %{aws_sns_message_validator_min_ver}
BuildRequires: php-composer(doctrine/cache)                    >= %{doctrine_cache_min_ver}
BuildRequires: php-composer(nette/neon)                        >= %{nette_neon_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(psr/cache)                         >= %{psr_cache_min_ver}
BuildRequires: php-dom
BuildRequires: php-json
BuildRequires: php-openssl
BuildRequires: php-pcre
BuildRequires: php-simplexml
BuildRequires: php-spl
## phpcompatinfo (computed from version 3.20.6)
BuildRequires: php-curl
BuildRequires: php-date
BuildRequires: php-filter
BuildRequires: php-hash
BuildRequires: php-libxml
BuildRequires: php-reflection
BuildRequires: php-session
BuildRequires: php-xml
BuildRequires: php-xmlwriter
%endif

# composer.json
Requires:      php(language)                        >= %{php_min_ver}
Requires:      php-composer(guzzlehttp/guzzle)      <  %{guzzle_max_ver}
Requires:      php-composer(guzzlehttp/guzzle)      >= %{guzzle_min_ver}
Requires:      php-composer(guzzlehttp/promises)    <  %{guzzle_promises_max_ver}
Requires:      php-composer(guzzlehttp/promises)    >= %{guzzle_promises_min_ver}
Requires:      php-composer(guzzlehttp/psr7)        <  %{guzzle_psr7_max_ver}
Requires:      php-composer(guzzlehttp/psr7)        >= %{guzzle_psr7_min_ver}
Requires:      php-composer(mtdowling/jmespath.php) <  %{jmespath_max_ver}
Requires:      php-composer(mtdowling/jmespath.php) >= %{jmespath_min_ver}
# phpcompatinfo (computed from version 3.20.6)
Requires:      php-date
Requires:      php-filter
Requires:      php-hash
Requires:      php-json
Requires:      php-libxml
Requires:      php-pcre
Requires:      php-session
Requires:      php-simplexml
Requires:      php-spl
Requires:      php-xmlwriter
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Weak dependencies
## composer.json: optional
%if 0%{?fedora} >= 21
Suggests:      php-curl
Suggests:      php-openssl
Suggests:      php-composer(doctrine/cache)
Conflicts:     php-doctrine-cache <  %{doctrine_cache_min_ver}
Conflicts:     php-doctrine-cache >= %{doctrine_cache_max_ver}
Suggests:      php-composer(aws/aws-php-sns-message-validator)
Conflicts:     php-aws-php-sns-message-validator <  %{aws_sns_message_validator_min_ver}
Conflicts:     php-aws-php-sns-message-validator >= %{aws_sns_message_validator_max_ver}
%endif

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
The AWS SDK for PHP makes it easy for developers to access Amazon Web
Services [1] in their PHP code, and build robust applications and software
using services like Amazon S3, Amazon DynamoDB, Amazon Glacier, etc.

Autoloader: %{phpdir}/Aws3/autoload.php

[1] http://aws.amazon.com/


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 */
require_once '%{phpdir}/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Aws\\', __DIR__);

\Fedora\Autoloader\Dependencies::required([
    __DIR__.'/functions.php',
    [
        '%{phpdir}/GuzzleHttp6/autoload.php',
        '%{phpdir}/GuzzleHttp/autoload.php',
    ],
    '%{phpdir}/GuzzleHttp/Promise/autoload.php',
    '%{phpdir}/GuzzleHttp/Psr7/autoload.php',
    '%{phpdir}/JmesPath/autoload.php',
]);

\Fedora\Autoloader\Dependencies::optional([
    '%{phpdir}/Aws/Sns/autoload.php',
    '%{phpdir}/Doctrine/Common/Cache/autoload.php',
]);
AUTOLOAD


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}/Aws3
cp -pr src/* %{buildroot}%{phpdir}/Aws3/


%check
: Library version value and autoloader check
%{_bindir}/php -r '
    require_once "%{buildroot}%{phpdir}/Aws3/autoload.php";
    $version = \Aws\Sdk::VERSION;
    echo "Version $version (expected %{version})\n";
    exit(version_compare("%{version}", "$version", "=") ? 0 : 1);
'

%if %{with_tests}
: Create tests classmap
%{_bindir}/phpab --nolower --output bootstrap.classmap.php build/

: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
error_reporting(-1);
date_default_timezone_set('UTC');

require_once '%{buildroot}%{phpdir}/Aws3/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Aws\\Test\\', __DIR__.'/tests');
\Fedora\Autoloader\Autoload::addPsr4('TokenReflection\\', '%{phpdir}/TokenReflection');

\Fedora\Autoloader\Dependencies::required([
    __DIR__.'/bootstrap.classmap.php',
    '%{phpdir}/Nette/Neon/autoload.php',
    '%{phpdir}/Psr/Cache/autoload.php',
]);
BOOTSTRAP

: Skip tests known to fail
rm -f \
    tests/Integ/GuzzleV5HandlerTest.php \
    tests/Integ/GuzzleV6StreamHandlerTest.php

export AWS_ACCESS_KEY_ID=foo
export AWS_SECRET_ACCESS_KEY=bar

run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit -d memory_limit=1G --testsuite=unit --bootstrap bootstrap.php || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit -d memory_limit=1G --testsuite=unit --bootstrap bootstrap.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit -d memory_limit=1G --verbose  --testsuite=unit \
    --bootstrap bootstrap.php
fi
exit $ret
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc CHANGELOG.md
%doc composer.json
%doc README.md
%doc UPGRADING.md
%{phpdir}/Aws3


%changelog
* Fri Dec 23 2016 Remi Collet <remi@remirepo.net> - 3.20.11-1
- update to 3.20.11

* Thu Dec 22 2016 Remi Collet <remi@remirepo.net> - 3.20.10-1
- update to 3.20.10

* Wed Dec 21 2016 Remi Collet <remi@remirepo.net> - 3.20.9-1
- update to 3.20.9

* Tue Dec 20 2016 Remi Collet <remi@remirepo.net> - 3.20.8-1
- update to 3.20.8

* Fri Dec 16 2016 Remi Collet <remi@remirepo.net> - 3.20.7-1
- update to 3.20.7

* Thu Dec 15 2016 Shawn Iwinski <shawn@iwin.ski> - 3.20.6-1
- Updated to 3.20.6 (RHBZ #1402170)

* Tue Dec 13 2016 Remi Collet <remi@remirepo.net> - 3.20.5-1
- update to 3.20.5

* Fri Dec  9 2016 Remi Collet <remi@remirepo.net> - 3.20.4-1
- update to 3.20.4

* Thu Dec  8 2016 Remi Collet <remi@remirepo.net> - 3.20.3-1
- update to 3.20.3

* Wed Dec  7 2016 Remi Collet <remi@remirepo.net> - 3.20.2-1
- update to 3.20.2

* Fri Dec  2 2016 Remi Collet <remi@remirepo.net> - 3.20.1-1
- update to 3.20.1

* Thu Dec 01 2016 Shawn Iwinski <shawn@iwin.ski> - 3.20.0-1
- Updated to 3.20.0 (RHBZ #1397218)

* Wed Nov 30 2016 Remi Collet <remi@remirepo.net> - 3.19.33-1
- update to 3.19.33

* Wed Nov 23 2016 Remi Collet <remi@remirepo.net> - 3.19.32-1
- update to 3.19.32

* Tue Nov 22 2016 Remi Collet <remi@remirepo.net> - 3.19.31-1
- update to 3.19.31

* Mon Nov 21 2016 Shawn Iwinski <shawn@iwin.ski> - 3.19.30-1
- Updated to 3.19.30 (RHBZ #1380046)
- Switched autoloader from php-composer(symfony/class-loader) to
  php-composer(fedora/autoloader)

* Fri Nov 18 2016 Remi Collet <remi@remirepo.net> - 3.19.28-1
- update to 3.19.28

* Thu Nov 17 2016 Remi Collet <remi@remirepo.net> - 3.19.27-1
- update to 3.19.27

* Wed Nov 16 2016 Remi Collet <remi@remirepo.net> - 3.19.26-1
- update to 3.19.26

* Tue Nov 15 2016 Remi Collet <remi@remirepo.net> - 3.19.25-1
- update to 3.19.25

* Fri Nov 11 2016 Remi Collet <remi@remirepo.net> - 3.19.24-1
- update to 3.19.24

* Fri Nov  4 2016 Remi Collet <remi@remirepo.net> - 3.19.23-1
- update to 3.19.23

* Thu Nov  3 2016 Remi Collet <remi@remirepo.net> - 3.19.22-1
- update to 3.19.22

* Wed Nov  2 2016 Remi Collet <remi@remirepo.net> - 3.19.21-1
- update to 3.19.21

* Wed Oct 26 2016 Remi Collet <remi@remirepo.net> - 3.19.20-1
- update to 3.19.20

* Tue Oct 25 2016 Remi Collet <remi@remirepo.net> - 3.19.19-1
- update to 3.19.19

* Fri Oct 21 2016 Remi Collet <remi@remirepo.net> - 3.19.18-1
- update to 3.19.18

* Wed Oct 19 2016 Remi Collet <remi@remirepo.net> - 3.19.17-1
- update to 3.19.17

* Tue Oct 18 2016 Remi Collet <remi@remirepo.net> - 3.19.16-1
- update to 3.19.16

* Fri Oct 14 2016 Remi Collet <remi@remirepo.net> - 3.19.15-1
- update to 3.19.15

* Thu Oct 13 2016 Remi Collet <remi@remirepo.net> - 3.19.14-1
- update to 3.19.14

* Fri Oct  7 2016 Remi Collet <remi@remirepo.net> - 3.19.13-1
- update to 3.19.13

* Fri Sep 30 2016 Remi Collet <remi@remirepo.net> - 3.19.12-1
- update to 3.19.12

* Wed Sep 28 2016 Remi Collet <remi@remirepo.net> - 3.19.11-1
- update to 3.19.11

* Sun Sep 25 2016 Shawn Iwinski <shawn@iwin.ski> - 3.19.10-1
- Updated to 3.19.10 (RHBZ #1376241)

* Fri Sep 23 2016 Remi Collet <remi@remirepo.net> - 3.19.10-1
- update to 3.19.10

* Mon Sep 19 2016 Remi Collet <remi@remirepo.net> - 3.19.8-1
- update to 3.19.8

* Wed Sep 14 2016 Remi Collet <remi@remirepo.net> - 3.19.7-1
- update to 3.19.7

* Sun Sep 11 2016 Shawn Iwinski <shawn@iwin.ski> - 3.19.6-1
- Updated to 3.19.6 (RHBZ #1365099)

* Fri Aug 12 2016 Remi Collet <remi@remirepo.net> - 3.18.39-1
- update to 3.18.39

* Wed Aug 10 2016 Remi Collet <remi@remirepo.net> - 3.18.38-1
- update to 3.18.38

* Fri Aug  5 2016 Remi Collet <remi@remirepo.net> - 3.18.37-1
- update to 3.18.37

* Wed Aug  3 2016 Remi Collet <remi@remirepo.net> - 3.18.36-1
- update to 3.18.36

* Fri Jul 29 2016 Remi Collet <remi@remirepo.net> - 3.18.35-1
- update to 3.18.35

* Thu Jul 21 2016 Remi Collet <remi@remirepo.net> - 3.18.31-1
- update to 3.18.31

* Sun Jul 17 2016 Remi Collet <remi@remirepo.net> - 3.18.28-1
- update to 3.18.28

* Fri Jul  8 2016 Remi Collet <remi@remirepo.net> - 3.18.27-1
- update to 3.18.27

* Wed Jul  6 2016 Remi Collet <remi@remirepo.net> - 3.18.25-1
- update to 3.18.25

* Mon Jul 04 2016 Shawn Iwinski <shawn@iwin.ski> - 3.18.24-1
- Updated to 3.18.24 (RHBZ #1342771)

* Sat Jul  2 2016 Remi Collet <remi@remirepo.net> - 3.18.24-1
- update to 3.18.24

* Fri Jul  1 2016 Remi Collet <remi@remirepo.net> - 3.18.23-1
- update to 3.18.23

* Thu Jun 30 2016 Remi Collet <remi@remirepo.net> - 3.18.22-1
- update to 3.18.22

* Tue Jun 28 2016 Remi Collet <remi@remirepo.net> - 3.18.21-1
- update to 3.18.21

* Fri Jun 24 2016 Remi Collet <remi@remirepo.net> - 3.18.20-1
- update to 3.18.20

* Wed Jun 22 2016 Remi Collet <remi@remirepo.net> - 3.18.19-1
- update to 3.18.19

* Wed Jun 15 2016 Remi Collet <remi@remirepo.net> - 3.18.18-1
- update to 3.18.18

* Fri Jun 10 2016 Remi Collet <remi@remirepo.net> - 3.18.17-1
- update to 3.18.17

* Fri Jun  3 2016 Remi Collet <remi@remirepo.net> - 3.18.15-1
- update to 3.18.15

* Fri May 27 2016 Remi Collet <remi@remirepo.net> - 3.18.14-1
- update to 3.18.14

* Wed May 25 2016 Remi Collet <remi@remirepo.net> - 3.18.13-1
- update to 3.18.13

* Fri May 20 2016 Remi Collet <remi@remirepo.net> - 3.18.12-1
- update to 3.18.12

* Fri May 20 2016 Remi Collet <remi@remirepo.net> - 3.18.11-1
- update to 3.18.11

* Wed May 18 2016 Remi Collet <remi@remirepo.net> - 3.18.9-1
- update to 3.18.9

* Fri May  6 2016 Remi Collet <remi@remirepo.net> - 3.18.6-1
- update to 3.18.6

* Wed May  4 2016 Remi Collet <remi@remirepo.net> - 3.18.5-1
- update to 3.18.5

* Fri Apr 29 2016 Remi Collet <remi@remirepo.net> - 3.18.4-1
- update to 3.18.4

* Thu Apr 28 2016 Remi Collet <remi@remirepo.net> - 3.18.3-1
- update to 3.18.3

* Fri Apr 22 2016 Remi Collet <remi@remirepo.net> - 3.18.1-1
- update to 3.18.1

* Thu Apr 21 2016 Remi Collet <remi@remirepo.net> - 3.18.0-1
- backport for remi repository

* Wed Apr 20 2016 Shawn Iwinski <shawn@iwin.ski> - 3.18.0-1
- Updated to 3.18.0
- Modified autoloader to not use @include_once for optional dependencies
- Set test memory_limit because build issues on certain systems

* Tue Apr 12 2016 Shawn Iwinski <shawn@iwin.ski> - 3.17.6-1
- Initial package
