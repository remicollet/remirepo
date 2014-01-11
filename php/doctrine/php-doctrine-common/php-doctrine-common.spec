%global github_owner     doctrine
%global github_name      common
%global github_version   2.4.1
%global github_commit    ceb18cf9b0230f3ea208b6238130fd415abda0a7

# "php": ">=5.3.2"
%global php_min_ver      5.3.2
# "doctrine/*": "1.*"
%global doctrine_min_ver 1.0
%global doctrine_max_ver 2.0

Name:          php-%{github_owner}-%{github_name}
Version:       %{github_version}
Release:       2%{?dist}
Summary:       Common library for Doctrine projects

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# For tests
BuildRequires: php(language)            >= %{php_min_ver}
BuildRequires: php-doctrine-annotations >= %{doctrine_min_ver}
BuildRequires: php-doctrine-annotations <  %{doctrine_max_ver}
BuildRequires: php-doctrine-cache       >= %{doctrine_min_ver}
BuildRequires: php-doctrine-cache       <  %{doctrine_max_ver}
BuildRequires: php-doctrine-collections >= %{doctrine_min_ver}
BuildRequires: php-doctrine-collections <  %{doctrine_max_ver}
BuildRequires: php-doctrine-inflector   >= %{doctrine_min_ver}
BuildRequires: php-doctrine-inflector   <  %{doctrine_max_ver}
BuildRequires: php-doctrine-lexer       >= %{doctrine_min_ver}
BuildRequires: php-doctrine-lexer       <  %{doctrine_max_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
# For tests: phpcompatinfo (computed from v2.4.1)
BuildRequires: php-date
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
BuildRequires: php-tokenizer

Requires:      php(language)            >= %{php_min_ver}
Requires:      php-doctrine-annotations >= %{doctrine_min_ver}
Requires:      php-doctrine-annotations <  %{doctrine_max_ver}
Requires:      php-doctrine-cache       >= %{doctrine_min_ver}
Requires:      php-doctrine-cache       <  %{doctrine_max_ver}
Requires:      php-doctrine-collections >= %{doctrine_min_ver}
Requires:      php-doctrine-collections <  %{doctrine_max_ver}
Requires:      php-doctrine-inflector   >= %{doctrine_min_ver}
Requires:      php-doctrine-inflector   <  %{doctrine_max_ver}
Requires:      php-doctrine-lexer       >= %{doctrine_min_ver}
Requires:      php-doctrine-lexer       <  %{doctrine_max_ver}
# phpcompatinfo (computed from v2.4.1)
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
Requires:      php-tokenizer

# PEAR
Provides:      php-pear(pear.doctrine-project.org/DoctrineCommon) = %{version}
# Rename
Obsoletes:     php-doctrine-DoctrineCommon < %{version}
Provides:      php-doctrine-DoctrineCommon = %{version}

%description
The Doctrine Common project is a library that provides extensions to core PHP
functionality.


%prep
%setup -q -n %{github_name}-%{github_commit}


%build
# Empty build section, nothing required


%install
mkdir -p %{buildroot}/%{_datadir}/php
cp -rp lib/* %{buildroot}/%{_datadir}/php/


%check
# Create tests' init
cat > tests/Doctrine/Tests/TestInit.php <<'TESTINIT'
<?php
namespace Doctrine\Tests;

spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', str_replace('_', '/', $class)).'.php';
    @include_once $src;
});

\Doctrine\Common\Annotations\AnnotationRegistry::registerAutoloadNamespace(
    'Doctrine\Tests\Common\Annotations\Fixtures', __DIR__ . '/../../'
);
TESTINIT

# Create PHPUnit config w/ colors turned off
sed 's/colors="true"/colors="false"/' phpunit.xml.dist > phpunit.xml

%{_bindir}/phpunit --include-path ./lib:./tests -d date.timezone="UTC"


%files
%doc LICENSE *.md UPGRADE* composer.json
%{_datadir}/php/Doctrine/Common/*.php
%{_datadir}/php/Doctrine/Common/Persistence
%{_datadir}/php/Doctrine/Common/Proxy
%{_datadir}/php/Doctrine/Common/Reflection
%{_datadir}/php/Doctrine/Common/Util


%changelog
* Sat Jan 04 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 2.4.1-2
- Conditional %%{?dist}
- Removed php-channel-doctrine obsolete

* Fri Dec 27 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.4.1-1
- Initial package
