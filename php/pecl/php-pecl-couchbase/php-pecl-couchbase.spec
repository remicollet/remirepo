# spec file for php-pecl-couchbase
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%{?scl:          %scl_package         php-pecl-couchbase}

%global pecl_name couchbase
%global with_zts  0%{?__ztsphp:1}
%global with_fastlz 1

%if "%{php_version}" < "5.6"
# After igbinary
%global ini_name  z-%{pecl_name}.ini
%else
# After 40-igbinary
%global ini_name  50-%{pecl_name}.ini
%endif

Summary:       Couchbase Server PHP extension
Name:          %{?scl_prefix}php-pecl-couchbase
Version:       1.2.2
Release:       5%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:       PHP
Group:         Development/Languages
URL:           pecl.php.net/package/couchbase
Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}%{?svnrev:-dev}.tgz

# https://github.com/couchbase/php-ext-couchbase/pull/11
Patch0:        %{pecl_name}-fastlz.patch

BuildRequires: %{?scl_prefix}php-devel >= 5.3.0
BuildRequires: %{?scl_prefix}php-pecl-igbinary-devel
BuildRequires: %{?scl_prefix}php-pear
BuildRequires: zlib-devel
BuildRequires: libcouchbase-devel
# for tests
BuildRequires: %{?scl_prefix}php-json
%if %{with_fastlz}
BuildRequires: fastlz-devel
%endif

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
Requires:      %{?scl_prefix}php-pecl-igbinary%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:      %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:      %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}

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
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The PHP client library provides fast access to documents stored
in a Couchbase Server.

This package provides API version 1.
%{?scl_prefix}php-pecl-couchbase2 provides API version 2.

Documentation:
http://docs.couchbase.com/couchbase-sdk-php-1.2/index.html

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection}.


%prep
%setup -q -c

mv %{pecl_name}-%{version} NTS

%{?_licensedir:sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml}

cd NTS
%patch0 -p1 -b .fastlz
%if %{with_fastlz}
rm -r fastlz
sed -e '/name="fastlz/d' -i ../package.xml
%endif

# Fix version
sed -e '/PHP_COUCHBASE_VERSION/s/1.2.0/%{version}/' -i php_couchbase.h

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_COUCHBASE_VERSION/{s/.* "//;s/".*$//;p}' php_couchbase.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}..
   exit 1
fi
cd ..

%if 0%{?__ztsphp:1}
# duplicate for ZTS build
cp -pr NTS ZTS
%else
: Only NTS build, no ZTS
%endif


%build
peclconf() {
%configure \
%if %{with_fastlz}
     --with-system-fastlz \
%endif
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
install -D -m 644 NTS/example/%{pecl_name}.ini %{buildroot}%{php_inidir}/%{ini_name}

# Install the ZTS stuff
%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}
install -D -m 644 ZTS/example/%{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Test & Documentation
cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
: minimal NTS load test
%{__php} -n \
   -d extension=igbinary.so \
   -d extension=json.so \
   -d extension=NTS/modules/%{pecl_name}.so \
   -m | grep %{pecl_name}

%if %{with_zts}
: minimal ZTS load test
ln -sf %{php_ztsextdir}/{json,igbinary}.so ZTS/modules/
%{__ztsphp}    -n \
   -d extension=igbinary.so \
   -d extension=json.so \
   -d extension=ZTS/modules/%{pecl_name}.so \
   -m | grep %{pecl_name}
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
* Tue Mar  8 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-5
- adapt for F24
- drop runtime dependency on pear, new scriptlets
- fix license management

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.2.2-4.1
- Fedora 21 SCL mass rebuild

* Sat Sep 20 2014 Remi Collet <remi@fedoraproject.org> - 1.2.2-4
- rebuild with new libcouchbase
- improve description (API v1 /v2)

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

