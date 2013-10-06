# spec file for php-pecl-xattr
#
# Copyright (c) 2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?php_inidir:  %{expand: %%global php_inidir  %{_sysconfdir}/php.d}}
%{!?__pecl:      %{expand: %%global __pecl      %{_bindir}/pecl}}

%global with_zts  0%{?__ztsphp:1}
%global pecl_name xattr

Summary:        Extended attributes
Name:           php-pecl-%{pecl_name}
Version:        1.2.0
Release:        1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# https://bugs.php.net/65842 Please Provides LICENSE file

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel
BuildRequires:  php-pear
BuildRequires:  libattr-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

Provides:       php-%{pecl_name} = %{version}
Provides:       php-%{pecl_name}%{?_isa} = %{version}
Provides:       php-pecl(%{pecl_name}) = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}

# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
This package allows to manipulate extended attributes on filesystems that
support them. Requires libattr from Linux XFS project.


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

cd NTS
# http://svn.php.net/viewvc?view=revision&revision=331704
sed -e 's:/lib:/$PHP_LIBDIR:' -i config.m4

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_XATTR_VERSION/{s/.* "//;s/".*$//;p}' php_xattr.h)
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
cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
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
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
: Minimal load test for NTS extension
%{_bindir}/php --no-php-ini \
    --define extension=NTS/modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=ZTS/modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc NTS/CREDITS
%{pecl_xmldir}/%{name}.xml
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Sun Oct  6 2013 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- initial package
