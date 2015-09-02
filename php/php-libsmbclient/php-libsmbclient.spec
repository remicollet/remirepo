# remirepo spec file for php-libsmbclient
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
%endif

%global gh_commit  f33dd8c67254d0f0202f5e6212bc29ea35b055cf
%global gh_short   %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner   eduardok
%global gh_project libsmbclient-php
%{?scl:          %scl_package         php-libsmbclient}
%{!?scl:         %global pkg_name     %{name}}
%{!?php_inidir:  %global php_inidir   %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl       %{_bindir}/pecl}
%{!?__php:       %global __php        %{_bindir}/php}

%global ext_name   libsmbclient
%global with_zts   0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
%global ini_name   %{ext_name}.ini
%else
%global ini_name   40-%{ext_name}.ini
%endif
# Test suite requires a Samba server and configuration file
%global with_tests 0%{?_with_tests:1}

Name:           %{?sub_prefix}php-libsmbclient
Version:        0.6.1
Release:        1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
Summary:        PHP wrapper for libsmbclient

Group:          Development/Languages
# See https://github.com/eduardok/libsmbclient-php/issues/15 - switch to BSD
# See https://github.com/eduardok/libsmbclient-php/issues/19 - License file
License:        PHP
URL:            https://github.com/eduardok/libsmbclient-php
Source0:        %{pkg_name}-%{version}-%{gh_short}.tgz
# git snapshot as upstream doesn't provide test suite
Source1:        makesrc.sh
%if %{with_tests}
Source2:        %{gh_project}-phpunit.xml
%endif

Patch0:         %{gh_project}-upstream.patch
Patch1:         %{gh_project}-pr17.patch
Patch2:         %{gh_project}-pr18.patch

BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  libsmbclient-devel > 3.6
%if %{with_tests}
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  samba
%endif

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:     php53-%{ext_name}  <= %{version}
Obsoletes:     php53u-%{ext_name} <= %{version}
Obsoletes:     php54-%{ext_name}  <= %{version}
Obsoletes:     php54w-%{ext_name} <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-%{ext_name} <= %{version}
Obsoletes:     php55w-%{ext_name} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-%{ext_name} <= %{version}
Obsoletes:     php56w-%{ext_name} <= %{version}
%endif
%endif

# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
libsmbclient-php is a PHP extension that uses Samba's libsmbclient
library to provide Samba related functions to PHP programs.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl})}.


%prep
%setup -q -c
mv %{gh_project}-%{gh_commit} NTS

cd NTS
%patch0 -p1 -b .upstream
%patch1 -p1 -b .pr17
%patch2 -p1 -b .pr18

# Check extension version
ver=$(sed -n '/define LIBSMBCLIENT_VERSION/{s/.*\t"//;s/".*$//;p}' libsmbclient.c)
if test "$ver" != "%{version}"; then
   : Error: Upstream LIBSMBCLIENT_VERSION version is ${ver}, expecting %{version}.
   exit 1
fi
cd ..

cat  << 'EOF' | tee %{ini_name}
; Enable %{summary} extension module
extension=%{ext_name}.so
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
    --define extension=%{buildroot}%{php_extdir}/%{ext_name}.so \
    --modules | grep %{ext_name}

%if %{with_zts}
: Minimal load test for NTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{ext_name}.so \
    --modules | grep %{ext_name}
%endif

%if %{with_tests}
: Upstream test suite for NTS extension
cd NTS
cp %{SOURCE2} phpunit.xml

%{__php} \
    --define extension=%{buildroot}%{php_extdir}/%{ext_name}.so \
    %{_bindir}/phpunit --verbose
%endif


%files
#{!?_licensedir:%global license %%doc}
#license NTS/LICENSE
%doc NTS/README.md

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{ext_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{ext_name}.so
%endif


%changelog
* Wed Sep  2 2015 Remi Collet <rcollet@redhat.com> - 0.6.1-1
- Initial packaging of 0.6.1
- open https://github.com/eduardok/libsmbclient-php/pull/17
  test suite configuration
- open https://github.com/eduardok/libsmbclient-php/pull/18
  add reflection and improve phpinfo
- open https://github.com/eduardok/libsmbclient-php/issues/19
  missing license file