%{!?php_inidir: %{expand: %%global php_inidir %{_sysconfdir}/php.d}}
%{!?__php:      %{expand: %%global __php      %{_bindir}/php}}
%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}

%global pecl_name couchbase
%global with_zts  0%{?__ztsphp:1}
%global versuf    dp1

Summary:       Couchbase Server PHP extension
Name:          php-pecl-couchbase
Version:       1.1.4
Release:       1%{?dist}
License:       PHP
Group:         Development/Languages
URL:           pecl.php.net/package/couchbase
Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}%{?svnrev:-dev}.tgz

BuildRequires: php-devel >= 5.3.0
BuildRequires: php-pear
BuildRequires: httpd-devel
BuildRequires: pcre-devel
BuildRequires: libcouchbase-devel
# for tests
BuildRequires: php-json

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

Provides:      php-%{pecl_name} = %{version}
Provides:      php-%{pecl_name}%{?_isa} = %{version}
Provides:      php-pecl(%{pecl_name}) = %{version}
Provides:      php-pecl(%{pecl_name})%{?_isa} = %{version}

# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
The PHP client library provides fast access to documents stored
in a Couchbase Server.


%prep
%setup -q -c -T
tar xif %{SOURCE0}

mv %{pecl_name}-%{version} NTS

cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

EOF

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_COUCHBASE_VERSION/{s/.* "//;s/".*$//;p}' NTS/php_couchbase.h)
if test "x${extver}" != "x%{version}%{?versuf}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?versuf}..
   exit 1
fi

%if 0%{?__ztsphp:1}
# duplicate for ZTS build
cp -pr NTS ZTS
%else
: Only NTS build, no ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
# for short-circuit
rm -f */modules/json.so

# Install the NTS stuff
make install -C NTS INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/z-%{pecl_name}.ini

# Install the ZTS stuff
%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/z-%{pecl_name}.ini
%endif

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
: minimal NTS load test
ln -sf %{php_extdir}/json.so NTS/modules/
%{__php} -n \
   -d extension_dir=NTS/modules \
   -d extension=json.so \
   -d extension=%{pecl_name}.so \
   -m | grep %{pecl_name}

%if %{with_zts}
: minimal ZTS load test
ln -sf %{php_ztsextdir}/json.so ZTS/modules/
%{__ztsphp}    -n \
   -d extension_dir=ZTS/modules \
   -d extension=json.so \
   -d extension=%{pecl_name}.so \
   -m | grep %{pecl_name}
%endif


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%doc NTS/{CREDITS,LICENSE,*md}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/z-%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/z-%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif



%changelog
* Fri Mar 22 2013 Remi Collet <remi@fedoraproject.org> - 1.1.14-1
- initial package
