# remirepo spec file for php-pimple, from:
# adapted for SCL
#
# Fedora spec file for php-pimple
#
# Copyright (c) 2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     silexphp
%global github_name      Pimple
%global github_version   3.0.2
%global github_commit    a30f7d6e57565a2e1a316e1baf2a483f788b258a

# Lib
%global composer_vendor  pimple
%global composer_project pimple

# Ext
%global ext_name pimple
%global with_zts 0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
%global ini_name %{ext_name}.ini
%else
%global ini_name 40-%{ext_name}.ini
%endif

# "php": ">=5.3.0"
%global php_min_ver 5.3.0

%if 0%{?scl:1}
# No need for noarch package in SCL (base package can be used)
%global with_lib   0
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
%else
%global with_lib   1
%endif

# Build using "--without tests" to disable tests
%global with_tests  %{?_without_tests:0}%{!?_without_tests:1}

%{?scl:          %scl_package        php-pimple}
%{!?scl:         %global pkg_name    %{name}}
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?phpdir:      %global phpdir      %{_datadir}/php}
%{!?__php:       %global __php       %{_bindir}/php}

Name:          %{?sub_prefix}php-%{composer_project}
Version:       %{github_version}
Release:       1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Summary:       A simple dependency injection container for PHP (extension)

Group:         Development/Libraries
License:       MIT
URL:           http://pimple.sensiolabs.org
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{pkg_name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{?scl_prefix}php-devel >= %{php_min_ver}
%if %{with_tests} && %{with_lib}
# For tests
## composer.json
BuildRequires: %{_bindir}/phpunit
## phpcompatinfo (computed from version 3.0.2)
BuildRequires: %{?scl_prefix}php-reflection
BuildRequires: %{?scl_prefix}php-spl
%endif

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api)      = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
%{summary}.

NOTE: This package installs the Pimple EXTENSION.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


# ------------------------------------------------------------------------------

%if %{with_lib}
%package lib

Summary:   A simple dependency injection container for PHP (library)
Group:     Development/Libraries

%if 0%{?rhel} != 5
BuildArch: noarch
%endif

# composer.json
Requires:  php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 3.0.2)
Requires:  php-spl

# Composer
Provides:  php-composer(%{composer_vendor}/%{composer_project}) = %{version}
# Rename
Obsoletes: php-Pimple < %{version}-%{release}
Provides:  php-Pimple = %{version}-%{release}

%description lib
%{summary}.

NOTE: This package installs the Pimple LIBRARY. If you would like the EXTENSION
for improved speed, install "%{name}".
%endif

# ------------------------------------------------------------------------------

%prep
%setup -qn %{github_name}-%{github_commit}

%if %{with_lib}
: Library: Create autoloader
cat <<'AUTOLOAD' | tee src/Pimple/autoload.php
<?php
/**
 * Autoloader for %{name}-lib and its' dependencies
 *
 * Created by %{name}-lib-%{version}-%{release}
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

$fedoraClassLoader->addPrefix('Pimple\\', dirname(__DIR__));

return $fedoraClassLoader;
AUTOLOAD
%endif

: Extension: NTS
mv ext/%{ext_name} ext/NTS
%if %{with_zts}
: Extension: ZTS
cp -pr ext/NTS ext/ZTS
%endif

: Extension: Create configuration file
cat << 'INI' | tee %{ini_name}
; Enable %{ext_name} extension
extension=%{ext_name}.so
INI


%build
: Extension: NTS
pushd ext/NTS
    %{_bindir}/phpize
    %configure --with-php-config=%{_bindir}/php-config
    make %{?_smp_mflags}
popd
%if %{with_zts}
: Extension: ZTS
pushd ext/ZTS
    %{_bindir}/zts-phpize
    %configure --with-php-config=%{_bindir}/zts-php-config
    make %{?_smp_mflags}
popd
%endif


%install
rm -rf %{buildroot}

%if %{with_lib}
: Library
mkdir -p %{buildroot}/%{phpdir}/
cp -rp src/* %{buildroot}/%{phpdir}/
%endif

: Extension: NTS
make -C ext/NTS install INSTALL_ROOT=%{buildroot}
install -D -m 0644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}
%if %{with_zts}
: Extension: ZTS
make -C ext/ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 0644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif


%check
: Extension: NTS minimal load test
%{__php} --no-php-ini \
    --define extension=ext/NTS/modules/%{ext_name}.so \
    --modules | grep %{ext_name}

%if %{with_zts}
: Extension: ZTS minimal load test
%{__ztsphp} --no-php-ini \
    --define extension=ext/ZTS/modules/%{ext_name}.so \
    --modules | grep %{ext_name}
%endif

%if %{with_tests}
%if %{with_lib}
: Library: Test suite without extension
%{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}/%{phpdir}/Pimple/autoload.php

: Library: Test suite with extension
%{_bindir}/php --define extension=ext/NTS/modules/%{ext_name}.so \
    %{_bindir}/phpunit --verbose \
        --bootstrap %{buildroot}/%{phpdir}/Pimple/autoload.php
%endif

: Extension: NTS test suite
pushd ext/NTS
    make test NO_INTERACTION=1 REPORT_EXIT_STATUS=1
popd

%if %{with_zts}
: Extension: ZTS test suite
pushd ext/ZTS
    make test NO_INTERACTION=1 REPORT_EXIT_STATUS=1
popd
%endif
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%{!?_licensedir:%global license %%doc}

%files
%defattr(-,root,root,-)
%license LICENSE
%doc CHANGELOG
%doc README.rst
# NTS
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{ext_name}.so
# ZTS
%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{ext_name}.so
%endif

%if %{with_lib}
%files lib
%defattr(-,root,root,-)
%license LICENSE
%doc CHANGELOG
%doc README.rst
%doc composer.json
%{phpdir}/Pimple
%exclude %{phpdir}/Pimple/Tests
%endif


%changelog
* Sat Sep 12 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.0.2-1
- Updated to 3.0.2 (RHBZ #1262507)

* Wed Aug  5 2015 Remi Collet <remi@remirepo.net> - 3.0.1-1
- backport for #remirepo
- adapt for SCL
- drop library subpackage in SCL

* Sun Aug 02 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.0.1-1
- Updated to 3.0.1

* Mon Jul 20 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.0.0-5
- Autoloader changed to Symfony ClassLoader

* Thu May 21 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.0.0-4
- Add library autoloader
- Spec cleanup

* Wed Sep 03 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.0.0-3
- Separate extension and library (i.e. sub-package library)

* Mon Aug 25 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.0.0-2
- Fixed compat file location in description
- Included real class in compat file
- Always run extension minimal load test
- Fixed test suite with previous installed version
- "make test NO_INTERACTION=1 REPORT_EXIT_STATUS=1" instead of "echo "n" | make test"

* Thu Jul 31 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.0.0-1
- Updated to 3.0.0
- Added custom compat file for obsoleted php-Pimple

* Tue Jul 29 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.1.1-1
- Initial package
