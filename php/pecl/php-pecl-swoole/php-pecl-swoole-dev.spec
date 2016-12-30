# remirepo spec file for php-pecl-swoole
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package       php-pecl-swoole
%endif

%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name  swoole
%if "%{php_version}" < "5.6"
# After sockets
%global ini_name    %{pecl_name}.ini
%else
# After 20-sockets
%global ini_name    40-%{pecl_name}.ini
%endif

%if 0%{?fedora} >= 22 || 0%{?rhel} >= 6
%global with_nghttpd2 1
%else
%global with_nghttpd2 0
%endif
%global with_hiredis  1

Summary:        PHP's asynchronous concurrent distributed networking framework
Name:           %{?sub_prefix}php-pecl-%{pecl_name}
Version:        2.0.5
Release:        1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRequires:  %{?scl_prefix}php-devel >= 5.5
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-sockets
BuildRequires:  %{?scl_prefix}php-mysqli
BuildRequires:  pcre-devel
BuildRequires:  openssl-devel
%if %{with_nghttpd2}
BuildRequires:  libnghttp2-devel
%endif
%if %{with_hiredis}
BuildRequires:  hiredis-devel
%endif

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
Event-driven asynchronous and concurrent networking engine with
high performance for PHP.
- event-driven
- asynchronous non-blocking
- multi-thread reactor
- multi-process worker
- multi-protocol
- millisecond timer
- async mysql client
- built-in http/websocket/http2 server
- async http/websocket client
- async redis client
- async task
- async read/write file system
- async dns lookup
- support IPv4/IPv6/UnixSocket/TCP/UDP
- support SSL/TLS encrypted transmission

Documentation: https://rawgit.com/tchiotludo/swoole-ide-helper/english/docs/

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

# Don't install/register tests, install examples as doc
sed -e 's/role="test"/role="src"/' \
    -e '/examples/s/role="src"/role="doc"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml


cd NTS
# Sanity check, really often broken
extver=$(sed -n '/#define PHP_SWOOLE_VERSION/{s/.* "//;s/".*$//;p}' php_swoole.h)
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
cat << 'EOF' | tee %{ini_name}
; Enable %{summary} extension module
extension=%{pecl_name}.so

; Configuration
;swoole.aio_thread_num = 2
;swoole.display_errors = On
;swoole.use_namespace = On
;swoole.message_queue_key = 0
;swoole.unixsock_buffer_size = 8388608
EOF


%build
peclbuild() {
%configure \
    --with-swoole \
    --enable-openssl \
    --enable-sockets \
    --enable-coroutine \
%if %{with_nghttpd2}
    --enable-http2 \
%endif
%if %{with_hiredis}
    --enable-async-redis \
%endif
    --with-php-config=$1

make %{?_smp_mflags}
}

cd NTS
%{_bindir}/phpize
peclbuild %{_bindir}/php-config

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
peclbuild %{_bindir}/zts-php-config
%endif


%install
make -C NTS \
     install INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS \
     install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
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
[ -f %{php_extdir}/sockets.so ] && modules="-d extension=sockets.so"

cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    $modules \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    $modules \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


%files
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
* Fri Dec 30 2016 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- Update to 2.0.5 (beta)
- raise dependency on PHP 5.5

* Fri Dec 30 2016 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4 (beta)
- open https://github.com/swoole/swoole-src/issues/987 - Options
- open https://github.com/swoole/swoole-src/issues/989 - ZTS build
- disable ZTS extension for now
- open https://github.com/swoole/swoole-src/issues/990 - PHP 5.4

* Fri Dec 23 2016 Remi Collet <remi@fedoraproject.org> - 1.9.3-1
- Update to 1.9.3

* Mon Dec 19 2016 Remi Collet <remi@fedoraproject.org> - 1.9.2-1
- Update to 1.9.2

