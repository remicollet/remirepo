# remirepo spec file for php-pecl-ds
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%scl_package         php-pecl-ds
%global sub_prefix   %{scl_prefix}
# No phpunit in SCL
%global with_tests   0
%else
%global with_tests   0%{!?_without_tests:1}
%endif

%global with_zts     0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name    ds
# After json
%global ini_name     40-%{pecl_name}.ini

# For test suite, see https://github.com/php-ds/tests/commits/master
%global gh_commit    59193bb8e75daf06779fcd881528f7c437cd1a2d
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     php-ds
%global gh_project   tests


Summary:        Data Structures for PHP
Name:           %{?sub_prefix}php-pecl-%{pecl_name}
Version:        1.1.7
Release:        1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:        MIT
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
# Only use for tests during the build, no value to be packaged separately
# in composer.json:  "require-dev": {  "php-ds/tests": "dev-master" }
Source1:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{gh_short}.tar.gz

BuildRequires:  %{?scl_prefix}php-devel >= 7
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-json
%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  %{_bindir}/phpab
%endif

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-json%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
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
%{summary}.
Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c -a 1
mv %{pecl_name}-%{version} NTS
mv %{gh_project}-%{gh_commit} tests

# Don't install/register tests, install examples as doc
%{?_licensedir:sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml}

cd NTS

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_DS_VERSION/{s/.* "//;s/".*$//;p}' php_ds.h)
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
cat << 'EOF' | tee %{ini_name}
; Enable '%{summary}' extension module
extension=%{pecl_name}.so
EOF


%build
%{?dtsenable}

peclbuild() {
%configure \
    --enable-ds \
    --with-php-config=$1

make %{?_smp_mflags}
}

cd NTS
%{_bindir}/phpize
peclbuild %{_bindir}/php-config

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
peclbuild %{_bindir}/zts-php-config
%endif


%install
%{?dtsenable}

make -C NTS \
     install INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS \
     install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
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
modules="-d extension=json.so"

cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    $modules \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    $modules \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif
cd ..

%if %{with_tests}
: Generate autoloader for tests
%{_bindir}/phpab \
   --output tests/autoload.php \
   tests

: Run upstream test suite
%{_bindir}/php \
   -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
   %{_bindir}/phpunit \
      --bootstrap tests/autoload.php \
      tests
%endif


%files
%{?_licensedir:%license NTS/LICENSE}
%{!?_licensedir:%doc %{pecl_docdir}/%{pecl_name}}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Mon Feb 13 2017 Remi Collet <remi@fedoraproject.org> - 1.1.7-1
- Update to 1.1.7

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 1.1.6-3
- rebuild with PHP 7.1.0 GA

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 1.1.6-2
- rebuild for PHP 7.1 new API version

* Sun Sep 04 2016 Remi Collet <remi@fedoraproject.org> - 1.1.6-1
- Update to 1.1.6

* Thu Sep 01 2016 Remi Collet <remi@fedoraproject.org> - 1.1.5-1
- Update to 1.1.5

* Mon Aug 08 2016 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4

* Mon Aug 08 2016 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3
- Fix License tag

* Fri Aug 05 2016 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2 (stable)

* Wed Aug 03 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1 (stable)

* Wed Aug 03 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0 (stable)

* Mon Aug 01 2016 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4 (stable)

* Mon Aug 01 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3 (stable)

* Sat Jul 30 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2 (stable)

* Thu Jul 28 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Thu Jul 28 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package, version 1.0.0 (devel)
  open tests/tests/Map/sort.php
  open https://github.com/php-ds/extension/pull/26

