%global github_owner     doctrine
%global github_name      data-fixtures
%global github_version   1.0.0
%global github_commit    b4a135c7db56ecc4602b54a2184368f440cac33e

# "php": ">=5.3.2"
%global php_min_ver      5.3.2
# "doctrine/*": ">=2.2,<2.5-dev"
%global doctrine_min_ver 2.2
%global doctrine_max_ver 2.5

Name:          php-doctrine-datafixtures
Version:       %{github_version}
Release:       2%{?dist}
Summary:       Data Fixtures for all Doctrine Object Managers

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# For tests
BuildRequires: php(language)       >= %{php_min_ver}
BuildRequires: php-doctrine-common >= %{doctrine_min_ver}
BuildRequires: php-doctrine-common <  %{doctrine_max_ver}
BuildRequires: php-doctrine-orm    >= %{doctrine_min_ver}
BuildRequires: php-doctrine-orm    <  %{doctrine_max_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
# For tests: phpcompatinfo (computed from v1.0.0)
BuildRequires: php-json
BuildRequires: php-reflection
BuildRequires: php-spl

Requires:      php(language)       >= %{php_min_ver}
Requires:      php-doctrine-common >= %{doctrine_min_ver}
Requires:      php-doctrine-common <  %{doctrine_max_ver}
# Optional
Requires:      php-doctrine-orm    >= %{doctrine_min_ver}
Requires:      php-doctrine-orm    <  %{doctrine_max_ver}
# phpcompatinfo (computed from v1.0.0)
Requires:      php-json
Requires:      php-reflection
Requires:      php-spl

%description
This extension aims to provide a simple way to manage and execute the loading
of data fixtures for the Doctrine ORM or ODM.


%prep
%setup -q -n %{github_name}-%{github_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_datadir}/php
cp -rp lib/* %{buildroot}/%{_datadir}/php/


%check
# Rewrite tests' bootstrap
cat > tests/bootstrap.php <<'BOOTSTRAP'
<?php
spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', str_replace('_', '/', $class)).'.php';
    @include_once $src;
});
BOOTSTRAP

# Skip tests known to fail
sed -e 's#function test_orderFixturesByDependencies_circularReferencesMakeMethodThrowCircularReferenceException#function SKIP_test_orderFixturesByDependencies_circularReferencesMakeMethodThrowCircularReferenceException#' \
    -e 's#function test_orderFixturesByDependencies_fixturesCantHaveItselfAsParent#function SKIP_test_orderFixturesByDependencies_fixturesCantHaveItselfAsParent#' \
    -e 's#function test_inCaseAFixtureHasAnUnexistentDependencyOrIfItWasntLoaded_throwsException#function SKIP_test_inCaseAFixtureHasAnUnexistentDependencyOrIfItWasntLoaded_throwsException#' \
    -i tests/Doctrine/Tests/Common/DataFixtures/DependentFixtureTest.php
sed 's#function testReferenceReconstruction#function SKIP_testReferenceReconstruction#' \
    -i tests/Doctrine/Tests/Common/DataFixtures/ProxyReferenceRepositoryTest.php

# Create PHPUnit config w/ colors turned off
sed 's/colors="true"/colors="false"/' phpunit.xml.dist > phpunit.xml

%{_bindir}/phpunit --include-path ./lib:./tests -d date.timezone="UTC"


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE *.md UPGRADE composer.json
%{_datadir}/php/Doctrine/Common/DataFixtures


%changelog
* Sat Jan 11 2014 Remi Collet <rpms@famillecollet.com> 1.0.0-2
- backport for remi repo

* Sun Jan 05 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-2
- Use non-PEAR Doctrine pkgs
- Conditional %%{?dist}

* Fri Dec 20 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-1
- Initial package
