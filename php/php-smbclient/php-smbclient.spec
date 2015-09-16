# remirepo spec file for php-smbclient
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

%global gh_commit  8b9587df1a0859074eae6133c5210451d6527e38
%global gh_short   %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner   eduardok
%global gh_project libsmbclient-php
%global gh_date    20150909
%global prever     -rc1

%{?scl:          %scl_package         php-smbclient}
%{!?scl:         %global pkg_name     %{name}}
%{!?php_inidir:  %global php_inidir   %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl       %{_bindir}/pecl}
%{!?__php:       %global __php        %{_bindir}/php}

%global ext_name   smbclient
%global with_zts   0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
%global ini_name   %{ext_name}.ini
%else
%global ini_name   40-%{ext_name}.ini
%endif
# Test suite requires a Samba server and configuration file
%global with_tests 0%{?_with_tests:1}

Name:           %{?sub_prefix}php-smbclient
Version:        0.8.0
Release:        0.2.rc1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Summary:        PHP wrapper for libsmbclient

Group:          Development/Languages
License:        BSD
URL:            https://github.com/eduardok/libsmbclient-php
Source0:        %{pkg_name}-%{version}-%{gh_short}.tgz
# git snapshot as upstream doesn't provide test suite
Source1:        makesrc.sh
%if %{with_tests}
Source2:        %{gh_project}-phpunit.xml
%endif

BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  libsmbclient-devel > 3.6
%if %{with_tests}
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  samba
%endif

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}
# Rename
Obsoletes:      %{?sub_prefix}php-libsmbclient         < 0.8.0-0.2
Provides:       %{?sub_prefix}php-libsmbclient         = %{version}-%{release}
Provides:       %{?sub_prefix}php-libsmbclient%{?_isa} = %{version}-%{release}

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
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-%{ext_name} <= %{version}
Obsoletes:     php70w-%{ext_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
%{ext_name} is a PHP extension that uses Samba's libsmbclient
library to provide Samba related functions to PHP programs.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{scl_vendor})}.


%prep
%setup -q -c
mv %{gh_project}-%{gh_commit} NTS

cd NTS
# Check extension version
ver=$(sed -n '/define PHP_SMBCLIENT_VERSION/{s/.* "//;s/".*$//;p}' php_smbclient.h)
if test "$ver" != "%{version}%{?prever}"; then
   : Error: Upstream VERSION version is ${ver}, expecting %{version}%{?prever}.
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
%{!?_licensedir:%global license %%doc}
%license NTS/LICENSE
%doc NTS/README.md

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{ext_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{ext_name}.so
%endif


%changelog
* Wed Sep 16 2015 Remi Collet <rcollet@redhat.com> - 0.8.0-0.2.rc1
- update to 0.8.0-rc1
- rename from php-libsmbclient to php-smbclient
- https://github.com/eduardok/libsmbclient-php/pull/26 rename

* Thu Sep  3 2015 Remi Collet <rcollet@redhat.com> - 0.8.0-0.1.20150909gita65127d
- update to 0.8.0-dev
- https://github.com/eduardok/libsmbclient-php/pull/20 streams support
- https://github.com/eduardok/libsmbclient-php/pull/23 PHP 7

* Thu Sep  3 2015 Remi Collet <rcollet@redhat.com> - 0.7.0-1
- Update to 0.7.0
- drop patches merged upstream
- license is now BSD

* Wed Sep  2 2015 Remi Collet <rcollet@redhat.com> - 0.6.1-1
- Initial packaging of 0.6.1
- open https://github.com/eduardok/libsmbclient-php/pull/17
  test suite configuration
- open https://github.com/eduardok/libsmbclient-php/pull/18
  add reflection and improve phpinfo
- open https://github.com/eduardok/libsmbclient-php/issues/19
  missing license file