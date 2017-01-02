# remirepo spec file for php-pecl-qb
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package        php-pecl-qb}
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global pecl_name    qb
%global with_zts     0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
%global ini_name     %{pecl_name}.ini
%else
%global ini_name     40-%{pecl_name}.ini
%endif

Summary:        Accelerator designed mainly for graphic work
Name:           %{?scl_prefix}php-pecl-%{pecl_name}
Version:        2.4.0
%global tarver  2.4.0
Release:        2%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{tarver}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-pear

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}

%if "%{?vendor}" == "Remi Collet"
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
Obsoletes:     php54-pecl-%{pecl_name}
Obsoletes:     php54w-pecl-%{pecl_name}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}
Obsoletes:     php55w-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name}
Obsoletes:     php56w-pecl-%{pecl_name}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
QB stands for "Quick Binary".

It's a PHP extension designed to enable faster handling of binary data.
It takes a function written in PHP and translate it for a specialized
virtual machine. The use of static type information leads significantly
higher performance than under PHP's regular dynamic type system.
A PHP+QB function can run anywhere from five to twenty times faster
than regular PHP code. For even higher level of performance, one can compile
PHP+QB functions to native code (on supported platforms).

QB performs code translation on a per-function basis. It does not affect
in anyway code not specially marked. Interaction between PHP+QB functions
and regular PHP code is basically seamless. A key design objective of QB
is to let developers harness greater processing power than what baseline
PHP offers without the risk involved in adopting a brand new platform.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
mv %{pecl_name}-%{tarver}    NTS

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS
# Sanity check, really often broken
extver=$(sed -n '/#define PHP_QB_VERSION/{s/.*[[:space:]]"//;s/".*$//;p}' php_qb.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

# install NTS extension
make -C NTS install INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 NTS/%{pecl_name}.ini %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
# install ZTS extension
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 ZTS/%{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


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


%check
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif

: Upstream test suite  for NTS extension
cd NTS
export TEST_PHP_EXECUTABLE=%{__php}
export TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{pecl_name}.so"
export NO_INTERACTION=1
# ignore result for now
export REPORT_EXIT_STATUS=0
%{__php} -n run-tests.php --show-diff


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
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Tue Mar  8 2016 Remi Collet <remi@fedoraproject.org> - 2.4.0-2
- adapt for F24
- drop runtime dependency on pear, new scriptlets
- fix license management
- don't install/register tests

* Mon Jul 21 2014 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0 (stable)
- ignore test results

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 2.3-1
- Update to 2.3 (stable)
- allow <12 failed tests (on ~450)
# Need investigation - https://github.com/chung-leong/qb/issues/25
* Wed Apr 16 2014 Remi Collet <remi@fedoraproject.org> - 2.2.0-3
- add numerical prefix to extension configuration file (php 5.6)

* Sun Mar 30 2014 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0 (stable)
- use sources from pecl

* Wed Mar 26 2014 Remi Collet <remi@fedoraproject.org> - 2.1.2-1
- Update to 2.1.2 (stable)
- enable ZTS build
- https://github.com/chung-leong/qb/issues/31 - missing files

* Tue Mar 25 2014 Remi Collet <remi@fedoraproject.org> - 2.1.1-2
- allow SCL build

* Mon Mar 17 2014 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- initial package, version 2.1.1 (stable)
- https://github.com/chung-leong/qb/issues/23 - Bad archive
- https://github.com/chung-leong/qb/issues/24 - ZTS broken
- https://github.com/chung-leong/qb/issues/25 - Failed tests
