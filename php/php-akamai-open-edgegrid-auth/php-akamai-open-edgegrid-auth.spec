# remirepo spec file for php-akamai-open-edgegrid-auth, from:
#
# Fedora spec file for php-akamai-open-edgegrid-auth
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     akamai-open
%global github_name      AkamaiOPEN-edgegrid-php
%global github_version   0.6.1
%global github_commit    a97a2194067800bb552c8b4cc0d1770588db00ad

%global composer_vendor  akamai-open
%global composer_project edgegrid-auth

# "php": ">=5.3"
%global php_min_ver 5.3

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Implements the Akamai {OPEN} EdgeGrid Authentication

Group:         Development/Libraries
License:       ASL 2.0
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Autoloader
BuildRequires: php-fedora-autoloader-devel
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
## phpcompatinfo (computed from version 0.6.0)
BuildRequires: php-date
BuildRequires: php-hash
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 0.6.0)
Requires:      php-date
Requires:      php-hash
Requires:      php-pcre
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Weak dependencies
%if 0%{?fedora} >= 21
Suggests:      php-composer(akamai-open/edgegrid-client)
%endif

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

# Broken out from client as of version 0.6.0
Conflicts:     php-akamai-open-edgegrid-client < 0.6.0

%description
This library implements the Akamai {OPEN} EdgeGrid Authentication scheme.

For more information visit the Akamai {OPEN} Developer Community [1].

Autoloader: %{phpdir}/Akamai/Open/EdgeGrid/autoload-auth.php

[1] https://developer.akamai.com/


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Create autoloader
%{_bindir}/phpab --template fedora --output src/autoload-auth.php src/


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}/Akamai/Open/EdgeGrid
cp -rp src/* %{buildroot}%{phpdir}/Akamai/Open/EdgeGrid/


%check
%if %{with_tests}
: Remove logging from PHPUnit config
sed '/log/d' phpunit.xml.dist > phpunit.xml

%if 0%{?fedora} > 25
: Temporarily skip test known to fail for PHP 7.1
: See https://github.com/akamai-open/AkamaiOPEN-edgegrid-php/issues/2
sed 's/function testTimestampFormat/function SKIP_testTimestampFormat/' \
    -i tests/Authentication/TimestampTest.php
%endif

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/Akamai/Open/EdgeGrid/autoload-auth.php || ret=1
   run=1
fi
if which php71; then
   sed 's/function testTimestampFormat/function SKIP_testTimestampFormat/' -i tests/Authentication/TimestampTest.php
   php71 %{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/Akamai/Open/EdgeGrid/autoload-auth.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}%{phpdir}/Akamai/Open/EdgeGrid/autoload-auth.php
# remirepo:2
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
%license LICENSE
%doc *.md
%doc composer.json
%dir %{phpdir}/Akamai
%dir %{phpdir}/Akamai/Open
%dir %{phpdir}/Akamai/Open/EdgeGrid
     %{phpdir}/Akamai/Open/EdgeGrid/Authentication
     %{phpdir}/Akamai/Open/EdgeGrid/Authentication.php
     %{phpdir}/Akamai/Open/EdgeGrid/autoload-auth.php


%changelog
* Thu Dec 22 2016 Remi Collet <remim@remirepo.net> - 0.6.1-1
- update to 0.6.1

* Fri Dec 09 2016 Shawn Iwinski <shawn@iwin.ski> - 0.6.0-2
- Temporarily skip test known to fail for PHP 7.1 (see
  https://github.com/akamai-open/AkamaiOPEN-edgegrid-php/issues/2 )
- Use php-composer(fedora/autoloader)

* Fri Oct 21 2016 Remi Collet <remim@remirepo.net> - 0.6.0-1
- add backport stuff

* Mon Oct 10 2016 Shawn Iwinski <shawn@iwin.ski> - 0.6.0-1
- Initial package
