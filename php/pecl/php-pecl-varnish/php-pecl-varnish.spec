# remirepo spec file for php-pecl-varnish
#
# Copyright (c) 2013-2017 Remi Collet
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

%{?scl:          %scl_package        php-pecl-varnish}

%global with_zts   0%{?__ztsphp:1}
%global pecl_name  varnish
%global with_tests %{?_with_tests:1}%{!?_with_tests:0}
%if "%{php_version}" < "5.6"
%global ini_name   %{pecl_name}.ini
%else
%global ini_name   40-%{pecl_name}.ini
%endif

Summary:        Varnish Cache bindings
Name:           %{?sub_prefix}php-pecl-%{pecl_name}
Version:        1.2.2
Release:        2%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel > 5.3
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-hash
BuildRequires:  varnish-libs-devel > 3
# For tests
%if %{with_tests}
BuildRequires:  varnish
%endif

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-hash%{?_isa}

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
Varnish Cache is an open source, state of the art web application accelerator.

The extension makes it possible to interact with a running varnish instance
through TCP socket or shared memory.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_VARNISH_VERSION/{s/.* "//;s/".*$//;p}' php_varnish.h)
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
ret=0

: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=NTS/modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=ZTS/modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif

%if %{with_tests}
cd NTS

: Run a varnish server for test suite
sed -n '/secret/{s/.* "//;s/".*$//;p}' \
    tests/config.php-dist | tail -n 1 | tee /tmp/secret

if [ 0%{?__isa_bits} -eq 64 ]; then
    PORTUSR=6085
    PORTADM=6086
else
    PORTUSR=6081
    PORTADM=6082
fi
%{_sbindir}/varnishd \
  -b 127.0.0.1:80 \
  -P /tmp/varnish.pid \
  -S /tmp/secret \
  -s file,/tmp,1G \
  -n /tmp/vtest \
  -a :$PORTUSR \
  -T :$PORTADM

export VARNISH_TEST_IPV4=1
export VARNISH_TEST_IPV6=1
export VARNISH_TEST_SECRET=1
export VARNISH_TEST_SHM=0

: Upstream test suite for NTS extension
sed -e 's:/var/lib/varnish/silent:/tmp/vtest:' \
    -e "s/6081/$PORTUSR/" \
    -e "s/6082/$PORTADM/" \
    tests/config.php-dist | tee tests/config.php

TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff || ret=1

%if %{with_zts}
cd ../ZTS

: Upstream test suite for ZTS extension
sed -e 's:/var/lib/varnish/silent:/tmp/vtest:' \
    -e "s/6081/$PORTUSR/" \
    -e "s/6082/$PORTADM/" \
    tests/config.php-dist | tee tests/config.php

TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff || ret=1
%endif

: Stop the test server
[ -s /tmp/varnish.pid ] && kill $(cat /tmp/varnish.pid)
rm -rf /tmp/{secret,varnish.pid,vtest}

exit $ret
%else
: Upstream test suite disabled, missing '--with tests' option.
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{pecl_name}
%{?_licensedir:%license NTS/LICENSE}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-2
- rebuild with PHP 7.1.0 GA

* Tue Oct 25 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2

* Thu Oct 20 2016 Remi Collet <remi@fedoraproject.org> - 1.2.1-9
- add patch for varnish 4.1 (F24) and 5.0 (F25)

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 1.2.1-8
- rebuild for PHP 7.1 new API version

* Sun Mar  6 2016 Remi Collet <remi@fedoraproject.org> - 1.2.1-7
- adapt for F24

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 1.2.1-6
- rebuild for PHP 7.0.0RC5 new API version

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 1.2.1-5
- F23 rebuild with rh_layout

* Wed Jul 22 2015 Remi Collet <remi@fedoraproject.org> - 1.2.1-4
- rebuild against php 7.0.0beta2

* Wed Jul  8 2015 Remi Collet <remi@fedoraproject.org> - 1.2.1-3
- rebuild against php 7.0.0beta1

* Wed Jun 24 2015 Remi Collet <remi@fedoraproject.org> - 1.2.1-2
- allow build against rh-php56 (as more-php56)
- rebuild for "rh_layout" (php70)

* Sat Feb 14 2015 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1

* Sat Feb 14 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0
- don't install test suite
- drop runtime dependency on pear, new scriptlets
- add upstream build patches

* Tue Aug 26 2014 Remi Collet <rcollet@redhat.com> - 1.1.1-3
- allow SCL build

* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 1.1.1-2
- add numerical prefix to extension configuration file (php 5.6)

* Sun Oct 20 2013 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1
- install doc in pecl doc_dir
- install tests in pecl test_dir

* Wed Oct 02 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0
- License now provided in upstream sources
- Drop merged patch for configure
- Use sha256 from hash extension instead of bundled copy
- Add option --with tests to run upstream test suite

* Mon Sep 30 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package

