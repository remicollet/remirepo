# remirepo spec file for php-pecl-apcu-bc
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%endif

%{?scl:          %scl_package        php-pecl-apcu-bc}
%{!?scl:         %global pkg_name    %{name}}

%global gh_commit  52b97a7ef7565509ff1db58ad95fb13c87ab2544
%global gh_short   %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner   krakjoe
%global gh_project apcu-bc
#global gh_date    20151204
%global proj_name  apcu_bc
%global pecl_name  apcu-bc
%global ext_name   apc
%global apcver     %(%{_bindir}/php -r 'echo (phpversion("apcu")?:0);' 2>/dev/null || echo 65536)
%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
# After 40-apcu.ini
%global ini_name   50-%{ext_name}.ini

Name:           %{?sub_prefix}php-pecl-%{pecl_name}
Summary:        APCu Backwards Compatibility Module
Version:        1.0.3
%if 0%{?gh_date:1}
Release:        0.1.%{gh_date}git%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{proj_name}-%{version}-%{gh_short}.tar.gz
%else
Release:        2%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Source0:        http://pecl.php.net/get/%{proj_name}-%{version}.tgz
%endif

License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/APCu

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel > 7
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-pecl-apcu-devel >= 5.1.2

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}
Requires:       %{?scl_prefix}php-pecl-apcu%{?_isa} >= 5.1.2

Obsoletes:      %{?scl_prefix}php-pecl-apc              < 4
Provides:       %{?scl_prefix}php-apc                   = %{apcver}
Provides:       %{?scl_prefix}php-apc%{?_isa}           = %{apcver}
Provides:       %{?scl_prefix}php-pecl-apc              = %{apcver}-%{release}
Provides:       %{?scl_prefix}php-pecl-apc%{?_isa}      = %{apcver}-%{release}
Provides:       %{?scl_prefix}php-pecl(APC)             = %{apcver}
Provides:       %{?scl_prefix}php-pecl(APC)%{?_isa}     = %{apcver}
Provides:       %{?scl_prefix}php-pecl(%{proj_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{proj_name})%{?_isa} = %{version}
# For "more" SCL
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:      php53-pecl-%{ext_name}  <= %{version}
Obsoletes:     php53u-pecl-%{ext_name}  <= %{version}
Obsoletes:      php54-pecl-%{ext_name}  <= %{version}
Obsoletes:     php54w-pecl-%{ext_name}  <= %{version}
Obsoletes:     php55u-pecl-%{ext_name}  <= %{version}
Obsoletes:     php55w-pecl-%{ext_name}  <= %{version}
Obsoletes:     php56u-pecl-%{ext_name}  <= %{version}
Obsoletes:     php56w-pecl-%{ext_name}  <= %{version}
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This module provides a backwards compatible API for APC.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -qc
%if 0%{?gh_date:1}
mv %{gh_project}-%{gh_commit} NTS
mv NTS/package.xml .
%else
mv %{proj_name}-%{version} NTS
%endif

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
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
rm -rf %{buildroot}

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
%{_bindir}/php -n \
   -d extension=apcu.so \
   -d extension=%{buildroot}%{php_extdir}/apc.so \
   -m | grep 'apc$'

# Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{_bindir}/php \
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
%defattr(-,root,root,-)
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{proj_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/apc.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/apc.so
%endif


%changelog
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
