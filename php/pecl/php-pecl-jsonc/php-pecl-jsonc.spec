# spec file for php-pecl-jsonc
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{?scl:     %scl_package       php-pecl-jsonc}
%{!?__pecl: %global __pecl     %{_bindir}/pecl}

%global pecl_name  json
%global proj_name  jsonc
%global with_zts   0%{?__ztsphp:1}

%if "%{php_version}" > "5.5"
%global ext_name     json
%else
%global ext_name     jsonc
%endif

%if "%{php_version}" < "5.6"
%global ini_name  %{ext_name}.ini
%else
%global ini_name  40-%{ext_name}.ini
%endif

%if 0%{?fedora} < 19 || 0%{?fedora} > 20
%global with_libjson 0
%else
%global with_libjson 1
%endif


Summary:       Support for JSON serialization
Name:          %{?scl_prefix}php-pecl-%{proj_name}
Version:       1.3.6
Release:       2%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/%{proj_name}
Source0:       http://pecl.php.net/get/%{proj_name}-%{version}.tgz

Patch0:        %{proj_name}-el5-32.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: %{?scl_prefix}php-devel >= 5.4
BuildRequires: %{?scl_prefix}php-pear
BuildRequires: pcre-devel
%if %{with_libjson}
BuildRequires: json-c-devel >= 0.11
BuildRequires: json-c-devel <  0.12
%else
Provides:      bundled(libjson-c) = 0.11
%endif

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:      %{?scl_prefix}php-%{pecl_name} = %{version}
Provides:      %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:      %{?scl_prefix}php-pecl(%{proj_name}) = %{version}
Provides:      %{?scl_prefix}php-pecl(%{proj_name})%{?_isa} = %{version}
Obsoletes:     %{?scl_prefix}php-pecl-json < 1.3.1-2
Provides:      %{?scl_prefix}php-pecl-json = %{version}-%{release}
Provides:      %{?scl_prefix}php-pecl-json%{?_isa} = %{version}-%{release}

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
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The %{name} module will add support for JSON (JavaScript Object Notation)
serialization to PHP.

This is a dropin alternative to standard PHP JSON extension which
use the json-c library parser.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection}.


%package devel
Summary:       JSON developer files (header)
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{?scl_prefix}php-devel%{?_isa}

%description devel
These are the files needed to compile programs using JSON serializer.

%if 0%{?rhel} == 5 && "%{php_version}" > "5.5" && 0%{!?scl:1}
%package -n php-json
Summary:       Meta package fo json extension
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description  -n php-json
Meta package fo json extension.
Only used to be the best provider for php-json.
%endif


%prep
%setup -q -c 
cd %{proj_name}-%{version}

%ifarch i386
%if 0%{?rhel} == 5
%patch0 -p1 -b .el5
%endif
%endif

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_JSON_VERSION/{s/.* "//;s/".*$//;p}' php_json.h )
if test "x${extver}" != "x%{version}%{?prever:-%{prever}}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever:-%{prever}}.
   exit 1
fi
cd ..

cat << 'EOF' | tee %{ini_name}
; Enable %{ext_name} extension module
%if "%{ext_name}" == "json"
extension = %{pecl_name}.so
%else
; You must disable standard %{pecl_name}.so before you enable %{proj_name}.so
;extension = %{proj_name}.so
%endif
EOF

%if %{with_zts}
# duplicate for ZTS build
cp -pr %{proj_name}-%{version} %{proj_name}-zts
%endif


%build
cd %{proj_name}-%{version}
%{_bindir}/phpize
%configure \
%if %{with_libjson}
  --with-libjson \
%endif
%if "%{ext_name}" == "jsonc"
  --with-jsonc \
%endif
  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../%{proj_name}-zts
%{_bindir}/zts-phpize
%configure \
%if %{with_libjson}
  --with-libjson \
%endif
%if "%{ext_name}" == "jsonc"
  --with-jsonc \
%endif
  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}
# Install the NTS stuff
make -C %{proj_name}-%{version} \
     install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
# Install the ZTS stuff
make -C %{proj_name}-zts \
     install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Test & Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 %{proj_name}-%{version}/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 %{proj_name}-%{version}/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd %{proj_name}-%{version}

: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{ext_name}.so \
    -m | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{ext_name}.so \
    -m | grep %{pecl_name}
%endif

TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{ext_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php

%if %{with_zts}
cd ../%{proj_name}-zts

TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{ext_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php
%endif


%triggerin -- php-pear
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%triggerun -- php-pear
if [ $1 -eq 0 -o $2 -eq 0 ] ; then
    %{pecl_uninstall} %{proj_name} >/dev/null || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{ext_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{ext_name}.so
%endif


%files devel
%defattr(-,root,root,-)
%doc %{pecl_testdir}/%{pecl_name}

%{php_incldir}/ext/json

%if %{with_zts}
%{php_ztsincldir}/ext/json
%endif

%if 0%{?rhel} == 5 && "%{php_version}" > "5.5" && 0%{!?scl:1}
%files -n php-json
%defattr(-,root,root,-)
%endif

#
# Note to remi : remember to always build in remi-php55(56) first
#
%changelog
* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.3.6-2
- new scriptlets

* Fri Aug  1 2014 Remi Collet <remi@fedoraproject.org> - 1.3.6-1
- release 1.3.6 (stable, bugfix)

* Thu Apr 10 2014 Remi Collet <remi@fedoraproject.org> - 1.3.5-1.1
- missing __sync_val_compare_and_swap_4 in el5 i386

* Thu Apr 10 2014 Remi Collet <remi@fedoraproject.org> - 1.3.5-1
- release 1.3.5 (stable) - security

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 1.3.4-2
- add numerical prefix to extension configuration file

* Sat Feb 22 2014 Remi Collet <rcollet@redhat.com> - 1.3.4-1
- release 1.3.4 (stable)
- move documentation in pecl_docdir
- move tests in pecl_testdir (devel)

* Thu Dec 12 2013 Remi Collet <rcollet@redhat.com> - 1.3.3-1
- release 1.3.3 (stable)

* Thu Sep 26 2013 Remi Collet <rcollet@redhat.com> - 1.3.2-2
- fix decode of string value with null-byte

* Mon Sep  9 2013 Remi Collet <rcollet@redhat.com> - 1.3.2-1
- release 1.3.2 (stable)

* Mon Jun 24 2013 Remi Collet <rcollet@redhat.com> - 1.3.1-2.el5.2
- add metapackage "php-json" to fix upgrade issue (EL-5)

* Wed Jun 12 2013 Remi Collet <rcollet@redhat.com> - 1.3.1-2
- rename to php-pecl-jsonc

* Wed Jun 12 2013 Remi Collet <rcollet@redhat.com> - 1.3.1-1
- release 1.3.1 (beta)

* Tue Jun  4 2013 Remi Collet <rcollet@redhat.com> - 1.3.0-1
- release 1.3.0 (beta)
- use system json-c when available (fedora >= 20)
- use jsonc name for module and configuration

* Mon Apr 29 2013 Remi Collet <rcollet@redhat.com> - 1.3.0-0.3
- rebuild with latest changes
- use system json-c library
- temporarily rename to jsonc-c.so

* Sat Apr 27 2013 Remi Collet <rcollet@redhat.com> - 1.3.0-0.2
- rebuild with latest changes

* Sat Apr 27 2013 Remi Collet <rcollet@redhat.com> - 1.3.0-0.1
- initial package
