# remirepo spec file for php-pecl-xmldiff
#
# Copyright (c) 2013-2016 Remi Collet
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

%{?scl:          %scl_package        php-pecl-xmldiff}

%global with_zts  0%{?__ztsphp:1}
%global pecl_name xmldiff
%if "%{php_version}" < "5.6"
# After dom
%global ini_name  %{pecl_name}.ini
%else
# After 20-dom
%global ini_name  40-%{pecl_name}.ini
%endif

Summary:        XML diff and merge
Name:           %{?sub_prefix}php-pecl-%{pecl_name}
Version:        1.1.2
Release:        8%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel > 5.3
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-dom
BuildRequires:  %{?scl_prefix}php-libxml
BuildRequires:  diffmark-devel
BuildRequires:  libxml2-devel

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%if "%{php_version}" < "5.4"
# php 5.3.3 in EL-6 don't use arched virtual provides
# so requires the real package instead
Requires:       %{?scl_prefix}php-xml%{?_isa}
%else
Requires:       %{?scl_prefix}php-dom%{?_isa}
Requires:       %{?scl_prefix}php-libxml%{?_isa}
%endif
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
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The extension is able to produce diffs of two XML documents and then to apply
the difference to the source document. The diff is a XML document containing
copy/insert/delete instruction nodes in human readable format. DOMDocument
objects, local files and strings in memory can be processed.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%package devel
Summary:       %{name} developer files (header)
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{?scl_prefix}php-devel%{?_isa}
Requires:      libxml2-devel%{?_isa}

%description devel
These are the files needed to compile programs using %{name}.


%prep
%setup -q -c

sed -e '/name="diffmark/d' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

mv %{pecl_name}-%{version} NTS

cd NTS
# drop bundled library to ensure it is not used
rm -rf diffmark

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_XMLDIFF_VERSION/{s/.* "//;s/".*$//;p}' php_xmldiff.h)
if test "x${extver}" != "x%{version}%{?prever:-%{prever}}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever:-%{prever}}.
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
    --with-libdiffmark \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-libdiffmark \
    --with-libdir=%{_lib} \
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

# Test & Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
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
# Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=dom.so \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}

# Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n -d extension=dom.so -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php

%if %{with_zts}
cd ../ZTS
# Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=dom.so \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}

# Upstream test suite for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension=dom.so -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php
%endif


%clean
rm -rf %{buildroot}


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

%files devel
%defattr(-,root,root,-)
%doc %{pecl_testdir}/%{pecl_name}
%{php_incldir}/ext/%{pecl_name}

%if %{with_zts}
%{php_ztsincldir}/ext/%{pecl_name}
%endif


%changelog
* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 1.1.2-8
- rebuild for PHP 7.1 new API version

* Sun Mar  6 2016 Remi Collet <remi@fedoraproject.org> - 1.1.2-7
- adapt for F24

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 1.1.2-6
- rebuild for PHP 7.0.0RC5 new API version

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 1.1.2-5
- F23 rebuild with rh_layout

* Wed Jul 22 2015 Remi Collet <remi@fedoraproject.org> - 1.1.2-4
- rebuild against php 7.0.0beta2

* Wed Jul  8 2015 Remi Collet <remi@fedoraproject.org> - 1.1.2-3
- rebuild against php 7.0.0beta1

* Fri Jun 19 2015 Remi Collet <remi@fedoraproject.org> - 1.1.2-2
- allow build against rh-php56 (as more-php56)
- rebuild for "rh_layout" (php70)

* Mon Feb 09 2015 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2 (stable)

* Mon Feb 02 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1 (stable)

* Mon Feb 02 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0 (stable)
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 0.9.2-5.1
- Fedora 21 SCL mass rebuild

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 0.9.2-5
- improve SCL build

* Fri May 30 2014 Remi Collet <remi@fedoraproject.org> - 0.9.2-4
- rebuild to have NEVR > Fedora or EPEL one

* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 0.9.2-3
- add numerical prefix to extension configuration file (php 5.6)

* Thu Jan  2 2014 Remi Collet <remi@fedoraproject.org> - 0.9.2-2
- adapt for SCL
- doc in pecl_docdir
- tests in pecl_test_dir (devel)

* Wed Jan  1 2014 Remi Collet <remi@fedoraproject.org> - 0.9.2-1
- Update to 0.9.2 (stable)

* Sat Nov 02 2013 Remi Collet <remi@fedoraproject.org> - 0.9.1-1
- Update to 0.9.1 (stable)
- drop our patch merged upstream

* Fri Nov 01 2013 Remi Collet <remi@fedoraproject.org> - 0.9.0-2
- fix build with php 5.3.3 in RHEL-6

* Wed Oct 02 2013 Remi Collet <remi@fedoraproject.org> - 0.9.0-1
- Update to 0.9.0 (stable)
- License now provided in upstream sources
- Drop merged patch for system libdiffmark

* Sun Sep 29 2013 Remi Collet <remi@fedoraproject.org> - 0.8.0-1
- initial package

