%{!?phpname:  %{expand: %%global phpname     php}}
%{!?__pecl:   %{expand: %%global __pecl     %{_bindir}/pecl}}

%global pecl_name mysqlnd_qc
%global svnver    322628
%global prever    alpha

%if 0%{?fedora} >= 9 || 0%{?rhel} >= 6
%global withsqlite 1
%else
%global withsqlite 0
%endif

Summary:      A query cache plugin for mysqlnd
Name:         %{phpname}-pecl-mysqlnd-qc
Version:      1.0.2
%if 0%{?svnver}
# svn export -r 322628 https://svn.php.net/repository/pecl/mysqlnd_qc/trunk mysqlnd_qc-svn322628
# tar czf mysqlnd_qc-svn322628.tgz mysqlnd_qc-svn322628
Source:       mysqlnd_qc-svn318164.tgz
Release:      0.1.%{prever}.svn%{svnver}%{?dist}
%else
Source0:      http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Release:      2%{?dist}
%endif
License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/mysqlnd_qc


# From http://www.php.net/manual/en/mysqlnd-qc.configuration.php
Source1:      mysqlnd_qc.ini

# http://pecl.php.net/bugs/bug.php?id=24365
Patch0:       mysqlnd_qc-build.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{phpname}-devel >= 5.3.4
BuildRequires: %{phpname}-mysqlnd
BuildRequires: %{phpname}-pear
BuildRequires: libmemcached-devel >= 0.38
%if %{withsqlite}
BuildRequires: sqlite-devel >= 3.5.9
%endif

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:     %{phpname}-mysqlnd%{?_isa}
Requires:     %{phpname}-sqlite3%{?_isa}
Requires:     %{phpname}(zend-abi) = %{php_zend_api}
Requires:     %{phpname}(api) = %{php_core_api}

Provides:     %{phpname}-pecl(%{pecl_name}) = %{version}-%{release}
Provides:     %{phpname}-pecl(%{pecl_name})%{?_isa} = %{version}-%{release}


#{?filter_setup}


%description
The mysqlnd query result cache plugin is a mysqlnd plugin. 
It adds basic client side result set caching to all PHP MySQL extensions
(ext/mysql, ext/mysqli, PDO_MySQL). if they are compiled to use mysqlnd.
It does not change the API of the MySQL extensions and thus it operates
virtually transparent for applications.

Documentation : http://www.php.net/mysqlnd_qc


%prep 
%setup -c -q

%if 0%{?svnver}
mv %{pecl_name}-svn%{svnver}/package.xml .
mv %{pecl_name}-svn%{svnver} %{pecl_name}-%{version}
%endif

cp %{SOURCE1} %{pecl_name}.ini

cd %{pecl_name}-%{version}
%patch0 -p1 -b .build
cd ..

cp -r %{pecl_name}-%{version} %{pecl_name}-%{version}-zts


%build
cd %{pecl_name}-%{version}
%{php_bindir}/phpize

# don't use --enable-mysqlnd-qc-apc because:
# APC is onlysupported if both APC and MySQL Query Cache are compiled statically

%configure \
    --with-libdir=%{_lib} \
    --enable-mysqlnd-qc \
    --enable-mysqlnd-qc-memcache \
%if %{withsqlite}
    --enable-mysqlnd-qc-sqlite \
    --with-sqlite-dir=%{_prefix} \
%endif
    --with-php-config=%{php_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-%{version}-zts
%{php_ztsbindir}/phpize
%configure \
    --with-libdir=%{_lib} \
    --enable-mysqlnd-qc \
    --enable-mysqlnd-qc-memcache \
%if %{withsqlite}
    --enable-mysqlnd-qc-sqlite \
    --with-sqlite-dir=%{_prefix} \
%endif
    --with-php-config=%{php_ztsbindir}/php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
# for short-circuit
rm -rf %{pecl_name}-*/modules/{sqlite3,mysqlnd}.so

make install -C %{pecl_name}-%{version}     INSTALL_ROOT=%{buildroot}
make install -C %{pecl_name}-%{version}-zts INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini

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
%if %{withsqlite}
ln -s %{php_extdir}/sqlite3.so modules/
%endif

# only check if build extension can be loaded
%{__php} -n -q \
    -d extension_dir=modules \
    -d extension=mysqlnd.so \
%if %{withsqlite}
    -d extension=sqlite3.so \
%endif
    -d extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


%files
%defattr(-, root, root, -)
%doc %{pecl_name}-%{version}/license
%doc %{pecl_name}-%{version}/web
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Mon Nov 21 2011  Remi Collet <remi@fedoraproject.org> - 1.0.1-3.svn318164
- fix from svn, build against php 5.4

* Sun Sep 18 2011  Remi Collet <remi@fedoraproject.org> - 1.0.1-2
- enable relocation
- build zts extension

* Sun Sep 18 2011  Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Initial RPM

