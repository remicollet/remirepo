# remirepo spec file for php-sqlsrv
#
# Copyright (c) 2016-2017 Remi Collet
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
%global from_pecl   1

%global extname       sqlsrv
%global with_zts      0%{!?_without_zts:%{?__ztsphp:1}}
# After 20-pdo.ini
%global ininame       40-%{extname}.ini

Name:          %{?scl_prefix}php-sqlsrv
Summary:       Microsoft Drivers for PHP for SQL Server
Version:       4.1.6.1
Release:       1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:       MIT
Group:         Development/Languages

URL:           https://github.com/Microsoft/msphpsql
%if %{from_pecl}
Source0:       http://pecl.php.net/get/%{extname}-%{version}.tgz
Source1:       http://pecl.php.net/get/pdo_%{extname}-%{version}.tgz
%else
Source0:       https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz
%endif

BuildRequires: %{?scl_prefix}php-devel > 7
BuildRequires: %{?scl_prefix}php-pdo
BuildRequires: %{?scl_prefix}php-pear
BuildRequires: msodbcsql-devel >= 13
BuildRequires: unixODBC-devel >= 2.3.1

Requires:      msodbcsql-libs%{?_isa} >= 13
# ABI check
Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api)      = %{php_core_api}
Requires:      %{?scl_prefix}php(pdo-abi)  = %{php_pdo_api}
Requires:      %{?scl_prefix}php-pdo%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:      %{?scl_prefix}php-pdo_%{extname}              = %{version}
Provides:      %{?scl_prefix}php-pdo_%{extname}%{_isa}       = %{version}
# Also available as pecl packages
Provides:      %{?scl_prefix}php-pecl(%{extname})            = %{version}
Provides:      %{?scl_prefix}php-pecl(%{extname})%{_isa}     = %{version}
Provides:      %{?scl_prefix}php-pecl(pdo_%{extname})        = %{version}
Provides:      %{?scl_prefix}php-pecl(pdo_%{extname})%{_isa} = %{version}


%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
Obsoletes:     php70u-sqlsrv <= %{version}
Obsoletes:     php70w-sqlsrv <= %{version}
%if "%{php_version}" > "7.1"
Obsoletes:     php71u-sqlsrv <= %{version}
Obsoletes:     php71w-sqlsrv <= %{version}
%endif
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
%if %{from_pecl}
%setup -qcT
mkdir NTS

tar xf %{SOURCE0}
mv %{extname}-%{version}/LICENSE .
mv %{extname}-%{version} NTS/%{extname}
mv package.xml NTS/%{extname}

tar xf %{SOURCE1}
mv pdo_%{extname}-%{version} NTS/pdo_%{extname}
mv package.xml NTS/pdo_%{extname}
%else
%setup -qc
mv %{gh_project}-%{gh_commit}/source NTS
mv %{gh_project}-%{gh_commit}/LICENSE .
%endif

cd NTS
# Sanity check, really often broken
extmaj=$(sed -n '/#define SQLVERSION_MAJOR/{s/.*MAJOR //;s/\r//;p}' sqlsrv/shared/version.h)
extmin=$(sed -n '/#define SQLVERSION_MINOR/{s/.*MINOR //;s/\r//;p}' sqlsrv/shared/version.h)
extrel=$(sed -n '/#define SQLVERSION_RELEASE/{s/.*ASE //;s/\r//;p}' sqlsrv/shared/version.h)
extbld=$(sed -n '/#define SQLVERSION_BUILD/{s/.*BUILD //;s/\r//;p}' sqlsrv/shared/version.h)
extver=${extmaj}.${extmin}.${extrel}.${extbld}
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
%{?dtsenable}

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
%{?dtsenable}

install -Dpm 644 NTS/%{extname}/package.xml %{buildroot}%{pecl_xmldir}/php-pecl-%{extname}.xml
install -Dpm 644 NTS/pdo_%{extname}/package.xml %{buildroot}%{pecl_xmldir}/php-pecl-pdo-%{extname}.xml

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


%if 0%{?fedora} < 24
# when pear installed alone, after us
%triggerin -- %{?scl_prefix}php-pear
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/php-pecl-%{extname}.xml     >/dev/null || :
    %{pecl_install} %{pecl_xmldir}/php-pecl-pdo-%{extname}.xml >/dev/null || :
fi

# posttrans as pear can be installed after us
%posttrans
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/php-pecl-%{extname}.xml     >/dev/null || :
    %{pecl_install} %{pecl_xmldir}/php-pecl-pdo-%{extname}.xml >/dev/null || :
fi

%postun
if [ $1 -eq 0 -a -x %{__pecl} ] ; then
    %{pecl_uninstall} %{extname}     >/dev/null || :
    %{pecl_uninstall} pdo_%{extname} >/dev/null || :
fi
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{pecl_xmldir}/php-pecl-%{extname}.xml
%{pecl_xmldir}/php-pecl-pdo-%{extname}.xml

%config(noreplace) %{php_inidir}/%{ininame}
%{php_extdir}/%{extname}.so
%{php_extdir}/pdo_%{extname}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ininame}
%{php_ztsextdir}/%{extname}.so
%{php_ztsextdir}/pdo_%{extname}.so
%endif


%changelog
* Thu Feb  9 2017 Remi Collet <remi@remirepo.net> - 4.1.6.1-1
- update to 4.1.6.1 (devel)

* Sat Feb  4 2017 Remi Collet <remi@remirepo.net> - 4.1.6-1
- update to 4.1.6 (devel)

* Tue Dec 20 2016 Remi Collet <remi@remirepo.net> - 4.0.8-1
- update to 4.0.8 (stable)

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 4.0.7-2
- rebuild with PHP 7.1.0 GA

* Fri Nov 18 2016 Remi Collet <remi@remirepo.net> - 4.0.7-1
- update to 4.0.7 (devel)

* Sat Oct 22 2016 Remi Collet <remi@remirepo.net> - 4.0.6-1
- update to 4.0.6 (devel)

* Sat Oct  1 2016 Remi Collet <remi@remirepo.net> - 4.0.5-1
- update to 4.0.5, sources from PECL
- drop all patches merged upstream
- open https://github.com/Microsoft/msphpsql/issues/164

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

