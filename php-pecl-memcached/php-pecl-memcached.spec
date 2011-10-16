%{!?phpname:  %{expand: %%global phpname     php}}
%{!?__pecl:   %{expand: %%global __pecl     %{_bindir}/pecl}}
%global pecl_name memcached

Summary:      Extension to work with the Memcached caching daemon
Name:         %{phpname}-pecl-memcached
Version:      1.0.2
Release:      10%{?dist}
License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{pecl_name}

Source:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# http://pecl.php.net/bugs/bug.php?id=24362
Patch0:       memcached-incl.patch

# Fix ZTS build with igbinary support
# https://github.com/php-memcached-dev/php-memcached/commit/5beaeedefe5c1eea6d637e3eeeeaf0957a5660ac
Patch1:       memcached-zts.patch


BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# 5.2.10 required to HAVE_JSON enabled
BuildRequires: %{phpname}-devel >= 5.2.10
BuildRequires: %{phpname}-pear
BuildRequires: %{phpname}-pecl-igbinary-devel
BuildRequires: libmemcached-devel
BuildRequires: zlib-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:     %{phpname}-common%{?_isa} >= 5.2.10
Requires:     %{phpname}-pecl-igbinary%{?_isa}
Requires:     %{phpname}(zend-abi) = %{php_zend_api}
Requires:     %{phpname}(api) = %{php_core_api}

Provides:     %{phpname}-pecl(%{pecl_name}) = %{version}-%{release}
Provides:     %{phpname}-pecl(%{pecl_name})%{?_isa} = %{version}-%{release}


# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{php_ztsextdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$
%global __provides_exclude_from %__provides_exclude_from|%{php_ztsextdir}/.*\\.so$


%description
This extension uses libmemcached library to provide API for communicating
with memcached servers.

memcached is a high-performance, distributed memory object caching system,
generic in nature, but intended for use in speeding up dynamic web 
applications by alleviating database load.

It also provides a session handler (memcached). 


%prep 
%setup -c -q

cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; ----- Options to use the memcached session handler

;  Use memcache as a session handler
;session.save_handler=memcached
;  Defines a comma separated list of server urls to use for session storage
;session.save_path="localhost:11211"
EOF

cd %{pecl_name}-%{version}
%patch0 -p1 -b .incl
%patch1 -p1 -b .zts
cd ..

cp -r %{pecl_name}-%{version} %{pecl_name}-%{version}-zts


%build
cd %{pecl_name}-%{version}
%{php_bindir}/phpize
%configure --enable-memcached-igbinary \
           --with-php-config=%{php_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-%{version}-zts
%{php_ztsbindir}/phpize
%configure --enable-memcached-igbinary \
           --with-php-config=%{php_ztsbindir}/php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
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
# only check if build extension can be loaded
ln -s %{php_extdir}/json.so modules/
ln -s %{php_extdir}/igbinary.so modules/
%{__php} -n -q \
    -d extension_dir=modules \
    -d extension=json.so \
    -d extension=igbinary.so \
    -d extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


%files
%defattr(-, root, root, -)
%doc %{pecl_name}-%{version}/{CREDITS,LICENSE,README.markdown,ChangeLog}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Sun Oct 16 2011  Remi Collet <remi@fedoraproject.org> - 1.0.2-10
- rebuild against latest libmemcached (f16 only)

* Tue Oct 04 2011  Remi Collet <remi@fedoraproject.org> - 1.0.2-9
- ZTS extension

* Sat Sep 17 2011  Remi Collet <remi@fedoraproject.org> - 1.0.2-8
- allow relocation
- work for ZTS (not yet ok)

* Sat Sep 17 2011  Remi Collet <remi@fedoraproject.org> - 1.0.2-7
- rebuild against libmemcached 0.52
- adapted filter
- clean spec

* Thu Jun 02 2011  Remi Collet <Fedora@FamilleCollet.com> - 1.0.2-6
- rebuild against libmemcached 0.49

* Sat Feb 19 2011 Remi Collet <fedora@famillecollet.com> - 1.0.2-3.2
- rebuild for remi repo with SASL for fedora <= 10 and EL <= 5

* Sat Oct 02 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-3.1
- remove patch 

* Fri Oct 01 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-3
- rebuild against libmemcached 0.44 with SASL support

* Wed Sep 29 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-2
- rebuild with igbinary support

* Tue May 04 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-1
- update to 1.0.2 for libmemcached 0.40

* Sat Mar 13 2010 Remi Collet <fedora@famillecollet.com> - 1.0.1-1
- update to 1.0.1 for libmemcached 0.38

* Sun Feb 07 2010 Remi Collet <fedora@famillecollet.com> - 1.0.0-3.1
- bump release

* Sat Feb 06 2010 Remi Collet <fedora@famillecollet.com> - 1.0.0-3
- rebuilt against new libmemcached
- add minimal %%check

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <fedora@famillecollet.com> - 1.0.0-1
- Update to 1.0.0 (First stable release)

* Sat Jun 27 2009 Remi Collet <fedora@famillecollet.com> - 0.2.0-1
- Update to 0.2.0 + Patch for HAVE_JSON constant

* Sun Apr 29 2009 Remi Collet <fedora@famillecollet.com> - 0.1.5-1
- Initial RPM

