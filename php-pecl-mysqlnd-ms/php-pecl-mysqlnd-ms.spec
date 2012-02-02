%{!?__pecl:   %{expand: %%global __pecl     %{_bindir}/pecl}}
%global pecl_name mysqlnd_ms

Summary:      A replication and load balancing plugin for mysqlnd
Name:         php-pecl-mysqlnd-ms
Version:      1.2.2
Release:      1%{?dist}

License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/mysqlnd_ms

Source0:      http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# From http://www.php.net/manual/en/mysqlnd-ms.configuration.php
Source1:      %{pecl_name}.ini

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel >= 5.3.6
BuildRequires: php-mysqlnd
BuildRequires: php-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:     php-mysqlnd%{?_isa}
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}

Provides:     php-pecl(%{pecl_name}) = %{version}-%{release}
Provides:     php-pecl(%{pecl_name})%{?_isa} = %{version}-%{release}

%{?filter_setup}


%description
The replication and load balancing plugin is a plugin for the mysqlnd library.
It can be used with PHP MySQL extensions (ext/mysql, ext/mysqli, PDO_MySQL),
if they are compiled to use mysqlnd. The plugin inspects queries to do
read-write splitting. Read-only queries are send to configured MySQL
replication slave servers all other queries are redirected to the MySQL
replication master server. Very little, if any, application changes required,
dependent on the usage scenario required.

Documentation : http://www.php.net/mysqlnd_ms


%prep 
%setup -c -q

cp %{SOURCE1} %{pecl_name}.ini

%if 0%{?__ztsphp:1}
# Build ZTS extension if ZTS devel available (fedora >= 17)
cp -r %{pecl_name}-%{version} %{pecl_name}-zts
%endif


%build
cd %{pecl_name}-%{version}
%{_bindir}/phpize
%configure \
    --with-libdir=%{_lib} \
    --enable-mysqlnd-ms \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if 0%{?__ztsphp:1}
cd ../%{pecl_name}-zts
%{_bindir}/zts-phpize
%configure \
    --with-libdir=%{_lib} \
    --enable-mysqlnd-ms \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif

%install
rm -rf %{buildroot}
# for short-circuit
rm -rf %{pecl_name}-*/modules/{json,mysqlnd}.so

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
ln -sf %{php_extdir}/mysqlnd.so modules/
ln -sf %{php_extdir}/json.so modules/

# only check if build extension can be loaded
php -n -q \
    -d extension_dir=modules \
    -d extension=json.so \
    -d extension=mysqlnd.so \
    -d extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if 0%{?__ztsphp:1}
cd ../%{pecl_name}-zts
ln -sf %{php_ztsextdir}/mysqlnd.so modules/
ln -sf %{php_ztsextdir}/json.so modules/

# only check if build extension can be loaded
%{__ztsphp} -n -q \
    -d extension_dir=modules \
    -d extension=json.so \
    -d extension=mysqlnd.so \
    -d extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


%files
%defattr(-, root, root, -)
%doc %{pecl_name}-%{version}/{CHANGES,CREDITS,LICENSE,README}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if 0%{?__ztsphp:1}
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Thu Feb 02 2012 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- update to 1.2.2 (stable)

* Wed Jan 25 2012 Remi Collet <remi@fedoraproject.org> - 1.1.2-5
- zts binary in /usr/bin with zts prefix

* Sun Jan 21 2012 Remi Collet <remi@fedoraproject.org> - 1.1.2-4
- merge ZTS change for fedora 17
- filter_setup is enough

* Sun Nov 13 2011 Remi Collet <remi@fedoraproject.org> - 1.1.2-3
- build against php 5.4

* Mon Nov 07 2011 Remi Collet <remi@fedoraproject.org> - 1.1.2-2
- update to 1.1.2 (stable) with zts extension

* Mon Nov 07 2011 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- update to 1.1.2 (stable)

* Fri Oct 14 2011 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1

* Sun Oct 02 2011 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Initial RPM
