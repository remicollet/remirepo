%{!?__pecl: %{expand: %%global __pecl %{_bindir}/pecl}}

%global pecl_name yaf

Summary:       Yet Another Framework
Name:          php-pecl-yaf
Version:       2.2.5
Release:       1%{?dist}
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/yaf
Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source1:       %{pecl_name}.ini

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php-devel >= 5.2.0
BuildRequires: php-pear
BuildRequires: pcre-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

Provides:      php-pecl(%{pecl_name}) = %{version}
Provides:      php-pecl(%{pecl_name})%{?_isa} = %{version}

# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
%if "%{php_version}" > "5.4"
Obsoletes:     php54-pecl-%{pecl_name}
%endif


# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
The Yet Another Framework (Yaf) extension is a PHP framework that is used
to develop web applications. 


%prep
%setup -q -c 

# Sanity check, really often broken
extver=$(sed -n '/#define YAF_VERSION/{s/.*\t"//;s/".*$//;p}' %{pecl_name}-%{version}/php_yaf.h )
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi

%if 0%{?__ztsphp:1}
# duplicate for ZTS build
cp -pr %{pecl_name}-%{version}  %{pecl_name}-zts
%endif


%build
cd %{pecl_name}-%{version}
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if 0%{?__ztsphp:1}
cd ../%{pecl_name}-zts
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}
# Install the NTS stuff
make -C %{pecl_name}-%{version} \
     install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini

# Install the ZTS stuff
%if 0%{?__ztsphp:1}
make -C %{pecl_name}-zts \
     install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

# Install the package XML file
install -D -m 644 package2.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
cd %{pecl_name}-%{version}

TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php

%if 0%{?__ztsphp:1}
cd ../%{pecl_name}-zts

TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php
%endif


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/{LICENSE,CREDITS}

%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%if 0%{?__ztsphp:1}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%endif


%changelog
* Mon Oct 22 2012 Remi Collet <remi@fedoraproject.org> - 2.2.5-1
- version 2.2.5 (stable)
- LICENSE now provided by upstream

* Tue Sep  4 2012 Remi Collet <remi@fedoraproject.org> - 2.2.4-1
- version 2.2.4 (beta)
- initial package

