# remirepo spec file for php-pecl-couchbase2
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%{?scl:          %scl_package         php-pecl-couchbase2}

%global pecl_name couchbase
%global with_zts  0%{!?_without_zts:%{?__ztsphp:1}}

%if "%{php_version}" < "5.6"
# After igbinary (and XDebug for 5.4)
%global ini_name  z-%{pecl_name}.ini
%else
# After 40-igbinary and 40-json
%global ini_name  50-%{pecl_name}.ini
%endif
%global        prever beta2

Summary:       Couchbase Server PHP extension
Name:          %{?scl_prefix}php-pecl-couchbase2
Version:       2.2.0
Release:       0.1.%{prever}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:       PHP
Group:         Development/Languages
URL:           pecl.php.net/package/couchbase
Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz

BuildRequires: %{?scl_prefix}php-devel >= 5.3.0
BuildRequires: %{?scl_prefix}php-pear
BuildRequires: %{?scl_prefix}php-json
BuildRequires: libcouchbase-devel
BuildRequires: fastlz-devel
BuildRequires: zlib-devel
# to ensure compatibility with XDebug
BuildRequires: %{?scl_prefix}php-pecl-xdebug

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
# used in embded php code
Requires:      %{?scl_prefix}php-igbinary%{?_isa}
Requires:      %{?scl_prefix}php-json%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:      %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:      %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}2         = %{version}-%{release}
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}2%{?_isa} = %{version}-%{release}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:     %{?scl_prefix}php-pecl-couchbase < 2
%else
# Only 1 version can be installed
Conflicts:     %{?scl_prefix}php-pecl-couchbase < 2
%endif

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}2  <= %{version}
Obsoletes:     php53u-pecl-%{pecl_name}2 <= %{version}
Obsoletes:     php54-pecl-%{pecl_name}2  <= %{version}
Obsoletes:     php54w-pecl-%{pecl_name}2 <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}2 <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name}2 <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name}2 <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name}2 <= %{version}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The PHP client library provides fast access to documents stored
in a Couchbase Server.

%{?scl_prefix}php-pecl-couchbase provides API version 1.
This package provides API version 2.

Documentation:
http://docs.couchbase.com/prebuilt/php-sdk-2.0/topics/overview.html

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c

mv %{pecl_name}-%{version}%{?prever} NTS

%{?_licensedir:sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml}

cd NTS
# Drop bundled library
sed -e '/fastlz/d' -i ../package.xml
rm -r fastlz

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_COUCHBASE_VERSION/{s/.* "//;s/".*$//;p}' php_couchbase.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever}
   exit 1
fi
cd ..

cat << 'EOF' | tee %{ini_name}
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

%if 0%{?__ztsphp:1}
# duplicate for ZTS build
cp -pr NTS ZTS
%else
: Only NTS build, no ZTS
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
# Install the NTS stuff
make install -C NTS INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install the ZTS stuff
%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Install the package XML file
install -D -m 644 package2.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Test & Documentation
cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
: minimal NTS load test
%{__php} -n \
   -d extension=json.so \
   -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
   -m | grep %{pecl_name}

%if %{with_zts}
: minimal ZTS load test
%{__ztsphp} -n \
   -d extension=json.so \
   -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
   -m | grep %{pecl_name}
%endif


%if 0%{?fedora} < 24
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
* Wed Mar 20 2016 Remi Collet <remi@fedoraproject.org> - 2.2.0-0.1.beta1
- Update to 2.2.0beta2 (php 5 and 7, beta)

* Tue Mar  8 2016 Remi Collet <remi@fedoraproject.org> - 2.1.0-2
- adapt for F24

* Thu Nov 05 2015 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0
- add patch to use system fastlz library
  from https://github.com/couchbase/php-couchbase/pull/10

* Wed Apr 22 2015 Remi Collet <remi@fedoraproject.org> - 2.0.7-1
- Update to 2.0.7

* Wed Apr 08 2015 Remi Collet <remi@fedoraproject.org> - 2.0.6-1
- Update to 2.0.6 (stable)

* Wed Mar 04 2015 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- Update to 2.0.5 (stable)

* Mon Feb 09 2015 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4 (stable)
- drop runtime dependency on pear, new scriptlet

* Wed Jan 07 2015 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 2.0.2-1.1
- Fedora 21 SCL mass rebuild

* Wed Dec 03 2014 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2

* Wed Nov 05 2014 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1

* Sat Sep 20 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- rename to php-pecl-couchbase2 for new API
- update to 2.0.0
- open http://www.couchbase.com/issues/browse/PCBC-292 license
- open http://www.couchbase.com/issues/browse/PCBC-293 fastlz
- open http://www.couchbase.com/issues/browse/PCBC-294 xdebug

* Sat Sep  6 2014 Remi Collet <remi@fedoraproject.org> - 1.2.2-3
- test build with system fastlz

* Tue Aug 26 2014 Remi Collet <rcollet@redhat.com> - 1.2.2-2
- improve SCL build

* Mon May 12 2014 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 1.2.1-4
- add numerical prefix to extension configuration file

* Sun Mar 16 2014 Remi Collet <remi@fedoraproject.org> - 1.2.1-2
- install doc in pecl_docdir

* Sat Oct 05 2013 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1
- add patch to fix ZTS build
  https://github.com/couchbase/php-ext-couchbase/pull/9

* Mon May 13 2013 Remi Collet <remi@fedoraproject.org> - 1.1.15-2
- fix dependency on php-pecl-igbinary

* Thu May  9 2013 Remi Collet <remi@fedoraproject.org> - 1.1.15-1
- update to 1.1.15 (no change)

* Fri Mar 22 2013 Remi Collet <remi@fedoraproject.org> - 1.1.14-1
- initial package

