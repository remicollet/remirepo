# remirepo spec file for php-pecl-geoip
# with SCL compatibility, from:
#
# Fedora spec file for php-pecl-geoip
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
%scl_package        php-pecl-geoip
%endif

%define pecl_name  geoip
%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%if "%{php_version}" < "5.6"
%global ini_name  %{pecl_name}.ini
%else
%global ini_name  40-%{pecl_name}.ini
%endif


Name:           %{?sub_prefix}php-pecl-geoip
Version:        1.1.1
Release:        2%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Summary:        Extension to map IP addresses to geographic places
Group:          Development/Languages
License:        PHP
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  GeoIP-devel
BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-pear

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
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
%if "%{php_version}" > "7.1"
Obsoletes:     php71u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php71w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This PHP extension allows you to find the location of an IP address 
City, State, Country, Longitude, Latitude, and other information as 
all, such as ISP and connection type. It makes use of Maxminds geoip
database

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -c -q

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

mv %{pecl_name}-%{version} NTS

cd NTS
extver=$(sed -n '/#define PHP_GEOIP_VERSION/{s/.* "//;s/".*$//;p}' php_geoip.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

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

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
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

cd NTS
# Missing IPv6 data
rm tests/019.phpt

TEST_PHP_EXECUTABLE=%{__php} \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__php} run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=%{pecl_name}.so \
    --show-diff


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
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%endif


%changelog
* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-2
- rebuild for PHP 7.1 new API version

* Thu Sep 01 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1

* Sat Mar  5 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-10
- adapt for F24

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-9
- rebuild for PHP 7.0.0RC5 new API version

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-8
- F23 rebuild with rh_layout

* Wed Jul 22 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-7
- rebuild against php 7.0.0beta2

* Wed Jul  8 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-6
- rebuild against php 7.0.0beta1

* Sat Jun 20 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-5
- allow build against rh-php56 (as more-php56)

* Mon Apr  6 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-4
- add fix for PHP 7 compatibility
- drop runtime dependency on pear, new scriptlets
- don't install/register tests

* Sat Feb 28 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-3
- ignore 1 test on Fedora >= 22

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-2.1
- Fedora 21 SCL mass rebuild

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 1.1.0-2
- improve SCL build

* Sat May 03 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0 (beta)
- upstream patch for old auto* version (rhel <= 6)

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 1.0.8-8
- add numerical prefix to extension configuration file

* Wed Mar 19 2014 Remi Collet <remi@fedoraproject.org> - 1.0.8-7
- allow SCL build

* Sun Mar  2 2014 Remi Collet <remi@fedoraproject.org> - 1.0.8-6
- cleaups
- install doc in pecl_docdir
- install tests in pecl_testdir
- add missing License file

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> - 1.0.8-3.1
- also provides php-geoip

* Fri Sep  7 2012 Remi Collet <remi@fedoraproject.org> - 1.0.8-3
- Obsoletes php53*, php54* on EL

* Sun Nov 13 2011 Remi Collet <remi@fedoraproject.org> - 1.0.8-2
- build against php 5.4

* Mon Oct 24 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.8-1
- update to 1.0.8

* Sat Oct 15 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.7-7
- upstream patch for https://bugs.php.net/bug.php?id=60066

* Wed Oct 05 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.7-6
- ZTS extension
- spec cleanups
- run test suite
- patch for https://bugs.php.net/bug.php?id=60066
- patch for https://bugs.php.net/bug.php?id=59804

* Fri Jul 15 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.7-6
- Fix bugzilla #715693

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> 1.0.7-3
- rebuild for new PHP 5.3.0 ABI (20090626)

* Mon Jun 22 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.7-2
- Fix timestamps on installed files

* Sun Jun 14 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.7-1
- Initial RPM package
