%{!?phpname:  %{expand: %%global phpname     php}}
%{!?__pecl:   %{expand: %%global __pecl     %{_bindir}/pecl}}
%global pecl_name mysqlnd_qc

Summary:      A query cache plugin for mysqlnd
Name:         %{phpname}-pecl-mysqlnd-qc
Version:      1.0.1
Release:      1%{?dist}
License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{pecl_name}

Source0:      http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# From http://www.php.net/manual/en/mysqlnd-qc.configuration.php
Source1:      mysqlnd_qc.ini

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{phpname}-devel >= 5.3.4
BuildRequires: %{phpname}-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:     %{phpname}-mysqlnd%{?_isa}
Requires:     %{phpname}(zend-abi) = %{php_zend_api}
Requires:     %{phpname}(api) = %{php_core_api}

Provides:     %{phpname}-pecl(%{pecl_name}) = %{version}-%{release}
Provides:     %{phpname}-pecl(%{pecl_name})%{?_isa} = %{version}-%{release}


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
virtually transparent for applications.


%prep 
%setup -c -q

cp %{SOURCE1} %{pecl_name}.ini

#cp -r %{pecl_name}-%{version} %{pecl_name}-%{version}-zts


%build
cd %{pecl_name}-%{version}
%{php_bindir}/phpize
%configure --with-php-config=%{php_bindir}/php-config
make %{?_smp_mflags}

#cd ../%{pecl_name}-%{version}-zts
#{php_ztsbindir}/phpize
#configure --enable-memcached-igbinary \
#           --with-php-config=%{php_ztsbindir}/php-config
#make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install -C %{pecl_name}-%{version}     INSTALL_ROOT=%{buildroot}
#make install -C %{pecl_name}-%{version}-zts INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini
#install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini

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
# only check if build extension can be loaded
%{__php} -n -q \
    -d extension_dir=modules \
    -d extension=mysqlnd.so \
    -d extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


%files
%defattr(-, root, root, -)
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
#%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
#%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Sun Sep 18 2011  Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Initial RPM

