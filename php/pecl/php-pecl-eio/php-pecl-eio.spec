# spec file for php-pecl-eio
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package        php-pecl-eio}
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

#
# NOTE: bundled libeio (which is retired from Fedora)
#

%global pecl_name eio
%global with_zts  0%{?__ztsphp:1}

%if "%{php_version}" < "5.6"
# After sockets
%global ini_name  z-%{pecl_name}.ini
%else
# After 20-sockets
%global ini_name  40-%{pecl_name}.ini
%endif

Summary:        Provides interface to the libeio library
Name:           %{?scl_prefix}php-pecl-%{pecl_name}
Version:        1.2.5
Release:        3%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}.1
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel > 5.3
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-sockets
# For tests
BuildRequires:  %{?scl_prefix}php-posix

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%if "%{php_version}" < "5.4"
# php 5.3.3 in EL-6 don't use arched virtual provides
# so only requires real packages instead
Requires:       %{?scl_prefix}php-common%{?_isa}
%else
Requires:       %{?scl_prefix}php-sockets%{?_isa}
%endif
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name} = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
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
# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This extension provides interface to the libeio library written by Marc Lehmann
(see http://software.schmorp.de/pkg/libeio.html).

Libeio is a an asynchronous I/O library. Features basically include
asynchronous versions of POSIX API(read, write, open, close, stat, unlink,
fdatasync, mknod, readdir etc.); sendfile (native on Solaris, Linux, HP-UX,
FreeBSD); readahead. libeio itself emulates the system calls, if they are not
available on specific(UNIX-like) platform.


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

cd NTS

# Sanity check, really often broken
extver=$(sed -n '/define PHP_EIO_VERSION/{s/.* "//;s/".*$//;p}' php_eio.h)
if test "x${extver}" != "x%{version}%{?prever:-%{prever}}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever:-%{prever}}.
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
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in LICENSE $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
# Need investigation (output order)
rm  ?TS/tests/eio_custom_basic.phpt
%if 0%{?rhel} <= 7
rm  ?TS/tests/eio_fallocate_basic.phpt
%endif
%if 0%{?rhel} <= 6
rm  ?TS/tests/eio_write_variation.phpt
rm  ?TS/tests/fork.phpt
%endif

DEPMOD=
[ -f %{php_extdir}/sockets.so ] && DEPMOD="$DEPMOD -d extension=sockets.so"
[ -f %{php_extdir}/posix.so ]   && DEPMOD="$DEPMOD -d extension=posix.so"

: Minimal load test for NTS extension
cd NTS
%{_bindir}/php --no-php-ini \
    $DEPMOD \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n $DEPMOD -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php


%if %{with_zts}
: Minimal load test for ZTS extension
cd ../ZTS
%{__ztsphp} --no-php-ini \
    $DEPMOD \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n $DEPMOD -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{pecl_name}
%doc %{pecl_testdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.2.5-3.1
- Fedora 21 SCL mass rebuild

* Tue Aug 26 2014 Remi Collet <rcollet@redhat.com> - 1.2.5-3
- improve SCL build

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 1.2.5-2
- add numerical prefix to extension configuration file

* Thu Mar 27 2014 Remi Collet <remi@fedoraproject.org> - 1.2.5-1
- Update to 1.2.5 (stable)

* Sun Mar 23 2014 Remi Collet <remi@fedoraproject.org> - 1.2.4-2
- allow SCL build

* Sat Mar 15 2014 Remi Collet <remi@fedoraproject.org> - 1.2.4-1
- Update to 1.2.4 (stable)
- install doc in pecl_docdir
- install tests in pecl_testdir

* Tue Oct  8 2013 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- initial package
