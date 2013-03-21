%{!?__pecl: %{expand: %%global __pecl %{_bindir}/pecl}}

%global pecl_name   uuid

Summary:       Universally Unique Identifier extension for PHP
Name:          php-pecl-uuid
Version:       1.0.3
Release:       3%{?dist}.5
License:       LGPLv2+
Group:         Development/Languages
URL:           http://pecl.php.net/package/uuid
Source:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
# https://bugs.php.net/63446 - Please Provides LICENSE file
# http://svn.php.net/viewvc/pecl/uuid/trunk/LICENSE?view=co
Source1:       %{pecl_name}-LICENSE

# http://svn.php.net/viewvc?view=revision&revision=328255
# Use preg_match to avoid "Function ereg() is deprecated" in test suite
Patch0:        %{pecl_name}-ereg.patch
# http://svn.php.net/viewvc?view=revision&revision=328259
# Fix build warnings
Patch1:        %{pecl_name}-build.patch
# http://svn.php.net/viewvc?view=revision&revision=328261
# Improves phpinfo() output
Patch2:        %{pecl_name}-info.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php-devel
BuildRequires: php-pear
BuildRequires: libuuid-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}
# both provides same extension, with different API
Conflicts:     uuid-php

Provides:      php-%{pecl_name} = %{version}
Provides:      php-%{pecl_name}%{?_isa} = %{version}
Provides:      php-pecl(%{pecl_name}) = %{version}
Provides:      php-pecl(%{pecl_name})%{?_isa} = %{version}

# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
%if "%{php_version}" > "5.4"
Obsoletes:     php54-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.5"
Obsoletes:     php55-pecl-%{pecl_name}
%endif


# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
A wrapper around Universally Unique Identifier library (libuuid).


%prep
%setup -q -c 

cd %{pecl_name}-%{version}
cp %{SOURCE1} LICENSE

%patch0 -p3 -b .ereg
%patch1 -p3 -b .build
%patch2 -p3 -b .info

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_UUID_VERSION/{s/.* "//;s/".*$//;p}' php_uuid.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

# duplicate for ZTS build
cp -pr %{pecl_name}-%{version} %{pecl_name}-zts

# Drop in the bit of configuration
cat > %{pecl_name}.ini << 'EOF'
; Enable UUID extension module
extension = %{pecl_name}.so
EOF


%build
export PHP_RPATH=no

cd %{pecl_name}-%{version}
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-zts
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
# Install the NTS stuff
make -C %{pecl_name}-%{version} install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

# Install the ZTS stuff
make -C %{pecl_name}-zts install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
cd %{pecl_name}-%{version}

TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php

cd ../%{pecl_name}-zts

TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc %{pecl_name}-%{version}/{CREDITS,LICENSE}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini


%changelog
* Sat Nov 24 2012 Remi Collet <remi@fedoraproject.org> - 1.0.3-3
- add LICENSE from upstream SVN
- also provides php-uuid

* Tue Nov  6 2012 Remi Collet <remi@fedoraproject.org> - 1.0.3-2
- more upstream patches (build warning + phpinfo output)

* Tue Nov  6 2012 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- initial package, version 1.0.3 (stable)
