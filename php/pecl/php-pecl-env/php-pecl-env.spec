# remirepo spec file for php-pecl-env
#
# Copyright (c) 2015-2016 Remi Collet
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
%endif

%{?scl:          %scl_package        php-pecl-env}

%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name  env
%if "%{php_version}" < "5.6"
%global ini_name   %{pecl_name}.ini
%else
%global ini_name   40-%{pecl_name}.ini
%endif

Summary:       Load environment variables
Name:          %{?sub_prefix}php-pecl-%{pecl_name}
Version:       0.2.1
Release:       3%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:       MIT
Group:         Development/Languages
URL:           http://pecl.php.net/package/%{pecl_name}

Source:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

Patch0:        %{pecl_name}-pr4.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# ignore min PHP version 5.5 (as work with 5.4)
BuildRequires: %{?scl_prefix}php-devel
BuildRequires: %{?scl_prefix}php-pear

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:      %{?scl_prefix}php-%{pecl_name} = %{version}
Provides:      %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
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

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Based on 12Factor Application rules this extension allows
you to load environment variables into every PHP request,
in every SAPI using a global configuration file with key
value pairs of environment variables.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -c -q
mv %{pecl_name}-%{version} NTS

# Remove test file to avoid regsitration
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS
%patch0 -p1 -b .pr4

# Check upstream version (often broken)
extver=$(sed -n '/#define PHP_ENV_VERSION/{s/.* "//;s/".*$//;p}' php_env.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

cat << 'EOF' | tee %{ini_name}
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; Configuration
;env.file = ''
EOF

cp -pr NTS ZTS


%build
cd NTS

%{_bindir}/phpize
%configure \
    --enable-env \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --enable-env \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
make -C NTS install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -Dpm644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff

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
* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 0.2.1-3
- rebuild for PHP 7.1 new API version

* Sat Mar  5 2016 Remi Collet <remi@fedoraproject.org> - 0.2.1-2
- adapt for F24

* Sat Jan 02 2016 Remi Collet <remi@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1 (beta)
- fix broken PHP 7 build
  open https://github.com/beberlei/env/pull/4

* Fri Jan 01 2016 Remi Collet <remi@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0 (beta)
- fix strange php 5.5 / i386 / ZTS
  open https://github.com/beberlei/env/pull/2

* Thu Dec 31 2015 Remi Collet <remi@fedoraproject.org> - 0.1.0-1
- initial RPM, version 0.1.0 (beta)