* Wed Dec  7 2016 Remi Collet <remi@fedoraproject.org> - 1.9.1-1
- Update to 1.9.1

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 1.9.0-2
- rebuild with PHP 7.1.0 GA

* Tue Nov 22 2016 Remi Collet <remi@fedoraproject.org> - 1.9.0-1
- Update to 1.9.0

* Tue Oct 25 2016 Remi Collet <remi@fedoraproject.org> - 1.8.13-1
- Update to 1.8.13

* Fri Sep 30 2016 Remi Collet <remi@fedoraproject.org> - 1.8.12-1
- Update to 1.8.12

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 1.8.11-2
- rebuild for PHP 7.1 new API version

* Fri Sep 09 2016 Remi Collet <remi@fedoraproject.org> - 1.8.11-1
- Update to 1.8.11

* Thu Sep 01 2016 Remi Collet <remi@fedoraproject.org> - 1.8.10-1
- Update to 1.8.10

* Thu Sep 01 2016 Remi Collet <remi@fedoraproject.org> - 1.8.9-1
- Update to 1.8.9

* Thu Jul 28 2016 Remi Collet <remi@fedoraproject.org> - 1.8.8-2
- add upstream patch and add back --enable-http2 build option

* Thu Jul 28 2016 Remi Collet <remi@fedoraproject.org> - 1.8.8-1
- Update to 1.8.8
- drop --enable-http2 build option (broken)
  open https://github.com/swoole/swoole-src/issues/787

* Fri Jul 01 2016 Remi Collet <remi@fedoraproject.org> - 1.8.7-1
- Update to 1.8.7

* Thu Jun 16 2016 Remi Collet <remi@fedoraproject.org> - 1.8.6-1
- Update to 1.8.6
- drop --enable-async-mysql and --enable-async-httpclient
  removed upstream

* Thu May 12 2016 Remi Collet <remi@fedoraproject.org> - 1.8.5-1
- Update to 1.8.5

* Wed Apr 13 2016 Remi Collet <remi@fedoraproject.org> - 1.8.4-1
- Update to 1.8.4 (stable)

* Mon Mar 21 2016 Remi Collet <remi@fedoraproject.org> - 1.8.3-1
- Update to 1.8.3 (stable)

* Wed Mar 02 2016 Remi Collet <remi@fedoraproject.org> - 1.8.2-1
- Update to 1.8.2 (stable)
- add --enable-openssl, --enable-async-httpclient
  --enable-http2 and --enable-async-redis to build options

* Thu Feb  4 2016 Remi Collet <remi@fedoraproject.org> - 1.8.1-1
- Update to 1.8.1 (stable)

* Wed Jan 27 2016 Remi Collet <remi@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0 (stable)

* Thu Dec 31 2015 Remi Collet <remi@fedoraproject.org> - 1.7.22-2
- Update to 1.7.22 (new sources)

* Thu Dec 31 2015 Remi Collet <remi@fedoraproject.org> - 1.7.22-1
- Update to 1.7.22
- add patch to fix PHP 7 build
  open https://github.com/swoole/swoole-src/pull/462
  open https://github.com/swoole/swoole-src/issues/461

* Tue Dec 01 2015 Remi Collet <remi@fedoraproject.org> - 1.7.21-1
- Update to 1.7.21

* Wed Oct 21 2015 Remi Collet <remi@fedoraproject.org> - 1.7.20-1
- Update to 1.7.20

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 1.7.19-4
- rebuild for PHP 7.0.0RC5 new API version

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 1.7.19-3
- F23 rebuild with rh_layout

* Thu Sep  3 2015 Remi Collet <remi@fedoraproject.org> - 1.7.19-2
- allow build against rh-php56 (as more-php56)

* Mon Aug 31 2015 Remi Collet <remi@fedoraproject.org> - 1.7.19-1
- Update to 1.7.19

* Thu Jul 23 2015 Remi Collet <remi@fedoraproject.org> - 1.7.18-1
- Update to 1.7.18

