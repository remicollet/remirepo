# remirepo spec file for php-zendframework-zend-diactoros, from
#
# Fedora spec file for php-zendframework-zend-diactoros
#
# Copyright (c) 2015-2017 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     zendframework
%global github_name      zend-diactoros
%global github_version   1.3.10
%global github_commit    83e8d98b9915de76c659ce27d683c02a0f99fa90

%global composer_vendor  zendframework
%global composer_project zend-diactoros

# "php": "^5.4 || ^7.0"
%global php_min_ver 5.4
# "psr/http-message": "~1.0"
%global psr_http_message_min_ver 1.0
%global psr_http_message_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       PSR HTTP Message implementations

Group:         Development/Libraries
License:       BSD
URL:           https://zendframework.github.io/%{gh_project}/

# GitHub export does not include tests.
# Run php-zendframework-zend-diactoros-get-source.sh to create full source.
Source0:       %{name}-%{github_version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language)                  >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(psr/http-message) <  %{psr_http_message_max_ver}
BuildRequires: php-composer(psr/http-message) >= %{psr_http_message_min_ver}
## phpcompatinfo (computed from version 1.3.10)
### NOTE: curl, gd, gmp, and shmop are all optional for
###       ZendTest\Diactoros\StreamTest::getResourceFor67()
###       (test/StreamTest.php) but the first one found wins
###       so only curl is chosen as a requirement here.
BuildRequires: php-curl
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(psr/http-message) <  %{psr_http_message_max_ver}
Requires:      php-composer(psr/http-message) >= %{psr_http_message_min_ver}
# phpcompatinfo (computed from version 1.3.10)
Requires:      php-json
Requires:      php-pcre
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}
Provides:      php-composer(psr/http-message-implementation) = 1.0.0

%description
A PHP package containing implementations of the accepted PSR-7 HTTP message
interfaces [1], as well as a "server" implementation similar to node's
http.Server [2].

Documentation: https://zendframework.github.io/%{gh_project}/

Autoloader: %{phpdir}/Zend/Diactoros/autoload.php

[1] http://www.php-fig.org/psr/psr-7/
[2] http://nodejs.org/api/http.html


%prep
%setup -qn %{github_name}-%{github_commit}

mv LICENSE.md LICENSE

%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 */
require_once '%{phpdir}/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Zend\\Diactoros\\', __DIR__);

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/Psr/Http/Message/autoload.php',
));
AUTOLOAD


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}/Zend/Diactoros
cp -rp src/* %{buildroot}%{phpdir}/Zend/Diactoros/


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php

require_once '%{buildroot}%{phpdir}/Zend/Diactoros/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('ZendTest\\Diactoros\\', __DIR__.'/test');

\Fedora\Autoloader\Dependencies::required(array(
    __DIR__.'/test/TestAsset/Functions.php',
    __DIR__.'/test/TestAsset/SapiResponse.php',
));
BOOTSTRAP

: Upstream tests
%{_bindir}/phpunit --verbose --bootstrap bootstrap.php

: Upstream tests with SCLs if available
SCL_RETURN_CODE=0
for SCL in %{?rhel:php55} php56 php70 php71; do
    if which $SCL; then
        $SCL %{_bindir}/phpunit --verbose --bootstrap bootstrap.php || SCL_RETURN_CODE=1
    fi
done
exit $SCL_RETURN_CODE
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%dir %{phpdir}/Zend
     %{phpdir}/Zend/Diactoros


%changelog
* Sun Mar 05 2017 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.10-1
- Updated to 1.3.10 (RHBZ #1411062)
- Test with SCLs if available

* Mon Jan 23 2017 Remi Collet <remi@remirepo.net> - 1.3.10-1
- update to 1.3.10

* Wed Jan 18 2017 Remi Collet <remi@remirepo.net> - 1.3.9-1
- update to 1.3.9

* Fri Jan  6 2017 Remi Collet <remi@remirepo.net> - 1.3.8-1
- update to 1.3.8

* Sat Dec 03 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.7-1
- Updated to 1.3.7 (RHBZ #1318837)
- Switch autoloader from php-composer(symfony/class-loader) to
  php-composer(fedora/autoloader)

* Wed Oct 12 2016 Remi Collet <remi@remirepo.net> - 1.3.7-1
- update to 1.3.7

* Thu Sep  8 2016 Remi Collet <remi@remirepo.net> - 1.3.6-1
- update to 1.3.6

* Wed Apr  6 2016 Remi Collet <remi@remirepo.net> - 1.3.5-1
- update to 1.3.5

* Mon Jan 04 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.3-1
- Updated to 1.3.3 (RHBZ #1285581)

* Mon Oct 26 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.4-1
- Updated to 1.1.4 (RHBZ #1272627)

* Sun Oct 18 2015 Remi Collet <remi@remirepo.net> - 1.1.4-1
- update to 1.1.4

* Tue Aug 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.3-1
- Updated to 1.1.3 (RHBZ #1252195)
- Updated autoloader to load dependencies after self registration

* Tue Aug 11 2015 Remi Collet <remi@remirepo.net> - 1.1.3-1
- update to 1.1.3

* Mon Jul 20 2015 Remi Collet <remi@remirepo.net> - 1.1.2-1
- add EL-5 stuff, backport for #remirepo

* Wed Jul 15 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.2-1
- Update to 1.1.2
- Fix license
- Update description
- Use full path in autoloader

* Wed Jul 08 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.1-1
- Initial package
