# remirepo spec file for php-doctrine-annotations, from:
#
# Fedora spec file for php-doctrine-annotations
#
# Copyright (c) 2013-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      annotations
%global github_version   1.2.7
%global github_commit    f25c8aab83e0c3e976fd7d19875f198ccf2f7535

%global composer_vendor  doctrine
%global composer_project annotations

# "php": ">=5.3.2"
%global php_min_ver      5.3.2
# "doctrine/cache": "1.*"
#     NOTE: Min version not 1.0 because autoloader required
%global cache_min_ver    1.4.1
%global cache_max_ver    2.0
# "doctrine/lexer": "1.*"
#     NOTE: Min version not 1.0 because autoloader required
%global lexer_min_ver    1.0.1-4
%global lexer_max_ver    2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       PHP docblock annotations parser library

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}

# GitHub export does not include tests.
# Run php-doctrine-annotations-get-source.sh to create full source.
Source0:       %{name}-%{version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: %{_bindir}/phpunit
BuildRequires: php(language)                >= %{php_min_ver}
BuildRequires: php-composer(doctrine/cache) >= %{cache_min_ver}
#BuildRequires: php-composer(doctrine/lexer) >= %%{lexer_min_ver}
BuildRequires: php-doctrine-lexer           >= %{lexer_min_ver}
## phpcompatinfo (computed from version 1.2.7)
BuildRequires: php-ctype
BuildRequires: php-date
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
BuildRequires: php-tokenizer
# Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                >= %{php_min_ver}
#Requires:      php-composer(doctrine/lexer) >= %%{lexer_min_ver}
Requires:      php-doctrine-lexer           >= %{lexer_min_ver}
Requires:      php-composer(doctrine/lexer) <  %{lexer_max_ver}
# phpcompatinfo (computed from version 1.2.7)
Requires:      php-ctype
Requires:      php-date
Requires:      php-json
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
Requires:      php-tokenizer
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

# Extracted from Doctrine Common as of version 2.4
Conflicts:     php-pear(pear.doctrine-project.org/DoctrineCommon) < 2.4

%description
%{summary} (extracted from Doctrine Common).


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee lib/Doctrine/Common/Annotations/autoload.php
<?php
/**
 * Autoloader created by %{name}-%{version}-%{release}
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

$fedoraClassLoader->addPrefix('Doctrine\\Common\\Annotations\\', dirname(dirname(dirname(__DIR__))));

require_once '%{phpdir}/Doctrine/Common/Lexer/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}
cp -rp lib/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Modify tests init
sed "s#require.*autoload.*#require_once '%{buildroot}%{phpdir}/Doctrine/Common/Annotations/autoload.php';#" \
    -i tests/Doctrine/Tests/TestInit.php

: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php

require_once '%{phpdir}/Doctrine/Common/Cache/autoload.php';
require_once __DIR__ . '/tests/Doctrine/Tests/TestInit.php';
BOOTSTRAP

: Run tests
%{_bindir}/phpunit \
    -d pcre.recursion_limit=10000 \
    --verbose --bootstrap bootstrap.php
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
%{phpdir}/Doctrine/Common/Annotations


%changelog
* Sat Sep 05 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.7-1
- Updated to 1.2.7 (RHBZ #1258669 / CVE-2015-5723)
- Updated autoloader to load dependencies after self registration

* Sat Jun 27 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.6-2
- Updated autoloader with trailing separator

* Wed Jun 24 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.6-1
- Updated to 1.2.6 (RHBZ #1211816)
- Added autoloader

* Sun Dec 28 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.3-1
- Updated to 1.2.3 (BZ #1176942)

* Sun Oct 19 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.1-1
- Updated to 1.2.1 (BZ #1146910)
- %%license usage

* Mon Sep 29 2014 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- update to 1.2.1

* Thu Jul 17 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.0-2
- Removed skipping of test (php-phpunit-PHPUnit-MockObject patched to fix issue)

* Tue Jul 15 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.0-1
- Updated to 1.2.0 (BZ #1116887)

* Fri Jun 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.2-5.20131220gita11349d
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide
- Added option to build without tests ("--without tests")
- Updated dependencies to use php-composer virtual provides

* Sat Jan 11 2014 Remi Collet <rpms@famillecollet.com> 1.1.2-3.20131220gita11349d
- backport for remi repo

* Mon Jan 06 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.2-3.20131220gita11349d
- Minor syntax changes

* Fri Jan 03 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.2-2.20131220gita11349d
- Conditional %%{?dist}
- Added conflict w/ PEAR-based DoctrineCommon pkg (version < 2.4)

* Mon Dec 23 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.2-1.20131220gita11349d
- Initial package
