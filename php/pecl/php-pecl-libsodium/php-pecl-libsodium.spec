# remirepo spec file for php-pecl-libsodium
#
# Copyright (c) 2014-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
%scl_package       php-pecl-libsodium
%endif

%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name  libsodium
%global with_tests 0%{!?_without_tests:1}
%if "%{php_version}" < "5.6"
%global ini_name   %{pecl_name}.ini
%else
%global ini_name   40-%{pecl_name}.ini
%endif
%global buildver   %(pkg-config --silence-errors --modversion libsodium 2>/dev/null || echo 65536)

Summary:        Wrapper for the Sodium cryptographic library
Name:           %{?sub_prefix}php-pecl-%{pecl_name}
Version:        1.0.6
Release:        1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if "%{?vendor}" == "Remi Collet"
# Ensure libsodium-last is used
BuildRequires:  libsodium-devel >= 1.0.7
%else
# Per upstream documentation
BuildRequires:  libsodium-devel >= 0.6.0
%endif
BuildRequires:  %{?scl_prefix}php-devel > 5.4
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-json
BuildRequires:  pkgconfig

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       libsodium%{?_isa} >= %{buildver}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif

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
%endif

# Filter shared private - always as libsodium.so is a bad name
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
A simple, low-level PHP extension for libsodium.

Documentation: https://paragonie.com/book/pecl-libsodium

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{scl_vendor})}.


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

# Don't install tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_LIBSODIUM_VERSION/{s/.* "//;s/".*$//;p}' php_libsodium.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif

# Create configuration file
cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


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
cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_tests}
: Upstream test suite  for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=json.so -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff
%endif

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_tests}
: Upstream test suite  for ZTS extension
TEST_PHP_EXECUTABLE=%{_bindir}/zts-php \
TEST_PHP_ARGS="-n -d extension=json.so -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/zts-php -n run-tests.php --show-diff
%endif
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{pecl_name}
%{?_licensedir:%license NTS/LICENSE}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Thu May 05 2016 Remi Collet <remi@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6

* Fri Apr 08 2016 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5

* Tue Apr 05 2016 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4 (no change since 1.0.3)

* Tue Apr  5 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3
- raise minimal PHP version to 5.4
- drop patch merged upstream

* Sun Mar  6 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-4
- adapt for F24

* Wed Dec  9 2015 Remi Collet <remi@fedoraproject.org> - 1.0.2-3
- rebuild against libsodium 1.0.7
- add upstream patch for test suite from
  https://github.com/jedisct1/libsodium-php/pull/70

* Wed Nov  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.2-2
- rebuild against libsodium 1.0.6

* Tue Oct 27 2015 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2
- drop all patches, merged upstream

* Tue Oct 27 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1
- fix for old libsodium
  https://github.com/jedisct1/libsodium-php/pull/63
- don't zero interned string
  https://github.com/jedisct1/libsodium-php/pull/62
- add dependency on libsodium version used at build time

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-3
- rebuild for PHP 7.0.0RC5 new API version

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- F23 rebuild with rh_layout

* Thu Sep 03 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0 (stable)

* Mon Jul 27 2015 Remi Collet <remi@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1 (beta)

* Sun Jul 26 2015 Remi Collet <remi@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0 (beta)

* Wed Jul 22 2015 Remi Collet <remi@fedoraproject.org> - 0.1.3-4
- rebuild against php 7.0.0beta2

* Wed Jul  8 2015 Remi Collet <remi@fedoraproject.org> - 0.1.3-3
- rebuild against php 7.0.0beta1

* Wed Jun 24 2015 Remi Collet <remi@fedoraproject.org> - 0.1.3-2
- allow build against rh-php56 (as more-php56)
- rebuild for "rh_layout" (php70)

* Wed Apr 15 2015 Remi Collet <remi@fedoraproject.org> - 0.1.3-1
- Update to 0.1.3 (beta)

* Thu Apr 02 2015 Remi Collet <remi@fedoraproject.org> - 0.1.2-1
- Update to 0.1.2 (beta)
- drop runtime dependency on pear, new scriptlets
- open https://github.com/jedisct1/libsodium-php/pull/22 - build
- open https://github.com/jedisct1/libsodium-php/pull/23 - php 7

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 0.1.1-1.1
- Fedora 21 SCL mass rebuild

* Sun Sep 28 2014 Remi Collet <rcollet@redhat.com> - 0.1.1-1
- initial package, version 0.1.1 (beta)
- open https://github.com/jedisct1/libsodium-php/pull/14

