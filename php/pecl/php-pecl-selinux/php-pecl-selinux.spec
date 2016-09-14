# remirepo spec file for php-pecl-selinux
# adapted for SCL
#
# Copyright (c) 2011-2016 Remi Collet
#
# Fedora spec file for php-pecl-selinux
#
# Copyright (c) 2009-2010 KaiGai Kohei
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
%endif

%{?scl:          %scl_package         php-pecl-selinux}

%define pecl_name   selinux
%global with_zts    0%{?__ztsphp:1}
%global with_tests  %{?_without_tests:0}%{!?_without_tests:1}
%if "%{php_version}" < "5.6"
%global ini_name    %{pecl_name}.ini
%else
%global ini_name    40-%{pecl_name}.ini
%endif

Summary:        SELinux binding for PHP scripting language
Name:           %{?sub_prefix}php-pecl-selinux
Version:        0.4.1
Release:        8%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  %{?scl_prefix}php-devel >= 5.2.0
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  libselinux-devel >= 2.0.80

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       libselinux >= 2.0.80
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}

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
# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This package is an extension to the PHP Hypertext Preprocessor.
It wraps the libselinux library and provides a set of interfaces
to the PHP runtime engine.
The libselinux is a set of application program interfaces towards in-kernel
SELinux, contains get/set security context, communicate security server,
translate between raw and readable format and so on.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -c -q
mv %{pecl_name}-%{version} NTS

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

pushd NTS
extver=$(sed -n '/#define PHP_SELINUX_VERSION/{s/.* "//;s/".*$//;p}' php_selinux.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
popd

# Drop in the bit of configuration
cat > %{ini_name} << 'EOF'
; Enable SELinux extension module
extension=%{pecl_name}.so
EOF

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif


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

# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
# Install the ZTS stuff
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
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_tests}
: Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=0 \
%{__php} -n run-tests.php --show-diff
: Ignore result as unreliable in mock
%endif

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
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
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 0.4.1-8
- rebuild for PHP 7.1 new API version

* Sun Mar  6 2016 Remi Collet <remi@fedoraproject.org> - 0.4.1-7
- adapt for F24

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 0.4.1-6
- rebuild for PHP 7.0.0RC5 new API version

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 0.4.1-5
- F23 rebuild with rh_layout

* Wed Jul 22 2015 Remi Collet <remi@fedoraproject.org> - 0.4.1-4
- rebuild against php 7.0.0beta2

* Wed Jul  8 2015 Remi Collet <remi@fedoraproject.org> - 0.4.1-3
- rebuild against php 7.0.0beta1

* Fri Jun 19 2015 Remi Collet <remi@fedoraproject.org> - 0.4.1-2
- allow build against rh-php56 (as more-php56)
- rebuild for "rh_layout" (php70)

* Sun May 24 2015 Remi Collet <remi@fedoraproject.org> - 0.4.1-1
- version 0.4.1 (beta)

* Sun Apr  5 2015 Remi Collet <remi@fedoraproject.org> - 0.3.1-17
- add upstream fix for PHP 7
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 0.3.1-16.1
- Fedora 21 SCL mass rebuild

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 0.3.1-16
- improve SCL build

* Wed Apr 16 2014 Remi Collet <remi@fedoraproject.org> - 0.3.1-15
- add numerical prefix to extension configuration file (php 5.6)

* Mon Mar 24 2014 Remi Collet <remi@fedoraproject.org> - 0.3.1-14
- allow SCL build

* Fri Mar 14 2014 Remi Collet <remi@fedoraproject.org> - 0.3.1-13
- fix syntax in provided configuration

* Thu Mar 13 2014 Remi Collet <RPMS@FamilleCollet.com> - 0.3.1-12
- cleanups
- install doc in pecl_docdir

* Thu Jan 24 2013 Remi Collet <RPMS@FamilleCollet.com> - 0.3.1-9.1
- also provides php-selinux

* Sun Oct 21 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.3.1-9
- bump release (fedora >= 17 rebuild)

* Mon Dec 12 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.3.1-7.1
- bump release (f16 rebuild)

* Sun Nov 27 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.3.1-7
- php 5.4 and ZTS build

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Mar  3 2010 KaiGai Kohei <kaigai@kaigai.gr.jp> - 0.3.1-5
- Rebuilt for package 

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.3.1-2
- rebuild for new PHP 5.3.0 ABI (20090626)

* Thu Apr 16 2009 KaiGai Kohei <kaigai@kaigai.gr.jp> - 0.3.1-1
- The "permissive" tag was added to selinux_compute_av
- The selinux_deny_unknown() was added
- README is updated for the new features

* Thu Mar 12 2009 KaiGai Kohei <kaigai@kaigai.gr.jp> - 0.2.1-1
- Specfile to build RPM package is added.

* Thu Mar  5 2009 KaiGai Kohei <kaigai@kaigai.gr.jp> - 0.1.2-1
- The initial release of SELinux binding for PHP script language.
