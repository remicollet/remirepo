# spec file for php-pecl-eio
#
# Copyright (c) 2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?php_inidir:  %{expand: %%global php_inidir  %{_sysconfdir}/php.d}}
%{!?__pecl:      %{expand: %%global __pecl      %{_bindir}/pecl}}

#
# NOTE: bundled libeio (which is retired from Fedora)
#

%global with_zts  0%{?__ztsphp:1}
%global pecl_name eio

Summary:        Provides interface to the libeio library
Name:           php-pecl-%{pecl_name}
Version:        1.2.3
Release:        1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# http://svn.php.net/viewvc?view=revision&revision=331727
Patch0:         %{pecl_name}-svn.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel > 5.3
BuildRequires:  php-pear
BuildRequires:  php-sockets
# For tests
BuildRequires:  php-posix

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires:       php-sockets%{?_isa}

Provides:       php-%{pecl_name} = %{version}
Provides:       php-%{pecl_name}%{?_isa} = %{version}
Provides:       php-pecl(%{pecl_name}) = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}

# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


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
%patch0 -p3

# Need investigation (output order)
rm -f tests/eio_custom_basic.phpt \
      tests/fork.phpt
%if 0%{?rhel} == 5
rm -f tests/eio_fallocate_basic.phpt
%endif

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
cat > %{pecl_name}.ini << 'EOF'
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
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/z-%{pecl_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/z-%{pecl_name}.ini
%endif


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
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
%doc NTS/{LICENSE,CREDITS,README}
%{pecl_xmldir}/%{name}.xml
%config(noreplace) %{php_inidir}/z-%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/z-%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Tue Oct  8 2013 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- initial package
