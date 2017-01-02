# remirepo spec file for php-pecl-radius
# adapted for SCL, from:
#
# Fedora spec file for php-pecl-radius
#
# Copyright (c) 2009-2017 Remi Collet
# Copyright (c) 2006-2009 Christopher Stone
#
# License: MIT
# http://opensource.org/licenses/MIT
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

%{?scl:          %scl_package         php-pecl-radius}

%global pecl_name radius
%global with_zts  0%{!?_without_zts:%{?__ztsphp:1}}
%if "%{php_version}" < "5.6"
%global ini_name  %{pecl_name}.ini
%else
%global ini_name  40-%{pecl_name}.ini
%endif

Name:           %{?sub_prefix}php-pecl-radius
Version:        1.3.0
Release:        1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Summary:        Radius client library

License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/radius
Source0:        http://pecl.php.net/get/radius-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-pear
# Used by test suite
BuildRequires:  %{?scl_prefix}php-posix
BuildRequires:  %{?scl_prefix}php-sockets

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
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
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This package is based on the libradius of FreeBSD, with some modifications
and extensions.  This PECL provides full support for RADIUS authentication
(RFC 2865) and RADIUS accounting (RFC 2866), works on Unix and on Windows.
Its an easy way to authenticate your users against the user-database of your
OS (for example against Windows Active-Directory via IAS).

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -qc

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

mv %{pecl_name}-%{version} NTS
cd NTS

extver=$(sed -n '/#define PHP_RADIUS_VERSION/{s/.* "//;s/".*$//;p}' php_radius.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -Dpm644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
DEP=
[ -f %{php_extdir}/posix.so ]   && DEP="$DEP -d extension=posix.so"
[ -f %{php_extdir}/sockets.so ] && DEP="$DEP -d extension=sockets.so"

%if "%{php_version}" > "5.5"
# used fake_server is not compatible with php 5.5
# Deprecated: Non-static method xxx should not be called statically
rm -f $(grep -l fake_server ?TS/tests/*phpt)
%endif

# simple module load test
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite for NTS extension
cd NTS
TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n $DEP -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php

%if %{with_zts}
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite for ZTS extension
cd ../ZTS
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n $DEP -d extension=$PWD/modules/%{pecl_name}.so" \
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
* Mon Feb 15 2016 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0 (stable)

* Sat Jun 20 2015 Remi Collet <remi@fedoraproject.org> - 1.1.2-6
- allow build against rh-php56 (as more-php56)
- drop runtime dependency on pear, new scriptlets
- don't install/register tests

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-5.1
- Fedora 21 SCL mass rebuild

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 1.1.2-5
- improve SCL build

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-4
- add numerical prefix to extension configuration file

* Wed Mar 19 2014 Remi Collet <rcollet@redhat.com> - 1.1.2-3
- allow SCL build

* Sun Mar 16 2014 Remi Collet <remi@fedoraproject.org> - 1.2.7-2
- run upstream test suite
- install doc in pecl_docdir
- install tests in pecl_testdir
- add missing License file (extracted from headers)

* Fri Jun 28 2013 Remi Collet <remi@fedoraproject.org> - 1.2.7-1
- Update to 1.2.7

* Thu Jun 20 2013 Remi Collet <remi@fedoraproject.org> - 1.2.6-1
- Update to 1.2.6

* Fri Nov 18 2011 Remi Collet <rpms@famillecollet.com> 1.2.5-14
- also provides php-radius

* Fri Nov 18 2011 Remi Collet <rpms@famillecollet.com> 1.2.5-12
- php 5.4 build

* Thu Oct 06 2011 Remi Collet <rpms@famillecollet.com> 1.2.5-11
- ZTS extension
- spec cleanups

* Wed Jul  6 2011  Remi Collet <Fedora@FamilleCollet.com> - 1.2.5-11
- fix php_zend_api usage, fix FTBFS #715846

* Sat Oct 23 2010  Remi Collet <Fedora@FamilleCollet.com> - 1.2.5-10
- add filter_provides to avoid private-shared-object-provides ncurses.so

* Sat Aug 28 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.2.5-9
- clean define
- use more macros
- add simple load test in %%check

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.2.5-7
- rebuild for new PHP 5.3.0 ABI (20090626)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Apr 19 2008 Christopher Stone <chris.stone@gmail.com> 1.2.5-5
- Fix Requires for post/postun sections (bz #442699)

* Fri Feb 22 2008 Christopher Stone <chris.stone@gmail.com> 1.2.5-4
- Properly register package

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.5-3
- Autorebuild for GCC 4.3

* Sun Sep 30 2007 Christopher Stone <chris.stone@gmail.com> 1.2.5-2
- Update to new standards

* Sat Sep 08 2007 Christopher Stone <chris.stone@gmail.com> 1.2.5-1
- Upstream sync

* Sun Mar 11 2007 Christopher Stone <chris.stone@gmail.com> 1.2.4-2
- Use new ABI check for FC-6
- Create directory to untar sources
- Remove %%{release} from Provides

* Sat Jul 01 2006 Christopher Stone <chris.stone@gmail.com> 1.2.4-1
- Initial release
