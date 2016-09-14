# remirepo spec file for php-pecl-ev
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
#
# NOTE: bundled libev
#
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
%scl_package        php-pecl-ev
%endif

%global pecl_name ev
%global with_zts  0%{!?_without_zts:%{?__ztsphp:1}}
%if "%{php_version}" < "5.6"
# After sockets
%global ini_name  z-%{pecl_name}.ini
%else
# After 20-sockets
%global ini_name  40-%{pecl_name}.ini
%endif
#global prever    RC9

Summary:        Provides interface to libev library
Name:           %{?sub_prefix}php-pecl-%{pecl_name}
Version:        1.0.3
Release:        2%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel > 5.4
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-sockets
# For tests
BuildRequires:  %{?scl_prefix}php-posix

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-sockets%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
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
# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The ev extension provides interface to libev library - high performance
full-featured event loop written in C.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
mv %{pecl_name}-%{version}%{?prever} NTS

# Don't register test files on install
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS
# Sanity check, really often broken
extver=$(sed -n '/define PHP_EV_VERSION/{s/.* "//;s/".*$//;p}' php%(%{__php} -r 'echo PHP_MAJOR_VERSION;')/php_ev.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
cd ..

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif

# Create configuration file
cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/php-config

make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/zts-php-config

make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# install config file - z-eio.ini to ensure load order (after sockets)
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Test & Documentation
cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
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
DEPMOD=
[ -f %{php_extdir}/sockets.so ] && DEPMOD="$DEPMOD -d extension=sockets.so"
[ -f %{php_extdir}/posix.so ]   && DEPMOD="$DEPMOD -d extension=posix.so"

: Minimal load test for NTS extension
cd NTS
%{_bindir}/php --no-php-ini \
    $DEPMOD \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n $DEPMOD -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php --show-diff


%if %{with_zts}
: Minimal load test for ZTS extension
cd ../ZTS

%{__ztsphp} --no-php-ini \
    $DEPMOD \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n $DEPMOD -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff
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
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-2
- rebuild for PHP 7.1 new API version

* Fri Jul 29 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Fri Jul 29 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2 (stable)

* Fri Jul 29 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1 (stable)
- ignore 1 failed test with PHP 5.4, see
  https://bitbucket.org/osmanov/pecl-ev/issues/28/101-failed-test-with-php-54

* Tue May 17 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- update to 1.0.0 (stable)

* Sat Mar  5 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.7.RC9
- adapt for F24

* Thu Feb 25 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.6.RC9
- Update to 1.0.0RC9 (php 5 and 7, beta)

* Mon Feb 22 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.5.RC8
- Update to 1.0.0RC8

* Thu Feb 11 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.4.RC4
- Update to 1.0.0RC4

* Wed Dec 16 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3.RC3
- Update to 1.0.0RC3

* Wed Nov 25 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.RC2
- Update to 1.0.0RC2

* Fri Nov 20 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.RC1
- Update to 1.0.0RC1
- open https://bitbucket.org/osmanov/pecl-ev/issues/16 - ZTS segfault

* Mon May 04 2015 Remi Collet <remi@fedoraproject.org> - 0.2.15-1
- Update to 0.2.15 (stable, no change)
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 0.2.13-1.1
- Fedora 21 SCL mass rebuild

* Tue Dec 09 2014 Remi Collet <remi@fedoraproject.org> - 0.2.13-1
- Update to 0.2.13 (stable, no change)

* Tue Sep 09 2014 Remi Collet <remi@fedoraproject.org> - 0.2.12-1
- Update to 0.2.12 (no change, only our patch merged)
- enable posix during build as some tests need it

* Mon Sep  8 2014 Remi Collet <rcollet@redhat.com> - 0.2.11-2
- open https://bitbucket.org/osmanov/pecl-ev/pull-request/3
- enable ZTS build

* Mon Sep  8 2014 Remi Collet <rcollet@redhat.com> - 0.2.11-1
- initial package, version 0.2.11 (stable)
