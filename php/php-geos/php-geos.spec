# remirepo spec file for php-geos
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package         php-geos
%else
%global pkg_name     php-geos
%endif

%global prever     rc2

%global pecl_name  geos
%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%if "%{php_version}" < "5.6"
%global ini_name   %{pecl_name}.ini
%else
%global ini_name   40-%{pecl_name}.ini
%endif
%global with_tests 0%{!?_without_tests:1}

Name:           %{?sub_prefix}php-%{pecl_name}
Version:        1.0.0
Release:        0.2.%{prever}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}

Summary:        PHP module for GEOS

Group:          Development/Languages
# See COPYING
License:        LGPLv2+ and MIT
URL:            http://trac.osgeo.org/geos
Source0:        https://git.osgeo.org/gogs/geos/php-geos/archive/%{version}%{prever}.tar.gz

BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-pear
# Test failures with 3.3 (EL-6)
BuildRequires:  geos-devel >= 3.4

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}-%{release}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}-%{release}
%endif
# Dropped from geos
Obsoletes:      %{?scl_prefix}geos-php        <= 3.5.0
Provides:       %{?scl_prefix}geos-php         = 1:%{version}-%{release}
Provides:       %{?scl_prefix}geos-php%{?_isa} = 1:%{version}-%{release}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
Obsoletes:     php54-%{pecl_name}       <= %{version}
Obsoletes:     php54w-%{pecl_name}      <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-%{pecl_name}      <= %{version}
Obsoletes:     php55w-%{pecl_name}      <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-%{pecl_name}      <= %{version}
Obsoletes:     php56w-%{pecl_name}      <= %{version}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-%{pecl_name}      <= %{version}
Obsoletes:     php70w-%{pecl_name}      <= %{version}
%endif
%if "%{php_version}" > "7.1"
Obsoletes:     php71u-%{pecl_name}      <= %{version}
Obsoletes:     php71w-%{pecl_name}      <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
PHP module for GEOS.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
mv %{pkg_name} NTS

cd NTS
sed -e '/PHP_GEOS_VERSION/s/"0.0"/"%{version}%{?prever}"/' -i php_geos.h

# Check extension version
ver=$(sed -n '/define PHP_GEOS_VERSION/{s/.* "//;s/".*$//;p}' php_geos.h)
if test "$ver" != "%{version}%{?prever}%{?gh_date:-dev}"; then
   : Error: Upstream VERSION version is ${ver}, expecting %{version}%{?prever}%{?gh_date:-dev}.
   exit 1
fi
cd ..

cat  << 'EOF' | tee %{ini_name}
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF


%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
make -C NTS install INSTALL_ROOT=%{buildroot}

# install configuration
install -Dpm 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif


%check
# https://git.osgeo.org/gogs/geos/php-geos/pulls/13
: Fix test for old PHP versions
sed -e 's/GEOSWKTWriter::class/"GEOSWKTWriter"/'  \
    -e 's/GEOSGeometry::class/"GEOSGeometry"/' \
    -i ?TS/tests/*phpt

: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for NTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif

%if %{with_tests}
cd NTS
: Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff || ret=1

%if %{with_zts}
cd ../ZTS
: Upstream test suite for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff || ret=1
%endif

exit $ret
%endif


%files
%{!?_licensedir:%global license %%doc}
%license NTS/{COPYING,LGPL-2,MIT-LICENSE}
%doc NTS/{CREDITS,NEWS,README.md,TODO}

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Mon Dec 12 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.rc2
- update to 1.0.0-rc2
- open https://git.osgeo.org/gogs/geos/php-geos/pulls/13 - fix for tests

* Sun Dec 11 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.rc1
- Initial packaging of 1.0.0rc1

