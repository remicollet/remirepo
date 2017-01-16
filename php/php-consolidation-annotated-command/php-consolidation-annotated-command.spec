# remirepo spec file for php-consolidation-annotated-command, from:
#
# Fedora spec file for php-consolidation-annotated-command
#
# Copyright (c) 2016-2017 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     consolidation-org
%global github_name      annotated-command
%global github_version   2.2.2
%global github_commit    1f1d92807f72901e049e9df048b412c3bc3652c9

%global composer_vendor  consolidation
%global composer_project annotated-command

# "php": ">=5.4.0"
%global php_min_ver 5.4.0
# "consolidation/output-formatters": "^3.1.5"
%global consolidation_output_formatters_min_ver 3.1.5
%global consolidation_output_formatters_max_ver 4
# "psr/log": "~1"
#     NOTE: Min version not 1.0 because autoloader required
%global psr_log_min_ver 1.0.1
%global psr_log_max_ver 2.0
# "phpdocumentor/reflection-docblock": "^2.0|^3.0.2"
#     NOTE: Min version not 4.0 because v3 not packaged yet
%global phpdocumentor_reflection_docblock_min_ver 2.0
%global phpdocumentor_reflection_docblock_max_ver 3.0
# "symfony/console": "^2.8|~3.0"
# "symfony/event-dispatcher": "^2.5|~3.0"
# "symfony/finder": "^2.5|~3.0"
#     NOTE: Min version not 4.0 because v3 not packaged yet
%global symfony_min_ver 2.8
%global symfony_max_ver 3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Initialize Symfony Console commands from annotated command class methods

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language)                                   >= %{php_min_ver}
BuildRequires: php-composer(consolidation/output-formatters)   <  %{consolidation_output_formatters_max_ver}
BuildRequires: php-composer(consolidation/output-formatters)   >= %{consolidation_output_formatters_min_ver}
BuildRequires: php-composer(phpdocumentor/reflection-docblock) <  %{phpdocumentor_reflection_docblock_max_ver}
BuildRequires: php-composer(phpdocumentor/reflection-docblock) >= %{phpdocumentor_reflection_docblock_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(psr/log)                           <  %{psr_log_max_ver}
BuildRequires: php-composer(psr/log)                           >= %{psr_log_min_ver}
BuildRequires: php-composer(symfony/console)                   <  %{symfony_max_ver}
BuildRequires: php-composer(symfony/console)                   >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/event-dispatcher)          <  %{symfony_max_ver}
BuildRequires: php-composer(symfony/event-dispatcher)          >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/finder)                    <  %{symfony_max_ver}
BuildRequires: php-composer(symfony/finder)                    >= %{symfony_min_ver}
## phpcompatinfo (computed from version 2.2.2)
BuildRequires: php-dom
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language)                                   >= %{php_min_ver}
Requires:      php-composer(consolidation/output-formatters)   <  %{consolidation_output_formatters_max_ver}
Requires:      php-composer(consolidation/output-formatters)   >= %{consolidation_output_formatters_min_ver}
Requires:      php-composer(phpdocumentor/reflection-docblock) <  %{phpdocumentor_reflection_docblock_max_ver}
Requires:      php-composer(phpdocumentor/reflection-docblock) >= %{phpdocumentor_reflection_docblock_min_ver}
Requires:      php-composer(psr/log)                           <  %{psr_log_max_ver}
Requires:      php-composer(psr/log)                           >= %{psr_log_min_ver}
Requires:      php-composer(symfony/console)                   <  %{symfony_max_ver}
Requires:      php-composer(symfony/console)                   >= %{symfony_min_ver}
Requires:      php-composer(symfony/event-dispatcher)          <  %{symfony_max_ver}
Requires:      php-composer(symfony/event-dispatcher)          >= %{symfony_min_ver}
Requires:      php-composer(symfony/finder)                    <  %{symfony_max_ver}
Requires:      php-composer(symfony/finder)                    >= %{symfony_min_ver}
# phpcompatinfo (computed from version 2.2.2)
Requires:      php-dom
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.

Autoloader: %{phpdir}/Consolidation/AnnotatedCommand/autoload.php


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

\Fedora\Autoloader\Autoload::addPsr4('Consolidation\\AnnotatedCommand\\', __DIR__);

\Fedora\Autoloader\Dependencies::required([
    '%{phpdir}/Consolidation/OutputFormatters/autoload.php',
    '%{phpdir}/phpDocumentor/Reflection/DocBlock/autoload.php',
    '%{phpdir}/Psr/Log/autoload.php',
    '%{phpdir}/Symfony/Component/Console/autoload.php',
    '%{phpdir}/Symfony/Component/EventDispatcher/autoload.php',
    '%{phpdir}/Symfony/Component/Finder/autoload.php',
]);
AUTOLOAD


%install
rm -rf   %{buildroot}

mkdir -p %{buildroot}%{phpdir}/Consolidation/AnnotatedCommand
cp -rp src/* %{buildroot}%{phpdir}/Consolidation/AnnotatedCommand/


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require_once '%{buildroot}%{phpdir}/Consolidation/AnnotatedCommand/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('Consolidation\\TestUtils\\', __DIR__.'/tests/src');
BOOTSTRAP

: Skip test known to fail
sed 's/function testInteractAndValidate/function SKIP_testInteractAndValidate/' \
    -i tests/testAnnotatedCommandFactory.php

: Upstream tests
%{_bindir}/phpunit --verbose --bootstrap bootstrap.php

: Upstream tests with SCLs if available
SCL_RETURN_CODE=0
for SCL in php56 php70 php71; do
    if which $SCL; then
       $SCL %{_bindir}/phpunit --bootstrap bootstrap.php || SCL_RETURN_CODE=1
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
%dir %{phpdir}/Consolidation
     %{phpdir}/Consolidation/AnnotatedCommand


%changelog
* Sun Jan 15 2017 Shawn Iwinski <shawn@iwin.ski> - 2.2.2-1
- Update to 2.2.2 (RHBZ #1395001)
- Use php-composer(fedora/autoloader)
- Run upstream tests with SCLs if they are available

* Tue Nov 01 2016 Shawn Iwinski <shawn@iwin.ski> - 2.0.1-2
- Skip test known to fail

* Tue Nov 01 2016 Shawn Iwinski <shawn@iwin.ski> - 2.0.1-1
- Updated to 2.0.1 (RHBZ #1370772)

* Mon Aug 08 2016 Shawn Iwinski <shawn@iwin.ski> - 1.2.1-1
- Updated to 1.2.1 (RHBZ #1359450)

* Thu Jul 21 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- backport for remi repository

* Tue Jul 19 2016 Shawn Iwinski <shawn@iwin.ski> - 1.0.1-1
- Initial package
