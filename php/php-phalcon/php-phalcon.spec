# spec file for php-phalcon
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package             php-phalcon}
%{!?scl:         %global pkg_name         %{name}}
%{!?__php:       %global __php            %{_bindir}/php}
%global gh_commit    33e85f551c253ddff58e594e2bace5c2e55f12ef
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     phalcon
%global gh_project   cphalcon
%global with_zts     0%{?__ztsphp:1}
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%global ext_name     phalcon
%if "%{php_version}" < "5.6"
# after pdo.ini, json.ini, igbinary.ini
%global ini_name  z-%{ext_name}.ini
%else
# after 40-json.ini, 20-pdo.ini, 40-igbinary.ini
%global ini_name  50-%{ext_name}.ini
%endif

Name:           %{?scl_prefix}php-phalcon
Version:        1.3.4
Release:        1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}.1
Summary:        Phalcon Framework

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{gh_project}-%{version}-strip.tar.bz2
# Script to generate the stripped archive
Source1:        strip.sh

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: %{?scl_prefix}php-devel > 5.3
BuildRequires: %{?scl_prefix}php-date
BuildRequires: %{?scl_prefix}php-hash
BuildRequires: %{?scl_prefix}php-json
BuildRequires: %{?scl_prefix}php-pdo
BuildRequires: %{?scl_prefix}php-session
BuildRequires: %{?scl_prefix}php-spl
BuildRequires: %{?scl_prefix}php-pecl-igbinary-devel

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
%if "%{php_version}" < "5.4"
# php 5.3.3 in EL-6 don't use arched virtual provides
# so only requires real packages instead
Requires:      %{?scl_prefix}php-common%{?_isa}
%else
Requires:      %{?scl_prefix}php-date%{?_isa}
Requires:      %{?scl_prefix}php-hash%{?_isa}
Requires:      %{?scl_prefix}php-json%{?_isa}
Requires:      %{?scl_prefix}php-session%{?_isa}
Requires:      %{?scl_prefix}php-spl%{?_isa}
%endif
Requires:      %{?scl_prefix}php-pdo%{?_isa}
Requires:      %{?scl_prefix}php-pecl(igbinary)%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

# Don't provides php-composer(phalcon/cphalcon), not registered on packagist

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%endif
%{?filter_setup}


%description
Phalcon is a web framework implemented as a C extension offering
high performance and lower resource consumption.

Notice: non-free JS and CSS minifiers are disabled.

Documentation: http://docs.phalconphp.com

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection}.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_PHALCON_VERSION/{s/.* "//;s/".*$//;p}' ext/php_phalcon.h)
if test "x${extver}" != "x%{version}%{?prever:-%{prever}}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever:-%{prever}}.
   exit 1
fi

# Create configuration file
cat << 'EOF' | tee %{ini_name}
; Enable '%{summary}' extension module
extension=%{ext_name}.so

; Configuration
;phalcon.orm.events=1
;phalcon.orm.virtual_foreign_keys=1
;phalcon.orm.column_renaming=1
;phalcon.orm.not_null_validations=1
;phalcon.orm.exception_on_failed_save=0
;phalcon.orm.enable_literals=1
;phalcon.db.escape_identifiers=1
;phalcon.register_psr3_classes=0
EOF


%build
peclconf() {
%configure \
  --without-non-free \
  --enable-phalcon \
  --with-libdir=%{_lib} \
  --with-php-config=$1
}

: Generate the SAFE sources
pushd build
%{__php} gen-build.php
popd

: Build SAFE extension, needed to regenerate sources
pushd build/safe
%{_bindir}/phpize
peclconf %{_bindir}/php-config
make %{?_smp_mflags}
popd

: Generate optimized sources
pushd build
%{__php} -d extension=safe/modules/phalcon.so gen-build.php
popd

# Use the optimized sources, is available
if [ -d build/%{?__isa_bits}bits ]; then
  mv build/%{__isa_bits}bits build/NTS
else
  mv build/safe build/NTS
fi

%if %{with_zts}
: Duplicate source tree for NTS / ZTS build
cp -r build/NTS build/ZTS
%endif

: Build NTS extension
cd build/NTS
%{_bindir}/phpize
peclconf %{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
: Build ZTS extension
cd ../ZTS
%{_bindir}/zts-phpize
peclconf %{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C build/NTS install INSTALL_ROOT=%{buildroot}

# install config file (z-http.ini to be loaded after json)
install -Dpm644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
make -C build/ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif


%check
# Shared needed extensions
modules=""
for mod in json hash pdo igbinary; do
  if [ -f %{php_extdir}/${mod}.so ]; then
    modules="$modules -d extension=${mod}.so"
  fi
done

: Minimal load test for NTS extension
%{__php} --no-php-ini \
    $modules \
    --define extension=%{buildroot}%{php_extdir}/%{ext_name}.so \
    --modules | grep -i %{ext_name}

%if %{with_tests}
: Upstream test suite NTS extension
cd build/NTS
SKIP_ONLINE_TESTS=1 \
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n $modules -d extension=$PWD/modules/%{ext_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff
%endif

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    $modules \
    --define extension=%{buildroot}%{php_ztsextdir}/%{ext_name}.so \
    --modules | grep -i %{ext_name}
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license docs/LICENSE.txt
%doc CHANGELOG
%doc CONTRIBUTING.md
%doc docs/DOCUMENTATION.txt

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{ext_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{ext_name}.so
%endif


%changelog
* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.3.4-1.1
- Fedora 21 SCL mass rebuild

* Sat Nov 15 2014 Remi Collet <remi@fedoraproject.org> - 1.3.4-1
- update to 1.3.4

* Mon Sep 29 2014 Remi Collet <remi@fedoraproject.org> - 1.3.3-1
- update to 1.3.3
- drop all patches merged upstream

* Sun Sep  7 2014 Remi Collet <remi@fedoraproject.org> - 1.3.2-2
- use striped archive, without non-free sources
- generate and use optimized sources
- open https://github.com/phalcon/cphalcon/pull/2793

* Thu Sep  4 2014 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- initial package, version 1.3.2
- open https://github.com/phalcon/cphalcon/pull/2772 (merged)
- open https://github.com/phalcon/cphalcon/pull/2774
- open https://github.com/phalcon/cphalcon/pull/2775