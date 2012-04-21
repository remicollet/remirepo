%{!?__pecl:  %{expand: %%global __pecl  %{_bindir}/pecl}}

%define pecl_name sphinx

Name:           php-pecl-sphinx
Version:        1.2.0
Release:        1%{?dist}
Summary:        PECL extension for Sphinx SQL full-text search engine
Group:          Development/Languages
License:        PHP
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libsphinxclient-devel
BuildRequires:  php-pear
BuildRequires:  php-devel >= 5.1.3

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Provides:       php-pecl(%{pecl_name}) = %{version}


# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{-libdir}/.*\\.so$


%description
This extension provides PHP bindings for libsphinxclient, 
client library for Sphinx the SQL full-text search engine.


%prep
%setup -q -c

# https://bugs.php.net/bug.php?id=61793
sed -i -e '/PHP_SPHINX_VERSION/s/1.1.0/%{version}/'  %{pecl_name}-%{version}/php_sphinx.h

# Check reported version (phpinfo), as this is often broken
extver=$(sed -n '/#define PHP_SPHINX_VERSION/{s/.* "//;s/".*$//;p}' %{pecl_name}-%{version}/php_sphinx.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

cp -pr %{pecl_name}-%{version} %{pecl_name}-%{version}-zts


%build
cd %{pecl_name}-%{version}
phpize
%configure  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-%{version}-zts
zts-phpize
%configure  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%check
# simple module load test
%{__php} --no-php-ini \
    --define extension_dir=%{pecl_name}-%{version}/modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}
%{__ztsphp} --no-php-ini \
    --define extension_dir=%{pecl_name}-%{version}-zts/modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


%install
rm -rf %{buildroot}

make -C %{pecl_name}-%{version} \
     install INSTALL_ROOT=%{buildroot}

make -C %{pecl_name}-%{version}-zts \
     install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini


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
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Sat Apr 21 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.2.0-1
- update to 1.2.0

* Mon Nov 21 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.1.0-3
- add patch for php 5.4, see https://bugs.php.net/60349

* Wed Oct 05 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.1.0-2
- ZTS extension
- spec cleanups

* Sat Jul 16 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.1.0-1
- rebuild for remi repository

* Fri Jul 15 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 1.1.0-1
- Update to latest upstream
- Fix bugzilla #715830

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 26 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.0.4-1
- update to 1.0.4

* Sat Sep 12 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-2
- rebuild for remi repository and PHP 5.3

* Sun Sep 06 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.0-2
- Add checks
- Add php-devel version requirement

* Mon Aug 05 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.0-1
- Initial package
