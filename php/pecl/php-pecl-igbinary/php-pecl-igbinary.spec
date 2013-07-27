# spec file for php-pecl-igbinary
#
# Copyright (c) 2010-2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?__pecl: %{expand: %%global __pecl %{_bindir}/pecl}}

%global extname   igbinary
%global commit    c35d48f3d14794373b2ef89a6d79020bb7418d7f
%global short     %(c=%{commit}; echo ${c:0:7})
%global gitver    3b8ab7e
%global prever    -dev

Summary:        Replacement for the standard PHP serializer
Name:           php-pecl-igbinary
Version:        1.1.2
%if 0%{?short:1}
Release:        0.6.git%{short}%{?dist}
Source0:        https://github.com/%{extname}/%{extname}/archive/%{commit}/%{extname}-%{version}-%{short}.tar.gz
%else
Release:        2%{?dist}
Source0:        http://pecl.php.net/get/%{extname}-%{version}.tgz
# http://pecl.php.net/bugs/22598
Source1:        %{extname}-tests.tgz
%endif
# http://pecl.php.net/bugs/22599
License:        BSD
Group:          System Environment/Libraries

URL:            http://pecl.php.net/package/igbinary

# https://github.com/igbinary/igbinary/pull/24
Patch0:         igbinary-apcu.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
BuildRequires:  php-pear
BuildRequires:  php-devel >= 5.2.0
# php-pecl-apcu-devel provides php-pecl-apc-devel
BuildRequires:  php-pecl-apc-devel >= 3.1.7

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

Obsoletes:      php-%{extname} <= 1.1.1
Provides:       php-%{extname} = %{version}
Provides:       php-%{extname}%{?_isa} = %{version}
Provides:       php-pecl(%{extname}) = %{version}
Provides:       php-pecl(%{extname})%{?_isa} = %{version}

# Other third party repo stuff
Obsoletes:     php53-pecl-%{extname}
Obsoletes:     php53u-pecl-%{extname}
Obsoletes:     php54-pecl-%{extname}
%if "%{php_version}" > "5.5"
Obsoletes:     php55-pecl-%{extname}
%endif

# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
Igbinary is a drop in replacement for the standard PHP serializer.

Instead of time and space consuming textual representation, 
igbinary stores PHP data structures in a compact binary form. 
Savings are significant when using memcached or similar memory
based storages for serialized data.


%package devel
Summary:       Igbinary developer files (header)
Group:         Development/Libraries
Requires:      php-pecl-%{extname}%{?_isa} = %{version}-%{release}
Requires:      php-devel%{?_isa}
Obsoletes:     php-%{extname}-devel <= 1.1.1
Provides:      php-%{extname}-devel = %{version}-%{release}
Provides:      php-%{extname}-devel%{?_isa} = %{version}-%{release}

%description devel
These are the files needed to compile programs using Igbinary


%prep
%setup -q -c

%if 0%{?short:1}
mv igbinary-%{commit}/package.xml .
mv igbinary-%{commit} %{extname}-%{version}
sed -e '/release/s/-dev/dev/' -i package.xml

cd %{extname}-%{version}

%patch0 -p1 -b .apcu

%else
cd %{extname}-%{version}
tar xzf %{SOURCE1}
%endif

extver=$(sed -n '/#define IGBINARY_VERSION/{s/.* "//;s/".*$//;p}' igbinary.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
cd ..

cp -r %{extname}-%{version} %{extname}-%{version}-zts

cat >%{extname}.ini <<EOF
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
cd %{extname}-%{version}
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../%{extname}-%{version}-zts
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
# for short circuit
rm -f  %{extname}*/modules/apc.so

make install -C %{extname}-%{version} \
     INSTALL_ROOT=%{buildroot}
     
make install -C %{extname}-%{version}-zts \
     INSTALL_ROOT=%{buildroot}

install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

install -D -m 644 %{extname}.ini %{buildroot}%{php_inidir}/%{extname}.ini
install -D -m 644 %{extname}.ini %{buildroot}%{php_ztsinidir}/%{extname}.ini


%check
cd %{extname}-%{version}

# APC required for test 045
if [ -f %{php_extdir}/apcu.so ]; then
  ln -s %{php_extdir}/apcu.so modules/apc.so
else
  ln -s %{php_extdir}/apc.so  modules/apc.so
fi

: simple NTS module load test, without APC, as optional
%{__php} --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{extname}.so \
    --modules | grep %{extname}

: upstream test suite
TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=apc.so -d extension=%{extname}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php


cd ../%{extname}-%{version}-zts
if [ -f %{php_ztsextdir}/apcu.so ]; then
  ln -s %{php_ztsextdir}/apcu.so modules/apc.so
else
  ln -s %{php_ztsextdir}/apc.so  modules/apc.so
fi
: simple ZTS module load test, without APC, as optional
%{__ztsphp} --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{extname}.so \
    --modules | grep %{extname}

: upstream test suite
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=apc.so -d extension=%{extname}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php


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
%doc %{extname}-%{version}/COPYING
%doc %{extname}-%{version}/CREDITS
%doc %{extname}-%{version}/ChangeLog
%doc %{extname}-%{version}/NEWS
%doc %{extname}-%{version}/README
%config(noreplace) %{php_inidir}/%{extname}.ini
%config(noreplace) %{php_ztsinidir}/%{extname}.ini
%{php_extdir}/%{extname}.so
%{php_ztsextdir}/%{extname}.so
%{pecl_xmldir}/%{name}.xml


%files devel
%defattr(-,root,root,-)
%{php_incldir}/ext/%{extname}
%{php_ztsincldir}/ext/%{extname}


%changelog
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

