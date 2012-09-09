%global ext_name   xcache

Summary:       Fast, stable PHP opcode cacher
Name:          php-xcache
Version:       2.0.1
Release:       1%{?dist}
License:       PHP
Group:         Development/Languages
URL:           http://xcache.lighttpd.net/

Source0:       http://xcache.lighttpd.net/pub/Releases/%{version}/%{ext_name}-%{version}.tar.gz

# Specific RPM extension PATH
Patch0:        %{ext_name}-conf.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php-devel

Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

Conflicts:     php-pecl-apc, php-eaccelerator

# Other third party repo stuff
Obsoletes: php53-xcache
Obsoletes: php53u-xcache
%if "%{php_version}" > "5.4"
Obsoletes: php54-xcache
%endif

# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
XCache is a fast, stable  PHP opcode cacher that has been tested and is now
running on production servers under high load. 

It is tested (on linux) and supported on all of the latest PHP release. 
ThreadSafe is also perfectly supported. 

It overcomes a lot of problems that has been with other competing opcachers
such as being able to be used with new  PHP versions. 


%prep
%setup -q -c 

# rename source folder
mv %{ext_name}-%{version} nts

# Sanity check, really often broken
extver=$(sed -n '/define XCACHE_VERSION/{s/.* "//;s/".*$//;p}' nts/xcache.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi

# duplicate for ZTS build
cp -pr nts zts

cd nts
%patch0 -p0 -b .upstream
sed -e 's:@EXTDIR@:%{php_extdir}:'    -i %{ext_name}.ini

cd ../zts
%patch0 -p0 -b .upstream
sed -e 's:@EXTDIR@:%{php_ztsextdir}:' -i %{ext_name}.ini


%build
# Without --enable-xcache-assembler, --enable-xcache-encoder, --enable-xcache-decoder
# This seems not yet implemented

cd nts
%{_bindir}/phpize
%configure \
    --enable-xcache \
    --enable-xcache-constant \
    --enable-xcache-optimizer \
    --enable-xcache-coverager \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../zts
%{_bindir}/zts-phpize
%configure \
    --enable-xcache \
    --enable-xcache-constant \
    --enable-xcache-optimizer \
    --enable-xcache-coverager \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
# Install the NTS stuff
make -C nts install INSTALL_ROOT=%{buildroot}
install -D -m 644 nts/%{ext_name}.ini %{buildroot}%{php_inidir}/%{ext_name}.ini

# Install the ZTS stuff
make -C zts install INSTALL_ROOT=%{buildroot}
install -D -m 644 zts/%{ext_name}.ini %{buildroot}%{php_ztsinidir}/%{ext_name}.ini


%check
# simple module load test
php --no-php-ini \
    --define zend_extension=%{buildroot}%{php_extdir}/%{ext_name}.so \
    --modules | grep XCache

%{__ztsphp} --no-php-ini \
    --define zend_extension=%{buildroot}%{php_ztsextdir}/%{ext_name}.so \
    --modules | grep XCache


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc nts/{AUTHORS,ChangeLog,COPYING,README,THANKS}
%doc nts/admin
%doc nts/coverager
%config(noreplace) %{php_inidir}/%{ext_name}.ini
%{php_extdir}/%{ext_name}.so

%{php_ztsextdir}/%{ext_name}.so
%config(noreplace) %{php_ztsinidir}/%{ext_name}.ini


%changelog
* Sun Sep  9 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- initial package

