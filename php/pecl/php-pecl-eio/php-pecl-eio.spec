# remirepo spec file for php-pecl-eio
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global pecl_name eio
%global with_zts  0%{!?_without_zts:%{?__ztsphp:1}}
%if "%{php_version}" < "5.6"
# After sockets
%global ini_name  z-%{pecl_name}.ini
%else
# After 20-sockets
%global ini_name  40-%{pecl_name}.ini
%endif
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
Provides: %{?scl_prefix}php-pecl-%{pecl_name}         = %{version}-%{release}
Provides: %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa} = %{version}-%{release}
%else
%global sub_prefix %{scl_prefix}
%endif
%scl_package       php-pecl-eio
%endif
#global prever     RC3


#
# NOTE: bundled libeio (which is retired from Fedora)
#

Summary:        Provides interface to the libeio library
Name:           %{?sub_prefix}php-pecl-%{pecl_name}
Version:        2.0.1
Release:        2%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel > 5.3
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-sockets
# For tests
BuildRequires:  %{?scl_prefix}php-posix

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
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-pecl-%{pecl_name} = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa} = %{version}-%{release}
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
This extension provides interface to the libeio library written by Marc Lehmann
(see http://software.schmorp.de/pkg/libeio.html).

Libeio is a an asynchronous I/O library. Features basically include
asynchronous versions of POSIX API(read, write, open, close, stat, unlink,
fdatasync, mknod, readdir etc.); sendfile (native on Solaris, Linux, HP-UX,
FreeBSD); readahead. libeio itself emulates the system calls, if they are not
available on specific(UNIX-like) platform.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
mv %{pecl_name}-%{version}%{?prever} NTS

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS

# Sanity check, really often broken
extver=$(sed -n '/define PHP_EIO_VERSION/{s/.* "//;s/".*$//;p}' php%(%{__php} -r 'echo PHP_MAJOR_VERSION;')/php_eio.h)
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

# Documentation
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
# Need investigation (output order, erratic results)
rm  ?TS/tests/eio_custom_basic.phpt
%if 0%{?rhel} == 5
rm  ?TS/tests/eio_fallocate_basic.phpt
%endif

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
* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-2
- rebuild for PHP 7.1 new API version

* Mon Jul 25 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1

* Wed Jun  8 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0 (stable)

* Wed Mar 23 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.4.RC3
- Update to 2.0.0RC3 (no change)

* Fri Mar  4 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.3.RC2
- Update to 2.0.0RC2

* Fri Nov 20 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.2.RC1
- fix PHP 7 and ZTS build
  open https://bitbucket.org/osmanov/pecl-eio/issues/3
  open https://bitbucket.org/osmanov/pecl-eio/pull-requests/4

* Thu Nov 19 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.RC1
- Update to 2.0.0RC1

* Mon Sep 28 2015 Remi Collet <remi@fedoraproject.org> - 1.2.6-1
- Update to 1.2.6
- don't install/register tests
- allow build against rh-php56 (as more-php56)
- drop runtime dependency on pear, new scriptlets

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
