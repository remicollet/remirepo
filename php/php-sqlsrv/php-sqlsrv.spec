# remirepo spec file for php-sqlsrv
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package             php-sqlsrv}

%global __arch_install_post  /bin/true
%global debug_package        %{nil}
%global __debug_install_post /bin/true

%global extname       sqlsrv
%global with_zts      0%{?__ztsphp:1}
# After 20-pdo.ini
%global ininame       40-%{extname}.ini

Name:          %{?scl_prefix}php-sqlsrv
Summary:       Microsoft Drivers for PHP for SQL Server
Version:       4.0.4
Release:       1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:       MIT
Group:         Development/Languages

URL:           https://github.com/Microsoft/msphpsql
Source0:       https://github.com/Microsoft/msphpsql/releases/download/%{version}-Linux/CentOS7.zip#/CentOS7-%{version}.zip
Source1:       https://github.com/Microsoft/msphpsql/blob/master/LICENSE

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: %{?scl_prefix}php-devel > 7
BuildRequires: %{?scl_prefix}php-pdo
BuildRequires: msodbcsql >= 13

Requires:      msodbcsql%{?_isa} >= 13
# ABI check
Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api)      = %{php_core_api}
Requires:      %{?scl_prefix}php(pdo-abi)  = %{php_pdo_api}
Requires:      %{?scl_prefix}php-pdo%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:      %{?scl_prefix}php-pdo_%{extname}        = %{version}
Provides:      %{?scl_prefix}php-pdo_%{extname}%{_isa} = %{version}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
Obsoletes:     php70u-sqlsrv <= %{version}
Obsoletes:     php70w-sqlsrv <= %{version}
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The Microsoft Drivers for PHP for SQL Server are PHP extensions that allow for
the reading and writing of SQL Server data from within PHP scripts.

The SQLSRV extension provides a procedural interface while the PDO_SQLSRV
extension implements PDO for accessing data in all editions of SQL Server
2005 and later (including Azure SQL DB).

These drivers rely on the Microsoft ODBC Driver for SQL Server to handle the
low-level communication with SQL Server.

Package built for PHP %(%{__php} -n -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -n CentOS7
cp %{SOURCE1} LICENSE

cat << 'EOF' | tee %{ininame}
; Enable '%{summary}' extension module
extension = %{extname}.so
extension = pdo_%{extname}.so

; Configuration

;sqlsrv.WarningsReturnAsErrors = 1
;sqlsrv.LogSeverity = 0
;sqlsrv.LogSubsystems = 0
;sqlsrv.ClientBufferMaxKBSize = 10240

;pdo_sqlsrv.log_severity = 0
;pdo_sqlsrv.client_buffer_max_kb_size = 10240
EOF


%build
: tarball provides binaries


%install
rm -rf %{buildroot}
ver=$(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')


install -D -pm 755 php_pdo_sqlsrv_7_nts.so %{buildroot}%{php_extdir}/pdo_%{extname}.so
install -D -pm 755 php_sqlsrv_7_nts.so     %{buildroot}%{php_extdir}/%{extname}.so
install -D  -m 644 %{ininame}              %{buildroot}%{php_inidir}/%{ininame}

%if %{with_zts}
install -D -pm 755 php_pdo_sqlsrv_7_ts.so  %{buildroot}%{php_ztsextdir}/pdo_%{extname}.so
install -D -pm 755 php_sqlsrv_7_ts.so      %{buildroot}%{php_ztsextdir}/%{extname}.so
install -D  -m 644 %{ininame}              %{buildroot}%{php_ztsinidir}/%{ininame}
%endif


%check
# simple module load test
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{extname}.so \
    --modules | grep %{extname}
%{__php} --no-php-ini \
    --define extension=pdo.so \
    --define extension=%{buildroot}%{php_extdir}/pdo_%{extname}.so \
    --modules | grep %{extname}

%if %{with_zts}
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{extname}.so \
    --modules | grep %{extname}
%{__ztsphp} --no-php-ini \
    --define extension=pdo.so \
    --define extension=%{buildroot}%{php_ztsextdir}/pdo_%{extname}.so \
    --modules | grep %{extname}
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE

%config(noreplace) %{php_inidir}/%{ininame}
%{php_extdir}/%{extname}.so
%{php_extdir}/pdo_%{extname}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ininame}
%{php_ztsextdir}/%{extname}.so
%{php_ztsextdir}/pdo_%{extname}.so
%endif


%changelog
* Fri Sep 16 2016 Remi Collet <remi@remirepo.net> - 4.0.4-1
- initial package

