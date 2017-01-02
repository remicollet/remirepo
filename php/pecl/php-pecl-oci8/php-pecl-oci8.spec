# remirepo spec file for php-pecl-oci8
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package         php-pecl-oci8}
%{!?scl:         %global _root_libdir %{_libdir}}

%global with_zts  0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name oci8
%global with_tests 0%{?_with_tests:1}
%if "%{php_version}" < "5.6"
%global ini_name  %{pecl_name}.ini
%else
%global ini_name  40-%{pecl_name}.ini
%endif
%global oraclever 12.1
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
%global with_dtrace 1
%else
%global with_dtrace 0
%endif


Summary:        Extension for Oracle Database
Name:           %{?scl_prefix}php-pecl-%{pecl_name}
Version:        2.0.12
Release:        1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}

License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# Fix header/library detection
Patch0:         %{pecl_name}-2.0.8-conf.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel > 5.2
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  oracle-instantclient-devel >= %{oraclever}
%if %{with_dtrace}
BuildRequires:  systemtap-sdt-devel
%endif

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
# Should requires libclntsh.so.12.1 but it's not provided by Oracle RPM.
AutoReq:        0

Conflicts:      %{?scl_prefix}php-%{pecl_name}               < %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
Obsoletes:      php53-pecl-%{pecl_name} <= %{version}
Obsoletes:     php53u-pecl-%{pecl_name} <= %{version}
Obsoletes:      php54-pecl-%{pecl_name} <= %{version}
Obsoletes:     php54w-pecl-%{pecl_name} <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Use the OCI8 extension to access Oracle Database.

The extension is linked with Oracle client libraries %{oraclever}
(Oracle Instant Client).  For details, see Oracle's note
"Oracle Client / Server Interoperability Support" (ID 207303.1).

You must install libclntsh.so.%{oraclever} to use this package, provided
in the database installation, or in the free Oracle Instant Client
available from Oracle.

Notice:
- %{?scl_prefix}php-oci8 provides oci8 and pdo_oci extensions from php sources.
- %name only provides oci8 extension.

Documentation is at http://php.net/oci8

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -qc
mv %{pecl_name}-%{version} NTS

# don't install tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS
%patch0 -p0 -b .remi

# Check reported version (phpinfo), as this is often broken
extver=$(sed -n '/#define PHP_OCI8_VERSION/{s/.* "//;s/".*$//;p}' php_oci8.h)
if test "x${extver}" != "x%{version}%{?versuffix}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

# Drop in the bit of configuration
cat > %{ini_name} << 'EOF'
; Enable %{summary}
extension = %{pecl_name}.so

; Connection: Enables privileged connections using external
; credentials (OCI_SYSOPER, OCI_SYSDBA)
; http://php.net/oci8.privileged-connect
;oci8.privileged_connect = Off

; Connection: The maximum number of persistent OCI8 connections per
; process. Using -1 means no limit.
; http://php.net/oci8.max-persistent
;oci8.max_persistent = -1

; Connection: The maximum number of seconds a process is allowed to
; maintain an idle persistent connection. Using -1 means idle
; persistent connections will be maintained forever.
; http://php.net/oci8.persistent-timeout
;oci8.persistent_timeout = -1

; Connection: The number of seconds that must pass before issuing a
; ping during oci_pconnect() to check the connection validity. When
; set to 0, each oci_pconnect() will cause a ping. Using -1 disables
; pings completely.
; http://php.net/oci8.ping-interval
;oci8.ping_interval = 60

; Connection: Set this to a user chosen connection class to be used
; for all pooled server requests with Oracle 11g Database Resident
; Connection Pooling (DRCP).  To use DRCP, this value should be set to
; the same string for all web servers running the same application,
; the database pool must be configured, and the connection string must
; specify to use a pooled server.
;oci8.connection_class =

; High Availability: Using On lets PHP receive Fast Application
; Notification (FAN) events generated when a database node fails. The
; database must also be configured to post FAN events.
;oci8.events = Off

; Tuning: This option enables statement caching, and specifies how
; many statements to cache. Using 0 disables statement caching.
; http://php.net/oci8.statement-cache-size
;oci8.statement_cache_size = 20

; Tuning: Enables statement prefetching and sets the default number of
; rows that will be fetched automatically after statement execution.
; http://php.net/oci8.default-prefetch
;oci8.default_prefetch = 100

; Compatibility. Using On means oci_close() will not close
; oci_connect() and oci_new_connect() connections.
; http://php.net/oci8.old-oci-close-semantics
;oci8.old_oci_close_semantics = Off
EOF


%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif


%build
%if %{with_dtrace}
%if "%{php_version}" > "5.5"
export PHP_DTRACE=yes
%endif
%endif

peclconf() {
%configure \
%ifarch x86_64
    --with-oci8=shared,instantclient,%{_root_libdir}/oracle/%{oraclever}/client64/lib,%{oraclever} \
%else
    --with-oci8=shared,instantclient,%{_root_libdir}/oracle/%{oraclever}/client/lib,%{oraclever} \
%endif
    --with-php-config=$1
}

cd NTS
%{_bindir}/phpize
peclconf %{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
peclconf %{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}
# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Install the ZTS stuff
%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd NTS

: Minimal load test for NTS extension
%{_bindir}/php --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_tests}
exprt NO_INTERACTION=1
: Upstream test suite for NTS extension
make test
%else
: Upstream test suite disabled
%endif

%if %{with_zts}
cd ../ZTS

: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_tests}
: Upstream test suite for ZTS extension
make test
%else
: Upstream test suite disabled
%endif
%endif


%if 0%{?fedora} < 24
# when pear installed alone, after us
%triggerin -- %{?scl_prefix}php-pear
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

# posttrans as pear can be installed after us
%posttrans
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

%postun
if [ $1 -eq 0 -a -x %{__pecl} ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%endif


%changelog
* Thu Sep 01 2016 Remi Collet <remi@fedoraproject.org> - 2.0.12-1
- Update to 2.0.12

* Mon Apr 18 2016 Remi Collet <remi@fedoraproject.org> - 2.0.11-1
- Update to 2.0.11

* Thu Mar 10 2016 Remi Collet <remi@fedoraproject.org> - 2.0.10-2
- adapt for F24
- fix license management

* Sat Dec 12 2015 Remi Collet <remi@fedoraproject.org> - 2.0.10-1
- Update to 2.0.10
- drop runtime dependency on pear, new scriptlets

* Mon Sep  1 2014 Remi Collet <remi@fedoraproject.org> - 2.0.8-2
- fix SCL build

* Fri Aug  1 2014 Remi Collet <remi@fedoraproject.org> - 2.0.8-1
- initial package, version 2.0.8
