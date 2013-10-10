# spec file for php-pecl-xrange
#
# Copyright (c) 2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?php_inidir:  %{expand: %%global php_inidir  %{_sysconfdir}/php.d}}
%{!?__pecl:      %{expand: %%global __pecl      %{_bindir}/pecl}}

%global with_zts  0%{?__ztsphp:1}
%global pecl_name Judy
%global  ext_name judy

Summary:        PHP Judy implements sparse dynamic arrays
Name:           php-pecl-%{pecl_name}
Version:        1.0.0
Release:        2%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# Retrieved from http://svn.php.net/viewvc/pecl/judy/trunk/
Source1:        LICENSE
Source2:        README
Source3:        CREDITS

# http://svn.php.net/viewvc?view=revision&revision=331753
# http://svn.php.net/viewvc?view=revision&revision=331755
# http://svn.php.net/viewvc?view=revision&revision=331758
# http://svn.php.net/viewvc?view=revision&revision=331760
# http://svn.php.net/viewvc?view=revision&revision=331761
Patch0:         %{pecl_name}-svn.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel
BuildRequires:  php-pear
BuildRequires:  Judy-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires:       php-spl%{?_isa}

Provides:       php-%{ext_name} = %{version}
Provides:       php-%{ext_name}%{?_isa} = %{version}
Provides:       php-pecl(%{pecl_name}) = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}

# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
PHP Judy implements sparse dynamic arrays (aka Judy Arrays).
This extension is based on the Judy C library. A Judy array
consumes memory only when it is populated, yet can grow to
take advantage of all available memory if desired. Judy's key
benefits are scalability, high performance, and memory efficiency.


%package devel
Summary:       %{name} developer files (header)
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      php-devel%{?_isa}

%description devel
These are the files needed to compile programs using %{name}.


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

cd NTS
%ifarch x86_64
# https://bugzilla.redhat.com/show_bug.cgi?id=1017338
# Segfault in large bitset array
rm -f tests/bitset_003.phpt \
      tests/bitset_004.phpt
%endif
%patch0 -p3

cp %{SOURCE1} %{SOURCE2} %{SOURCE3} .

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_JUDY_VERSION/{s/.* "//;s/".*$//;p}' php_judy.h)
if test "x${extver}" != "x%{version}%{?prever:-%{prever}}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever:-%{prever}}.
   exit 1
fi
cd ..

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif

# Create configuration file
cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{ext_name}.so
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/php-config

make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/zts-php-config

make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{ext_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{ext_name}.ini
%endif


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
: Minimal load test for NTS extension
cd NTS
%{_bindir}/php --no-php-ini \
    --define extension=modules/%{ext_name}.so \
    --modules | grep %{ext_name}

: Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{ext_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php


%if %{with_zts}
: Minimal load test for ZTS extension
cd ../ZTS
%{__ztsphp} --no-php-ini \
    --define extension=modules/%{ext_name}.so \
    --modules | grep %{ext_name}

: Upstream test suite for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{ext_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc NTS/{LICENSE,CREDITS}
%{pecl_xmldir}/%{name}.xml
%config(noreplace) %{php_inidir}/%{ext_name}.ini
%{php_extdir}/%{ext_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ext_name}.ini
%{php_ztsextdir}/%{ext_name}.so
%endif

%files devel
%defattr(-,root,root,-)
%{php_incldir}/ext/%{ext_name}

%if %{with_zts}
%{php_ztsincldir}/ext/%{ext_name}
%endif


%changelog
* Thu Oct 10 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- fix extension name in configuration file

* Wed Oct  9 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package, version 1.0.0 (stable)
