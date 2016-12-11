# remirepo spec file for php-pecl-judy
# With SCL stuff, from Fedora:
#
# Fedora spec file for php-pecl-judy
#
# Copyright (c) 2013-2016 Remi Collet
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

%{?scl:          %scl_package        php-pecl-judy}

%global with_zts   0%{?__ztsphp:1}
%global pecl_name  Judy
%global  ext_name  judy
%if "%{php_version}" < "5.6"
%global ini_name   %{ext_name}.ini
%else
%global ini_name   40-%{ext_name}.ini
%endif

Summary:        PHP Judy implements sparse dynamic arrays
Name:           %{?sub_prefix}php-pecl-judy
Version:        1.0.2
Release:        5%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel > 5.3
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  Judy-devel
BuildRequires:  pcre-devel

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-spl%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{ext_name}                = %{version}
Provides:       %{?scl_prefix}php-%{ext_name}%{?_isa}        = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl-%{ext_name}           = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{ext_name}%{?_isa}   = %{version}-%{release}

# Package have been renamed
Obsoletes:      %{?scl_prefix}php-pecl-Judy < 1.0.1
Provides:       %{?scl_prefix}php-pecl-Judy = %{version}-%{release}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
Obsoletes:     php53-pecl-%{ext_name}  <= %{version}
Obsoletes:     php53u-pecl-%{ext_name} <= %{version}
Obsoletes:     php54-pecl-%{ext_name}  <= %{version}
Obsoletes:     php54w-pecl-%{ext_name} <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{ext_name} <= %{version}
Obsoletes:     php55w-pecl-%{ext_name} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{ext_name} <= %{version}
Obsoletes:     php56w-pecl-%{ext_name} <= %{version}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-pecl-%{ext_name} <= %{version}
Obsoletes:     php70w-pecl-%{ext_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
PHP Judy implements sparse dynamic arrays (aka Judy Arrays).
This extension is based on the Judy C library. A Judy array
consumes memory only when it is populated, yet can grow to
take advantage of all available memory if desired. Judy's key
benefits are scalability, high performance, and memory efficiency.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%package devel
Summary:       %{name} developer files (header)
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{?scl_prefix}php-devel%{?_isa}
# Package have been renamed
Obsoletes:     %{?scl_prefix}php-pecl-Judy-devel < 1.0.1
Provides:      %{?scl_prefix}php-pecl-Judy-devel = %{version}-%{release}

%description devel
These are the files needed to compile programs using %{name}.


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

%{?_licensedir:sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml}

cd NTS
# Sanity check, really often broken
extver=$(sed -n '/#define PHP_JUDY_VERSION/{s/.* "//;s/".*$//;p}' php_judy.h)
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
; Enable %{pecl_name} extension module
extension=%{ext_name}.so
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

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Test & Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
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
: Minimal load test for NTS extension
cd NTS
%{__php} --no-php-ini \
    --define extension=modules/%{ext_name}.so \
    --modules | grep %{ext_name}

: Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{ext_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php


%if %{with_zts}
: Minimal load test for ZTS extension
cd ../ZTS
%{__ztsphp} --no-php-ini \
    --define extension=modules/%{ext_name}.so \
    --modules | grep %{ext_name}

: Upstream test suite for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{ext_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%exclude %{pecl_docdir}/%{pecl_name}/examples
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{ext_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{ext_name}.so
%endif


%files devel
%defattr(-,root,root,-)
%doc %{pecl_testdir}/%{pecl_name}
%doc %{pecl_docdir}/%{pecl_name}/examples
%{php_incldir}/ext/%{ext_name}

%if %{with_zts}
%{php_ztsincldir}/ext/%{ext_name}
%endif


%changelog
* Wed Mar  9 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-5
- adapt for F24

* Tue Jun 23 2015 Remi Collet <rcollet@redhat.com> - 1.0.2-4
- allow build against rh-php56 (as more-php56)
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-3.1
- Fedora 21 SCL mass rebuild

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 1.0.2-3
- improve SCL build

* Wed Apr 16 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-2
- use %%{ini_name} macro
- add numerical prefix to extension configuration file

* Fri Nov 29 2013 Remi Collet <rcollet@redhat.com> - 1.0.2-1
- adapt for SCL

* Sun Nov 03 2013 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2 (stable)

* Fri Nov 01 2013 Remi Collet <remi@fedoraproject.org> - 1.0.1-3
- missing BR pcre-devel

* Mon Oct 21 2013 Remi Collet <remi@fedoraproject.org> - 1.0.1-2
- move tests and examples in devel subpackage

* Mon Oct 21 2013 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- rename from php-pecl-Judy to php-pecl-judy
- Update to 1.0.1 (stable)
- install doc in pecl doc_dir
- install tests in pecl test_dir
- drop merged patches

* Thu Oct 10 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- fix extension name in configuration file

* Wed Oct  9 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package, version 1.0.0 (stable)
