# remirepo spec file for php-ocramius-proxy-manager from Fedora:
#
# RPM spec file for php-ocramius-proxy-manager
#
# Copyright (c) 2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner      Ocramius
%global github_name       ProxyManager
%global github_version    2.0.2
%global github_commit     001e730968f17cb36816ad68914994341d16e029
%global github_short      %(c=%{github_commit}; echo ${c:0:7})

%global composer_vendor   ocramius
%global composer_project  proxy-manager

# "php": "7.0.0 - 7.0.5 || ^7.0.7"
%global php_min_ver 7.0.7
# "zendframework/zend-code": "~3.0"
%global zf_min_ver  3.0
%global zf_max_ver  4

# Build using "--without tests" to disable tests
%global with_tests %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       OOP proxy wrappers utilities

Group:         Development/Libraries
License:       MIT
URL:           http://ocramius.github.io/ProxyManager/
Source0:       %{name}-%{github_version}-%{github_short}.tgz
# git snapshot to retrieve test suite
Source1:       makesrc.sh
# Hardcode library version
# drop dependency on ocramius/package-versions
Patch0:        %{name}-rpm.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:     noarch
# Autoload generation
BuildRequires: %{_bindir}/phpab
%if %{with_tests}
# Tests
## composer.json
BuildRequires: %{_bindir}/phpunit
BuildRequires: php-composer(zendframework/zend-code) >= %{zf_min_ver}
BuildRequires: php-composer(zendframework/zend-loader)
## phpcompatinfo (computed from version 2.0.0)
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
# Autoloader
BuildRequires: php-composer(phpunit/phpunit)         >= 5.1.3
%endif

# composer.json
Requires:      php(language)                         >= %{php_min_ver}
Requires:      php-composer(zendframework/zend-code) >= %{zf_min_ver}
Requires:      php-composer(zendframework/zend-code) <  %{zf_max_ver}
# phpcompatinfo (computed from version 2.0.0)
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(zendframework/zend-loader)
%if 0%{?fedora} >= 21
Suggests:      php-composer(zendframework/zend-xmlrpc)
Suggests:      php-composer(zendframework/zend-json)
Suggests:      php-composer(zendframework/zend-soap)
%endif

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
This library aims at providing abstraction for generating various kinds
of proxy classes.

Autoloader: %{phpdir}/ProxyManager/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

%patch0 -p0
sed -e 's/@VERSION@/%{version}/' \
    -e 's/@COMMIT@/%{github_commit}/' \
    -i src/ProxyManager/Version.php
grep ' return' src/ProxyManager/Version.php


%build
: Generate autoloader
%{_bindir}/phpab --output src/ProxyManager/autoload.php src/ProxyManager
cat << 'EOF' | tee -a     src/ProxyManager/autoload.php
// For dependencies
require_once '%{phpdir}/Zend/autoload.php';
EOF


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create tests autoload
mkdir vendor
%{_bindir}/phpab --output vendor/autoload.php tests
cat << 'EOF' | tee -a vendor/autoload.php
require_once '%{buildroot}%{phpdir}/ProxyManager/autoload.php';
EOF

: Run tests
%{_bindir}/phpunit --verbose --exclude-group Performance
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
%{phpdir}/ProxyManager


%changelog
* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- update to 2.0.2
- raise dependency on php 7.0.7
- raise dependency on zendframework/zend-code 3.0

* Mon Aug 10 2015 Remi Collet <remi@remirepo.net> - 1.0.2-1
- update to 1.0.2

* Fri May 29 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.0-2
- Fix autoloader to load all optional pkgs
- Some spec cleanup

* Mon May 18 2015 Remi Collet <RPMS@FamilleCollet.com> - 1.0.0-1
- add needed backport stuff for remi repository

* Sat May 16 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.0-1
- Initial package
