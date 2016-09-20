# remirepo spec file for php-sqlsrv
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package             php-sqlsrv}

%global gh_commit   4ccffbbe077e87288bf00cc6327142579da46775
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    Microsoft
%global gh_project  msphpsql

%global extname       sqlsrv
%global with_zts      0%{!?_without_zts:%{?__ztsphp:1}}
# After 20-pdo.ini
%global ininame       40-%{extname}.ini

Name:          %{?scl_prefix}php-sqlsrv
Summary:       Microsoft Drivers for PHP for SQL Server
Version:       4.0.4
Release:       5%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:       MIT
Group:         Development/Languages

URL:           https://github.com/Microsoft/msphpsql
Source0:       https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# https://github.com/Microsoft/msphpsql/pull/153 - build
Patch0:        %{extname}-pr153.patch
# https://github.com/Microsoft/msphpsql/pull/154 - odbcver
Patch1:        %{extname}-pr154.patch
# https://github.com/Microsoft/msphpsql/pull/155 - PHP 7.1
Patch2:        %{extname}-pr155.patch
# https://github.com/Microsoft/msphpsql/pull/157 - buffer overflow
Patch3:        %{extname}-pr157.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: %{?scl_prefix}php-devel > 7
BuildRequires: %{?scl_prefix}php-pdo
BuildRequires: msodbcsql-devel >= 13
BuildRequires: unixODBC-devel >= 2.3.1

Requires:      msodbcsql-libs%{?_isa} >= 13
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
%setup -qc
cd %{gh_project}-%{gh_commit}
%patch0 -p1 -b .pr153
%patch1 -p1 -b .pr154
%patch2 -p1 -b .pr155
%patch3 -p1 -b .pr157
cd ..

mv %{gh_project}-%{gh_commit}/source NTS

cd NTS
sed -e '/VER_FILEVERSION_STR/s/4.0.0.0/%{version}/' \
    -i sqlsrv/version.h pdo_sqlsrv/version.h

# Sanity check, really often broken
extver=$(sed -n '/#define VER_FILEVERSION_STR/{s/.* "//;s/".*$//;p}' sqlsrv/version.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
extver=$(sed -n '/#define VER_FILEVERSION_STR/{s/.* "//;s/".*$//;p}' pdo_sqlsrv/version.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
cd ..

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

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif


%build
: =================== sqlsrv NTS ===================
cd NTS/%{extname}
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config \
    --enable-sqlsrv
make %{?_smp_mflags}

: =================== pdo_sqlsrv NTS ===================
cd ../../NTS/pdo_%{extname}
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config \
    --with-pdo_sqlsrv
make %{?_smp_mflags}

%if %{with_zts}
: =================== sqlsrv ZTS ===================
cd ../../ZTS/%{extname}
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config \
    --enable-sqlsrv
make %{?_smp_mflags}

: =================== pdo_sqlsrv ZTS ===================
cd ../../ZTS/pdo_%{extname}
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config \
    --with-pdo_sqlsrv
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}
ver=$(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')

make -C NTS/%{extname}     install INSTALL_ROOT=%{buildroot}
make -C NTS/pdo_%{extname} install INSTALL_ROOT=%{buildroot}
install -D  -m 644 %{ininame} %{buildroot}%{php_inidir}/%{ininame}

%if %{with_zts}
make -C ZTS/%{extname}     install INSTALL_ROOT=%{buildroot}
make -C ZTS/pdo_%{extname} install INSTALL_ROOT=%{buildroot}
install -D  -m 644 %{ininame} %{buildroot}%{php_ztsinidir}/%{ininame}
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
%license %{gh_project}-%{gh_commit}/LICENSE

%config(noreplace) %{php_inidir}/%{ininame}
%{php_extdir}/%{extname}.so
%{php_extdir}/pdo_%{extname}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ininame}
%{php_ztsextdir}/%{extname}.so
%{php_ztsextdir}/pdo_%{extname}.so
%endif


%changelog
* Tue Sep 20 2016 Remi Collet <remi@remirepo.net> - 4.0.4-5
- use the splitted msodbcsql packages

* Mon Sep 19 2016 Remi Collet <remi@remirepo.net> - 4.0.4-4
- fix reported version
- open https://github.com/Microsoft/msphpsql/pull/157 - buffer overflow

* Fri Sep 16 2016 Remi Collet <remi@remirepo.net> - 4.0.4-2
- build from sources
- open https://github.com/Microsoft/msphpsql/pull/153 - build
- open https://github.com/Microsoft/msphpsql/pull/154 - odbcver
- open https://github.com/Microsoft/msphpsql/pull/155 - PHP 7.1

* Fri Sep 16 2016 Remi Collet <remi@remirepo.net> - 4.0.4-1
- initial package