* Mon Jun 01 2015 Remi Collet <remi@fedoraproject.org> - 1.7.17-1
- Update to 1.7.17

* Fri May 08 2015 Remi Collet <remi@fedoraproject.org> - 1.7.16-1
- Update to 1.7.16

* Tue Apr 14 2015 Remi Collet <remi@fedoraproject.org> - 1.7.15-1
- Update to 1.7.15

* Thu Mar 26 2015 Remi Collet <remi@fedoraproject.org> - 1.7.14-1
- Update to 1.7.14

* Wed Mar 18 2015 Remi Collet <remi@fedoraproject.org> - 1.7.13-1
- Update to 1.7.13

* Thu Mar 12 2015 Remi Collet <remi@fedoraproject.org> - 1.7.12-1
- Update to 1.7.12

* Tue Mar 10 2015 Remi Collet <remi@fedoraproject.org> - 1.7.11-2
- rebuild with new sources

* Tue Mar 10 2015 Remi Collet <remi@fedoraproject.org> - 1.7.11-1
- Update to 1.7.11

* Sun Feb 15 2015 Remi Collet <remi@fedoraproject.org> - 1.7.10-1
- Update to 1.7.10
- drop runtime dependency on pear, new scriptlets

* Wed Jan 07 2015 Remi Collet <remi@fedoraproject.org> - 1.7.9-1
- Update to 1.7.9

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.7.8-1.1
- Fedora 21 SCL mass rebuild

* Wed Nov 26 2014 Remi Collet <remi@fedoraproject.org> - 1.7.8-1
- Update to 1.7.8 (stable)

* Tue Oct 28 2014 Remi Collet <remi@fedoraproject.org> - 1.7.7-1
- Update to 1.7.7 (stable)

* Fri Oct 10 2014 Remi Collet <remi@fedoraproject.org> - 1.7.6-1
- Update to 1.7.6 (stable)

* Wed Sep 10 2014 Remi Collet <remi@fedoraproject.org> - 1.7.5-1
- Update to 1.7.5 (stable)

* Tue Aug 26 2014 Remi Collet <rcollet@redhat.com> - 1.7.4-2
- improve SCL build

* Tue Jul 15 2014 Remi Collet <remi@fedoraproject.org> - 1.7.4-1
- Update to 1.7.4 (stable)

* Fri Jun 20 2014 Remi Collet <remi@fedoraproject.org> - 1.7.3-1
- Update to 1.7.3 (stable)

* Fri May 30 2014 Remi Collet <remi@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2 (stable)
- open https://github.com/matyhtf/swoole/pull/67 (fix EL5 build)

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1 (stable)

* Wed Apr 16 2014 Remi Collet <remi@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Sun Apr 13 2014 Remi Collet <remi@fedoraproject.org> - 1.6.12-1
- Update to 1.6.12

* Fri Feb 28 2014 Remi Collet <remi@fedoraproject.org> - 1.6.11-2
- no --enable-async-mysql with php 5.3

* Thu Feb 27 2014 Remi Collet <remi@fedoraproject.org> - 1.6.11-1
- Update to 1.6.11

* Sun Jan 26 2014 Remi Collet <remi@fedoraproject.org> - 1.6.10-1
- Update to 1.6.10

* Thu Jan 02 2014 Remi Collet <remi@fedoraproject.org> - 1.6.9-1
- Update to 1.6.9 (stable)

* Mon Dec 30 2013 Remi Collet <remi@fedoraproject.org> - 1.6.8-1
- Update to 1.6.8 (stable)

* Tue Dec 24 2013 Remi Collet <rcollet@redhat.com> - 1.6.7-1
- initial package, version 1.6.7 (stable)
- open https://github.com/matyhtf/swoole/issues/14 - archive
- open https://github.com/matyhtf/swoole/issues/15 - php 5.5
