# spec file for php-pecl-couchbase
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#

%{!?php_inidir:  %global php_inidir   %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl       %{_bindir}/pecl}
%{!?__php:       %global __php        %{_bindir}/php}

%global pecl_name couchbase
%global with_zts  0%{?__ztsphp:1}

Summary:       Couchbase Server PHP extension
Name:          php-pecl-couchbase
Version:       1.2.1
Release:       2%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:       PHP
Group:         Development/Languages
URL:           pecl.php.net/package/couchbase
Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}%{?svnrev:-dev}.tgz

# https://github.com/couchbase/php-ext-couchbase/pull/9
Patch0:        %{pecl_name}-zts.patch

BuildRequires: php-devel >= 5.3.0
BuildRequires: php-pecl-igbinary-devel
BuildRequires: php-pear
BuildRequires: zlib-devel
BuildRequires: libcouchbase-devel
# for tests
BuildRequires: php-json

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}
Requires:      php-pecl-igbinary%{?_isa}

Provides:      php-%{pecl_name} = %{version}
Provides:      php-%{pecl_name}%{?_isa} = %{version}
Provides:      php-pecl(%{pecl_name}) = %{version}
Provides:      php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet"
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
Obsoletes:     php54-pecl-%{pecl_name}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The PHP client library provides fast access to documents stored
in a Couchbase Server.


%prep
%setup -q -c

mv %{pecl_name}-%{version} NTS

cd NTS
%patch0 -p1 -b .ztsfix

# Fix version
sed -e '/PHP_COUCHBASE_VERSION/s/1.2.0/%{version}/' -i php_couchbase.h

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_COUCHBASE_VERSION/{s/.* "//;s/".*$//;p}' php_couchbase.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}..
   exit 1
fi
cd ..

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
rm -f */modules/{json,igbinary}.so

# Install the NTS stuff
make install -C NTS INSTALL_ROOT=%{buildroot}
install -D -m 644 NTS/example/%{pecl_name}.ini %{buildroot}%{php_inidir}/z-%{pecl_name}.ini

# Install the ZTS stuff
%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}
install -D -m 644 ZTS/example/%{pecl_name}.ini %{buildroot}%{php_ztsinidir}/z-%{pecl_name}.ini
%endif

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Test & Documentation
cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
: minimal NTS load test
ln -sf %{php_extdir}/{json,igbinary}.so NTS/modules/
%{__php} -n \
   -d extension_dir=NTS/modules \
   -d extension=igbinary.so \
   -d extension=json.so \
   -d extension=%{pecl_name}.so \
   -m | grep %{pecl_name}

%if %{with_zts}
: minimal ZTS load test
ln -sf %{php_ztsextdir}/{json,igbinary}.so ZTS/modules/
%{__ztsphp}    -n \
   -d extension_dir=ZTS/modules \
   -d extension=igbinary.so \
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
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/z-%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/z-%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif



%changelog
* Sun Mar 16 2014 Remi Collet <remi@fedoraproject.org> - 1.2.1-2
- install doc in pecl_docdir

* Sat Oct 05 2013 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1
- add patch to fix ZTS build
  https://github.com/couchbase/php-ext-couchbase/pull/9

* Mon May 13 2013 Remi Collet <remi@fedoraproject.org> - 1.1.15-2
- fix dependency on php-pecl-igbinary

* Thu May  9 2013 Remi Collet <remi@fedoraproject.org> - 1.1.15-1
- update to 1.1.15 (no change)

* Fri Mar 22 2013 Remi Collet <remi@fedoraproject.org> - 1.1.14-1
- initial package
