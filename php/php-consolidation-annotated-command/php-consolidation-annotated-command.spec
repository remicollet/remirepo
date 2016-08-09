# remirepo spec file for php-consolidation-annotated-command, from:
#
# Fedora spec file for php-consolidation-annotated-command
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     consolidation-org
%global github_name      annotated-command

%global github_version   1.2.1
%global github_commit    296b4f507b1e184a28c9969bc7ae779f689db5ee

%global composer_vendor  consolidation
%global composer_project annotated-command


# "php": ">=5.4.0"
%global php_min_ver 5.4.0
# "consolidation/output-formatters": "~1"
%global consolidation_output_formatters_min_ver 1
%global consolidation_output_formatters_max_ver 2
# "psr/log": "~1.0"
#     NOTE: Min version not 1.0 because autoloader required
%global psr_log_min_ver 1.0.0-8
%global psr_log_max_ver 2.0
# "phpdocumentor/reflection-docblock": "^2.0|^3.0.2"
%global phpdocumentor_reflection_docblock_min_ver 2
%global phpdocumentor_reflection_docblock_max_ver 4
# "symfony/console": "~2.5|~3.0"
# "symfony/finder": "~2.5|~3.0"
#     NOTE: Min version not 2.5 because autoloader required
%global symfony_min_ver 2.7.1
%global symfony_max_ver 4.0

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
#BuildRequires: php-composer(psr/log)                           >= %%{psr_log_min_ver}
BuildRequires: php-PsrLog                                      >= %{psr_log_min_ver}
BuildRequires: php-composer(symfony/console)                   <  %{symfony_max_ver}
BuildRequires: php-composer(symfony/console)                   >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/finder)                    <  %{symfony_max_ver}
BuildRequires: php-composer(symfony/finder)                    >= %{symfony_min_ver}
## phpcompatinfo (computed from version 1.2.1)
BuildRequires: php-pcre
BuildRequires: php-reflection
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                                   >= %{php_min_ver}
Requires:      php-composer(phpdocumentor/reflection-docblock) <  %{phpdocumentor_reflection_docblock_max_ver}
Requires:      php-composer(phpdocumentor/reflection-docblock) >= %{phpdocumentor_reflection_docblock_min_ver}
Requires:      php-composer(psr/log)                           <  %{psr_log_max_ver}
#Requires:      php-composer(psr/log)                           >= %%{psr_log_min_ver}
Requires:      php-PsrLog                                      >= %{psr_log_min_ver}
Requires:      php-composer(symfony/console)                   <  %{symfony_max_ver}
Requires:      php-composer(symfony/console)                   >= %{symfony_min_ver}
Requires:      php-composer(symfony/finder)                    <  %{symfony_max_ver}
Requires:      php-composer(symfony/finder)                    >= %{symfony_min_ver}
# phpcompatinfo (computed from version 1.2.1)
Requires:      php-pcre
Requires:      php-reflection
# Autoloader
Requires:      php-composer(symfony/class-loader)

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
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Consolidation\\AnnotatedCommand\\', dirname(dirname(__DIR__)));

// Required dependencies
require_once '%{phpdir}/phpDocumentor/Reflection/DocBlock/autoload.php';
require_once '%{phpdir}/Psr/Log/autoload.php';
require_once '%{phpdir}/Symfony/Component/Console/autoload.php';
require_once '%{phpdir}/Symfony/Component/Finder/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%install
rm -rf   %{buildroot}

mkdir -p %{buildroot}%{phpdir}/Consolidation/AnnotatedCommand
cp -rp src/* %{buildroot}%{phpdir}/Consolidation/AnnotatedCommand/


%check
%if %{with_tests}
: Mock PSR-0 tests
mkdir -p tests-psr0/Consolidation
ln -s ../../tests/src tests-psr0/Consolidation/TestUtils

: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
$fedoraClassLoader =
    require '%{buildroot}%{phpdir}/Consolidation/AnnotatedCommand/autoload.php';
$fedoraClassLoader->addPrefix('Consolidation\\TestUtils\\', __DIR__.'/tests-psr0');

require_once '%{phpdir}/Consolidation/OutputFormatters/autoload.php';
BOOTSTRAP

run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap bootstrap.php || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap bootstrap.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
   %{_bindir}/phpunit --verbose --bootstrap bootstrap.php
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
%dir %{phpdir}/Consolidation
     %{phpdir}/Consolidation/AnnotatedCommand


%changelog
* Mon Aug 08 2016 Shawn Iwinski <shawn@iwin.ski> - 1.2.1-1
- Updated to 1.2.1 (RHBZ #1359450)

* Thu Jul 21 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- backport for remi repository

* Tue Jul 19 2016 Shawn Iwinski <shawn@iwin.ski> - 1.0.1-1
- Initial package
