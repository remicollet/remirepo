# spec file for php-pecl-gnupg
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

%global pecl_name  gnupg
%global with_zts   0%{?__ztsphp:1}

Summary:      Wrapper around the gpgme library
Name:         php-pecl-gnupg
Version:      1.3.3
Release:      2%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}

License:      BSD
Group:        Development/Languages
URL:          http://pecl.php.net/package/gnupg
Source0:      http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# http://svn.php.net/viewvc?view=revision&revision=330950 Fix version
# http://svn.php.net/viewvc?view=revision&revision=330954 Fix double-free
Patch0:       %{pecl_name}-svn.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel
BuildRequires: gpgme-devel
BuildRequires: php-pear
BuildRequires: gnupg

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}
# We force use of /usr/bin/gpg as gpg2 is unusable in non-interactive mode
Requires:     gnupg

Provides:     php-%{pecl_name} = %{version}
Provides:     php-%{pecl_name}%{?_isa} = %{version}
Provides:     php-pecl(%{pecl_name}) = %{version}
Provides:     php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet"
# Other third party repo stuff
Obsoletes:    php53-pecl-%{pecl_name}
Obsoletes:    php53u-pecl-%{pecl_name}
Obsoletes:    php54-pecl-%{pecl_name}
%if "%{php_version}" > "5.5"
Obsoletes:    php55u-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:    php56u-pecl-%{pecl_name}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This module allows you to interact with gnupg. 

Documentation : http://www.php.net/gnupg


%prep 
%setup -c -q

# Create configuration file
cat >%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

mv %{pecl_name}-%{version} NTS
cd NTS
%patch0 -p3 -b .svn

# Check extension version
extver=$(sed -n '/#define PHP_GNUPG_VERSION/{s/.* "//;s/".*$//;p}' php_gnupg.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

%if %{with_zts}
# Build ZTS extension if ZTS devel available (fedora >= 17)
cp -r NTS ZTS
%endif


%build
export PHP_RPATH=no
export CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -DGNUPG_PATH='\"/usr/bin/gpg\"'"

cd NTS
%{_bindir}/phpize
%configure \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make install -C NTS INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

# Test & Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%clean
rm -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
sed -e 's:GnuPG v1.%d.%d (GNU/Linux):GnuPG v%s:' \
    -i ?TS/tests/gnupg_*_export.phpt

%if 0%{?rhel} == 5
# GnuPG seems to old
rm -f ?TS/tests/gnupg_{oo,res}_listsignatures.phpt
%endif
unset GPG_AGENT_INFO

# ignore test result on EL-6 which only have gnupg2
%if 0%{?rhel} >= 6
status=0
%else
status=1
%endif

cd NTS
: Check if build NTS extension can be loaded
%{__php} -n -q \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Run upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{_bindir}/php \
REPORT_EXIT_STATUS=$status \
NO_INTERACTION=1 \
%{__php} run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=%{pecl_name}.so

%if %{with_zts}
cd ../ZTS
: Check if build ZTS extension can be loaded
%{__php} -n -q \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Run upstream test suite for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
REPORT_EXIT_STATUS=$status \
NO_INTERACTION=1 \
%{__ztsphp} run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=%{pecl_name}.so
%endif


%files
%defattr(-, root, root, -)
%doc %{pecl_docdir}/%{pecl_name}
%doc %{pecl_testdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Mon Mar 17 2014 Remi Collet <remi@fedoraproject.org> - 1.3.3-2
- cleanups
- make ZTS build optional
- install doc in pecl_docdir
- install tests in pecl_testdir

* Wed Jul 17 2013 Remi Collet <remi@fedoraproject.org> - 1.3.3-1
- update to 1.3.3

* Sun Jun 30 2013 Remi Collet <remi@fedoraproject.org> - 1.3.2-4
- ignore test result

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> - 1.3.2-3.1
- also provides php-gnupg + cleanups

* Sun May 06 2012 Remi Collet <remi@fedoraproject.org> - 1.3.2-3
- improve patch

* Sat Jan 28 2012 Remi Collet <remi@fedoraproject.org> - 1.3.2-2
- build against PHP 5.4

* Sat Jan 28 2012 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- Initial RPM
- open upstream bugs
  https://bugs.php.net/60913 - test suite fails
  https://bugs.php.net/60914 - bad version
  https://bugs.php.net/60915 - php 5.4 build fails
  https://bugs.php.net/60916 - force use of /usr/bin/gpg
