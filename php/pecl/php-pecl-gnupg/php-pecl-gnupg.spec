%{!?__pecl:   %{expand: %%global __pecl     %{_bindir}/pecl}}
%global pecl_name   gnupg

Summary:      Wrapper around the gpgme library
Name:         php-pecl-gnupg
Version:      1.3.2
Release:      3%{?dist}.5

License:      BSD
Group:        Development/Languages
URL:          http://pecl.php.net/package/gnupg
Source0:      http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# http://svn.php.net/viewvc/pecl/gnupg/trunk/tests/vars.inc?view=co
Source1:      vars.inc
# https://bugs.php.net/60915 PHP 5.4 build
Patch0:       gnupg-php54.patch
# https://bugs.php.net/60913 Fix test suite
Patch1:       gnupg-tests.patch
# https://bugs.php.net/60916 Force use of /usr/bin/gpg
Patch2:       gnupg-gpg1.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel
BuildRequires: gpgme-devel
BuildRequires: php-pear
BuildRequires: gnupg

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}
# We force use of /usr/bin/gpg as gpg2 is unusable in non-interactive mode
Requires:     gnupg

Provides:     php-%{pecl_name} = %{version}
Provides:     php-%{pecl_name}%{?_isa} = %{version}
Provides:     php-pecl(%{pecl_name}) = %{version}
Provides:     php-pecl(%{pecl_name})%{?_isa} = %{version}

# Other third party repo stuff
Obsoletes:    php53-pecl-%{pecl_name}
Obsoletes:    php53u-pecl-%{pecl_name}
%if "%{php_version}" > "5.4"
Obsoletes:    php54-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.5"
Obsoletes:    php55-pecl-%{pecl_name}
%endif

# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
This module allows you to interact with gnupg. 

Documentation : http://www.php.net/gnupg


%prep 
%setup -c -q

cp %{SOURCE1} %{pecl_name}-%{version}/tests
%patch0 -p0 -b .php54
%patch1 -p0 -b .tests
%patch2 -p0 -b .gpg1

# Create configuration file
cat >%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

%if 0%{?rhel} == 5
# GnuPG seems to old
rm -f %{pecl_name}-%{version}/tests/gnupg_{oo,res}_listsignatures.phpt
%endif

# Fix version for phpinfo()
# https://bugs.php.net/60914
sed -i -e /PHP_GNUPG_VERSION/s/1.3.2-dev/1.3.2/ %{pecl_name}-%{version}/php_gnupg.h

# Check extension version
extver=$(sed -n '/#define PHP_GNUPG_VERSION/{s/.* "//;s/".*$//;p}' %{pecl_name}-%{version}/php_gnupg.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi

# Build ZTS extension if ZTS devel available (fedora >= 17)
cp -r %{pecl_name}-%{version} %{pecl_name}-zts


%build
export PHP_RPATH=no
export CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -DGNUPG_PATH='\"/usr/bin/gpg\"'"

cd %{pecl_name}-%{version}
%{_bindir}/phpize
%configure \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-zts
%{_bindir}/zts-phpize
%configure \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
# for short-circuit
rm -rf %{pecl_name}-*/modules/{json,mysqlnd}.so

make install -C %{pecl_name}-%{version} \
     INSTALL_ROOT=%{buildroot}

make install -C %{pecl_name}-zts \
     INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

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

unset GPG_AGENT_INFO

# run full test suite
TEST_PHP_EXECUTABLE=%{_bindir}/php \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
php run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=%{pecl_name}.so

cd ../%{pecl_name}-zts

# run full test suite
TEST_PHP_EXECUTABLE=%{__ztsphp} \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__ztsphp} run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=%{pecl_name}.so


%files
%defattr(-, root, root, -)
%doc %{pecl_name}-%{version}/{LICENSE,README}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so


%changelog
* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> - 1.3.2-3.1
- also provides php-gnupg + cleanups

* Sun May 06 2012 Remi Collet <remi@fedoraproject.org> - 1.3.2-3
- improve patch

* Sat Jan 28 2012 Remi Collet <remi@fedoraproject.org> - 1.3.2-2
- build against PHP 5.4

* Sat Jan 28 2012 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- Initial RPM
- open upstream bugs
  https://bugs.php.net/60913 - test suite fails
  https://bugs.php.net/60914 - bad version
  https://bugs.php.net/60915 - php 5.4 build fails
  https://bugs.php.net/60916 - force use of /usr/bin/gpg

