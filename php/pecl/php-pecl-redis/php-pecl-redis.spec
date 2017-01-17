# remirepo spec file for php-pecl-redis
# adapted for scl, from
#
# Fedora spec file for php-pecl-redis
#
# Copyright (c) 2012-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package       php-pecl-redis
%else
%global _root_bindir %{_bindir}
%endif

%global pecl_name   redis
%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
%global with_tests  1%{?_with_tests:1}
%global with_igbin  1
%if "%{php_version}" < "5.6"
# after igbinary
%global ini_name    %{pecl_name}.ini
%else
# after 40-igbinary
%global ini_name    50-%{pecl_name}.ini
%endif
%global prever      RC2

Summary:       Extension for communicating with the Redis key-value store
Name:          %{?sub_prefix}php-pecl-redis
Version:       3.1.1
Release:       0.2.%{prever}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/redis

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: %{?scl_prefix}php-devel
BuildRequires: %{?scl_prefix}php-pear
%if %{with_igbin}
BuildRequires: %{?sub_prefix}php-pecl-igbinary-devel
%endif
# to run Test suite
%if %{with_tests}
BuildRequires: redis >= 3
%endif

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
%if %{with_igbin}
Requires:      %{?sub_prefix}php-pecl(igbinary)%{?_isa}
%endif
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
%setup -q -c
# rename source folder
mv %{pecl_name}-%{version}%{?prever} NTS

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/COPYING/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_REDIS_VERSION/{s/.* "//;s/".*$//;p}' php_redis.h)
if test "x${extver}" != "x%{version}%{?gh_date:-dev}%{?prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?gh_date:-dev}%{?prever}.
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

; Configuration
;redis.arrays.names = ''
;redis.arrays.hosts = ''
;redis.arrays.previous = ''
;redis.arrays.functions = ''
;redis.arrays.index = ''
;redis.arrays.autorehash = ''
;redis.clusters.seeds = ''
;redis.clusters.timeout = ''
;redis.clusters.read_timeout = ''
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --enable-redis \
    --enable-redis-session \
%if %{with_igbin}
    --enable-redis-igbinary \
%endif
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --enable-redis \
    --enable-redis-session \
%if %{with_igbin}
    --enable-redis-igbinary \
%endif
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
%if %{with_igbin}
    --define extension=igbinary.so \
%endif
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
%{__ztsphp} --no-php-ini \
%if %{with_igbin}
    --define extension=igbinary.so \
%endif
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif

%if %{with_tests}
cd NTS/tests

# Launch redis server
mkdir -p data
pidfile=$PWD/redis.pid
port=$(%{__php} -r 'echo 9000 + PHP_MAJOR_VERSION*100 + PHP_MINOR_VERSION*10 + PHP_INT_SIZE;')
%{_root_bindir}/redis-server   \
    --bind      127.0.0.1      \
    --port      $port          \
    --daemonize yes            \
    --logfile   $PWD/redis.log \
    --dir       $PWD/data      \
    --pidfile   $pidfile

sed -e "s/6379/$port/" -i RedisTest.php

# Run the test Suite
ret=0
%{__php} --no-php-ini \
%if %{with_igbin}
    --define extension=igbinary.so \
%endif
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    TestRedis.php || ret=1

# Cleanup
if [ -f $pidfile ]; then
   %{_root_bindir}/redis-cli -p $port shutdown
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
* Tue Jan 17 2017 Remi Collet <remi@fedoraproject.org> - 3.1.1-0.2.RC2
- Update to 3.1.1RC2

* Thu Dec 22 2016 Remi Collet <remi@fedoraproject.org> - 3.1.1-0.1.RC1
- test build for open upcoming 3.1.1RC1

* Wed Dec 21 2016 Remi Collet <remi@fedoraproject.org> - 3.1.1-0
- test build for open upcoming 3.1.1

* Thu Dec 15 2016 Remi Collet <remi@fedoraproject.org> - 3.1.0-2
- test build for open upcoming 3.1.1
- open https://github.com/phpredis/phpredis/issues/1060 broken impl
  with https://github.com/phpredis/phpredis/pull/1064
- reed https://github.com/phpredis/phpredis/issues/1062 session php 7.1
  with https://github.com/phpredis/phpredis/pull/1063

* Thu Dec 15 2016 Remi Collet <remi@fedoraproject.org> - 3.1.0-1
- update to 3.1.0
- open https://github.com/phpredis/phpredis/issues/1052 max version
- open https://github.com/phpredis/phpredis/issues/1053 segfault
- open https://github.com/phpredis/phpredis/issues/1054 warnings
- open https://github.com/phpredis/phpredis/issues/1055 reflection
- open https://github.com/phpredis/phpredis/issues/1056 32bits tests

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-3
- rebuild with PHP 7.1.0 GA

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-2
- rebuild for PHP 7.1 new API version

* Sat Jun 11 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0 (stable)

* Thu Jun  9 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.1.20160603git6447940
- refresh and bump version

* Thu May  5 2016 Remi Collet <remi@fedoraproject.org> - 2.2.8-0.6.20160504gitad3c116
- refresh

* Thu Mar  3 2016 Remi Collet <remi@fedoraproject.org> - 2.2.8-0.5.20160215git2887ad1
- enable igbinary support

* Fri Feb 19 2016 Remi Collet <remi@fedoraproject.org> - 2.2.8-0.4.20160215git2887ad1
- refresh

* Thu Feb 11 2016 Remi Collet <remi@fedoraproject.org> - 2.2.8-0.3.20160208git0d4b421
- refresh

* Tue Jan 26 2016 Remi Collet <remi@fedoraproject.org> - 2.2.8-0.2.20160125git7b36957
- refresh

* Sun Jan 10 2016 Remi Collet <remi@fedoraproject.org> - 2.2.8-0.2.20160106git4a37e47
- improve package.xml, set stability=devel

* Sun Jan 10 2016 Remi Collet <remi@fedoraproject.org> - 2.2.8-0.1.20160106git4a37e47
- update to 2.2.8-dev for PHP 7
- use git snapshot

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
