# spec file for php-pecl-swoole
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package        php-pecl-swoole}
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global with_zts   0%{?__ztsphp:1}
%global pecl_name  swoole

Summary:        PHP's asynchronous concurrent distributed networking framework
Name:           %{?scl_prefix}php-pecl-%{pecl_name}
Version:        1.6.11
Release:        2%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-sockets
BuildRequires:  %{?scl_prefix}php-mysqli

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%if "%{php_version}" < "5.4"
# php 5.3.3 in EL-6 don't use arched virtual provides
# so only requires real packages instead
Requires:       %{?scl_prefix}php-common%{?_isa}
%else
Requires:       %{?scl_prefix}php-sockets%{?_isa}
%endif

Provides:       %{?scl_prefix}php-%{pecl_name} = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}

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
PHP's asynchronous concurrent distributed networking framework.
- Event-driven
- Full asynchronous non-blocking
- Multi-Thread or Multi-Process
- Millisecond timer
- Asynchronous MySQL
- AsyncTask workers


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

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
cat << 'EOF' | tee %{pecl_name}.ini
; Enable %{summary} extension module
extension=%{pecl_name}.so
EOF


%build
# --enable-async-mysql requires mysqlnd, so php >= 5.4

peclbuild() {
%configure \
    --with-swoole \
    --enable-msgqueue \
    --enable-sockets \
%if "%{php_version}" > "5.4"
    --enable-async-mysql \
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


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
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