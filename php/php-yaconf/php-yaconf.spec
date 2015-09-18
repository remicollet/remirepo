# remirepo spec file for php-yaconf
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package         php-yaconf}
%{!?php_inidir:  %global php_inidir   %{_sysconfdir}/php.d}
%{!?__php:       %global __php        %{_bindir}/php}

%global gh_commit   778424f5396321af728953e2d0fc960a98c6fa27
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    laruence
%global gh_project  yaconf
%global gh_date     20150718
%global ext_name    yaconf
%global with_zts    0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
%global ini_name  %{ext_name}.ini
%else
%global ini_name  40-%{ext_name}.ini
%endif

Summary:       Yet Another Configurations Container
Name:          %{?scl_prefix}php-yaconf
Version:       1.0.0
%if 0%{?gh_date:1}
Release:       0.6.%{gh_date}git%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%else
Release:       1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%endif
License:       PHP
Group:         Development/Languages
URL:           https://github.com/%{gh_owner}/%{gh_project}
Source0:       https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: %{?scl_prefix}php-devel > 7

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:     php53-%{gh_project}  <= %{version}
Obsoletes:     php53u-%{gh_project} <= %{version}
Obsoletes:     php54-%{gh_project}  <= %{version}
Obsoletes:     php54w-%{gh_project} <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-%{gh_project} <= %{version}
Obsoletes:     php55w-%{gh_project} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-%{gh_project} <= %{version}
Obsoletes:     php56w-%{gh_project} <= %{version}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-%{gh_project} <= %{version}
Obsoletes:     php70w-%{gh_project} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
A PHP Persistent Configurations Container.

This extension is still EXPERIMENTAL.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl})}.


%package devel
Summary:       %{name} developer files (header)
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{?scl_prefix}php-devel%{?_isa}

%description devel
These are the files needed to compile programs using %{name}.


%prep
%setup -qc
mv %{gh_project}-%{gh_commit} NTS

cd NTS
# When this file will be removed, clean the description.
[ -f EXPERIMENTAL ] || exit 1

# Sanity check, really often broken
extver=$(sed -n '/#define YACONF_VERSION/{s/.* "//;s/".*$//;p}' php_yaconf.h)
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
extension = %{ext_name}.so

; Configuration options
;yaconf.directory=''
;yaconf.check_delay=300
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config \
    --enable-yaconf
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config \
    --enable-yaconf
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}
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
    --define extension=%{buildroot}%{php_extdir}/%{ext_name}.so \
    --modules | grep %{ext_name}

: Upstream test suite  for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{ext_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff || : ignore

%if %{with_zts}
cd ../ZTS
rm tests/004.phpt
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{ext_name}.so \
    --modules | grep %{ext_name}

: Upstream test suite  for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{ext_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license NTS/LICENSE NTS/CREDITS
%doc NTS/README.md

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{ext_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{ext_name}.so
%endif


%files devel
%defattr(-,root,root,-)
%{php_incldir}/ext/%{ext_name}

%if %{with_zts}
%{php_ztsincldir}/ext/%{ext_name}
%endif


%changelog
* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.6.20150718git778424f
- F23 rebuild with rh_layout

* Thu Jul 23 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.5.20150718git778424f
- ignore 1 failed test on ZTS

* Wed Jul 22 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.4.20150718git778424f
- new snapshot
- rebuild against php 7.0.0beta2

* Wed Jul  8 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3.20150617gitad0c665
- rebuild against php 7.0.0beta1

* Wed Jun 24 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.20150617gitad0c665
- new snapshot
- add "devel" subpackage

* Fri Jun 12 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.20150612gitf3ca30d
- new package