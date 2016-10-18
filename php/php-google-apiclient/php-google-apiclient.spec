# remirepo spec file for php-google-apiclient, from:
#
# Fedora spec file for php-google-apiclient
#
# Copyright (c) 2014-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#                         Adam Williamson <awilliam@redhat.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     google
%global github_name      google-api-php-client
%global github_version   1.1.7
%global github_commit    400f250a30ae1dd4c4a0a4f750fe973fc70e6311

%global composer_vendor  google
%global composer_project apiclient

# "php": ">=5.2.1"
%global php_min_ver 5.2.1

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       2%{?dist}
# Epoch bumped to permit downgrade to 1.1.7 due to breaking change in 1.1.8 from v2 to v3 google API bz#1386167
Epoch:         2
Summary:       Client library for Google APIs

Group:         Development/Libraries
License:       ASL 2.0
URL:           https://developers.google.com/api-client-library/php/
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
## phpcompatinfo (computed from version 1.1.8)
BuildRequires: php-curl
BuildRequires: php-date
BuildRequires: php-filter
BuildRequires: php-json
BuildRequires: php-openssl
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-session
BuildRequires: php-spl
%endif

# use path as ca-certificates doesn't exists on EL-5
Requires:      /etc/pki/tls/certs/ca-bundle.crt
# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.1.8)
Requires:      php-curl
Requires:      php-date
Requires:      php-json
Requires:      php-openssl
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl

# Weak dependencies
%if 0%{?fedora} >= 21
Suggests:      php-pecl(apcu)
Suggests:      php-pecl(memcache)
Suggests:      php-pecl(memcached)
%endif

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Google APIs Client Library for PHP provides access to many Google APIs.
It is designed for PHP client-application developers and offers simple,
flexible, powerful API access.

Examples are available in the %{name}-examples package.

Autoloader: %{phpdir}/Google/autoload.php


%package examples

Summary:  Client library for Google APIs: Examples
Group:    Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}

%description examples
%{summary}


%prep
%setup -qn %{github_name}-%{github_commit}

: Unbundle CA cert
rm -f src/Google/IO/cacerts.pem
sed "s#dirname(__FILE__)\s*.\s*'/cacerts.pem'#'%{_sysconfdir}/pki/tls/certs/ca-bundle.crt'#" \
    -i src/Google/IO/{Stream,Curl}.php

: Update examples autoload require
sed "s#.*require.*autoload.*#require_once '%{phpdir}/Google/autoload.php';#" \
    -i examples/*.php


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
: Ensure unbundled CA cert is referenced
grep '%{_sysconfdir}/pki/tls/certs/ca-bundle.crt' --quiet \
    %{buildroot}%{phpdir}/Google/IO/{Curl,Stream}.php

%if %{with_tests}
: Skip tests requiring network access
rm -f tests/general/ApiBatchRequestTest.php

: Run tests
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose
fi
exit $ret
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%{!?_licensedir:%global license %%doc}

%files
%defattr(-,root,root,-)
%license LICENSE
%doc *.md
%doc composer.json
%{phpdir}/Google

%files examples
%defattr(-,root,root,-)
%doc examples/*


%changelog
* Tue Oct 18 2016 James Hogarth <james.hogarth@gmail.com> - 2:1.1.7-2
- Missed an %%{epoch} for the examples subpackage

* Tue Oct 18 2016 James Hogarth <james.hogarth@gmail.com> - 2:1.1.7-1
- Downgrade to 1.1.7 (RHBZ #1386167)

* Sun Jul 24 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.8-1
- Updated to 1.1.8 (RHBZ #1275453)
- Added weak dependencies
- Always ensure unbundled CA cert is referenced

* Fri Apr 15 2016 Remi Collet <remi@remirepo.net> - 1.1.5-1.1
- fix dep. on EL-5

* Sun Oct 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.5-1
- Updated to 1.1.5 (RHBZ #1266282)

* Fri May 22 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.4-1
- Updated to 1.1.4 (BZ #1222260)
- Added spec license header
- Removed autoload patch
- Added option to build without tests

* Fri Jan 02 2015 Adam Williamson <awilliam@redhat.com> - 1.1.2-2
- update autoloader relocation patch to match latest upstream submission

* Sat Dec 20 2014 Adam Williamson <awilliam@redhat.com> - 1.1.2-1
- new upstream release 1.1.2
- relocate autoloader to make it work with systemwide installation

* Sat Dec 20 2014 Adam Williamson <awilliam@redhat.com> - 1.0.6-0.3.beta
- use new %%license directory
- add Packagist/Composer provide

* Fri Nov 07 2014 Adam Williamson <awilliam@redhat.com> - 1.0.6-0.2.beta
- apply CA trust store path substitution to Curl as well as Stream

* Fri Nov 07 2014 Adam Williamson <awilliam@redhat.com> - 1.0.6-0.1.beta
- new upstream release 1.0.6-beta

* Fri Feb 21 2014 Remi Collet <remi@fedoraproject.org> 1.0.3-0.2.beta
- backport for remi repo

* Wed Feb 19 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.3-0.2.beta
- Backported commit c6949531d2399f81a5e15caf256f156dd68e00e9 for OwnCloud
- Sub-packaged examples

* Sat Feb 08 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.3-0.1.beta
- Initial package
