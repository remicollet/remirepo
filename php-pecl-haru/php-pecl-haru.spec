%{!?__pecl:   %{expand: %%global __pecl     %{_bindir}/pecl}}
%global pecl_name haru

Summary:      Haru PDF functions
Name:         php-pecl-haru
Version:      1.0.3
Release:      1%{?dist}

# https://bugs.php.net/60958 - Please Provides LICENSE file
License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/haru

Source0:      http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel
BuildRequires: php-pear
BuildRequires: libharu-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}

Provides:     php-pecl(%{pecl_name}) = %{version}
Provides:     php-pecl(%{pecl_name})%{?_isa} = %{version}

%{?filter_setup}


%description
The PECL/haru extension provides bindings to the libHaru library.

libHaru is a free, cross platform, and Open Source library for
generating PDF files. 

Documentation : http://www.php.net/haru


%prep 
%setup -c -q

# Create configuration file
cat >%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

# https://bugs.php.net/60959 - Version 1.0.3 reports as 1.0.1
sed -i -e '/PHP_HARU_VERSION/s/1.0.1/%{version}/' %{pecl_name}-%{version}/php_haru.h

# Check extension version
extver=$(sed -n '/#define PHP_HARU_VERSION/{s/.* "//;s/".*$//;p}' %{pecl_name}-%{version}/php_haru.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi

%if 0%{?__ztsphp:1}
# Build ZTS extension if ZTS devel available (fedora >= 17)
cp -r %{pecl_name}-%{version} %{pecl_name}-zts
%endif


%build
export PHP_RPATH=no

cd %{pecl_name}-%{version}
%{_bindir}/phpize
%configure \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if 0%{?__ztsphp:1}
cd ../%{pecl_name}-zts
%{_bindir}/zts-phpize
%configure \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif

%install
rm -rf %{buildroot}

make install -C %{pecl_name}-%{version} \
     INSTALL_ROOT=%{buildroot}

%if 0%{?__ztsphp:1}
make install -C %{pecl_name}-zts \
     INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif
install -D -m 644 %{pecl_name}.ini %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%clean
rm -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
cd %{pecl_name}-%{version}

# only check if build extension can be loaded
php -n -q \
    -d extension_dir=modules \
    -d extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if 0%{?__ztsphp:1}
cd ../%{pecl_name}-zts

# only check if build extension can be loaded
%{__ztsphp} -n -q \
    -d extension_dir=modules \
    -d extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


%files
%defattr(-, root, root, -)
%doc %{pecl_name}-%{version}/CREDITS
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if 0%{?__ztsphp:1}
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Thu Feb 02 2012 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Initial RPM
- https://bugs.php.net/60958 - Please Provides LICENSE file
- https://bugs.php.net/60959 - Version 1.0.3 reports as 1.0.1

