%{!?__pecl:  %{expand: %%global __pecl     %{_bindir}/pecl}}

%define pecl_name cairo

Name:           php-pecl-cairo
Version:        0.3.1
Release:        1%{?dist}
Summary:        Cairo Graphics Library Extension
Group:          Development/Languages
License:        PHP
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

Patch0:         cairo-tests.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  cairo-devel >= 1.4
BuildRequires:  freetype-devel
BuildRequires:  php-devel
BuildRequires:  php-pear >= 1:1.4.0

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Provides:       php-pecl(%{pecl_name}) = %{version}

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

# Fix version https://bugs.php.net/61795
sed -i -e '/PHP_CAIRO_VERSION/s/0.2.1-beta/%{version}/' Cairo-%{version}/php_cairo.h

# Check reported version (phpinfo), as this is often broken
extver=$(sed -n '/#define PHP_CAIRO_VERSION/{s/.* "//;s/".*$//;p}' Cairo-%{version}/php_cairo.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

cd Cairo-%{version}
%patch0 -p0
cd ..

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
cd Cairo-%{version}
TEST_PHP_EXECUTABLE=%{__php} \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__php} run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=%{pecl_name}.so

cd ../Cairo-%{version}-zts
TEST_PHP_EXECUTABLE=%{__ztsphp} \
REPORT_EXIT_STATUS=1 \
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
%doc Cairo-%{version}/{CREDITS,IGNORED,SYMBOLS,TODO}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%files devel
%{_includedir}/php/ext/%{pecl_name}
%{php_ztsincldir}/ext/%{pecl_name}


%changelog
* Sat Apr 21 2012 Remi Collet <remi@fedoraproject.org> - 0.3.1-1
- Initial RPM package
- request for LICENSE https://bugs.php.net/61794
