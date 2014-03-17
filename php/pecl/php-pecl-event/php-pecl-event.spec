# spec file for php-pecl-event
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global with_tests  %{?_without_tests:0}%{!?_without_tests:1}
%global pecl_name   event
%global with_zts    0%{?__ztsphp:1}

Summary:       Provides interface to libevent library
Name:          php-pecl-%{pecl_name}
Version:       1.9.0
Release:       1%{?dist}
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/event
Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRequires: php-devel > 5.4
BuildRequires: php-pear
BuildRequires: libevent-devel >= 2.0.2
BuildRequires: openssl-devel
BuildRequires: pkgconfig

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}
Requires:      php-sockets%{?_isa}

Provides:      php-%{pecl_name} = %{version}
Provides:      php-%{pecl_name}%{?_isa} = %{version}
Provides:      php-pecl(%{pecl_name}) = %{version}
Provides:      php-pecl(%{pecl_name})%{?_isa} = %{version}

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This is an extension to efficiently schedule I/O, time and signal based
events using the best I/O notification mechanism available for specific
platform. This is a port of libevent to the PHP infrastructure.

Version 1.0.0 introduces:
* new OO API breaking backwards compatibility
* support of libevent 2+ including HTTP, DNS, OpenSSL and the event listener.


%prep
%setup -q -c 

mv %{pecl_name}-%{version} NTS

# duplicate for ZTS build
%if %{with_zts}
cp -pr NTS ZTS
%endif

# Drop in the bit of configuration
cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension = %{pecl_name}.so
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-event-libevent-dir=%{_prefix} \
    --with-libdir=%{_lib} \
    --with-event-core \
    --with-event-extra \
    --with-event-openssl \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-event-libevent-dir=%{_prefix} \
    --with-libdir=%{_lib} \
    --with-event-core \
    --with-event-extra \
    --with-event-openssl \
    --with-event-pthreads \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
# use z-event.ini to ensure event.so load "after" sockets.so
: Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/z-%{pecl_name}.ini

%if %{with_zts}
: Install the ZTS stuff
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/z-%{pecl_name}.ini
%endif

: Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

: Test and Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
if [ -f %{php_extdir}/sockets.so ]; then
  OPTS="-d extension=sockets.so"
fi

: Minimal load test for NTS extension
%{__php} --no-php-ini $OPTS  \
    --define extension=NTS/modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini $OPTS  \
    --define extension=ZTS/modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif

%if %{with_tests}
cd NTS
: Upstream test suite for NTS extension
SKIP_ONLINE_TESTS=1 \
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n $OPTS -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php

%if %{with_zts}
cd ../ZTS
: Upstream test suite for ZTS extension
SKIP_ONLINE_TESTS=1 \
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n $OPTS -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php
%endif
%endif


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%doc %{pecl_docdir}/%{pecl_name}
%doc %{pecl_testdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/z-%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/z-%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Fri Jan 17 2014 Remi Collet <remi@fedoraproject.org> - 1.9.0-1
- Update to 1.9.0 (stable)
- add option to disable tests during build

* Sat Jan 11 2014 Remi Collet <remi@fedoraproject.org> - 1.8.1-2
- install doc in pecl doc_dir
- install tests in pecl test_dir
- open https://bitbucket.org/osmanov/pecl-event/pull-request/6

* Mon Oct 07 2013 Remi Collet <remi@fedoraproject.org> - 1.8.1-1
- Update to 1.8.1 (stable)
- drop patch merged upstream
- patch for https://bitbucket.org/osmanov/pecl-event/pull-request/4

* Sun Oct 06 2013 Remi Collet <remi@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0
- patch for https://bitbucket.org/osmanov/pecl-event/pull-request/3

* Mon Sep 16 2013 Remi Collet <remi@fedoraproject.org> - 1.7.8-1
- Update to 1.7.8

* Sun Sep 08 2013 Remi Collet <remi@fedoraproject.org> - 1.7.6-1
- Update to 1.7.6

* Mon Aug 19 2013 Remi Collet <remi@fedoraproject.org> - 1.7.5-1
- Update to 1.7.5

* Sun Jul 28 2013 Remi Collet <remi@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2

* Fri Jul 26 2013 Remi Collet <remi@fedoraproject.org> - 1.7.1-2
- cleanups before review

* Wed Jul 24 2013 Remi Collet <remi@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1

* Thu Jul 18 2013 Remi Collet <remi@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Thu Jul 18 2013 Remi Collet <remi@fedoraproject.org> - 1.6.2-2
- missing requires php-sockets
- enable thread safety for ZTS extension

* Thu Jul 18 2013 Remi Collet <remi@fedoraproject.org> - 1.6.2-1
- Update to 1.6.2

* Sat Apr 20 2013 Remi Collet <remi@fedoraproject.org> - 1.6.1-1
- initial package, version 1.6.1
- upstream bugs:
  https://bugs.php.net/64678 missing License
  https://bugs.php.net/64679 buffer overflow
  https://bugs.php.net/64680 skip online test
