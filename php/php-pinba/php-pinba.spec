# remirepo spec file for php-pinba
#
# Copyright (c) 2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package         php-pinba}

%global gh_commit   56d0ea04abdd995948d4a537d21caa8e55ae1006
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    tony2001
%global gh_project  pinba_extension
%global pecl_name   pinba
%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
%global ini_name    40-%{pecl_name}.ini

Summary:       Client extension for Pinba statistics server
Name:          %{?scl_prefix}php-pinba
Version:       1.1.0
%if 0%{?gh_date:1}
Release:       0.2.%{gh_date}git%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%else
Release:       1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%endif
License:       LGPLv2+
Group:         Development/Languages
URL:           https://github.com/%{gh_owner}/%{gh_project}
Source0:       https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRequires: %{?scl_prefix}php-devel > 7
BuildRequires: %{?scl_prefix}php-tokenizer

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
Obsoletes:     php70u-%{pecl_name} <= %{version}
Obsoletes:     php70w-%{pecl_name} <= %{version}
%if "%{php_version}" > "7.1"
Obsoletes:     php71u-%{pecl_name} <= %{version}
Obsoletes:     php71w-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Client extension for Pinba statistics server.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -qc
mv %{gh_project}-%{gh_commit} NTS

cd NTS
# Sanity check, really often broken
extver=$(sed -n '/#define PHP_PINBA_VERSION/{s/.* "//;s/".*$//;p}' php_pinba.h)
if test "x${extver}" != "x%{version}%{?gh_date:-dev}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?gh_date:-dev}.
   exit 1
fi
cd ..

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif

# Drop in the bit of configuration
cat << 'EOF' | tee %{ini_name}
; Enable '%{summary}' extension module
extension = %{pecl_name}.so

; Configuration
;pinba.server = ''
;pinba.enabled = 0
;pinba.auto_flush = 1
EOF


%build
%{?dtsenable}

cd NTS
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config \
    --enable-pinba
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config \
    --enable-pinba
make %{?_smp_mflags}
%endif


%install
%{?dtsenable}

# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
# Install the ZTS stuff
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif



%check
cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite  for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff || : ignore

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite  for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff
%endif


%files
%{!?_licensedir:%global license %%doc}
#license NTS/LICENSE
%doc NTS/{CREDITS,NEWS,README}

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Tue Jan 24 2017 Remi Collet <remi@remirepo.net> - 1.1.0-1
- new package, version 1.1.0

