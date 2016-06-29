# Fedora spec file for php-pecl-apcu-bc
# without SCL compatibility, from
#
# remirepo spec file for php-pecl-apcu-bc
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global proj_name  apcu_bc
%global pecl_name  apcu-bc
%global ext_name   apc
%global apcver     %(%{_bindir}/php -r 'echo (phpversion("apcu")?:0);' 2>/dev/null || echo 65536)
%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
# After 40-apcu.ini
%global ini_name   50-%{ext_name}.ini

Name:           php-pecl-%{pecl_name}
Summary:        APCu Backwards Compatibility Module
Version:        1.0.3
Release:        3%{?dist}
Source0:        http://pecl.php.net/get/%{proj_name}-%{version}.tgz

License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/APCu

BuildRequires:  php-devel > 7
BuildRequires:  php-pear
BuildRequires:  php-pecl-apcu-devel >= 5.1.2

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires:       php-pecl-apcu%{?_isa} >= 5.1.2

Obsoletes:      php-pecl-apc              < 4
Provides:       php-apc                   = %{apcver}
Provides:       php-apc%{?_isa}           = %{apcver}
Provides:       php-pecl-apc              = %{apcver}-%{release}
Provides:       php-pecl-apc%{?_isa}      = %{apcver}-%{release}
Provides:       php-pecl(APC)             = %{apcver}
Provides:       php-pecl(APC)%{?_isa}     = %{apcver}
Provides:       php-pecl(%{proj_name})         = %{version}
Provides:       php-pecl(%{proj_name})%{?_isa} = %{version}


%description
This module provides a backwards compatible API for APC.


%prep
%setup -qc
mv %{proj_name}-%{version} NTS

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    -e '/LICENSE/s/role="doc"/role="src"/' \
    -i package.xml

cd NTS
# Sanity check, really often broken
extver=$(sed -n '/#define PHP_APCU_BC_VERSION/{s/.* "//;s/".*$//;p}' php_apc.h)
if test "x${extver}" != "x%{version}%{?prever}%{?gh_date:dev}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever}%{?gh_date:dev}.
   exit 1
fi
cd ..

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif

cat << 'EOF' | tee %{ini_name}
; Enable %{summary}
extension=%{ext_name}.so
EOF

: Build apcu_bc %{version} with apcu %{apcver}


%build
cd NTS
%{_bindir}/phpize
%configure \
   --enable-apcu-bc \
   --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
   --enable-apcu-bc \
   --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
# Install the ZTS stuff
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{proj_name}/$i
done


%check
cd NTS
# Check than both extensions are reported (BC mode)
%{__php} -n \
   -d extension=apcu.so \
   -d extension=%{buildroot}%{php_extdir}/apc.so \
   -m | grep 'apc$'

# Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=apcu.so -d extension=%{buildroot}%{php_extdir}/apc.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php --show-diff

%if %{with_zts}
cd ../ZTS
%{__ztsphp} -n \
   -d extension=apcu.so \
   -d extension=%{buildroot}%{php_ztsextdir}/apc.so \
   -m | grep 'apc$'

# Upstream test suite for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension=apcu.so -d extension=%{buildroot}%{php_ztsextdir}/apc.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff
%endif


%files
%license NTS/LICENSE
%doc %{pecl_docdir}/%{proj_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/apc.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/apc.so
%endif


%changelog
* Sun Jun 26 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-3
- drop SCL stuff for Fedora review

* Mon Mar  7 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-2
- fix apcver macro definition

* Thu Feb 11 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3 (beta)

* Fri Jan 29 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2 (beta)

* Wed Jan  6 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1 (beta)

* Mon Jan  4 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-0
- test build for upcoming 1.0.1

* Sat Dec 26 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- missing dependency on APCu

* Mon Dec  7 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0 (beta)

* Mon Dec  7 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2
- test build of upcomming 1.0.0

* Fri Dec  4 2015 Remi Collet <remi@fedoraproject.org> - 5.1.2-0.1.20151204git52b97a7
- test build of upcomming 5.1.2
- initial package
