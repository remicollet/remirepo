%global ext_name   redis
%global with_zts   0%{?__ztsphp:1}

Summary:       Extension for communicating with the Redis key-value store
Name:          php-%{ext_name}
Version:       2.2.2
Release:       1%{?dist}
License:       PHP
Group:         Development/Languages
URL:           https://github.com/nicolasff/phpredis
# wget https://github.com/nicolasff/phpredis/tarball/2.2.2 -O php-redis-2.2.2.tgz
Source:        %{name}-%{version}.tgz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php-devel
BuildRequires: php-pecl-igbinary-devel

Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}
# php-pecl-igbinary missing php-pecl(igbinary)%{?_isa}
Requires:      php-pecl-igbinary%{?_isa}

# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
The phpredis extension provides an API for communicating
with the Redis key-value store.


%prep
%setup -q -c 

# rename source folder
mv *redis* nts

chmod -x nts/*{c,h}

# remove bundled lib
rm -rf nts/igbinary
sed -e 's:igbinary/[^ ]*\.c::g' \
    -i nts/config.m4

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_REDIS_VERSION/{s/.* "//;s/".*$//;p}' nts/php_redis.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi

%if %{with_zts}
# duplicate for ZTS build
cp -pr nts zts
%endif

# Drop in the bit of configuration
cat > %{ext_name}.ini << 'EOF'
; Enable %{ext_name} extension module
extension = %{ext_name}.so

; phpredis can be used to store PHP sessions. 
; To do this, uncomment and configure below
;session.save_handler = %{ext_name}
;session.save_path = "tcp://host1:6379?weight=1, tcp://host2:6379?weight=2&timeout=2.5, tcp://host3:6379?weight=2"
EOF


%build
cd nts
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../zts
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}
# Install the NTS stuff
make -C nts install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ext_name}.ini %{buildroot}%{_sysconfdir}/php.d/%{ext_name}.ini

# Install the ZTS stuff
%if %{with_zts}
make -C zts install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ext_name}.ini %{buildroot}%{php_ztsinidir}/%{ext_name}.ini
%endif


%check
# simple module load test
ln -s %{php_extdir}/igbinary.so nts/modules/
%{__php} --no-php-ini \
    --define extension_dir=nts/modules \
    --define extension=igbinary.so \
    --define extension=%{ext_name}.so \
    --modules | grep %{ext_name}

%if %{with_zts}
ln -s %{php_ztsextdir}/igbinary.so zts/modules/
%{__ztsphp} --no-php-ini \
    --define extension_dir=zts/modules \
    --define extension=igbinary.so \
    --define extension=%{ext_name}.so \
    --modules | grep %{ext_name}
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc nts/COPYING nts/CREDITS nts/README.markdown
%config(noreplace) %{_sysconfdir}/php.d/%{ext_name}.ini
%{php_extdir}/%{ext_name}.so

%if %{with_zts}
%{php_ztsextdir}/%{ext_name}.so
%config(noreplace) %{php_ztsinidir}/%{ext_name}.ini
%endif


%changelog
* Tue Aug 29 2012 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- update to 2.2.2
- enable ZTS build

* Tue Aug 28 2012 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- initial package

