%{!?__pecl:   %{expand: %%global __pecl     %{_bindir}/pecl}}

%global pecl_name mysqlnd_qc
%global svnver    322926
%global prever    alpha

%if 0%{?fedora} >= 9 || 0%{?rhel} >= 6
%global withsqlite 1
%else
%global withsqlite 0
%endif

Summary:      A query cache plugin for mysqlnd
Name:         php-pecl-mysqlnd-qc
Version:      1.1.0
%if 0%{?svnver}
# svn export -r 322926 https://svn.php.net/repository/pecl/mysqlnd_qc/trunk mysqlnd_qc-svn322926
# tar czf mysqlnd_qc-svn322926.tgz mysqlnd_qc-svn322926
Source:       mysqlnd_qc-svn322926.tgz
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

# https://bugs.php.net/59959
Patch0:       mysqlnd_qc-1.1.0-build.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel >= 5.4.0
BuildRequires: php-mysqlnd
BuildRequires: php-pear
BuildRequires: libmemcached-devel >= 0.38
%if %{withsqlite}
BuildRequires: sqlite-devel >= 3.5.9
%endif

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:     php-mysqlnd%{?_isa}
Requires:     php-sqlite3%{?_isa}
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}

Provides:     php-pecl(%{pecl_name}) = %{version}-%{release}
Provides:     php-pecl(%{pecl_name})%{?_isa} = %{version}-%{release}

%{?filter_setup}


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

extver=$(sed -n '/#define MYSQLND_QC_VERSION_STR/{s/.* "//;s/".*$//;p}' %{pecl_name}-*/php_mysqlnd_qc.h)
if test "x${extver}" != "x%{version}%{?prever:-}%{?prever}"; then
   : Error: Upstream %{pecl_name} version is now ${extver}, expecting %{version}%{?prever}.
   : Update the pdover macro and rebuild.
   exit 1
fi

cp %{SOURCE1} %{pecl_name}.ini

cd %{pecl_name}-%{version}
%patch0 -p1 -b .build
cd ..

cp -r %{pecl_name}-%{version} %{pecl_name}-zts


%build
cd %{pecl_name}-%{version}

%{_bindir}/phpize

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
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-zts
%{_bindir}/zts-phpize
%configure \
    --with-libdir=%{_lib} \
    --enable-mysqlnd-qc \
    --enable-mysqlnd-qc-memcache \
%if %{withsqlite}
    --enable-mysqlnd-qc-sqlite \
    --with-sqlite-dir=%{_prefix} \
%endif
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
# for short-circuit
rm -rf %{pecl_name}-*/modules/{sqlite3,mysqlnd}.so

make install -C %{pecl_name}-%{version} INSTALL_ROOT=%{buildroot}
make install -C %{pecl_name}-zts        INSTALL_ROOT=%{buildroot}

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
php -n -q \
    -d extension_dir=modules \
    -d extension=mysqlnd.so \
%if %{withsqlite}
    -d extension=sqlite3.so \
%endif
    -d extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

cd ../%{pecl_name}-zts
ln -s %{php_ztsextdir}/mysqlnd.so modules/
%if %{withsqlite}
ln -s %{php_ztsextdir}/sqlite3.so modules/
%endif

# only check if build extension can be loaded
zts-php -n -q \
    -d extension_dir=modules \
    -d extension=mysqlnd.so \
%if %{withsqlite}
    -d extension=sqlite3.so \
%endif
    -d extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


%files
%defattr(-, root, root, -)
%doc %{pecl_name}-%{version}/LICENSE
%doc %{pecl_name}-%{version}/web
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Mon Jan 30 2012  Remi Collet <remi@fedoraproject.org> - 1.1.0-0.1.svn322926
- new snapshot, update to 1.1.0-alpha

* Mon Nov 21 2011  Remi Collet <remi@fedoraproject.org> - 1.0.1-3.svn322926
- fix from svn, build against php 5.4

* Sun Sep 18 2011  Remi Collet <remi@fedoraproject.org> - 1.0.1-2
- build zts extension

* Sun Sep 18 2011  Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Initial RPM

