# spec file for php-pecl-haru
#
# Copyright (c) 2012-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global pecl_name  haru
%global with_zts   0%{?__ztsphp:1}

Summary:      Haru PDF functions
Name:         php-pecl-haru
Version:      1.0.4
Release:      2%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}

License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/haru

Source0:      http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel
BuildRequires: php-pear
BuildRequires: libharu-devel
BuildRequires: libpng-devel
BuildRequires: zlib-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}

Provides:     php-%{pecl_name} = %{version}
Provides:     php-%{pecl_name}%{?_isa} = %{version}
Provides:     php-pecl(%{pecl_name}) = %{version}
Provides:     php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet"
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
Obsoletes:     php54-pecl-%{pecl_name}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name}
%endif
%endif

%if 0%{?fedora} < 20
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The PECL/haru extension provides bindings to the libHaru library.

libHaru is a free, cross platform, and Open Source library for
generating PDF files. 

Documentation : http://www.php.net/haru


%prep 
%setup -c -q
mv %{pecl_name}-%{version} NTS

# Create configuration file
cat >%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

# Check extension version
extver=$(sed -n '/#define PHP_HARU_VERSION/{s/.* "//;s/".*$//;p}' NTS/php_haru.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi

%if %{with_zts}
# Build ZTS extension if ZTS devel available (fedora >= 17)
cp -r NTS ZTS
%endif


%build
export PHP_RPATH=no

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

make install -C NTS INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}

install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Test & Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%clean
rm -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
: Check if build NTS extension can be loaded
%{__php} -n -q \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Check if build ZTS extension can be loaded
%{__ztsphp} -n -q \
    -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


%files
%defattr(-, root, root, -)
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Mon Mar 17 2014 Remi Collet <remi@fedoraproject.org> - 1.0.4-2
- cleanups
- install doc in pecl_docdir

* Mon Dec 24 2012 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- update to 1.0.4
- also provides php-haru

* Thu Feb 02 2012 Remi Collet <remi@fedoraproject.org> - 1.0.3-2
- build against php 5.4

* Thu Feb 02 2012 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Initial RPM
- https://bugs.php.net/60958 - Please Provides LICENSE file
- https://bugs.php.net/60959 - Version 1.0.3 reports as 1.0.1