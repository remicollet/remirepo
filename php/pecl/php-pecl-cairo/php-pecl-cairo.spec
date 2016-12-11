# remirepo spec file for php-pecl-cairo
#
# Copyright (c) 2012-2016 Remi Collet
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

%{?scl:          %scl_package        php-pecl-cairo}

%global proj_name  Cairo
%global pecl_name  cairo
%global versuffix  -beta
%global with_zts   0%{?__ztsphp:1}
# Result vary too much with cairo version
%global with_tests %{?_with_tests:1}%{!?_with_tests:0}
%if "%{php_version}" < "5.6"
%global ini_name   %{pecl_name}.ini
%else
%global ini_name   40-%{pecl_name}.ini
%endif

Name:           %{?sub_prefix}php-pecl-cairo
Version:        0.3.2
Release:        11%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
Summary:        Cairo Graphics Library Extension
Group:          Development/Languages
License:        PHP
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# see https://bugs.php.net/61882
Patch0:         pecl-cairo-php_streams.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  cairo-devel
BuildRequires:  freetype-devel
BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-pear

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
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

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Cairo is a 2D graphics library with support for multiple output devices.
Currently supported output targets include the X Window System, Quartz,
Win32, image buffers, PostScript, PDF, and SVG file output.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl})}.

%package devel
Summary:       Cairo Graphics Library Extension developer files
Group:         Development/Libraries
Requires:      %{?scl_prefix}php-pecl-cairo%{?_isa} = %{version}-%{release}
Requires:      %{?scl_prefix}php-devel%{?_isa}

%description devel
These are the files needed to compile programs using cairo extension.


%prep
%setup -c -q

%{?_licensedir:sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml}

%patch0 -p0 -b .61882
mv %{proj_name}-%{version} NTS

# Check reported version (phpinfo), as this is often broken
extver=$(sed -n '/#define PHP_CAIRO_VERSION/{s/.* "//;s/".*$//;p}' NTS/php_cairo.h)
if test "x${extver}" != "x%{version}%{?versuffix}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

%if %{with_zts}
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -Dpm644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Test & Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_testdir}/%{proj_name}/$i
done
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{proj_name}/$i
done


%check
: Minimal load test for NTS extension
%{__php} -n \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    -m | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} -n \
    -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    -m | grep %{pecl_name}
%endif

%if %{with_tests}
# 32/445 test failing with old cairo 1.8

cd NTS
TEST_PHP_EXECUTABLE=%{__php} \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__php} run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=%{pecl_name}.so

%if %{with_zts}
cd ../ZTS
TEST_PHP_EXECUTABLE=%{__ztsphp} \
REPORT_EXIT_STATUS=0 \
NO_INTERACTION=1 \
%{__ztsphp} run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=%{pecl_name}.so
%endif
%endif


%clean
rm  -rf %{buildroot}


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
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%endif

%files devel
%defattr(-,root,root,-)
%doc %{pecl_testdir}/%{proj_name}
%{_includedir}/php/ext/%{pecl_name}
%if %{with_zts}
%{php_ztsincldir}/ext/%{pecl_name}
%endif


%changelog
* Tue Mar  8 2016 Remi Collet <remi@fedoraproject.org> - 0.3.2-11
- adapt for F24
- fix license management

* Sat Jun 20 2015 Remi Collet <remi@fedoraproject.org> - 0.3.2-10
- allow build against rh-php56 (as more-php56)
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 0.3.2-9.1
- Fedora 21 SCL mass rebuild

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 0.3.2-9
- improve SCL build

* Tue Apr 15 2014 Remi Collet <remi@fedoraproject.org> - 0.3.2-8
- add numerical prefix to extension configuration file

* Wed Mar 19 2014 Remi Collet <remi@fedoraproject.org> - 0.3.2-7
- allow SCL build

* Mon Mar 10 2014 Remi Collet <remi@fedoraproject.org> - 0.3.2-6
- fix build when ZTS not available

* Sun Mar  2 2014 Remi Collet <remi@fedoraproject.org> - 0.3.2-5
- cleanups
- move doc in pecl_docdir
- provide tests in pecl_testdir (devel)
- add build option --with tests for upstream test suite

* Thu Aug  9 2012 Remi Collet <remi@fedoraproject.org> - 0.3.2-4
- also provides php-cairo

* Thu Aug  9 2012 Remi Collet <remi@fedoraproject.org> - 0.3.2-3
- add patch for https://bugs.php.net/61882
- (re)enabling test result on fedora > 13

* Sun Apr 22 2012 Remi Collet <remi@fedoraproject.org> - 0.3.2-2
- update to 0.3.2-beta, rebuild for php 5.4

* Sun Apr 22 2012 Remi Collet <remi@fedoraproject.org> - 0.3.2-1
- update to 0.3.2-beta

* Sat Apr 21 2012 Remi Collet <remi@fedoraproject.org> - 0.3.1-2
- rebuild for php 5.4

* Sat Apr 21 2012 Remi Collet <remi@fedoraproject.org> - 0.3.1-1
- Initial RPM package
- request for LICENSE https://bugs.php.net/61794

