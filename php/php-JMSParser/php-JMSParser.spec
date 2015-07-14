# remirepo spec file for php-JMSParser, from Fedora:
#
# RPM spec file for php-JMSParser
#
# Copyright (c) 2013-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner      schmittjoh
%global github_name       parser-lib
%global github_version    1.0.0
%global github_commit     c509473bc1b4866415627af0e1c6cc8ac97fa51d

%global composer_vendor   jms
%global composer_project  parser-lib

%global php_min_ver       5.3.0
# "phpoption/phpoption": ">=0.9,<2.0-dev"
#     NOTE: min version not 0.9 because autoloader required
%global phpoption_min_ver 1.4.0-4
%global phpoption_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-JMSParser
Version:       %{github_version}
Release:       7%{?dist}
Summary:       Library for writing recursive-descent parsers

Group:         Development/Libraries
License:       ASL 2.0
URL:           http://jmsyst.com/libs/%{github_name}

# GitHub export contains non-allowable licened documentation.
# Run php-JMSParser-get-source.sh to create allowable source.
Source0:       %{name}-%{github_version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: %{_bindir}/phpunit
BuildRequires: php(language) >= %{php_min_ver}
## composer.json
#BuildRequires: php-composer(phpoption/phpoption) >= %%{phpoption_min_ver}
BuildRequires: php-PhpOption >= %{phpoption_min_ver}
## phpcompatinfo (computed from version 1.0.0)
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

Requires:      php(language) >= %{php_min_ver}
# composer.json
#Requires:      php-composer(phpoption/phpoption) >= %%{phpoption_min_ver}
Requires:      php-PhpOption                     >= %{phpoption_min_ver}
Requires:      php-composer(phpoption/phpoption) <  %{phpoption_max_ver}
# phpcompatinfo (computed from version 1.0.0)
Requires:      php-json
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming
Provides:      php-%{composer_vendor}-%{composer_project} = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.


%prep
%setup -q -n %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee src/JMS/Parser/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 *
 * Created by %{name}-%{version}-%{release}
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

require_once '%{phpdir}/PhpOption/autoload.php';

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('JMS\\Parser\\', dirname(dirname(__DIR__)));

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
%{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}%{phpdir}/JMS/Parser/autoload.php
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
%dir %{phpdir}/JMS
     %{phpdir}/JMS/Parser


%changelog
* Sun Jul 12 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.0-7
- Added spec license
- New source script %%{name}-get-source.sh instead of %%{name}-strip.sh
- Added autoloader
- Added standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming provides
- Added php-composer(jms/parser-lib) provide
- %%license usage

* Tue Mar 19 2013 Remi Collet <remi@fedoraproject.org> 1.0.0-3
- backport 1.0.0 for remi repo.

* Mon Mar 18 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-3
- Added %%{name}-strip.sh as Source1

* Sat Mar 16 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-2
- Added phpoption_min_ver and phpoption_max_ver globals
- Bad licensed files stripped from source
- php-common => php(language)
- Removed tests sub-package

* Thu Jan 24 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-1
- Initial package
