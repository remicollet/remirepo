# remirepo spec file for php-pecl-hdr-histogram
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package       php-pecl-hdr-histogram
%endif

%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name  hdr_histogram
%global ext_name   hdrhistogram
%if "%{php_version}" < "5.6"
%global ini_name   %{ext_name}.ini
%else
%global ini_name   40-%{ext_name}.ini
%endif

Summary:       PHP extension wrapper for the C hdrhistogram API
Name:          %{?sub_prefix}php-pecl-hdr-histogram
Version:       0.3.0
Release:       3%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:       MIT
Group:         Development/Languages
URL:           http://pecl.php.net/package/%{pecl_name}

Source:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRequires: %{?scl_prefix}php-devel >= 5.4
BuildRequires: %{?scl_prefix}php-pear
BuildRequires: hdrhistogram-devel

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:      %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:      %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
Obsoletes:     php54-pecl-hdr-histogram  <= %{version}
Obsoletes:     php54w-pecl-hdr-histogram <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-hdr-histogram <= %{version}
Obsoletes:     php55w-pecl-hdr-histogram <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-hdr-histogram <= %{version}
Obsoletes:     php56w-pecl-hdr-histogram <= %{version}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-pecl-hdr-histogram <= %{version}
Obsoletes:     php70w-pecl-hdr-histogram <= %{version}
%endif
%if "%{php_version}" > "7.1"
Obsoletes:     php71u-pecl-hdr-histogram <= %{version}
Obsoletes:     php71w-pecl-hdr-histogram <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
HdrHistogram: A High Dynamic Range Histogram.

A Histogram that supports recording and analyzing sampled data value counts
across a configurable integer value range with configurable value precision
within the range. Value precision is expressed as the number of significant
digits in the value recording, and provides control over value quantization
behavior across the value range and the subsequent value resolution at any
given level.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -c -q
mv %{pecl_name}-%{version} NTS

# Remove test file to avoid regsitration
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS
sed -e '/HDR_VERSION/s/0.2.0/0.3.0/' -i php_hdrhistogram.h

# Check upstream version (often broken)
extver=$(sed -n '/#define HDR_VERSION/{s/.* "//;s/".*$//;p}' php_hdrhistogram.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

cat << 'EOF' | tee %{ini_name}
; Enable %{pecl_name} extension module
extension=%{ext_name}.so
EOF

cp -pr NTS ZTS


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
    --define extension=%{buildroot}%{php_extdir}/%{ext_name}.so \
    --modules | grep %{ext_name}

: Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_extdir}/%{ext_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{ext_name}.so \
    --modules | grep %{ext_name}

: Upstream test suite for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_ztsextdir}/%{ext_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff

%endif


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
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{ext_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{ext_name}.so
%endif


%changelog
* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 0.3.0-3
- rebuild with PHP 7.1.0 GA

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 0.3.0-2
- rebuild for PHP 7.1 new API version

* Thu Sep 01 2016 Remi Collet <remi@fedoraproject.org> - 0.3.0-1
- Update to 0.3.0

* Mon Jul 18 2016 Remi Collet <remi@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0

* Sat Mar  5 2016 Remi Collet <remi@fedoraproject.org> - 0.1.0-2
- adapt for F24

* Fri Jan  1 2016 Remi Collet <remi@fedoraproject.org> - 0.1.0-1
- initial RPM, version 0.1.0 (beta)
- fix test suite on i386
  open https://github.com/beberlei/hdrhistogram-php/pull/10
- honours --with-libdir option
  open https://github.com/beberlei/hdrhistogram-php/pull/9

