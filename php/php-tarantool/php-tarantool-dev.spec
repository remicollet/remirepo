# remirepo spec file for php-tarantool
#
# Copyright (c) 2016 Remi Collet
#
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please preserve changelog entries
#

%if 0%{?scl:1}
# PHPUnit not available in SCL
%if "%{scl}" == "rh-php56"
%global sub_prefix  more-php56-
%else
%global sub_prefix  %{scl_prefix}
%endif
%scl_package        php-%{ext_name}

%else
%global pkg_name    %{name}
%endif

%global github_owner     tarantool
%global github_name      tarantool-php
%global github_version   0.2.0

%global ext_name         tarantool
%global with_zts         0%{!?_without_zts:%{?__ztsphp:1}}
%global ini_name         40-%{ext_name}.ini

# Test suite requires a running server
%global with_tests 0

Name:          %{?sub_prefix}php-%{ext_name}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       PHP driver for Tarantool/Box

Group:         Development/Libraries
# see https://github.com/tarantool/tarantool-php/issues/77
License:       BSD
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_version}.tar.gz

BuildRequires: %{?scl_prefix}php-devel >= 7
%if %{with_tests}
# For tests
BuildRequires: %{_bindir}/phpunit
%endif

%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:      %{?scl_prefix}php-%{ext_name}         = %{version}-%{release}
Provides:      %{?scl_prefix}php-%{ext_name}%{?_isa} = %{version}-%{release}
%endif
## PECL compatibility
Provides:      %{?scl_prefix}php-pecl(tarantool.github.io/tarantool-php/pecl/Tarantool)         = %{version}
Provides:      %{?scl_prefix}php-pecl(tarantool.github.io/tarantool-php/pecl/Tarantool)%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:      php53-%{ext_name} <= %{version}
Obsoletes:     php53u-%{ext_name} <= %{version}
Obsoletes:      php54-%{ext_name} <= %{version}
Obsoletes:     php54w-%{ext_name} <= %{version}
Obsoletes:     php55u-%{ext_name} <= %{version}
Obsoletes:     php55w-%{ext_name} <= %{version}
Obsoletes:     php56u-%{ext_name} <= %{version}
Obsoletes:     php56w-%{ext_name} <= %{version}
Obsoletes:     php70u-%{ext_name} <= %{version}
Obsoletes:     php70w-%{ext_name} <= %{version}
%if "%{php_version}" > "7.1"
Obsoletes:     php71u-%{ext_name} <= %{version}
Obsoletes:     php71w-%{ext_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
%{summary}.

Tarantool is an in-memory database and Lua application server.
This package provides PECL PHP driver for Tarantool/Box.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -qc 
mv %{github_name}-%{github_version} NTS

%if %{with_zts}
cp -pr NTS ZTS
%endif

: Ext -- Create configuration file
cat > %{ini_name} << 'INI'
; Enable tarantool extension module
extension=%{ext_name}.so

; ----- Configuration options
;tarantool.persistent = 0
;tarantool.use_namespace = 0
;tarantool.connection_alias = 0
;tarantool.timeout = '10.0'
;tarantool.request_timeout = '10.0'
;tarantool.retry_count = '1'
;tarantool.retry_sleep = '0.1'
INI


%build
: Ext -- NTS
pushd NTS
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}
popd

: Ext -- ZTS
%if %{with_zts}
pushd ZTS
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
popd
%endif


%install
: Ext -- NTS
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 0644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

: Ext -- ZTS
%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 0644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif


%check
: Extension NTS minimal load test
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{ext_name}.so \
    --modules | grep %{ext_name}

%if %{with_zts}
: Extension ZTS minimal load test
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{ext_name}.so \
    --modules | grep %{ext_name}
%endif


%files
%{!?_licensedir:%global license %%doc}
%license NTS/LICENSE NTS/AUTHORS

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{ext_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{ext_name}.so
%endif


%changelog
* Tue Nov 22 2016 Eugine Blikh <bigbes@tarantool.org> - 0.2.0-1
- provide next release 0.2.0

* Thu Mar 24 2016 Remi Collet <remi@fedoraproject.org> - 0.1.1-0.1.20160906git27697cf
- update to git snapshot for PHP 7

* Thu Mar 24 2016 Remi Collet <remi@fedoraproject.org> - 0.1.0-1
- Initial package

