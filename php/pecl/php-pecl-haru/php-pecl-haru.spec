# spec file for php-pecl-haru
#
# Copyright (c) 2012-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package        php-pecl-haru}

%global pecl_name  haru
%global with_zts   0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
%global ini_name   %{pecl_name}.ini
%else
%global ini_name   40-%{pecl_name}.ini
%endif

Summary:      Haru PDF functions
Name:         %{?scl_prefix}php-pecl-haru
Version:      1.0.4
Release:      6%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}

License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/haru

Source0:      http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{?scl_prefix}php-devel
BuildRequires: %{?scl_prefix}php-pear
BuildRequires: libharu-devel
BuildRequires: libpng-devel
BuildRequires: zlib-devel

Requires:     %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:     %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:     %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:     %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:     %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:     %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
Obsoletes:     php54-pecl-%{pecl_name}
Obsoletes:     php54w-pecl-%{pecl_name}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}
Obsoletes:     php55w-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name}
Obsoletes:     php56w-pecl-%{pecl_name}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The PECL/haru extension provides bindings to the libHaru library.

libHaru is a free, cross platform, and Open Source library for
generating PDF files. 

Documentation : http://www.php.net/haru

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep 
%setup -c -q
mv %{pecl_name}-%{version} NTS

%{?_licensedir:sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml}

# Create configuration file
cat >%{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

# Check extension version
extver=$(sed -n '/#define PHP_HARU_VERSION/{s/.* "//;s/".*$//;p}' NTS/php_haru.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi

%if %{with_zts}
# Build ZTS extension if ZTS devel available (fedora >= 17)
cp -r NTS ZTS
%endif


%build
export PHP_RPATH=no

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

make install -C NTS INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}

install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Test & Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%clean
rm -rf %{buildroot}


%if 0%{?fedora} < 24
# when pear installed alone, after us
%triggerin -- %{?scl_prefix}php-pear
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

# posttrans as pear can be installed after us
%posttrans
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

%postun
if [ $1 -eq 0 -a -x %{__pecl} ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%check
: Check if build NTS extension can be loaded
%{__php} -n -q \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Check if build ZTS extension can be loaded
%{__ztsphp} -n -q \
    -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


%files
%defattr(-, root, root, -)
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Tue Mar  8 2016 Remi Collet <remi@fedoraproject.org> - 1.0.4-6
- adapt for F24
- drop runtime dependency on pear, new scriptlets
- fix license management

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.0.4-5.1
- Fedora 21 SCL mass rebuild

* Tue Aug 26 2014 Remi Collet <rcollet@redhat.com> - 1.0.4-5
- improve SCL build

* Wed Apr 16 2014 Remi Collet <remi@fedoraproject.org> - 1.0.4-4
- add numerical prefix to extension configuration file

* Wed Mar 26 2014 Remi Collet <remi@fedoraproject.org> - 1.0.4-3
- allow SCL build

* Mon Mar 17 2014 Remi Collet <remi@fedoraproject.org> - 1.0.4-2
- cleanups
- install doc in pecl_docdir

* Mon Dec 24 2012 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- update to 1.0.4
- also provides php-haru

* Thu Feb 02 2012 Remi Collet <remi@fedoraproject.org> - 1.0.3-2
- build against php 5.4

* Thu Feb 02 2012 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Initial RPM
- https://bugs.php.net/60958 - Please Provides LICENSE file
- https://bugs.php.net/60959 - Version 1.0.3 reports as 1.0.1

