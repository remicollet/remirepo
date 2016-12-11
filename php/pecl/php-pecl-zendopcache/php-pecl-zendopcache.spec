# spec file for php-pecl-zendopcache
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package        php-pecl-zendopcache}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%global with_zts   0%{?__ztsphp:1}
%global proj_name  ZendOpcache
%global pecl_name  zendopcache
%global plug_name  opcache

Name:          %{?scl_prefix}php-pecl-%{pecl_name}
Version:       7.0.5
Release:       2%{?dist}
Summary:       The Zend OPcache

Group:         Development/Libraries
License:       PHP
URL:           http://pecl.php.net/package/%{proj_name}
Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
# this extension must be loaded before XDebug
# So "opcache" if before "xdebug"
Source1:       %{plug_name}.ini
Source2:       %{plug_name}-default.blacklist

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: %{?scl_prefix}php-devel >= 5.2.0
BuildRequires: %{?scl_prefix}php-pear

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:      %{?scl_prefix}php-pecl(%{plug_name}) = %{version}%{?prever}
Provides:      %{?scl_prefix}php-pecl(%{plug_name})%{?_isa} = %{version}%{?prever}
Provides:      %{?scl_prefix}php-%{plug_name} = %{version}-%{release}
Provides:      %{?scl_prefix}php-%{plug_name}%{?_isa} = %{version}-%{release}
%if 0%{!?scl:1}
Obsoletes:     php-pecl-zendoptimizerplus < %{version}-%{release}
Provides:      php-pecl-zendoptimizerplus = %{version}-%{release}
Provides:      php-pecl-zendoptimizerplus%{?_isa} = %{version}-%{release}
%endif

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php53u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php54-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php54w-pecl-%{pecl_name} <= %{version}
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The Zend OPcache provides faster PHP execution through opcode caching and
optimization. It improves PHP performance by storing precompiled script
bytecode in the shared memory. This eliminates the stages of reading code from
the disk and compiling it on future access. In addition, it applies a few
bytecode optimization patterns that make code execution faster.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

pushd NTS

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_ZENDOPCACHE_VERSION/{s/.*"7/7/;s/".*$//;p}' ZendAccelerator.h)
if test "x${extver}" != "x%{version}%{?prever:-%{prever}}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever:-%{prever}}.
   exit 1
fi
popd

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure \
    --enable-opcache \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --enable-opcache \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# Configuration file
install -D -p -m 644 %{SOURCE1} %{buildroot}%{php_inidir}/%{plug_name}.ini
sed -e 's:@EXTPATH@:%{php_extdir}:' \
    -e 's:@INIPATH@:%{php_inidir}:' \
    -i %{buildroot}%{php_inidir}/%{plug_name}.ini


# The default Zend OPcache blacklist file
install -D -p -m 644 %{SOURCE2} %{buildroot}%{php_inidir}/%{plug_name}-default.blacklist

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}

install -D -p -m 644 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{plug_name}.ini
sed -e 's:@EXTPATH@:%{php_ztsextdir}:' \
    -e 's:@INIPATH@:%{php_ztsinidir}:' \
    -i %{buildroot}%{php_ztsinidir}/%{plug_name}.ini

install -D -p -m 644 %{SOURCE2} %{buildroot}%{php_ztsinidir}/%{plug_name}-default.blacklist
%endif

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%clean
rm -rf %{buildroot}


%check
# ignore this one, works manually, run-tests.php issue
rm ?TS/tests/is_script_cached.phpt

cd NTS
%{__php} \
    -n -d zend_extension=%{buildroot}%{php_extdir}/%{plug_name}.so \
    -m | grep "Zend OPcache"

TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d zend_extension=%{buildroot}%{php_extdir}/%{plug_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php

%if %{with_zts}
cd ../ZTS
%{__ztsphp} \
    -n -d zend_extension=%{buildroot}%{php_ztsextdir}/%{plug_name}.so \
    -m | grep "Zend OPcache"

TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d zend_extension=%{buildroot}%{php_ztsextdir}/%{plug_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php
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


%files
%defattr(-,root,root,-)
%{?_licensedir:%license NTS/LICENSE}
%config(noreplace) %{php_inidir}/%{plug_name}-default.blacklist
%config(noreplace) %{php_inidir}/%{plug_name}.ini
%{php_extdir}/%{plug_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{plug_name}-default.blacklist
%config(noreplace) %{php_ztsinidir}/%{plug_name}.ini
%{php_ztsextdir}/%{plug_name}.so
%endif

%{pecl_xmldir}/%{name}.xml


%changelog
* Thu Mar 10 2016 Remi Collet <remi@fedoraproject.org> - 7.0.5-2
- adapt for F24

* Tue Apr 14 2015 Remi Collet <remi@fedoraproject.org> - 7.0.5-1
- Update to 7.0.5

* Wed Apr  8 2015 Remi Collet <remi@fedoraproject.org> - 7.0.4-2
- fix use after free in opcache CVE-2015-1351
- drop runtime dependency on pear, new scriptlets

* Mon Jan 12 2015 Remi Collet <remi@fedoraproject.org> - 7.0.4-1
- Update to 7.0.4
- disable opcache.fast_shutdown in default configuration

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 7.0.3-2.1
- Fedora 21 SCL mass rebuild

* Sun Aug 31 2014 Remi Collet <rcollet@redhat.com> - 7.0.3-2
- allow SCL build
- make ZTS build optional

* Mon Jan 20 2014 Remi Collet <remi@fedoraproject.org> - 7.0.3-1
- Update to 7.0.3
- open https://github.com/zendtech/ZendOptimizerPlus/issues/162

* Tue Jan 14 2014 Remi Collet <rcollet@redhat.com> - 7.0.2-3
- drop conflicts with other opcode cache

* Mon Jul 15 2013 Remi Collet <rcollet@redhat.com> - 7.0.2-1
- fix ZTS configuration

* Wed Jun  5 2013 Remi Collet <rcollet@redhat.com> - 7.0.2-1
- update to 7.0.2
- add spec License = CC-BY-SA

* Thu Apr 11 2013 Remi Collet <rcollet@redhat.com> - 7.0.1-2
- allow wildcard in opcache.blacklist_filename and provide
  default /etc/php.d/opcache-default.blacklist

* Mon Mar 25 2013 Remi Collet <remi@fedoraproject.org> - 7.0.1-1
- official PECL release, version 7.0.1 (beta)
- rename to php-pecl-zendopcache

* Mon Mar 18 2013 Remi Collet <remi@fedoraproject.org> - 7.0.1-0.1.gitcef6093
- update to git snapshot, with new name (opcache)

* Sun Mar 10 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-2
- allow to install with APC >= 3.1.15 (user data cache)

* Tue Mar  5 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-1
- official PECL release, version 7.0.0 (beta)

* Thu Feb 28 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-0.7.gitd39a49a
- new snapshot
- run test suite during build

* Thu Feb 21 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-0.6.git3a06991
- new snapshot

* Fri Feb 15 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-0.4.git2b6eede
- new snapshot (ZTS fixes)

* Thu Feb 14 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-0.2.gitafb43f5
- new snapshot
- better default configuration file (new upstream recommendation)
- License file now provided by upstream

* Wed Feb 13 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-0.1.gitaafc145
- initial package
