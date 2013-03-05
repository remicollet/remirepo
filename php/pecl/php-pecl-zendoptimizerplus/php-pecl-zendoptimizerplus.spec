%{!?php_inidir: %{expand: %%global php_inidir %{_sysconfdir}/php.d}}
%global owner      zend-dev
%global extname    ZendOptimizerPlus
%global commit     d39a49a5340643483f6a94f391328b2d46a24d3b
%global short      %(c=%{commit}; echo ${c:0:7})
%global prever     -dev
%global with_zts   0%{?__ztsphp:1}

Name:          php-ZendOptimizerPlus
Version:       7.0.0
Release:       0.7.git%{short}%{?dist}
Summary:       The Zend Optimizer+

Group:         Development/Libraries
License:       PHP
URL:           https://github.com/%{owner}/%{extname}
Source0:       %{url}/archive/%{commit}/%{extname}-%{version}-%{short}.tar.gz
# this extension must be loaded before XDebug
# So uppercase Z if before lowercase X (LANG=C order)
Source1:       %{extname}.ini

BuildRequires: php-devel

Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

# Only one opcode cache could be enabled
Conflicts:     php-eaccelerator
Conflicts:     php-xcache
Conflicts:     php-pecl-apc

# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
The Zend Optimizer+ provides faster PHP execution through opcode caching and
optimization. It improves PHP performance by storing precompiled script
bytecode in the shared memory. This eliminates the stages of reading code from
the disk and compiling it on future access. In addition, it applies a few
bytecode optimization patterns that make code execution faster.


%prep
%setup -q -c

mv %{extname}-%{commit} NTS

# Sanity check, really often broken
extver=$(sed -n '/#define ACCELERATOR_VERSION/{s/.* "//;s/".*$//;p}' NTS/ZendAccelerator.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure \
    --enable-optimizer-plus \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --enable-optimizer-plus \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
install -D -p -m 644 %{SOURCE1} %{buildroot}%{php_inidir}/%{extname}.ini
sed -e 's:@EXTPATH@:%{php_extdir}:' \
    -i %{buildroot}%{php_inidir}/%{extname}.ini

make -C NTS install INSTALL_ROOT=%{buildroot}

%if %{with_zts}
install -D -p -m 644 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{extname}.ini
sed -e 's:@EXTPATH@:%{php_ztsextdir}:' \
    -i %{buildroot}%{php_ztsinidir}/%{extname}.ini

make -C ZTS install INSTALL_ROOT=%{buildroot}
%endif


%check
cd NTS
%{_bindir}/php \
    -n -d zend_extension=%{buildroot}%{php_extdir}/%{extname}.so \
    -m | grep "Zend Optimizer+"

TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n -d zend_extension=%{buildroot}%{php_extdir}/%{extname}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php

%if %{with_zts}
cd ../ZTS
%{__ztsphp} \
    -n -d zend_extension=%{buildroot}%{php_ztsextdir}/%{extname}.so \
    -m | grep "Zend Optimizer+"

TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d zend_extension=%{buildroot}%{php_ztsextdir}/%{extname}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php
%endif


%files
%doc NTS/{LICENSE,README}
%config(noreplace) %{php_inidir}/%{extname}.ini
%{php_extdir}/%{extname}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{extname}.ini
%{php_ztsextdir}/%{extname}.so
%endif


%changelog
* Thu Feb 28 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-0.7.gitd39a49a
- new snapshot
- run test suite during build

* Thu Feb 21 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-0.6.git3a06991
- new snapshot

* Fri Feb 15 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-0.4.git2b6eede
- new snapshot (ZTS fixes)

* Thu Feb 14 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-0.3.gita84b588
- make zts build optional

* Thu Feb 14 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-0.2.gitafb43f5
- new snapshot
- better default configuration file (new upstream recommendation)
- License file now provided by upstream

* Wed Feb 13 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-0.1.gitaafc145
- initial package
