# remirepo spec file for php-pecl-redis
# adapted for scl, from
#
# Fedora spec file for php-pecl-redis
#
# Copyright (c) 2012-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
%endif

%{?scl:          %scl_package        php-pecl-redis}

%global pecl_name   redis
%global with_zts    0%{?__ztsphp:1}
%global with_tests  %{?_with_tests:1}%{!?_with_tests:0}
%if "%{php_version}" < "5.6"
# after igbinary
%global ini_name    %{pecl_name}.ini
%else
# after 40-igbinary
%global ini_name    50-%{pecl_name}.ini
%endif

Summary:       Extension for communicating with the Redis key-value store
Name:          %{?sub_prefix}php-pecl-redis
Version:       2.2.7
Release:       3%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/redis
Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
# https://github.com/nicolasff/phpredis/issues/332 - missing tests
Source1:       https://github.com/phpredis/phpredis/archive/%{version}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: %{?scl_prefix}php-devel
BuildRequires: %{?scl_prefix}php-pear
BuildRequires: %{?sub_prefix}php-pecl-igbinary-devel
# to run Test suite
%if %{with_tests}
BuildRequires: redis >= 2.6
%endif

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
# php-pecl-igbinary missing php-pecl(igbinary)%{?_isa}
Requires:      %{?sub_prefix}php-pecl-igbinary%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Obsoletes:     %{?scl_prefix}php-%{pecl_name}               < %{version}
Provides:      %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:      %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
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
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The phpredis extension provides an API for communicating
with the Redis key-value store.

This Redis client implements most of the latest Redis API.
As method only only works when also implemented on the server side,
some doesn't work with an old redis server version.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c -a 1

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/COPYING/s/role="doc"/role="src"/' } \
    -i package.xml

# rename source folder
mv %{pecl_name}-%{version} NTS
# tests folder from github archive
mv phpredis-%{version}/tests NTS/tests

cd NTS

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_REDIS_VERSION/{s/.* "//;s/".*$//;p}' php_redis.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif

# Drop in the bit of configuration
cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension = %{pecl_name}.so

; phpredis can be used to store PHP sessions. 
; To do this, uncomment and configure below

; RPM note : save_handler and save_path are defined
; for mod_php, in /etc/httpd/conf.d/php.conf
; for php-fpm, in %{_sysconfdir}/php-fpm.d/*conf

;session.save_handler = %{pecl_name}
;session.save_path = "tcp://host1:6379?weight=1, tcp://host2:6379?weight=2&timeout=2.5, tcp://host3:6379?weight=2"
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --enable-redis \
    --enable-redis-session \
    --enable-redis-igbinary \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --enable-redis \
    --enable-redis-session \
    --enable-redis-igbinary \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
# Install the ZTS stuff
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Documentation
cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
# simple module load test
%{__php} --no-php-ini \
    --define extension=igbinary.so \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
%{__ztsphp} --no-php-ini \
    --define extension=igbinary.so \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif

%if %{with_tests}
cd NTS/tests

# this test requires redis >= 2.6.9
# https://github.com/nicolasff/phpredis/pull/333
sed -e s/testClient/SKIP_testClient/ \
    -i TestRedis.php

# Launch redis server
mkdir -p {run,log,lib}/redis
sed -e "s:/^pidfile.*$:/pidfile $PWD/run/redis.pid:" \
    -e "s:/var:$PWD:" \
    -e "/daemonize/s/no/yes/" \
    /etc/redis.conf >redis.conf
# port number to allow 32/64 build at same time
# and avoid conflict with a possible running server
%if 0%{?__isa_bits}
port=$(expr %{__isa_bits} + 6350)
%else
%ifarch x86_64
port=6414
%else
port=6382
%endif
%endif
sed -e "s/6379/$port/" -i redis.conf
sed -e "s/6379/$port/" -i TestRedis.php
%{_bindir}/redis-server ./redis.conf

# Run the test Suite
ret=0
%{__php} --no-php-ini \
    --define extension=igbinary.so \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    TestRedis.php || ret=1

# Cleanup
if [ -f run/redis.pid ]; then
   %{_bindir}/redis-cli -p $port shutdown
fi

exit $ret

%else
: Upstream test suite disabled
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
%{?_licensedir:%license NTS/COPYING}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%{php_extdir}/%{pecl_name}.so
%config(noreplace) %{php_inidir}/%{ini_name}

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%endif


%changelog
* Wed Mar  9 2016 Remi Collet <remi@fedoraproject.org> - 2.2.7-3
- adapt for F24

* Sat Jun 20 2015 Remi Collet <remi@fedoraproject.org> - 2.2.7-2
- allow build against rh-php56 (as more-php56)

* Tue Mar 03 2015 Remi Collet <remi@fedoraproject.org> - 2.2.7-1
- Update to 2.2.7 (stable)
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 2.2.5-5.1
- Fedora 21 SCL mass rebuild

* Fri Oct  3 2014 Remi Collet <rcollet@redhat.com> - 2.2.5-5
- fix segfault with igbinary serializer
  https://github.com/nicolasff/phpredis/issues/341

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 2.2.5-4
- improve SCL build

* Wed Apr 16 2014 Remi Collet <remi@fedoraproject.org> - 2.2.5-3
- add numerical prefix to extension configuration file (php 5.6)
- add comment about session configuration

* Thu Mar 20 2014 Remi Collet <rcollet@redhat.com> - 2.2.5-2
- fix memory corruption with PHP 5.6
  https://github.com/nicolasff/phpredis/pull/447

* Wed Mar 19 2014 Remi Collet <remi@fedoraproject.org> - 2.2.5-1
- Update to 2.2.5

* Wed Mar 19 2014 Remi Collet <rcollet@redhat.com> - 2.2.4-3
- allow SCL build

* Fri Feb 28 2014 Remi Collet <remi@fedoraproject.org> - 2.2.4-2
- cleaups
- move doc in pecl_docdir

* Mon Sep 09 2013 Remi Collet <remi@fedoraproject.org> - 2.2.4-1
- Update to 2.2.4

* Tue Apr 30 2013 Remi Collet <remi@fedoraproject.org> - 2.2.3-1
- update to 2.2.3
- upstream moved to pecl, rename from php-redis to php-pecl-redis

* Tue Sep 11 2012 Remi Collet <remi@fedoraproject.org> - 2.2.2-5.git6f7087f
- more docs and improved description

* Sun Sep  2 2012 Remi Collet <remi@fedoraproject.org> - 2.2.2-4.git6f7087f
- latest snahot (without bundled igbinary)
- remove chmod (done upstream)

* Sat Sep  1 2012 Remi Collet <remi@fedoraproject.org> - 2.2.2-3.git5df5153
- run only test suite with redis > 2.4

* Fri Aug 31 2012 Remi Collet <remi@fedoraproject.org> - 2.2.2-2.git5df5153
- latest master
- run test suite

* Wed Aug 29 2012 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- update to 2.2.2
- enable ZTS build

* Tue Aug 28 2012 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- initial package
