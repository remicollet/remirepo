# spec file for php-horde-horde-lz4
#
# Copyright (c) 2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{?scl:         %scl_package        php-horde-horde-lz4}
%{!?php_inidir: %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:     %global __pecl      %{_bindir}/pecl}
%{!?__php:      %global __php       %{_bindir}/php}

%global with_zts     0%{?__ztsphp:1}
%global pecl_name    horde_lz4
%global pecl_channel pear.horde.org
%if "%{php_version}" < "5.6"
%global ini_name     %{pecl_name}.ini
%else
%global ini_name     40-%{pecl_name}.ini
%endif
%if 0%{?scl:1}
# PHPUnit not available in SCL
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Summary:        Horde LZ4 Compression Extension
Name:           %{?scl_prefix}php-horde-horde-lz4
Version:        1.0.7
Release:        1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}.1
License:        MIT
Group:          Development/Languages
URL:            http://www.horde.org
Source0:        http://%{pecl_channel}/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-channel(%{pecl_channel})
BuildRequires:  lz4-devel
%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
%endif

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-channel(%{pecl_channel})
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name} = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_channel}/%{pecl_name}) = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_channel}/%{pecl_name})%{?_isa} = %{version}

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
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
PHP extension that implements the LZ4 compression algorithm,
an extremely fast lossless compression algorithm.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection}.


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

cd NTS
# Use system library
rm -r lib
sed -e '/name="lib/d' -i ../package.xml

# Sanity check, really often broken
extver=$(sed -n '/#define HORDE_LZ4_EXT_VERSION/{s/.* "//;s/".*$//;p}' horde_lz4.h)
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
; Enable %{summary} module
extension=%{pecl_name}.so
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-liblz4 \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-liblz4 \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install-modules INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS install-modules INSTALL_ROOT=%{buildroot}

install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pear_docdir}/%{pecl_name}/$i
done


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_channel}/%{pecl_name} >/dev/null || :
fi


%check
cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_tests}
: Upstream test suite for NTS extension
%{__php} -d extension=modules/horde_lz4.so %{_bindir}/phpunit test
%endif

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_tests}
: Upstream test suite for ZTS extension
%{__ztsphp} -d extension=modules/horde_lz4.so %{_bindir}/phpunit test
%endif
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> 1.0.7-1.1
- Fedora 21 SCL mass rebuild

* Tue Sep 16 2014 Remi Collet <remi@fedoraproject.org> - 1.0.7-1
- Update to 1.0.7
- https://github.com/horde/horde/pull/103 is merged

* Mon Sep 15 2014 Remi Collet <remi@fedoraproject.org> - 1.0.6-1
- initial package, version 1.0.6