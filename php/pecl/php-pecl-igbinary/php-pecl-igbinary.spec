# spec file for php-pecl-igbinary
#
# Copyright (c) 2010-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package        php-pecl-igbinary}
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global extname   igbinary
%global with_zts  0%{?__ztsphp:1}
#global commit    c35d48f3d14794373b2ef89a6d79020bb7418d7f
#global short     %(c=%{commit}; echo ${c:0:7})
#global prever    -dev
%if "%{php_version}" < "5.6"
%global ini_name  %{extname}.ini
%else
%global ini_name  40-%{extname}.ini
%endif

Summary:        Replacement for the standard PHP serializer
Name:           %{?scl_prefix}php-pecl-igbinary
Version:        1.2.1
%if 0%{?short:1}
Release:        0.11.git%{short}%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
Source0:        https://github.com/%{extname}/%{extname}/archive/%{commit}/%{extname}-%{version}-%{short}.tar.gz
%else
Release:        1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
Source0:        http://pecl.php.net/get/%{extname}-%{version}.tgz
%endif
License:        BSD
Group:          System Environment/Libraries

URL:            http://pecl.php.net/package/igbinary

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-devel >= 5.2.0
# php-pecl-apcu-devel provides php-pecl-apc-devel
BuildRequires:  %{?scl_prefix}php-pecl-apc-devel >= 3.1.7

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}

Obsoletes:      %{?scl_prefix}php-%{extname} <= 1.1.1
Provides:       %{?scl_prefix}php-%{extname} = %{version}
Provides:       %{?scl_prefix}php-%{extname}%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl(%{extname}) = %{version}
Provides:       %{?scl_prefix}php-pecl(%{extname})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:     php53-pecl-%{extname}
Obsoletes:     php53u-pecl-%{extname}
Obsoletes:     php54-pecl-%{extname}
Obsoletes:     php54w-pecl-%{extname}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{extname}
Obsoletes:     php55w-pecl-%{extname}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{extname}
Obsoletes:     php56w-pecl-%{extname}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Igbinary is a drop in replacement for the standard PHP serializer.

Instead of time and space consuming textual representation, 
igbinary stores PHP data structures in a compact binary form. 
Savings are significant when using memcached or similar memory
based storages for serialized data.


%package devel
Summary:       Igbinary developer files (header)
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{?scl_prefix}php-devel%{?_isa}

Obsoletes:     %{?scl_prefix}php-%{extname}-devel <= 1.1.1
Provides:      %{?scl_prefix}php-%{extname}-devel = %{version}-%{release}
Provides:      %{?scl_prefix}php-%{extname}-devel%{?_isa} = %{version}-%{release}

%description devel
These are the files needed to compile programs using Igbinary


%prep
%setup -q -c

%if 0%{?short:1}
mv igbinary-%{commit}/package.xml .
mv igbinary-%{commit} NTS
sed -e '/release/s/-dev/dev/' -i package.xml
%else
mv %{extname}-%{version} NTS
%endif

cd NTS

# Check version
extver=$(sed -n '/#define PHP_IGBINARY_VERSION/{s/.* "//;s/".*$//;p}' igbinary.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
cd ..

%if %{with_zts}
cp -r NTS ZTS
%endif

cat <<EOF | tee %{ini_name}
; Enable %{extname} extension module
extension=%{extname}.so

; Enable or disable compacting of duplicate strings
; The default is On.
;igbinary.compact_strings=On

; Use igbinary as session serializer
;session.serialize_handler=igbinary

; Use igbinary as APC serializer
;apc.serializer=igbinary
EOF


%build
cd NTS
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make install -C NTS INSTALL_ROOT=%{buildroot}

install -D -m 644 package2.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install the ZTS stuff
%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Test & Documentation
cd NTS
for i in $(grep 'role="test"' ../package2.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_testdir}/%{extname}/tests/$i
done
for i in $(grep 'role="doc"' ../package2.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{extname}/$i
done


%check
# APC required for test 045
if [ -f %{php_extdir}/apcu.so ]; then
  MOD="-d extension=apcu.so"
elif [ -f %{php_extdir}/apc.so ]; then
  MOD="-d extension=apc.so"
fi

: simple NTS module load test, without APC, as optional
%{_bindir}/php --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{extname}.so \
    --modules | grep %{extname}

: upstream test suite
cd NTS
TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n $MOD -d extension=$PWD/modules/%{extname}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php --show-diff

%if %{with_zts}
: simple ZTS module load test, without APC, as optional
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{extname}.so \
    --modules | grep %{extname}

: upstream test suite
cd ../ZTS
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n $MOD -d extension=$PWD/modules/%{extname}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff
%endif


%clean
rm -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{extname} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{extname}
%config(noreplace) %{php_inidir}/%{ini_name}

%{php_extdir}/%{extname}.so
%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{extname}.so
%endif


%files devel
%defattr(-,root,root,-)
%doc %{pecl_testdir}/%{extname}
%{php_incldir}/ext/%{extname}

%if %{with_zts}
%{php_ztsincldir}/ext/%{extname}
%endif


%changelog
* Fri Aug 29 2014 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1

* Thu Aug 28 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0
- open https://github.com/igbinary/igbinary/pull/36

* Sun Aug 24 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-0.11.git3b8ab7e
- improve SCL stuff

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-0.10.git3b8ab7e
- add numerical prefix to extension configuration file

* Wed Mar 19 2014 Remi Collet <rcollet@redhat.com> - 1.1.2-0.9.git3b8ab7e
- fix SCL dependencies

* Fri Feb 28 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-0.8.git3b8ab7e
- cleanups
- move doc in pecl_docdir
- move tests in pecl_testdir (devel)

* Sat Jul 27 2013 Remi Collet <remi@fedoraproject.org> - 1.1.2-0.6.git3b8ab7e
- latest snapshot
- fix build with APCu

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> - 1.1.2-0.3.git3b8ab7e
- cleanups

* Sat Mar 03 2012 Remi Collet <remi@fedoraproject.org> - 1.1.2-0.2.git3b8ab7e
- macro usage for latest PHP

* Mon Nov 14 2011 Remi Collet <remi@fedoraproject.org> - 1.1.2-0.1.git3b8ab7e
- latest git against php 5.4
- partial patch for https://bugs.php.net/60298
- ignore test result because of above bug

* Sat Sep 17 2011 Remi Collet <rpms@famillecollet.com> 1.1.1-2
- use latest macro
- build zts extension

* Mon Mar 14 2011 Remi Collet <rpms@famillecollet.com> 1.1.1-1
- version 1.1.1 published on pecl.php.net
- rename to php-pecl-igbinary

* Mon Jan 17 2011 Remi Collet <rpms@famillecollet.com> 1.1.1-2
- allow relocation using phpname macro

* Mon Jan 17 2011 Remi Collet <rpms@famillecollet.com> 1.1.1-1
- update to 1.1.1

* Fri Dec 31 2010 Remi Collet <rpms@famillecollet.com> 1.0.2-3
- updated tests from Git.

* Sat Oct 23 2010 Remi Collet <rpms@famillecollet.com> 1.0.2-2
- filter provides to avoid igbinary.so
- add missing %%dist

* Wed Sep 29 2010 Remi Collet <rpms@famillecollet.com> 1.0.2-1
- initital RPM

