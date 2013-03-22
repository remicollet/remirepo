%{!?__pecl:  %{expand: %%global __pecl     %{_bindir}/pecl}}

%global pecl_name cairo
%global versuffix -beta

Name:           php-pecl-cairo
Version:        0.3.2
Release:        4%{?dist}
Summary:        Cairo Graphics Library Extension
Group:          Development/Languages
License:        PHP
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# see https://bugs.php.net/61882
Patch0:         pecl-cairo-php_streams.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  cairo-devel >= 1.4
BuildRequires:  freetype-devel
BuildRequires:  php-devel
BuildRequires:  php-pear >= 1:1.4.0

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Provides:       php-%{pecl_name} = %{version}
Provides:       php-%{pecl_name}%{?_isa} = %{version}
Provides:       php-pecl(%{pecl_name}) = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}

# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
%if "%{php_version}" > "5.4"
Obsoletes:     php54-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.5"
Obsoletes:     php55-pecl-%{pecl_name}
%endif

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{_libdir}/.*\\.so$


%description
Cairo is a 2D graphics library with support for multiple output devices.
Currently supported output targets include the X Window System, Quartz,
Win32, image buffers, PostScript, PDF, and SVG file output.

%package devel
Summary:       Cairo Graphics Library Extension developer files
Group:         Development/Libraries
Requires:      php-pecl-cairo%{?_isa} = %{version}-%{release}
Requires:      php-devel%{?_isa}

%description devel
These are the files needed to compile programs using cairo extension.


%prep
%setup -c -q

%patch0 -p0 -b .61882

# Check reported version (phpinfo), as this is often broken
extver=$(sed -n '/#define PHP_CAIRO_VERSION/{s/.* "//;s/".*$//;p}' Cairo-%{version}/php_cairo.h)
if test "x${extver}" != "x%{version}%{?versuffix}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

cp -pr Cairo-%{version} Cairo-%{version}-zts


%build
cd Cairo-%{version}
%{_bindir}/phpize
%configure  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../Cairo-%{version}-zts
%{_bindir}/zts-phpize
%configure  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make -C Cairo-%{version} \
     install INSTALL_ROOT=%{buildroot}

make -C Cairo-%{version}-zts \
     install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini


%check
# 32/445 test failing with old cairo 1.8

cd Cairo-%{version}
TEST_PHP_EXECUTABLE=%{__php} \
%if 0%{?fedora} > 13
REPORT_EXIT_STATUS=1 \
%else
REPORT_EXIT_STATUS=0 \
%endif
NO_INTERACTION=1 \
%{__php} run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=%{pecl_name}.so

cd ../Cairo-%{version}-zts
TEST_PHP_EXECUTABLE=%{__ztsphp} \
%if 0%{?fedora} > 13
REPORT_EXIT_STATUS=1 \
%else
REPORT_EXIT_STATUS=0 \
%endif
NO_INTERACTION=1 \
%{__ztsphp} run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=%{pecl_name}.so


%clean
rm  -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ]  ; then
   %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc Cairo-%{version}/{CREDITS,IGNORED,SYMBOLS,TODO,LICENSE}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%files devel
%{_includedir}/php/ext/%{pecl_name}
%{php_ztsincldir}/ext/%{pecl_name}


%changelog
* Thu Aug  9 2012 Remi Collet <remi@fedoraproject.org> - 0.3.2-4
- also provides php-cairo

* Thu Aug  9 2012 Remi Collet <remi@fedoraproject.org> - 0.3.2-3
- add patch for https://bugs.php.net/61882
- (re)enabling test result on fedora > 13

* Sun Apr 22 2012 Remi Collet <remi@fedoraproject.org> - 0.3.2-2
- update to 0.3.2-beta, rebuild for php 5.4

* Sun Apr 22 2012 Remi Collet <remi@fedoraproject.org> - 0.3.2-1
- update to 0.3.2-beta

* Sat Apr 21 2012 Remi Collet <remi@fedoraproject.org> - 0.3.1-2
- rebuild for php 5.4

* Sat Apr 21 2012 Remi Collet <remi@fedoraproject.org> - 0.3.1-1
- Initial RPM package
- request for LICENSE https://bugs.php.net/61794
