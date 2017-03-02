# remirepo spec file for php-consolidation-output-formatters, from
#
# Fedora spec file for php-consolidation-output-formatters
#
# Copyright (c) 2016-2017 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     consolidation-org
%global github_name      output-formatters
%global github_version   3.1.8
%global github_commit    0b50ba1134d581fd55376f3e21508dab009ced47

%global composer_vendor  consolidation
%global composer_project output-formatters

# "php": ">=5.4.0"
%global php_min_ver 5.4.0
# "symfony/console": "^2.8|~3"
# "symfony/finder": "~2.5|~3.0"
#     NOTE: Min version not 4.0 because v3 not packaged yet
%global symfony_min_ver 2.8
%global symfony_max_ver 3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Format text by applying transformations provided by plug-in formatters

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(symfony/console) <  %{symfony_max_ver}
BuildRequires: php-composer(symfony/console) >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/finder) <  %{symfony_max_ver}
BuildRequires: php-composer(symfony/finder) >= %{symfony_min_ver}
## phpcompatinfo (computed from version 3.1.6)
BuildRequires: php-dom
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(symfony/console) <  %{symfony_max_ver}
Requires:      php-composer(symfony/console) >= %{symfony_min_ver}
Requires:      php-composer(symfony/finder) <  %{symfony_max_ver}
Requires:      php-composer(symfony/finder) >= %{symfony_min_ver}
# phpcompatinfo (computed from version 3.1.6)
Requires:      php-dom
Requires:      php-json
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.

Autoloader: %{phpdir}/Consolidation/OutputFormatters/autoload.php


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

\Fedora\Autoloader\Autoload::addPsr4('Consolidation\\OutputFormatters\\', __DIR__);

\Fedora\Autoloader\Dependencies::required([
    '%{phpdir}/Symfony/Component/Console/autoload.php',
    '%{phpdir}/Symfony/Component/Finder/autoload.php',
]);
AUTOLOAD


%install
rm -rf   %{buildroot}

mkdir -p %{buildroot}%{phpdir}/Consolidation/OutputFormatters
cp -rp src/* %{buildroot}%{phpdir}/Consolidation/OutputFormatters/


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require_once '%{buildroot}%{phpdir}/Consolidation/OutputFormatters/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('Consolidation\\TestUtils\\', __DIR__.'/tests/src');
BOOTSTRAP

: Skip API documentation test
rm -f tests/testAPIDocs.php

: Upstream tests
%{_bindir}/phpunit --verbose --bootstrap bootstrap.php

: Upstream tests with SCLs if available
SCL_RETURN_CODE=0
for SCL in %{?rhel:php55} php56 php70 php71; do
    if which $SCL; then
       $SCL %{_bindir}/phpunit --bootstrap bootstrap.php || SCL_RETURN_CODE=1
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
%dir %{phpdir}/Consolidation
     %{phpdir}/Consolidation/OutputFormatters


%changelog
* Thu Mar  2 2017 Remi Collet <remi@remirepo.net> - 3.1.8-1
- Update to 3.1.8

* Tue Feb 28 2017 Shawn Iwinski <shawn@iwin.ski> - 3.1.7-1
- Update to 3.1.7 (RHBZ #1415386)

* Sat Jan 21 2017 Remi Collet <remi@remirepo.net> - 3.1.7-1
- Update to 3.1.7

* Mon Jan 16 2017 Remi Collet <remi@fedoraproject.org> - 3.1.6-2
- fix autoloader dependency

* Sun Jan 15 2017 Shawn Iwinski <shawn@iwin.ski> - 3.1.6-1
- Update to 3.1.6 (RHBZ #1392720)
- Use php-composer(fedora/autoloader)
- Run upstream tests with SCLs if they are available

* Tue Nov 01 2016 Shawn Iwinski <shawn@iwin.ski> - 2.0.1-1
- Update to 2.0.1 (RHBZ #1376274)

* Thu Jul 21 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- backport for remi repository

* Tue Jul 19 2016 Shawn Iwinski <shawn@iwin.ski> - 1.0.0-1
- Initial package
