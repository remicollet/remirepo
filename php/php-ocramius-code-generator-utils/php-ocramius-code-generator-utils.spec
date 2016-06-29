# remirepo spec file for php-ocramius-code-generator-utils, from
#
# Fedora spec file for php-ocramius-code-generator-utils
#
# Copyright (c) 2014-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     Ocramius
%global github_name      CodeGenerationUtils
%global github_version   0.4.0
%global github_commit    7dc0be1dec3376d95ba094688f0d84f7cf95f300

%global composer_vendor  ocramius
%global composer_project code-generator-utils

# "php": "~7.0"
%global php_min_ver 7.0
# "nikic/php-parser": "~2.0"
%global php_parser_min_ver 2.0
%global php_parser_max_ver 3

# Build using "--without tests" to disable tests
%global with_tests  %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:     %global phpdir     %{_datadir}/php}
%{!?__phpunit:  %global __phpunit  %{_bindir}/phpunit}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       A set of code generator utilities built on top of PHP-Parsers

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:     noarch
%if %{with_tests}
# composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(nikic/php-parser) >= %{php_parser_min_ver}
BuildRequires: php-composer(nikic/php-parser) <  %{php_parser_max_ver}
BuildRequires: php-composer(phpunit/phpunit)  >= 5.0
BuildRequires: %{_bindir}/phpab
# phpcompatinfo (computed from version 0.4.0)
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(nikic/php-parser) >= %{php_parser_min_ver}
Requires:      php-composer(nikic/php-parser) <  %{php_parser_max_ver}
# phpcompatinfo (computed from version 0.4.0)
Requires:      php-pcre
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
A set of code generator utilities built on top of PHP-Parsers that ease its use
when combined with Reflection.

Autoloader: %{phpdir}/CodeGenerationUtils/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}


%build
%{_bindir}/phpab --output src/CodeGenerationUtils/autoload.php src/CodeGenerationUtils
cat << 'EOF' | tee -a src/CodeGenerationUtils/autoload.php
require_once '%{phpdir}/PhpParser2/autoload.php';
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
require_once '%{buildroot}%{phpdir}/CodeGenerationUtils/autoload.php';
EOF

%{_bindir}/phpunit
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
%{phpdir}/CodeGenerationUtils


%changelog
* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 0.4.0-1
- update to 0.4.0
- raise dependency on php ~7.0
- raise dependency on nikic/php-parser ~2.0
- add simple autoloader

* Sun Aug  9 2015 Remi Collet <remi@fedoraproject.org> - 0.3.2-1
- update to 0.3.2
- raise dependency on nikic/php-parser ~1.3

* Wed Feb 25 2015 Remi Collet <remi@fedoraproject.org> - 0.3.1-1
- update to 0.3.1 (no change)
- raise nikic/php-parser max version

* Thu Nov  6 2014 Remi Collet <remi@fedoraproject.org> - 0.3.0-2
- backport for remi repository

* Wed Nov 05 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.3.0-2
- Silenced include in autoloader
- Removed debug from %%check

* Mon Oct 27 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.3.0-1
- Initial package
