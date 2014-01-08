# spec file for php-pecl-yaf
#
# Copyright (c) 2012-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package        php-pecl-fann}
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global with_zts  0%{?__ztsphp:1}
%global pecl_name yaf

Summary:       Yet Another Framework
Name:          %{?scl_prefix}php-pecl-yaf
Version:       2.3.0
Release:       1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/yaf
Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source1:       %{pecl_name}.ini

# https://github.com/laruence/php-yaf/issues/82
Source2:       https://raw.github.com/laruence/php-yaf/yaf-2.3.0/requests/yaf_request_http.h
Source3:       https://raw.github.com/laruence/php-yaf/yaf-2.3.0/requests/yaf_request_simple.h
Source4:       https://raw.github.com/laruence/php-yaf/yaf-2.3.0/responses/yaf_response_http.h
Source5:       https://raw.github.com/laruence/php-yaf/yaf-2.3.0/responses/yaf_response_cli.h
Source6:       https://raw.github.com/laruence/php-yaf/yaf-2.3.0/views/yaf_view_interface.h
Source7:       https://raw.github.com/laruence/php-yaf/yaf-2.3.0/views/yaf_view_simple.h
Source8:       https://raw.github.com/laruence/php-yaf/yaf-2.3.0/configs/yaf_config_ini.h
Source9:       https://raw.github.com/laruence/php-yaf/yaf-2.3.0/configs/yaf_config_simple.h
Source10:      https://raw.github.com/laruence/php-yaf/yaf-2.3.0/routes/yaf_route_interface.h
Source11:      https://raw.github.com/laruence/php-yaf/yaf-2.3.0/routes/yaf_route_simple.h
Source12:      https://raw.github.com/laruence/php-yaf/yaf-2.3.0/routes/yaf_route_static.h
Source13:      https://raw.github.com/laruence/php-yaf/yaf-2.3.0/routes/yaf_route_regex.h
Source14:      https://raw.github.com/laruence/php-yaf/yaf-2.3.0/routes/yaf_route_map.h
Source15:      https://raw.github.com/laruence/php-yaf/yaf-2.3.0/routes/yaf_route_rewrite.h
Source16:      https://raw.github.com/laruence/php-yaf/yaf-2.3.0/routes/yaf_route_supervar.h
Source17:      https://raw.github.com/laruence/php-yaf/yaf-2.3.0/tests/multi-section.ini

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: %{?scl_prefix}php-devel >= 5.2.0
BuildRequires: %{?scl_prefix}php-pear
BuildRequires: pcre-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}

Provides:      %{?scl_prefix}php-%{pecl_name} = %{version}
Provides:      %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}

%if 0%{!?scl:1}
# Other third party repo stuff
%if "%{php_version}" > "5.4"
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
Obsoletes:     php54-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}
%endif
%endif

%if 0%{?fedora} < 20
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The Yet Another Framework (Yaf) extension is a PHP framework that is used
to develop web applications. 


%prep
%setup -q -c 
mv %{pecl_name}-%{version} NTS

cp %{SOURCE2} %{SOURCE3} NTS/requests/
cp %{SOURCE4} %{SOURCE5} NTS/responses/
cp %{SOURCE6} %{SOURCE7} NTS/views/
cp %{SOURCE8} %{SOURCE9} NTS/configs/
cp %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} %{SOURCE16} NTS/routes/
cp %{SOURCE17} NTS/tests/

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_YAF_VERSION/{s/.*\t"//;s/".*$//;p}' NTS/php_yaf.h )
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}
# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini

# Install the ZTS stuff
%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

# Install the package XML file
install -D -m 644 package2.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Test & Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite  for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite  for NTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php
%endif


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{pecl_name}
%doc %{pecl_testdir}/%{pecl_name}

%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%endif


%changelog
* Wed Jan 08 2014 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0 (beta)
- install doc in pecl doc_dir
- install tests in pecl test_dir
- adapt for SCL
- add missing files from upstream git repo
  https://github.com/laruence/php-yaf/issues/82

* Fri Jan  4 2013 Remi Collet <remi@fedoraproject.org> - 2.2.9-1
- version 2.2.9 (stable)

* Tue Dec 18 2012 Remi Collet <remi@fedoraproject.org> - 2.2.8-1
- version 2.2.8 (stable)

* Mon Nov 19 2012 Remi Collet <remi@fedoraproject.org> - 2.2.7-1
- version 2.2.7 (stable)

* Thu Nov  1 2012 Remi Collet <remi@fedoraproject.org> - 2.2.6-1
- version 2.2.6 (stable)

* Mon Oct 22 2012 Remi Collet <remi@fedoraproject.org> - 2.2.5-1
- version 2.2.5 (stable)
- LICENSE now provided by upstream

* Tue Sep  4 2012 Remi Collet <remi@fedoraproject.org> - 2.2.4-1
- version 2.2.4 (beta)
- initial package