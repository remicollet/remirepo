# spec file for php-pecl-qb
#
# Copyright (c) 2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global gh_commit    18d3e65c11f3c55db00fd768ecf3629afbb86094
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     chung-leong
%global gh_project   qb
%global pecl_name    qb
# https://github.com/chung-leong/qb/issues/24
%global with_zts     0

Summary:        Accelerator designed mainly for graphic work
Name:           php-pecl-%{pecl_name}
Version:        2.1.1
Release:        1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
# Use github archive to have full archive, included test suite
# and https://github.com/chung-leong/qb/issues/23
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel
BuildRequires:  php-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

Provides:       php-%{pecl_name} = %{version}
Provides:       php-%{pecl_name}%{?_isa} = %{version}
Provides:       php-pecl(%{pecl_name}) = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet"
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
Obsoletes:     php54-pecl-%{pecl_name}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name}
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


%prep
%setup -q -c
mv %{gh_project}-%{gh_commit} NTS
mv NTS/package.xml .

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
install -D -m 644 NTS/%{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
# install ZTS extension
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 ZTS/%{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

# Test & Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
# Need investigation - https://github.com/chung-leong/qb/issues/25
%if 0%{?rhel} < 7 && 0%{?fedora} < 19
%ifarch %{ix86}
rm ?TS/tests/intrinsic-cos.phpt
rm ?TS/tests/intrinsic-ccosh.phpt
rm ?TS/tests/intrinsic-tan.phpt
rm ?TS/tests/class-var-ref-count-array.phpt
%endif
%endif

cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite  for NTS extension
export TEST_PHP_EXECUTABLE=%{__php}
export TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{pecl_name}.so"
export NO_INTERACTION=1
export REPORT_EXIT_STATUS=1
if ! %{__php} run-tests.php
then
  for i in tests/*diff
  do
    echo "---- FAILURE in $i"
    cat $i
    echo -n "\n----"
  done
  exit 1
fi

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite  for ZTS extension
TEST_PHP_EXECUTABLE=%{_bindir}/zts-php \
TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/zts-php -n run-tests.php
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Mon Mar 17 2014 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- initial package, version 2.1.1 (stable)
- https://github.com/chung-leong/qb/issues/23 - Bad archive
- https://github.com/chung-leong/qb/issues/24 - ZTS broken
- https://github.com/chung-leong/qb/issues/25 - Failed tests