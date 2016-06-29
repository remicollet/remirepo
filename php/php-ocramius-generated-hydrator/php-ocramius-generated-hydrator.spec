# remirpeo spec file for php-ocramius-generated-hydrator, from
#
# Fedora spec file for php-ocramius-generated-hydrator
#
# Copyright (c) 2014-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     Ocramius
%global github_name      GeneratedHydrator
%global github_version   2.0.0
%global github_commit    98a731e7d4e393513cb6f4e7f120da853680fb50

%global composer_vendor  ocramius
%global composer_project generated-hydrator

# "php": "~7.0"
#     NOTE: Max version ignored on purpose
%global php_min_ver 7.0
# "nikic/php-parser": "~2.0"
%global php_parser_min_ver 2.0
%global php_parser_max_ver 3
# "ocramius/code-generator-utils": "0.4.*"
%global ocramius_cgu_min_ver 0.4.0
%global ocramius_cgu_max_ver 0.5
# "zendframework/zend-hydrator": "~2.0"
%global zf_hydrator_min_ver 2.0
%global zf_hydrator_max_ver 3

# Build using "--without tests" to disable tests
%global with_tests  %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:     %global phpdir     %{_datadir}/php}
%{!?__phpunit:  %global __phpunit  %{_bindir}/phpunit}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       An object hydrator

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
BuildRequires: %{_bindir}/phpab
%if %{with_tests}
# composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(nikic/php-parser) >= %{php_parser_min_ver}
BuildRequires: php-composer(nikic/php-parser) <  %{php_parser_max_ver}
BuildRequires: php-composer(ocramius/code-generator-utils) >= %{ocramius_cgu_min_ver}
BuildRequires: php-composer(ocramius/code-generator-utils) <  %{ocramius_cgu_max_ver}
BuildRequires: php-composer(zendframework/zend-hydrator) >= %{zf_hydrator_min_ver}
BuildRequires: php-composer(zendframework/zend-hydrator) <  %{zf_hydrator_max_ver}
BuildRequires: php-composer(phpunit/phpunit) >= 5.0
# phpcompatinfo (computed from version 2.0.0)
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(nikic/php-parser) >= %{php_parser_min_ver}
Requires:      php-composer(nikic/php-parser) <  %{php_parser_max_ver}
Requires:      php-composer(ocramius/code-generator-utils) >= %{ocramius_cgu_min_ver}
Requires:      php-composer(ocramius/code-generator-utils) <  %{ocramius_cgu_max_ver}
Requires:      php-composer(zendframework/zend-hydrator) >= %{zf_hydrator_min_ver}
Requires:      php-composer(zendframework/zend-hydrator) <  %{zf_hydrator_max_ver}
# phpcompatinfo (computed from version 2.0.0)
Requires:      php-reflection
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
GeneratedHydrator is a library about high performance transition of data from
arrays to objects and from objects to arrays.

Autoloader: %{phpdir}/GeneratedHydrator/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}


%build
%{_bindir}/phpab --output src/GeneratedHydrator/autoload.php src/GeneratedHydrator
cat << 'EOF' | tee -a src/GeneratedHydrator/autoload.php
require_once '%{phpdir}/CodeGenerationUtils/autoload.php';
require_once '%{phpdir}/PhpParser2/autoload.php';
require_once '%{phpdir}/Zend/autoload.php';
EOF


%install
rm -rf %{buildroot}
mkdir -pm 0755 %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
mkdir vendor
%{_bindir}/phpab --output vendor/autoload.php tests
cat << 'EOF' | tee -a vendor/autoload.php
require_once '%{buildroot}%{phpdir}/GeneratedHydrator/autoload.php';
EOF

%{_bindir}/phpunit --verbose
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md composer.json
%{phpdir}/GeneratedHydrator


%changelog
* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0
- drop dependency on zendframework/zend-stdlib
- raise dependency on php ~7.0
- raise dependency on nikic/php-parser ~2.0
- raise dependency on ocramius/code-generator-utils 0.4.*
- add dependency on zendframework/zend-hydrator
- add simple autoloader

* Wed Feb 25 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1 (no change)
- raise nikic/php-parser max version

* Sat Nov 29 2014 Remi Collet <rpms@famillecollet.com> - 1.1.0-1
- backport for remi repo

* Mon Oct 27 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.0-1
- Initial package
