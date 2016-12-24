# Fedora spec file for php-geos
# Without SCL compatibility stuff, from:
#
# remirepo spec file for php-geos
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global pecl_name  geos
%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%global ini_name   40-%{pecl_name}.ini
%global with_tests 0%{!?_without_tests:1}

Name:           php-%{pecl_name}
Version:        1.0.0
Release:        1%{?dist}

Summary:        PHP module for GEOS

Group:          Development/Languages
# See COPYING
License:        LGPLv2+ and MIT
URL:            http://trac.osgeo.org/geos
Source0:        https://git.osgeo.org/gogs/geos/php-geos/archive/%{version}%{?prever}.tar.gz

BuildRequires:  php-devel
BuildRequires:  php-pear
# Test failures with 3.3 (EL-6)
BuildRequires:  geos-devel >= 3.4

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

# Dropped from geos
Obsoletes:      geos-php        <= 3.5.0
Provides:       geos-php         = 1:%{version}-%{release}
Provides:       geos-php%{?_isa} = 1:%{version}-%{release}


%description
PHP module for GEOS.


%prep
%setup -q -c
mv %{name} NTS

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
%license NTS/{COPYING,LGPL-2,MIT-LICENSE}
%doc NTS/{CREDITS,NEWS,README.md,TODO}

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Sat Dec 24 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- update to 1.0.0

* Fri Dec 16 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.4.rc3
- cleanup for Fedora review

* Fri Dec 16 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3.rc3
- update to 1.0.0-rc3

* Mon Dec 12 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.rc2
- update to 1.0.0-rc2
- open https://git.osgeo.org/gogs/geos/php-geos/pulls/13 - fix for tests

* Sun Dec 11 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.rc1
- Initial packaging of 1.0.0rc1

