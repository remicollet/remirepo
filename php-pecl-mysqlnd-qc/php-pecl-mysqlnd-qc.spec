%{!?__pecl:   %{expand: %%global __pecl     %{_bindir}/pecl}}
%global pecl_name mysqlnd_qc

Summary:      A query cache plugin for mysqlnd
Name:         php-pecl-mysqlnd-qc
Version:      1.0.1
Release:      1%{?dist}
License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{pecl_name}

Source0:      http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# From http://www.php.net/manual/en/mysqlnd-qc.configuration.php
Source1:      mysqlnd_qc.ini

# http://pecl.php.net/bugs/bug.php?id=24363
Patch0:       mysqlnd_qc-build.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel >= 5.3.4
BuildRequires: php-pear
BuildRequires: libmemcached-devel >= 0.38
BuildRequires: sqlite-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:     php-mysqlnd%{?_isa}
Requires:     php-sqlite3%{?_isa}
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}

Provides:     php-pecl(%{pecl_name}) = %{version}-%{release}
Provides:     php-pecl(%{pecl_name})%{?_isa} = %{version}-%{release}


# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$


%description
The mysqlnd query result cache plugin is a mysqlnd plugin. 
It adds basic client side result set caching to all PHP MySQL extensions
(ext/mysql, ext/mysqli, PDO_MySQL). if they are compiled to use mysqlnd.
It does not change the API of the MySQL extensions and thus it operates
virtually transparent for applications."


%prep 
%setup -c -q

cp %{SOURCE1} %{pecl_name}.ini

cd %{pecl_name}-%{version}
%patch0 -p1 -b .build

%build
cd %{pecl_name}-%{version}
%{_bindir}/phpize

# APC is onlysupported if both APC and MySQL Query Cache are compiled statically

%configure \
    --with-libdir=%{_lib} \
    --enable-mysqlnd-qc \
    --enable-mysqlnd-qc-memcache \
    --enable-mysqlnd-qc-sqlite \
    --with-sqlite-dir=%{_prefix} \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install -C %{pecl_name}-%{version}     INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

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
ln -s %{php_extdir}/mysqlnd.so modules/
ln -s %{php_extdir}/sqlite3.so modules/

# only check if build extension can be loaded
php -n -q \
    -d extension_dir=modules \
    -d extension=mysqlnd.so \
    -d extension=sqlite3.so \
    -d extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


%files
%defattr(-, root, root, -)
%doc %{pecl_name}-%{version}/web
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Sun Sep 18 2011  Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Initial RPM
