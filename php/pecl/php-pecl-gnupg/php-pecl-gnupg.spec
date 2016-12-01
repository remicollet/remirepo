# spec file for php-pecl-gnupg
#
# Copyright (c) 2012-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package       php-pecl-gnupg
%endif
%global with_tests 0%{!?_without_tests:1}

%global pecl_name  gnupg
%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%if "%{php_version}" < "5.6"
%global ini_name   %{pecl_name}.ini
%else
%global ini_name   40-%{pecl_name}.ini
%endif
#global prever     RC2

Summary:      Wrapper around the gpgme library
Name:         %{?sub_prefix}php-pecl-gnupg
Version:      1.4.0
Release:      3%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}

License:      BSD
Group:        Development/Languages
URL:          http://pecl.php.net/package/gnupg
Source0:      http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{?scl_prefix}php-devel
BuildRequires: %{?scl_prefix}php-pear
BuildRequires: gpgme-devel
BuildRequires: gnupg < 2

Requires:     %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:     %{?scl_prefix}php(api) = %{php_core_api}
# We force use of /usr/bin/gpg as gpg2 is unusable in non-interactive mode
Requires:     gnupg < 2
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:     %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:     %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:     %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:     %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
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
This module allows you to interact with gnupg. 

Documentation : http://www.php.net/gnupg

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep 
%setup -c -q

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

# Create configuration file
cat >%{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

mv %{pecl_name}-%{version}%{?prever} NTS
cd NTS

# Check extension version
extver=$(sed -n '/#define PHP_GNUPG_VERSION/{s/.* "//;s/".*$//;p}' php_gnupg.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
cd ..

%if %{with_zts}
# Build ZTS extension if ZTS devel available (fedora >= 17)
cp -r NTS ZTS
%endif


%build
export PHP_RPATH=no
export CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64"
export GPG1=$(which gpg1 2>/dev/null || which gpg)
$GPG1 --version

peclbuild() {
%{_bindir}/${1}ize
%configure \
    --with-gpg=$GPG1 \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/${1}-config

make %{?_smp_mflags}
}

cd NTS
peclbuild php

%if %{with_zts}
cd ../ZTS
peclbuild zts-php
%endif


%install
rm -rf %{buildroot}

make install -C NTS INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%clean
rm -rf %{buildroot}


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
%if 0%{?fedora} >= 23
sed -e '/GnuPG v1/d' \
%else
sed -e 's:GnuPG v1.%d.%d (GNU/Linux):GnuPG v%s:' \
%endif
    -i ?TS/tests/gnupg_*_export.phpt

%if 0%{?rhel} == 5
# GnuPG seems to old
rm -f ?TS/tests/gnupg_{oo,res}_listsignatures.phpt
%endif
unset GPG_AGENT_INFO

cd NTS
: Check if build NTS extension can be loaded
%{__php} -n -q \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_tests}
: Run upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{_bindir}/php \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__php} -n run-tests.php \
    -n -q \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --show-diff
%endif

%if %{with_zts}
cd ../ZTS
: Check if build ZTS extension can be loaded
%{__ztsphp} -n -q \
    -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_tests}
: Run upstream test suite for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__ztsphp} -n run-tests.php \
    -n -q \
    -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --show-diff
%endif
%endif


%files
%defattr(-, root, root, -)
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
* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 1.4.0-3
- rebuild with PHP 7.1.0 GA

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 1.4.0-2
- rebuild for PHP 7.1 new API version

* Thu Sep  1 2016 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- update to 1.4.0 (stable)

* Mon Jul 25 2016 Remi Collet <remi@fedoraproject.org> - 1.4.0-0.3.RC2
- update to 1.4.0RC2 (beta)

* Fri Jun 17 2016 Remi Collet <remi@fedoraproject.org> - 1.4.0-0.2.RC1
- always use gnupg < 2

* Thu Jun 16 2016 Remi Collet <remi@fedoraproject.org> - 1.4.0-0.1.RC1
- update to 1.4.0RC1 (beta)

* Tue Mar  8 2016 Remi Collet <remi@fedoraproject.org> - 1.3.6-2
- adapt for F24

* Thu Feb 12 2015 Remi Collet <remi@fedoraproject.org> - 1.3.6-1
- Update to 1.3.6
- don't install test suite
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.3.3-5.1
- Fedora 21 SCL mass rebuild

* Tue Aug 26 2014 Remi Collet <rcollet@redhat.com> - 1.3.3-5
- improve SCL build

* Wed Apr 16 2014 Remi Collet <remi@fedoraproject.org> - 1.3.3-4
- add numerical prefix to extension configuration file

* Wed Mar 26 2014 Remi Collet <remi@fedoraproject.org> - 1.3.3-3
- allow SCL build

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
