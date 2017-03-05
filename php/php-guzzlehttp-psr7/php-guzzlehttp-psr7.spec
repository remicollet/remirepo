# remirepo spec file for php-guzzlehttp-psr7, from
#
# Fedora spec file for php-guzzlehttp-psr7
#
# Copyright (c) 2015-2017 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     guzzle
%global github_name      psr7
%global github_version   1.4.1
%global github_commit    0d6c7ca039329247e4f0f8f8f6506810e8248855

%global composer_vendor  guzzlehttp
%global composer_project psr7

# "php": ">=5.4.0"
%global php_min_ver 5.4.0
# "psr/http-message": "~1.0"
%global psr_http_message_min_ver 1.0
%global psr_http_message_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       PSR-7 message implementation

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}

# GitHub export does not include tests.
# Run php-guzzlehttp-psr7-get-source.sh to create full source.
Source0:       %{name}-%{github_version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(psr/http-message) <  %{psr_http_message_max_ver}
BuildRequires: php-composer(psr/http-message) >= %{psr_http_message_min_ver}
## phpcompatinfo (computed from version 1.4.1)
BuildRequires: php-hash
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
BuildRequires: php-zlib
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(psr/http-message) <  %{psr_http_message_max_ver}
Requires:      php-composer(psr/http-message) >= %{psr_http_message_min_ver}
# phpcompatinfo (computed from version 1.4.1)
Requires:      php-hash
Requires:      php-pcre
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}
Provides:      php-composer(psr/http-message-implementation) = 1.0

%description
PSR-7 message implementation, several stream decorators, and some helpful
functionality like query string parsing.


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

\Fedora\Autoloader\Autoload::addPsr4('GuzzleHttp\\Psr7\\', __DIR__);

\Fedora\Autoloader\Dependencies::required([
    __DIR__.'/functions_include.php',
    '%{phpdir}/Psr/Http/Message/autoload.php',
]);
AUTOLOAD


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}/GuzzleHttp/Psr7
cp -rp src/* %{buildroot}%{phpdir}/GuzzleHttp/Psr7/


%check
%if %{with_tests}
BOOTSTRAP=%{buildroot}%{phpdir}/GuzzleHttp/Psr7/autoload.php

: Upstream tests
%{_bindir}/phpunit --verbose --bootstrap $BOOTSTRAP

: Upstream tests with SCLs if available
SCL_RETURN_CODE=0
for SCL in %{?rhel:php55} php56 php70 php71; do
    if which $SCL; then
        $SCL %{_bindir}/phpunit --verbose --bootstrap $BOOTSTRAP || SCL_RETURN_CODE=1
    fi
done
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
%dir %{phpdir}/GuzzleHttp
     %{phpdir}/GuzzleHttp/Psr7


%changelog
* Sat Mar 04 2017 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.4.1-1
- Updated to 1.4.1 (RHBZ #1425429)
- Switch autoloader to php-composer(fedora/autoloader)
- Test with SCLs if available

* Sun Jul 03 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.1-1
- Updated to 1.3.1 (RHBZ #1352354)

* Sat Jul  2 2016 Remi Collet <remi@remirepo.net> - 1.3.1-1
- Updated to 1.3.1

* Sun May 29 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.0-1
- Updated to 1.3.0 (RHBZ #1326975)

* Fri Mar 11 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.3-1
- Updated to 1.2.3 (RHBZ #1301276)

* Wed Nov 04 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.1-1
- Updated to 1.2.1 (RHBZ #1277467)

* Sun Aug 16 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.0-1
- Updated to 1.2.0 (RHBZ #1253997)
- Updated autoloader to load dependencies after self registration

* Mon Jul 20 2015 Remi Collet <remi@remirepo.net> - 1.1.0-3
- add EL-5 stuff, backport for #remirepo

* Sun Jul 19 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.0-3
- Use full paths in autoloader

* Wed Jul 08 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.0-2
- Add autoloader dependencies
- Modify autoloader

* Mon Jul 06 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.0-1
- Initial package
