%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global pecl_name memcached
%global libmemcached_build_version %(pkg-config --silence-errors --modversion libmemcached 2>/dev/null || echo 65536)

Summary:      Extension to work with the Memcached caching daemon
Name:         php-pecl-memcached
Version:      2.1.0
Release:      7%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
# memcached is PHP, FastLZ is MIT
License:      PHP and MIT
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{pecl_name}

Source0:      http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# https://github.com/php-memcached-dev/php-memcached/issues/25
# https://github.com/php-memcached-dev/php-memcached/commit/74542111f175fe2ec41c8bf722fc2cd3dac93eea.patch
Patch0:        %{pecl_name}-build.patch
# https://github.com/php-memcached-dev/php-memcached/pull/43
Patch1:        %{pecl_name}-info.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# 5.2.10 required to HAVE_JSON enabled
BuildRequires: php-devel >= 5.2.10
BuildRequires: php-pear
BuildRequires: php-pecl-igbinary-devel
BuildRequires: libmemcached-devel >= 1.0.0
BuildRequires: zlib-devel
BuildRequires: cyrus-sasl-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:     php-pecl-igbinary%{?_isa}
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}

Provides:     php-%{pecl_name} = %{version}
Provides:     php-%{pecl_name}%{?_isa} = %{version}
Provides:     php-pecl(%{pecl_name}) = %{version}
Provides:     php-pecl(%{pecl_name})%{?_isa} = %{version}

# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
Obsoletes:     php54-pecl-%{pecl_name}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}
%endif

%if 0%{?fedora} < 20
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This extension uses libmemcached library to provide API for communicating
with memcached servers.

memcached is a high-performance, distributed memory object caching system,
generic in nature, but intended for use in speeding up dynamic web 
applications by alleviating database load.

It also provides a session handler (memcached). 


%prep 
%setup -c -q

# Chech version as upstream often forget to update this
extver=$(sed -n '/#define PHP_MEMCACHED_VERSION/{s/.* "//;s/".*$//;p}' %{pecl_name}-%{version}/php_memcached.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream HTTP version is now ${extver}, expecting %{version}.
   : Update the pdover macro and rebuild.
   exit 1
fi

cp %{pecl_name}-%{version}/fastlz/LICENSE LICENSE-FastLZ

cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; ----- Options to use the memcached session handler

; RPM note : save_handler and save_path are defined
; for mod_php, in /etc/httpd/conf.d/php.conf
; for php-fpm, in /etc/php-fpm.d/*conf

;  Use memcache as a session handler
;session.save_handler=memcached
;  Defines a comma separated list of server urls to use for session storage
;session.save_path="localhost:11211"
EOF

cd %{pecl_name}-%{version}
%patch0 -p1 -b .build
%patch1 -p1 -b .info
cd ..

cp -r %{pecl_name}-%{version} %{pecl_name}-%{version}-zts


%build
cd %{pecl_name}-%{version}
%{_bindir}/phpize
%configure --enable-memcached-igbinary \
           --enable-memcached-json \
           --enable-memcached-sasl \
           --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-%{version}-zts
%{_bindir}/zts-phpize
%configure --enable-memcached-igbinary \
           --enable-memcached-json \
           --enable-memcached-sasl \
           --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
# Install the NTS extension
make install -C %{pecl_name}-%{version} INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Install the ZTS extension
make install -C %{pecl_name}-%{version}-zts INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini


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

cd ../%{pecl_name}-%{version}-zts
# only check if build extension can be loaded
ln -s %{php_ztsextdir}/json.so modules/
ln -s %{php_ztsextdir}/igbinary.so modules/
%{__ztsphp} -n -q \
    -d extension_dir=modules \
    -d extension=json.so \
    -d extension=igbinary.so \
    -d extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/{CREDITS,LICENSE,README.markdown,ChangeLog}
%doc LICENSE-FastLZ
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so


%changelog
* Fri Nov 15 2013  Remi Collet <remi@fedoraproject.org> - 2.1.0-7
- drop requires libmemcached >= build version
  as this can also be libmemcached-last

* Mon Nov 19 2012  Remi Collet <remi@fedoraproject.org> - 2.1.0-6
- requires libmemcached >= build version

* Sat Nov 17 2012  Remi Collet <remi@fedoraproject.org> - 2.1.0-5
- rebuild for libmemcached 1.0.14 (with SASL)
- switch to upstream patch
- add patch to report about SASL support in phpinfo

* Fri Oct 19 2012 Remi Collet <remi@fedoraproject.org> - 2.1.0-4
- improve comment in configuration about session.

* Sat Sep 22 2012 Remi Collet <remi@fedoraproject.org> - 2.1.0-3
- rebuild for new libmemcached
- drop sasl support

* Sat Sep  8 2012 Remi Collet <remi@fedoraproject.org> - 2.1.0-2
- sync with rawhide, cleanups
- Obsoletes php53*, php54* on EL

* Tue Aug 07 2012 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- update to 2.1.0
- add patch to lower libmemcached required version

* Sun Apr 22 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-6
- rebuild for libmemcached 1.0.6 (with SASL) and php 5.4

* Sun Apr 22 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-5
- rebuild for libmemcached 1.0.6 (with SASL) and php 5.3

* Sat Apr 21 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-4
- rebuild for libmemcached 1.0.6 and php 5.4

* Sat Apr 21 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-3
- rebuild for libmemcached 1.0.6 and php 5.3

* Sat Mar 03 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-2
- update to 2.0.1 for PHP 5.4

* Sat Mar 03 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1 for PHP 5.3

* Sat Mar 03 2012  Remi Collet <remi@fedoraproject.org> - 2.0.0-2
- update to 2.0.0 for PHP 5.4

* Sat Mar 03 2012  Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0 for PHP 5.3

* Wed Nov 16 2011  Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.1736623
- update to git snapshot (post 2.0.0b2) for php 5.4 build

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

