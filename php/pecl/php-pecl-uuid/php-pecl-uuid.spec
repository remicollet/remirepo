# spec file for php-pecl-uuid
#
# Copyright (c) 2012-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global pecl_name   uuid
%global with_zts    0%{?__ztsphp:1}

Summary:       Universally Unique Identifier extension for PHP
Name:          php-pecl-uuid
Version:       1.0.3
Release:       7%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:       LGPLv2+
Group:         Development/Languages
URL:           http://pecl.php.net/package/uuid
Source:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
# https://bugs.php.net/63446 - Please Provides LICENSE file
# http://svn.php.net/viewvc/pecl/uuid/trunk/LICENSE?view=co
Source1:       %{pecl_name}-LICENSE

# http://svn.php.net/viewvc?view=revision&revision=328255
# Use preg_match to avoid "Function ereg() is deprecated" in test suite
Patch0:        %{pecl_name}-ereg.patch
# http://svn.php.net/viewvc?view=revision&revision=328259
# Fix build warnings
Patch1:        %{pecl_name}-build.patch
# http://svn.php.net/viewvc?view=revision&revision=328261
# Improves phpinfo() output
Patch2:        %{pecl_name}-info.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php-devel
BuildRequires: php-pear
BuildRequires: libuuid-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}
# both provides same extension, with different API
Conflicts:     uuid-php

Provides:      php-%{pecl_name} = %{version}
Provides:      php-%{pecl_name}%{?_isa} = %{version}
Provides:      php-pecl(%{pecl_name}) = %{version}
Provides:      php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet"
# Other third party repo stuff
%if "%{php_version}" > "5.4"
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
Obsoletes:     php54-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
A wrapper around Universally Unique Identifier library (libuuid).


%prep
%setup -q -c 

mv %{pecl_name}-%{version} NTS
cd NTS
cp %{SOURCE1} LICENSE

%patch0 -p3 -b .ereg
%patch1 -p3 -b .build
%patch2 -p3 -b .info

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_UUID_VERSION/{s/.* "//;s/".*$//;p}' php_uuid.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif

# Drop in the bit of configuration
cat > %{pecl_name}.ini << 'EOF'
; Enable UUID extension module
extension = %{pecl_name}.so
EOF


%build
export PHP_RPATH=no

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
# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

%if %{with_zts}
# Install the ZTS stuff
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Test & Documentation
cd NTS
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in LICENSE $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd NTS

TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php

%if %{with_zts}
cd ../ZTS

TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php
%endif


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc %{pecl_docdir}/%{pecl_name}
%doc %{pecl_testdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%endif


%changelog
* Fri Mar 14 2014 Remi Collet <remi@fedoraproject.org> - 1.0.3-7
- cleanups
- install doc in pecl_docdir
- install tests in pecl_testdir

* Sat Nov 24 2012 Remi Collet <remi@fedoraproject.org> - 1.0.3-3
- add LICENSE from upstream SVN
- also provides php-uuid

* Tue Nov  6 2012 Remi Collet <remi@fedoraproject.org> - 1.0.3-2
- more upstream patches (build warning + phpinfo output)

* Tue Nov  6 2012 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- initial package, version 1.0.3 (stable)
