# remirepo spec file for php-pecl-hprose
#
# Copyright (c) 2015-2016 Remi Collet
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
%scl_package       php-pecl-hprose
%endif

%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name  hprose
%global with_tests 0%{!?_without_tests:1}
%if "%{php_version}" < "5.6"
%global ini_name   %{pecl_name}.ini
%else
%global ini_name   40-%{pecl_name}.ini
%endif

Summary:        Hprose for PHP
Name:           %{?sub_prefix}php-pecl-%{pecl_name}
Version:        1.6.5
Release:        2%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:        MIT
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel > 5.3
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
Hprose is a High Performance Remote Object Service Engine.

It is a modern, lightweight, cross-language, cross-platform, object-oriented,
high performance, remote dynamic communication middleware. It is not only
easy to use, but powerful. You just need a little time to learn, then you
can use it to easily construct cross language cross platform distributed
application system.

Hprose supports many programming languages. Through Hprose, You can
conveniently and efficiently intercommunicate between those programming
languages.

This project is the implementation of Hprose for PHP.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_HPROSE_VERSION/{s/.* "//;s/".*$//;p}' php_hprose.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif

# Create configuration file
cat > %{ini_name} << 'EOF'
; Enable '%{pecl_name}' extension module
extension=%{pecl_name}.so
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/php-config \
    --enable-hprose
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/zts-php-config \
    --enable-hprose
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
cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_tests}
: Upstream test suite  for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff
%endif

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_tests}
: Upstream test suite  for ZTS extension
TEST_PHP_EXECUTABLE=%{_bindir}/zts-php \
TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/zts-php -n run-tests.php --show-diff
%endif
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{?_licensedir:%license NTS/LICENSE.md}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 1.6.5-2
- rebuild for PHP 7.1 new API version

* Fri Jun 10 2016 Remi Collet <remi@fedoraproject.org> - 1.6.5-1
- Update to 1.6.5

* Fri Jun 10 2016 Remi Collet <remi@fedoraproject.org> - 1.6.4-3
- add upstream patch for PHP 7.1

* Sat Mar  5 2016 Remi Collet <remi@fedoraproject.org> - 1.6.4-2
- adapt for F24

* Wed Jan 06 2016 Remi Collet <remi@fedoraproject.org> - 1.6.4-1
- Update to 1.6.4 (stable)
  no change, only our patch merged

* Wed Jan 06 2016 Remi Collet <remi@fedoraproject.org> - 1.6.3-1
- Update to 1.6.3 (stable)

* Tue Jan 05 2016 Remi Collet <remi@fedoraproject.org> - 1.6.2-1
- Update to 1.6.2 (stable)
- fix PHP 5 build
  open https://github.com/hprose/hprose-pecl/pull/12

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 1.6.1-3
- rebuild for PHP 7.0.0RC5 new API version

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 1.6.1-2
- F23 rebuild with rh_layout

* Tue Sep 01 2015 Remi Collet <remi@fedoraproject.org> - 1.6.1-1
- Update to 1.6.1 (stable)

* Sun Aug 23 2015 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0

* Wed Jul 22 2015 Remi Collet <remi@fedoraproject.org> - 1.5.5-3
- rebuild against php 7.0.0beta2

* Wed Jul  8 2015 Remi Collet <remi@fedoraproject.org> - 1.5.5-2
- rebuild against php 7.0.0beta1

* Thu Jun 25 2015 Remi Collet <remi@fedoraproject.org> - 1.5.5-1
- Update to 1.5.5 (stable)

* Wed Jun 24 2015 Remi Collet <remi@fedoraproject.org> - 1.5.4-2
- allow build against rh-php56 (as more-php56)

* Sun May 24 2015 Remi Collet <remi@fedoraproject.org> - 1.5.4-1
- Update to 1.5.4

* Wed May 13 2015 Remi Collet <remi@fedoraproject.org> - 1.5.3-1
- Update to 1.5.3

* Mon May 11 2015 Remi Collet <remi@fedoraproject.org> - 1.5.2-1
- Update to 1.5.2

* Mon Apr 20 2015 Remi Collet <remi@fedoraproject.org> - 1.4.2-1
- Update to 1.4.2

* Mon Apr 13 2015 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- Update to 1.4.1

* Thu Apr 09 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- Update to 1.4.0

* Thu Apr 09 2015 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- Update to 1.3.2

* Thu Apr 09 2015 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1

* Wed Apr 08 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0

* Tue Apr 07 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Fri Apr  3 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0

* Thu Apr  2 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- add upstream fix
- open https://github.com/hprose/hprose-pecl/issues/4 - CR/LF

* Thu Apr  2 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package, version 1.0.0 (stable)
- open https://github.com/hprose/hprose-pecl/issues/1 - php 7
- open https://github.com/hprose/hprose-pecl/issues/2 - i386

