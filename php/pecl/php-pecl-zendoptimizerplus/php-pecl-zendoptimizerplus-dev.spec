%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%global prjname    ZendOptimizerPlus
%global extname    zendoptimizerplus

Name:          php-pecl-%{extname}
Version:       7.0.0
Release:       1%{?dist}.1
Summary:       The Zend Optimizer+

Group:         Development/Libraries
License:       PHP
URL:           http://pecl.php.net/package/%{prjname}
Source0:       http://pecl.php.net/get/%{extname}-%{version}.tgz
# this extension must be loaded before XDebug
# So uppercase Z if before lowercase X (LANG=C order)
Source1:       %{prjname}.ini

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php-devel >= 5.2.0
BuildRequires: php-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

# Only one opcode cache could be enabled
Conflicts:     php-eaccelerator
Conflicts:     php-xcache
Conflicts:     php-pecl-apc
Obsoletes:     php-ZendOptimizerPlus < 7.0.0-1
Provides:      php-pecl(%{extname}) = %{version}
Provides:      php-pecl(%{extname})%{?_isa} = %{version}
Provides:      php-%{extname} = %{version}-%{release}
Provides:      php-%{extname}%{?_isa} = %{version}-%{release}
Provides:      php-pecl(%{prjname}) = %{version}
Provides:      php-pecl(%{prjname})%{?_isa} = %{version}
Provides:      php-%{prjname} = %{version}-%{release}
Provides:      php-%{prjname}%{?_isa} = %{version}-%{release}

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

mv %{extname}-%{version} NTS

# Sanity check, really often broken
extver=$(sed -n '/#define ACCELERATOR_VERSION/{s/.* "//;s/".*$//;p}' NTS/ZendAccelerator.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi

# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS


%build
cd NTS
%{_bindir}/phpize
%configure \
    --enable-optimizer-plus \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --enable-optimizer-plus \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

install -D -p -m 644 %{SOURCE1} %{buildroot}%{php_inidir}/%{prjname}.ini
sed -e 's:@EXTPATH@:%{php_extdir}:' \
    -i %{buildroot}%{php_inidir}/%{prjname}.ini

make -C NTS install INSTALL_ROOT=%{buildroot}

install -D -p -m 644 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{prjname}.ini
sed -e 's:@EXTPATH@:%{php_ztsextdir}:' \
    -i %{buildroot}%{php_ztsinidir}/%{prjname}.ini

make -C ZTS install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%clean
rm -rf %{buildroot}


%check
cd NTS
%{__php} \
    -n -d zend_extension=%{buildroot}%{php_extdir}/%{prjname}.so \
    -m | grep "Zend Optimizer+"

TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d zend_extension=%{buildroot}%{php_extdir}/%{prjname}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php

cd ../ZTS
%{__ztsphp} \
    -n -d zend_extension=%{buildroot}%{php_ztsextdir}/%{prjname}.so \
    -m | grep "Zend Optimizer+"

TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d zend_extension=%{buildroot}%{php_ztsextdir}/%{prjname}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{extname} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc NTS/{LICENSE,README}
%config(noreplace) %{php_inidir}/%{prjname}.ini
%{php_extdir}/%{prjname}.so

%config(noreplace) %{php_ztsinidir}/%{prjname}.ini
%{php_ztsextdir}/%{prjname}.so

%{pecl_xmldir}/%{name}.xml


%changelog
* Tue Mar  5 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-1
- official PECL release, version 7.0.0 (beta)

* Thu Feb 28 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-0.7.gitd39a49a
- new snapshot
- run test suite during build

* Thu Feb 21 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-0.6.git3a06991
- new snapshot

* Fri Feb 15 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-0.4.git2b6eede
- new snapshot (ZTS fixes)

* Thu Feb 14 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-0.2.gitafb43f5
- new snapshot
- better default configuration file (new upstream recommendation)
- License file now provided by upstream

* Wed Feb 13 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-0.1.gitaafc145
- initial package
