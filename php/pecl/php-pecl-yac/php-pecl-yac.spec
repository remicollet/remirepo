# spec file for php-pecl-yac (previously php-yac)
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global with_zts    0%{?__ztsphp:1}
%global pecl_name   yac
%global with_tests  %{!?_without_tests:1}%{?_without_tests:0}
%if "%{php_version}" < "5.6"
%global ini_name    %{pecl_name}.ini
%else
%global ini_name    40-%{pecl_name}.ini
%endif

Summary:        Lockless user data cache
Name:           php-pecl-%{pecl_name}
Version:        0.9.1
Release:        3%{?dist}

License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# https://github.com/laruence/yac/pull/42
Patch0:         %{pecl_name}-fastlz.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel > 5.2
BuildRequires:  php-pear
BuildRequires:  fastlz-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

# Package have be renamed
Obsoletes:      php-%{pecl_name} < %{version}
Provides:       php-%{pecl_name} = %{version}
Provides:       php-%{pecl_name}%{?_isa} = %{version}
Provides:       php-pecl(%{pecl_name}) = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Yac (Yet Another Cache) is a shared memory user data cache for PHP.

It can be used to replace APC or local memcached.

Yac is lockless, that means, it is very fast, but there could be a
chance you will get a wrong data(depends on how many key slots are
allocated and how many keys are stored), so you'd better make sure
that your product is not very sensitive to that.


%prep
%setup -qc
mv %{pecl_name}-%{version} NTS

# Don't install (register) the tests
sed -e 's/role="test"/role="src"/' -i package.xml

cd NTS
%patch0 -p1 -b .pr42

# drop bundled fastlz to ensure it is not used
sed -e '\:name="compressor/fastlz:d' -i ../package.xml
rm -r compressor/fastlz

# Check version as upstream often forget to update this
extver=$(sed -n '/#define PHP_YAC_VERSION/{s/.* "//;s/".*$//;p}' php_yac.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream YAC version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
cd ..

# Drop in the bit of configuration
cat > %{ini_name} << 'EOF'
; Enable Yet Another Cache extension module
extension = %{pecl_name}.so

;yac.enable=1
;yac.enable_cli=0
;yac.debug=0
;yac.keys_memory_size=4M
;yac.values_memory_size=64M
;yac.compress_threshold=-1
EOF


%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif


%build
peclconf() {
%configure \
    --with-system-fastlz \
    --with-php-config=$1
}

cd NTS
%{_bindir}/phpize
peclconf %{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
peclconf %{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}
# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Install the ZTS stuff
%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Test & Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd NTS

: Minimal load test for NTS extension
%{_bindir}/php --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_tests}
: Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff
%else
: Upstream test suite disabled
%endif

%if %{with_zts}
cd ../ZTS

: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_tests}
: Upstream test suite for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff
%else
: Upstream test suite disabled
%endif
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
%defattr(-, root, root, 0755)
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%endif


%changelog
* Sat Sep  6 2014 Remi Collet <remi@fedoraproject.org> - 0.9.1-3
- cleanup for review
- build with system fastlz
- don't install the tests

* Tue Aug 26 2014 Remi Collet <rcollet@redhat.com> - 0.9.1-2
- improve SCL build

* Fri Jul 25 2014 Remi Collet <remi@fedoraproject.org> - 0.9.1-1
- Update to 0.9.1 (beta)

* Thu Jul 24 2014 Remi Collet <remi@fedoraproject.org> - 0.9.0-1
- upstream move to pecl
- rename from php-yac to php-pecl-yac
- update to 0.9.0 (beta)

* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 0.1.1-3
- add numerical prefix to extension configuration file (php 5.6)

* Tue Mar 25 2014 Remi Collet <remi@fedoraproject.org> - 0.1.1-2
- allow SCL build

* Sun Mar 16 2014 Remi Collet <remi@fedoraproject.org> - 0.1.1-1
- version 0.1.1

* Sat Mar 23 2013 Remi Collet <remi@fedoraproject.org> - 0.1.0-0.1.git57fe00d
- initial package, version 0.1.0 (experimental)