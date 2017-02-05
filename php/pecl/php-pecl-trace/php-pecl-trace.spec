# remirepo/fedora spec file for php-pecl-trace
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package       php-pecl-trace
%endif

%global pecl_name  trace
#global versuf     -beta
%if "%{php_version}" < "5.6"
%global ini_name   %{pecl_name}.ini
%else
%global ini_name   40-%{pecl_name}.ini
%endif

Summary:        Trace is a low-overhead tracing tool for PHP
Name:           %{?sub_prefix}php-pecl-%{pecl_name}
Version:        1.0.0
Release:        2%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
# common/sds is BSD-2, other is ASL 2.0
License:        ASL 2.0 and BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# https://github.com/Qihoo360/phptrace/issues/75
# https://github.com/Qihoo360/phptrace/pull/76
Patch0:         %{pecl_name}-pr76.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# https://github.com/Qihoo360/phptrace/issues/71
# PHP 7.1 build broken
BuildRequires:  %{?scl_prefix}php-devel < 7.1
BuildRequires:  %{?scl_prefix}php-pear

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php53u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php54-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php54w-pecl-%{pecl_name} <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.1"
Obsoletes:     php71u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php71w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Trace is a low-overhead tracing tool for PHP.

It can trace all PHP executing, function calls, request information during
run-time. And provides features like Filter, Statistics, Current Status and
so on.

It is very useful to locate blocking, heavy-load problems and debug in all
environments, especially in production environments.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
pushd %{pecl_name}-%{version}
%patch0 -p1 -b .pr76
popd

# Don't install tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

pushd %{pecl_name}-%{version}/extension
cp -p ../deps/sds/LICENSE ../LICENSE_sds

# https://github.com/Qihoo360/phptrace/issues/73
sed -e '/TRACE_EXT_VERSION/s/0.6.0-beta/%{version}/' -i ../common/trace_version.h

# Sanity check, really often broken
extver=$(sed -n '/#define TRACE_EXT_VERSION/{s/.* "//;s/".*$//;p}' ../common/trace_version.h)
if test "x${extver}" != "x%{version}%{?versuf}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?versuf}.
   exit 1
fi
popd

# Create configuration file
cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; Configuration
;trace.enable = 1
;trace.dotrace = 0
;trace.data_dir = "/tmp"
EOF


%build
%{?dtsenable}
cd %{pecl_name}-%{version}/extension

%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config \
    --enable-trace
make     %{?_smp_mflags}
make cli %{?_smp_mflags}


%install
rm -rf %{buildroot}
%{?dtsenable}

make -C %{pecl_name}-%{version}/extension install-all INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 %{pecl_name}-%{version}/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
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
cd %{pecl_name}-%{version}/extension
: Ignore failed test
%if "%{php_version}" > "7.0"
# https://github.com/Qihoo360/phptrace/issues/72
# PHP 7.0 failed tests
rm tests/trace_002.phpt
rm tests/trace_003.phpt
%endif
# https://github.com/Qihoo360/phptrace/issues/70
# Failed test requiring TRACE_DEBUG
rm tests/trace_015.phpt
rm tests/trace_016.phpt

: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php --show-diff


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{?_licensedir:%license %{pecl_name}-%{version}/LICENSE*}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml
%{_bindir}/phptrace

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so


%changelog
* Sun Feb  5 2017 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- add patch for security issue (umask=0)
  patch from https://github.com/Qihoo360/phptrace/pull/76
  see https://github.com/Qihoo360/phptrace/issues/75

* Thu Jan 19 2017 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0 (beta)
- open https://github.com/Qihoo360/phptrace/issues/71: PHP 7.1 build broken
- open https://github.com/Qihoo360/phptrace/issues/73: reported version
- open https://github.com/Qihoo360/phptrace/issues/72: PHP 7.0 failed tests
- open https://github.com/Qihoo360/phptrace/issues/70: Failed tests (debug)

* Wed Mar  9 2016 Remi Collet <remi@fedoraproject.org> - 0.3.0-3
- adapt for F24

* Fri May 22 2015 Remi Collet <remi@fedoraproject.org> - 0.3.0-2
- update to 0.3.0 (stable)
- enable test suite

* Fri May 15 2015 Remi Collet <remi@fedoraproject.org> - 0.3.0-1
- initial package, version 0.3.0 (beta)
