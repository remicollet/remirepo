# spec file for php-pecl-varnish
#
# Copyright (c) 2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global with_zts   0%{?__ztsphp:1}
%global pecl_name  varnish
%global with_tests %{?_with_tests:1}%{!?_with_tests:0}

Summary:        Varnish Cache bindings
Name:           php-pecl-%{pecl_name}
Version:        1.1.1
Release:        1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel > 5.3
BuildRequires:  php-pear
BuildRequires:  php-hash
BuildRequires:  varnish-libs-devel > 3
# For tests
%if %{with_tests}
BuildRequires:  varnish
%endif

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires:       php-hash%{?_isa}

Provides:       php-%{pecl_name} = %{version}
Provides:       php-%{pecl_name}%{?_isa} = %{version}
Provides:       php-pecl(%{pecl_name}) = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}

# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}

%description
Varnish Cache is an open source, state of the art web application accelerator.

The extension makes it possible to interact with a running varnish instance
through TCP socket or shared memory.


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

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

make -C NTS \
     install INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS \
     install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

# Test & Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


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
%{__php} -n run-tests.php || ret=1

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
%{__ztsphp} -n run-tests.php || ret=1
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
%doc %{pecl_testdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
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
