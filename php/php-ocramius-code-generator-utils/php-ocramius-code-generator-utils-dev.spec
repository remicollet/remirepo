# remirepo spec file for php-ocramius-code-generator-utils, from
#
# Fedora spec file for php-ocramius-code-generator-utils
#
# Copyright (c) 2014-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
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
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       3%{?github_release}%{?dist}
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
BuildRequires: php-nikic-php-parser
BuildRequires: php-composer(phpunit/phpunit)  >= 5.0
# phpcompatinfo (computed from version 0.4.0)
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
# Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# workaround for range version
Requires:      php-nikic-php-parser
# phpcompatinfo (computed from version 0.4.0)
Requires:      php-pcre
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
A set of code generator utilities built on top of PHP-Parsers that ease its use
when combined with Reflection.

Autoloader: %{phpdir}/CodeGenerationUtils/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/CodeGenerationUtils/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('CodeGenerationUtils\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/PhpParser2/autoload.php',
));
AUTOLOAD


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}
cp -rp src/CodeGenerationUtils %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require '%{buildroot}%{phpdir}/CodeGenerationUtils/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('CodeGenerationUtilsTest\\', __DIR__.'/tests/CodeGenerationUtilsTests');
\Fedora\Autoloader\Autoload::addPsr4('CodeGenerationUtilsTestAsset\\', __DIR__.'/tests/CodeGenerationUtilsTestAsset');
BOOTSTRAP

%{_bindir}/phpunit --verbose --bootstrap bootstrap.php
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
%{phpdir}/CodeGenerationUtils


%changelog
* Wed Feb 22 2017 Remi Collet <remi@fedoraproject.org> - 0.4.0-3
- switch to fedora-autoloader

* Wed Feb 22 2017 Remi Collet <remi@fedoraproject.org> - 0.4.0-2
- implicitly requires php-nikic-php-parser (v2)
- fix FTBFS #1424073

* Wed Oct 12 2016 Remi Collet <remi@fedoraproject.org> - 0.4.0-2
- switch from classmap autoloader to PSR-0 one (symfony)

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
