# remirepo spec file for php-pecl-event
# with SCL compatibility, from:
#
# Fedora spec file for php-pecl-event
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix   %{scl_prefix}
%scl_package         php-pecl-event
%else
%global _root_prefix %{_prefix}
%endif

%global with_tests  0%{!?_without_tests:1}
%global pecl_name   event
%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
%if "%{php_version}" < "5.6"
# After sockets.so
%global ini_name  z-%{pecl_name}.ini
%else
# After 20-sockets.so
%global ini_name  40-%{pecl_name}.ini
%endif
%global prever    RC1

Summary:       Provides interface to libevent library
Name:          %{?sub_prefix}php-pecl-%{pecl_name}
Version:       2.3.0
Release:       0.2.%{prever}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/event
Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{?scl_prefix}php-devel > 5.4
BuildRequires: %{?scl_prefix}php-pear

%if 0%{?scl:1} && 0%{?fedora} < 15 && 0%{?rhel} < 7 && "%{?scl_vendor}" != "remi"
# Filter in the SCL collection
%{?filter_requires_in: %filter_requires_in %{_libdir}/.*\.so}
# libvent from SCL as not available in system
BuildRequires: %{?sub_prefix}libevent-devel  >= 2.0.2
Requires:      %{?sub_prefix}libevent%{_isa} >= 2.0.2
%global        _event_prefix %{_prefix}
%else
BuildRequires: libevent-devel >= 2.0.2
%global        _event_prefix %{_root_prefix}
%endif

BuildRequires: openssl-devel
BuildRequires: pkgconfig

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
Requires:      %{?scl_prefix}php-sockets%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:      %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:      %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
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
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%endif
%{?filter_setup}


%description
This is an extension to efficiently schedule I/O, time and signal based
events using the best I/O notification mechanism available for specific
platform. This is a port of libevent to the PHP infrastructure.

Version 1.0.0 introduces:
* new OO API breaking backwards compatibility
* support of libevent 2+ including HTTP, DNS, OpenSSL and the event listener.

Documentation: http://php.net/event

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c 

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

mv %{pecl_name}-%{version}%{?prever} NTS

cd NTS

# Sanity check, really often broken
sed -e '/PHP_EVENT_VERSION/s/2.0.3/2.0.4/' -i php?/php_event.h

DIR=$(%{__php} -r 'echo "php" . PHP_MAJOR_VERSION;')
extver=$(sed -n '/#define PHP_EVENT_VERSION/{s/.* "//;s/".*$//;p}' $DIR/php_event.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
cd ..

# duplicate for ZTS build
%if %{with_zts}
cp -pr NTS ZTS
%endif

# Drop in the bit of configuration
cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension = %{pecl_name}.so
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-event-libevent-dir=%{_event_prefix} \
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
    --with-event-libevent-dir=%{_event_prefix} \
    --with-libdir=%{_lib} \
    --with-event-core \
    --with-event-extra \
    --with-event-openssl \
    --with-event-pthreads \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

# use z-event.ini to ensure event.so load "after" sockets.so
: Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
: Install the ZTS stuff
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

: Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

: Documentation
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
%{__php} -n run-tests.php --show-diff

%if %{with_zts}
cd ../ZTS
%if 0%{?rhel} == 6
rm tests/27-event-util-create-socket.phpt
%endif

: Upstream test suite for ZTS extension
SKIP_ONLINE_TESTS=1 \
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n $OPTS -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff
%endif
%endif


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
* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 2.3.0-0.2.RC1
- rebuild with PHP 7.1.0 GA

* Fri Nov 11 2016 Remi Collet <remi@fedoraproject.org> - 2.3.0-0.1.RC1
- Update to 2.3.0RC1 (php 5 and 7, beta)

* Thu Nov 10 2016 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1 (php 5 and 7, stable)

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 2.1.0-2
- rebuild for PHP 7.1 new API version

* Wed Jun 08 2016 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0

* Fri Apr 22 2016 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4

* Thu Apr 21 2016 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3 (php 5 and 7, stable)

* Fri Apr 01 2016 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2 (php 5 and 7, stable)

* Thu Mar 17 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1 (php 5 and 7, stable)

* Mon Feb 29 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0 (php 5 and 7, stable)

* Thu Feb 25 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.2.RC2
- Update to 2.0.0RC2 (php 5 and 7, beta)

* Sun Feb 21 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.RC1
- Update to 2.0.0RC1 (php 5 and 7, beta)

* Thu Feb 11 2016 Remi Collet <remi@fedoraproject.org> - 1.11.3-1
- Update to 1.11.3

* Sun Jun 21 2015 Remi Collet <remi@fedoraproject.org> - 1.11.1-2
- allow build against rh-php56 (as more-php56)
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.11.1-1.1
- Fedora 21 SCL mass rebuild

* Fri Nov 14 2014 Remi Collet <remi@fedoraproject.org> - 1.11.1-1
- Update to 1.11.1 (stable)
- no change, only our patch merged upstream

* Thu Nov 13 2014 Remi Collet <remi@fedoraproject.org> - 1.11.0-1
- Update to 1.11.0 (stable)
- don't provide test suite
- add patch for old openssl in EL-5
  https://bitbucket.org/osmanov/pecl-event/pull-request/10

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 1.10.3-2
- improve SCL build

* Mon Aug 11 2014 Remi Collet <remi@fedoraproject.org> - 1.10.3-1
- Update to 1.10.3 (no change)

* Fri Jun 20 2014 Remi Collet <remi@fedoraproject.org> - 1.10.2-1
- Update to 1.10.2 (stable)

* Sun May 11 2014 Remi Collet <remi@fedoraproject.org> - 1.10.1-1
- Update to 1.10.1 (stable, no change)

* Sat May 10 2014 Remi Collet <remi@fedoraproject.org> - 1.10.0-1
- Update to 1.10.0 (stable)

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 1.9.1-3
- add numerical prefix to extension configuration file

* Sun Mar 23 2014 Remi Collet <remi@fedoraproject.org> - 1.9.1-2
- allow SCL build, with libevent from SCL when needed

* Sun Mar 23 2014 Remi Collet <remi@fedoraproject.org> - 1.9.1-1
- Update to 1.9.1 (stable)

* Sun Mar 23 2014 Remi Collet <remi@fedoraproject.org> - 1.9.0-2
- add patch for php 5.6
  https://bitbucket.org/osmanov/pecl-event/pull-request/7

* Fri Jan 17 2014 Remi Collet <remi@fedoraproject.org> - 1.9.0-1
- Update to 1.9.0 (stable)
- add option to disable tests during build
- adapt for SCL

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
