# remirepo spec file for php-patchwork-utf8, from:
#
# Fedora spec file for php-patchwork-utf8
#
# Copyright (c) 2015-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     tchwork
%global github_name      utf8
%global github_version   1.2.6
%global github_commit    f986d18f4e37ab70b792e977c7d85970cf84f164

%global composer_vendor  patchwork
%global composer_project utf8

# "php": ">=5.3.0"
%global php_min_ver 5.3.0

# Build using "--without tests" to disable tests
%if 0%{?rhel} == 5
%global with_tests 0%{?_with_tests:1}
%else
%global with_tests 0%{!?_without_tests:1}
%endif

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Portable and performant UTF-8, Unicode and Grapheme Clusters for PHP

Group:         Development/Libraries
License:       ASL 2.0 or GPLv2
URL:           https://github.com/%{github_owner}/%{github_name}

# GitHub export does not include tests.
# Run php-patchwork-utf8-get-source.sh to create full source.
Source0:       %{name}-%{github_version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

# fix for php 5.5.35/5.6.21/7.0.6
# https://github.com/tchwork/utf8/pull/59
# NOTE: Upstream patch modified for version 1.2
Patch0:        %{name}-pr59-modified-for-1-2.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Relative paths
BuildRequires: python
# Tests
%if %{with_tests}
BuildRequires: php-composer(phpunit/phpunit)
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-iconv
BuildRequires: php-intl
BuildRequires: php-mbstring
BuildRequires: php-pcre
## phpcompatinfo (computed from version 1.2.6)
BuildRequires: php-reflection
BuildRequires: php-date
BuildRequires: php-exif
BuildRequires: php-filter
BuildRequires: php-json
BuildRequires: php-spl
BuildRequires: php-xml
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-pcre
# composer.json: optional
Requires:      php-iconv
Requires:      php-intl
Requires:      php-mbstring
# phpcompatinfo (computed from version 1.2.6)
#Requires:      php-exif
Requires:      php-filter
Requires:      php-json
Requires:      php-spl
Requires:      php-xml
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.


%prep
%setup -qn %{github_name}-%{github_commit}

: fix for php 5.5.35/5.6.21/7.0.6
%patch0 -p 1

: Create autoloader
cat <<'AUTOLOAD' | tee src/Patchwork/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 *
 * Created by %{name}-%{version}-%{release}
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

$fedoraClassLoader->addPrefix('Patchwork\\', dirname(__DIR__));

\Patchwork\Utf8\Bootup::initAll();

return $fedoraClassLoader;
AUTOLOAD

: Remove Windows files
rm -f \
    src/Patchwork/Utf8/WindowsStreamWrapper.php \
    tests/Patchwork/Tests/Utf8/WindowsStreamWrapperTest.php


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}

: Library
mkdir -p %{buildroot}%{phpdir}
cp -rp src/Patchwork %{buildroot}%{phpdir}/

: Data
mkdir -p %{buildroot}%{_datadir}/%{name}
mv %{buildroot}%{phpdir}/Patchwork/Utf8/data %{buildroot}%{_datadir}/%{name}/
ln -s \
    %(python -c "import os.path; print os.path.relpath('%{_datadir}/%{name}/data', '%{phpdir}/Patchwork/Utf8')") \
    %{buildroot}%{phpdir}/Patchwork/Utf8/data
mv %{buildroot}%{phpdir}/Patchwork/PHP/Shim/charset %{buildroot}%{_datadir}/%{name}/shim-charset
ln -s \
    %(python -c "import os.path; print os.path.relpath('%{_datadir}/%{name}/shim-charset', '%{phpdir}/Patchwork/PHP/Shim')") \
    %{buildroot}%{phpdir}/Patchwork/PHP/Shim/charset
mv %{buildroot}%{phpdir}/Patchwork/PHP/Shim/unidata %{buildroot}%{_datadir}/%{name}/shim-unidata
ln -s \
    %(python -c "import os.path; print os.path.relpath('%{_datadir}/%{name}/shim-unidata', '%{phpdir}/Patchwork/PHP/Shim')") \
    %{buildroot}%{phpdir}/Patchwork/PHP/Shim/unidata

%check
%if %{with_tests}
%{_bindir}/phpunit --verbose --bootstrap %{buildroot}%{phpdir}/Patchwork/autoload.php

if which php70; then
   php70 %{_bindir}/phpunit --verbose --bootstrap %{buildroot}%{phpdir}/Patchwork/autoload.php
fi
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE*
%doc *.md
%doc composer.json
%{phpdir}/Patchwork
%exclude %{phpdir}/Patchwork/Utf8/Compiler.php
%exclude %{phpdir}/Patchwork/Utf8/unicode-data.tbz2
%{_datadir}/%{name}


%changelog
* Tue May 03 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.6-1
- Updated to 1.2.6
- Added patch "fix for php 5.5.35/5.6.21/7.0.6"

* Thu Oct 15 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.5-1
- Updated to 1.2.5 (RHBZ #1271631)
- Exclude Patchwork/Utf8/Compiler.php

* Thu Oct 15 2015 Remi Collet <remi]remirepo.net> - 1.2.5-1
- update to 1.2.5

* Wed Sep 23 2015 Remi Collet <remi]remirepo.net> - 1.2.3-3
- backport for remi repository

* Tue Sep 22 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.3-3
- Update patch for license files

* Sat Sep 19 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.3-2
- Add patch for license files

* Fri Sep 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.3-1
- Initial package
