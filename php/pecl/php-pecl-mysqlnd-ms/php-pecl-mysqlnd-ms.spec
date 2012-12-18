%{!?__pecl:   %{expand: %%global __pecl     %{_bindir}/pecl}}
%global pecl_name mysqlnd_ms

Summary:      A replication and load balancing plugin for mysqlnd
Name:         php-pecl-mysqlnd-ms
Version:      1.4.2
Release:      2%{?dist}.3

License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/mysqlnd_ms

Source0:      http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# From http://www.php.net/manual/en/mysqlnd-ms.configuration.php
Source1:      %{pecl_name}.ini

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel >= 5.3.6
BuildRequires: php-mysqlnd
BuildRequires: php-json
BuildRequires: php-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:     php-mysqlnd%{?_isa}
Requires:     php-json%{?_isa}
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}

Provides:     php-%{pecl_name} = %{version}
Provides:     php-%{pecl_name}%{?_isa} = %{version}
Provides:     php-pecl(%{pecl_name}) = %{version}
Provides:     php-pecl(%{pecl_name})%{?_isa} = %{version}

# Other third party repo stuff
Obsoletes:     php53-pecl-mysqlnd-ms
Obsoletes:     php53u-pecl-mysqlnd-ms
%if "%{php_version}" > "5.4"
Obsoletes:     php54-pecl-mysqlnd-ms
%endif
%if "%{php_version}" > "5.5"
Obsoletes:     php55-pecl-mysqlnd-ms
%endif

# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
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


%package devel
Summary:       Mysqlnd_ms developer files (header)
Group:         Development/Libraries
Requires:      php-pecl-mysqlnd-ms%{?_isa} = %{version}-%{release}
Requires:      php-devel%{?_isa}

%description devel
These are the files needed to compile programs using mysqlnd_ms extension.


%prep 
%setup -c -q

cp %{SOURCE1} %{pecl_name}.ini

extver=$(sed -n '/#define MYSQLND_MS_VERSION /{s/.* "//;s/".*$//;p}' %{pecl_name}-%{version}/mysqlnd_ms.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

# Build ZTS extension if ZTS devel available (fedora >= 17)
cp -r %{pecl_name}-%{version} %{pecl_name}-zts


%build
# EXPERIMENTAL options not used
# --enable-mysqlnd-ms-table-filter
#         Enable support for table filter in mysqlnd_ms
# --enable-mysqlnd-ms-cache-support
#         Enable query caching through mysqlnd_qc

cd %{pecl_name}-%{version}
%{_bindir}/phpize
%configure \
    --with-libdir=%{_lib} \
    --enable-mysqlnd-ms \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-zts
%{_bindir}/zts-phpize
%configure \
    --with-libdir=%{_lib} \
    --enable-mysqlnd-ms \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
# for short-circuit
rm -f %{pecl_name}-*/modules/{json,mysqlnd}.so

make install -C %{pecl_name}-%{version} \
     INSTALL_ROOT=%{buildroot}

make install -C %{pecl_name}-zts \
     INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
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


%files
%defattr(-, root, root, -)
%doc %{pecl_name}-%{version}/{CHANGES,CREDITS,LICENSE,README}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so


%files devel
%defattr(-,root,root,-)
%{_includedir}/php/ext/%{pecl_name}
%{php_ztsincldir}/ext/%{pecl_name}


%changelog
* Fri Nov 30 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.4.2-2.1
- also provides php-mysqlnd_ms

* Sun Sep  9 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.4.2-2
- obsoletes php53*, php54*
- cleanups

* Wed Aug 22 2012 Remi Collet <remi@fedoraproject.org> - 1.4.2-1
- update to 1.4.2 (stable)
- add -devel sub package

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Remi Collet <remi@fedoraproject.org> - 1.3.2-2
- rebuild for EL and PHP 5.4

* Mon Apr 30 2012 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- update to 1.2.3 (stable)
- add version check
- add devel sub-package

* Thu Feb 02 2012 Remi Collet <remi@fedoraproject.org> - 1.2.2-2
- build against php 5.4

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
