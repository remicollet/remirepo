%{!?php_inidir: %{expand: %%global php_inidir %{_sysconfdir}/php.d}}
%global pecl_name yac
%global commit    57fe00ddb5eeeede9b2e197dcb736f211e929578
%global gitver    %(c=%{commit}; echo ${c:0:7})
%global with_zts  0%{?__ztsphp:1}

Name:           php-yac
Summary:        Shared memory user data cache for PHP
Version:        0.1.0
Release:        0.1%{?gitver:.git%{gitver}}%{?dist}.1
Source0:        https://github.com/laruence/%{pecl_name}/archive/%{commit}/%{pecl_name}-%{version}-%{gitver}.tar.gz

License:        PHP
Group:          Development/Languages
URL:            https://github.com/laruence/yac

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel >= 5.2

# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
Yac (Yet Another Cache) is a shared memory user data cache for PHP.

It can be used to replace APC or local memcached.

This extension is still EXPERIMENTAL.


%prep
%setup -qc
mv %{pecl_name}-%{commit} NTS

# Drop in the bit of configuration
cat > %{pecl_name}.ini << 'EOF'
; Enable Yet Another Cache extension module
extension = %{pecl_name}.so

yac.enable=1
;yac.debug=0
;yac.keys_memory_size=4M
;yac.values_memory_size=64M
;yac.compress_threshold=-1
EOF

# When this file will be removed, clean the description.
[ -f NTS/EXPERIMENTAL ] || exit 1

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
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

# Install the ZTS stuff
%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif


%check
cd NTS

TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php

%if %{with_zts}
cd ../ZTS

TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc NTS/{CREDITS,LICENSE,README.md}

%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%endif


%changelog
* Sat Mar 23 2013 Remi Collet <remi@fedoraproject.org> - 0.1.0-0.1.git57fe00d
- initial package, version 0.1.0 (experimental)
