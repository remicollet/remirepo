# spec file for php-twig-CTwig
#
# Copyright (c) 2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?php_inidir:  %{expand: %%global php_inidir  %{_sysconfdir}/php.d}}
%{!?php_incldir: %{expand: %%global php_incldir %{_includedir}/php}}
%{!?__pecl:      %{expand: %%global __pecl      %{_bindir}/pecl}}

%global with_zts  0%{?__ztsphp:1}
%global pecl_name    CTwig
%global ext_name     twig
%global pecl_channel pear.twig-project.org

Summary:        Extension to improve  performance of Twig
Name:           php-twig-%{pecl_name}
Version:        1.14.0
Release:        1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:        BSD
Group:          Development/Languages
URL:            http://twig.sensiolabs.org
Source0:        http://%{pecl_channel}/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel >= 5.2.4
BuildRequires:  php-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

Provides:       php-%{ext_name} = %{version}
Provides:       php-%{ext_name}%{?_isa} = %{version}
Provides:       php-pecl(%{pecl_channel}/%{pecl_name}) = %{version}
Provides:       php-pecl(%{pecl_channel}/%{pecl_name})%{?_isa} = %{version}

# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}

%description
Twig is a PHP template engine.

This package provides the Twig C extension (CTwig) to improve performance
of the Twig template language, used by Twig PHP extension (php-twig-Twig).


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

cd NTS
# Sanity check, really often broken
extver=$(sed -n '/#define PHP_TWIG_VERSION/{s/.* "//;s/".*$//;p}' php_twig.h)
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
cat > %{ext_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{ext_name}.so
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{ext_name}.ini %{buildroot}%{php_inidir}/%{ext_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{ext_name}.ini %{buildroot}%{php_ztsinidir}/%{ext_name}.ini
%endif


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_channel}/%{pecl_name} >/dev/null || :
fi


%check
# Minimal load test for NTS extension
php --no-php-ini \
    --define extension=NTS/modules/%{ext_name}.so \
    --modules | grep %{ext_name}

%if %{with_zts}
# Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=ZTS/modules/%{ext_name}.so \
    --modules | grep %{ext_name}
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc NTS/LICENSE
%{pecl_xmldir}/%{name}.xml
%config(noreplace) %{php_inidir}/%{ext_name}.ini
%{php_extdir}/%{ext_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ext_name}.ini
%{php_ztsextdir}/%{ext_name}.so
%endif


%changelog
* Thu Oct  3 2013 Remi Collet <remi@fedoraproject.org> - 1.14.0-1
- initial package
