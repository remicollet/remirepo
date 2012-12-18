%{!?__pecl:            %{expand: %%global __pecl     %{_bindir}/pecl}}

%define pecl_name LZF

Name:           php-pecl-lzf
Version:        1.6.2
Release:        2%{?dist}.4
Summary:        Extension to handle LZF de/compression
Group:          Development/Languages
License:        PHP
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# remove bundled lzf libs
Patch0:         php-lzf-rm-bundled-libs.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel
BuildRequires:  php-pear >= 1:1.4.0
%if 0%{?fedora} >= 14 || 0%{?rhel} >= 5
BuildRequires:  liblzf-devel
%endif

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Provides:       php-lzf = %{version}
Provides:       php-lzf%{?_isa} = %{version}
Provides:       php-pecl(%{pecl_name}) = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}

# Other third party repo stuff
Obsoletes:      php53-pecl-memcache
Obsoletes:      php53u-pecl-memcache
%if "%{php_version}" > "5.4"
Obsoletes:      php54-pecl-memcache
%endif
%if "%{php_version}" > "5.5"
Obsoletes:      php55-pecl-memcache
%endif

# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
This extension provides LZF compression and decompression using the liblzf
library

LZF is a very fast compression algorithm, ideal for saving space with a 
slight speed cost.


%prep
%setup -c -q

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 5
cd %{pecl_name}-%{version}
%patch0 -p1 -b liblzf
rm -f lzf_c.c lzf_d.c lzf.h
cd ..
%endif

cp -r %{pecl_name}-%{version} %{pecl_name}-%{version}-zts

cat >lzf.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=lzf.so
EOF


%build
cd %{pecl_name}-%{version}
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-%{version}-zts
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install -C %{pecl_name}-%{version}     INSTALL_ROOT=%{buildroot}
make install -C %{pecl_name}-%{version}-zts INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 lzf.ini %{buildroot}%{php_inidir}/lzf.ini
install -D -m 644 lzf.ini %{buildroot}%{php_ztsinidir}/lzf.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
cd %{pecl_name}-%{version}

TEST_PHP_EXECUTABLE=%{__php} \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__php} run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=lzf.so \

cd ../%{pecl_name}-%{version}-zts

TEST_PHP_EXECUTABLE=%{__ztsphp} \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__ztsphp} run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=lzf.so \


%clean
rm -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ]  ; then
   %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/CREDITS
%config(noreplace) %{php_inidir}/lzf.ini
%config(noreplace) %{php_ztsinidir}/lzf.ini
%{php_extdir}/lzf.so
%{php_ztsextdir}/lzf.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Fri Nov 30 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.6.2-2.1
- also provides php-lzf

* Sun Oct 21 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.6.2-2
- sync with rawhide (use system liblzf)

* Sat Oct 20 2012 Andrew Colin Kissa - 1.6.2-1
- Upgrade to latest upstream
- Fix bugzilla #838309 #680230

* Mon Jul 09 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.6.2-1
- update to 1.6.2

* Sat Jul 07 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.6.1-1
- update to 1.6.1

* Fri Nov 18 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.5.2-8
- php 5.4 build

* Sat Oct 15 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.5.2-7
- zts extension
- spec cleanup

* Fri Jul 15 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 1.5.2-7
- Fix bugzilla #715791

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.5.2-4
- rebuild for new PHP 5.3.0 ABI (20090626)

* Mon Jun 22 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.5.2-3
- Consistent use of macros

* Mon Jun 22 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.5.2-2
- Fixes to the install to retain timestamps and other fixes raised in review

* Sun Jun 14 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.5.2-1
- Initial RPM package
