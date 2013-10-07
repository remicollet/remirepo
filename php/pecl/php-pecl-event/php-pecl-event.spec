# spec file for php-pecl-event
#
# Copyright (c) 2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?__pecl:      %{expand: %%global __pecl      %{_bindir}/pecl}}

%global pecl_name   event
%global with_zts    0%{?__ztsphp:1}

Summary:       Provides interface to libevent library
Name:          php-pecl-event
Version:       1.8.1
Release:       1%{?dist}
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/event
Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# https://bitbucket.org/osmanov/pecl-event/pull-request/4
Patch0:        %{pecl_name}-ver.patch

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

# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
This is an extension to efficiently schedule I/O, time and signal based
events using the best I/O notification mechanism available for specific
platform. This is a port of libevent to the PHP infrastructure.

Version 1.0.0 introduces:
* new OO API breaking backwards compatibility
* support of libevent 2+ including HTTP, DNS, OpenSSL and the event listener.


%prep
%setup -q -c 

cd %{pecl_name}-%{version}
%patch0 -p1

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_EVENT_VERSION/{s/.* "//;s/".*$//;p}' php_event.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

# duplicate for ZTS build
%if %{with_zts}
cp -pr %{pecl_name}-%{version} %{pecl_name}-zts
%endif

# Drop in the bit of configuration
cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension = %{pecl_name}.so
EOF


%build
cd %{pecl_name}-%{version}
%{_bindir}/phpize
%configure \
    --with-libdir=%{_lib} \
    --with-event-core \
    --with-event-extra \
    --with-event-openssl \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../%{pecl_name}-zts
%{_bindir}/zts-phpize
%configure \
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
make -C %{pecl_name}-%{version} install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/z-%{pecl_name}.ini

%if %{with_zts}
: Install the ZTS stuff
make -C %{pecl_name}-zts install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/z-%{pecl_name}.ini
%endif

: Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
cd %{pecl_name}-%{version}
if [ -f %{php_extdir}/sockets.so ]; then
  OPTS="-d extension=sockets.so"
fi

SKIP_ONLINE_TESTS=1 \
TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n $OPTS -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php

%if %{with_zts}
cd ../%{pecl_name}-zts
if [ -f %{php_ztsextdir}/sockets.so ]; then
  OPTS="-d extension=sockets.so"
fi

SKIP_ONLINE_TESTS=1 \
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n $OPTS -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php
%endif


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%doc %{pecl_name}-%{version}/{CREDITS,LICENSE,README.md}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/z-%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/z-%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
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
