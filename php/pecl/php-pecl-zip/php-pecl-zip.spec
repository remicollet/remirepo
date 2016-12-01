# remirepo spec file for php-pecl-zip
# with SCL compatibility, from:
#
# fedora spec file for php-pecl-zip
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:     %scl_package       php-pecl-zip}

%global with_zts       0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name      zip

%if 0%{?rhel} != 5
%global with_libzip    1
%else
%global with_libzip    0
%endif

%if "%{php_version}" < "5.6"
%global ini_name  %{pecl_name}.ini
%else
%global ini_name  40-%{pecl_name}.ini
%endif
#global prever    dev

Summary:      A ZIP archive management extension
Summary(fr):  Une extension de gestion des ZIP
Name:         %{?scl_prefix}php-pecl-zip
Version:      1.13.5
Release:      2%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%if %{with_libzip}
License:      PHP
%else
# Zip extension is PHP, Libzip library is BSD
License:      PHP and BSD
%endif
Group:        Development/Languages
URL:          http://pecl.php.net/package/zip

Source:       http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{?scl_prefix}php-devel
%if %{with_libzip}
BuildRequires: pkgconfig(libzip) >= 1.0.0
%endif
BuildRequires: zlib-devel
BuildRequires: %{?scl_prefix}php-pear

Requires:     %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:     %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:     %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:     %{?scl_prefix}php-%{pecl_name} = 1:%{version}-%{release}
Provides:     %{?scl_prefix}php-%{pecl_name}%{?_isa} = 1:%{version}-%{release}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php53u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php54-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php54w-pecl-%{pecl_name} <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.1"
Obsoletes:     php71u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php71w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if "%{php_version}" > "7.0"
Obsoletes:     %{?scl_prefix}php-zip <= 7.0.0
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Zip is an extension to create and read zip files.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{scl_vendor})}.

%description -l fr
Zip est une extension pour créer et lire les archives au format ZIP.

Paquet construit pour PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: en Software Collection (%{scl} by %{scl_vendor})}.


%prep 
%setup -c -q

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

mv %{pecl_name}-%{version}%{?prever} NTS
cd NTS

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_ZIP_VERSION/{s/.* "//;s/".*$//;p}' php5/php_zip.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi

%if %{with_libzip}
sed -e '/LICENSE_libzip/d' -i ../package.xml
# delete bundled libzip to ensure it is not used
rm -r lib
%endif

cd ..
: Create the configuration file
cat >%{ini_name} << 'EOF'
; Enable ZIP extension module
extension=%{pecl_name}.so
EOF

%if %{with_zts}
: Duplicate sources tree for ZTS build
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure \
%if %{with_libzip}
  --with-libzip \
%endif
  --with-libdir=%{_lib} \
  --with-php-config=%{_bindir}/php-config

make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
%if %{with_libzip}
  --with-libzip \
%endif
  --with-libdir=%{_lib} \
  --with-php-config=%{_bindir}/zts-php-config

make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd NTS
: minimal load test of NTS extension
%{_bindir}/php --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

: upstream test suite for NTS extension
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
TEST_PHP_EXECUTABLE=%{_bindir}/php \
%{_bindir}/php -n \
   run-tests.php --show-diff

%if %{with_zts}
cd ../ZTS
: minimal load test of ZTS extension
%{_bindir}/zts-php --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

: upstream test suite for ZTS extension
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
TEST_PHP_EXECUTABLE=%{_bindir}/zts-php \
%{_bindir}/zts-php -n \
   run-tests.php --show-diff
%endif


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
* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 1.13.5-2
- rebuild with PHP 7.1.0 GA

* Fri Oct 14 2016 Remi Collet <remi@fedoraproject.org> - 1.13.5-1
- Update to 1.13.5

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 1.13.4-2
- rebuild for PHP 7.1 new API version

* Thu Jul 21 2016 Remi Collet <remi@fedoraproject.org> - 1.13.4-1
- Update to 1.13.4

* Thu Jun 23 2016 Remi Collet <remi@fedoraproject.org> - 1.13.3-1
- Update to 1.13.3

* Tue Mar  1 2016 Remi Collet <remi@fedoraproject.org> - 1.13.2-1
- Update to 1.13.2
- fix license management

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 1.13.1-3
- rebuild for PHP 7.0.0RC5 new API version

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 1.13.1-2
- F23 rebuild with rh_layout

* Wed Sep  9 2015 Remi Collet <remi@fedoraproject.org> - 1.13.1-1
- Update to 1.13.1

* Mon Sep  7 2015 Remi Collet <remi@fedoraproject.org> - 1.13.0-1
- Update to 1.13.0
- raise dependency on libzip 1.0.0

* Wed Apr 15 2015 Remi Collet <remi@fedoraproject.org> - 1.12.5-1
- Update to 1.12.5
- Don't install/register tests

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.12.1-3
- new scriptlets

* Sun Aug 24 2014 Remi Collet <rcollet@redhat.com> 1.12.1-2
- allow SCL build

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 1.12.4-2
- add numerical prefix to extension configuration file

* Wed Jan 29 2014 Remi Collet <remi@fedoraproject.org> - 1.12.4-1
- Update to 1.12.4 (stable) for libzip 0.11.2

* Thu Dec 12 2013 Remi Collet <remi@fedoraproject.org> - 1.12.3-1
- Update to 1.12.3 (stable)
- drop merged patch

* Thu Oct 24 2013 Remi Collet <remi@fedoraproject.org> 1.12.2-2
- upstream patch, don't use any libzip private struct
- drop LICENSE_libzip when system version is used
- always build ZTS extension

* Wed Oct 23 2013 Remi Collet <remi@fedoraproject.org> 1.12.2-1
- update to 1.12.2 (beta)
- drop merged patches
- install doc in pecl doc_dir
- install tests in pecl test_dir

* Tue Aug 20 2013 Remi Collet <remi@fedoraproject.org> 1.12.1-2.1
- backport stuff

* Tue Aug 20 2013 Remi Collet <rcollet@redhat.com> 1.12.1-2
- refresh our merged patches from upstream git

* Thu Aug 08 2013 Remi Collet <rcollet@redhat.com> 1.12.1-1
- New spec for version 1.12.1
