# remirepo spec file for php-smbclient
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package       php-smbclient
%else
%global pkg_name   %{name}
%endif

%global gh_commit  18570160a5cb427ed4d55a3a4dc4431d2bea6949
%global gh_short   %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner   eduardok
%global gh_project libsmbclient-php
#global gh_date    20161104
#global prever     RC1

%global pecl_name  smbclient
%global with_zts   0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
%global ini_name   %{pecl_name}.ini
%else
%global ini_name   40-%{pecl_name}.ini
%endif
# Test suite requires a Samba server and configuration file
%global with_tests 0%{?_with_tests:1}

Name:           %{?sub_prefix}php-smbclient
Version:        0.9.0
%if 0%{?gh_date}
Release:        0.2.%{gh_date}git%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%else
Release:        1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%endif

Summary:        PHP wrapper for libsmbclient

Group:          Development/Languages
License:        BSD
URL:            https://github.com/eduardok/libsmbclient-php
%if 0%{?gh_date}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{pecl_name}-%{version}-%{gh_short}.tar.gz
%else
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz
%endif
%if %{with_tests}
Source2:        %{gh_project}-phpunit.xml
%endif

BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  libsmbclient-devel > 3.6
%if %{with_tests}
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  samba
%endif

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}
# Rename
Obsoletes:      %{?sub_prefix}php-libsmbclient               < 0.8.0-0.2
Provides:       %{?sub_prefix}php-libsmbclient               = %{version}-%{release}
Provides:       %{?sub_prefix}php-libsmbclient%{?_isa}       = %{version}-%{release}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}-%{release}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}-%{release}
%endif
# PECL
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-%{pecl_name}      <= %{version}
Obsoletes:     php55u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55w-%{pecl_name}      <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-%{pecl_name}      <= %{version}
Obsoletes:     php56u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56w-%{pecl_name}      <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-%{pecl_name}      <= %{version}
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-%{pecl_name}      <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.1"
Obsoletes:     php71u-%{pecl_name}      <= %{version}
Obsoletes:     php71u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php71w-%{pecl_name}      <= %{version}
Obsoletes:     php71w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
%{pecl_name} is a PHP extension that uses Samba's libsmbclient
library to provide Samba related functions and 'smb' streams
to PHP programs.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
%if 0%{?gh_date}
mv %{gh_project}-%{gh_commit} NTS
mv NTS/package.xml .
%else
mv %{pecl_name}-%{version}%{?prever} NTS
%endif

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS
# Check extension version
ver=$(sed -n '/define PHP_SMBCLIENT_VERSION/{s/.* "//;s/".*$//;p}' php_smbclient.h)
if test "$ver" != "%{version}%{?prever}%{?gh_date:-dev}"; then
   : Error: Upstream VERSION version is ${ver}, expecting %{version}%{?prever}%{?gh_date:-dev}.
   exit 1
fi
cd ..

cat  << 'EOF' | tee %{ini_name}
; Enable %{summary} extension module
extension=%{pecl_name}.so
EOF


%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif


%build
%{?dtsenable}

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
%{?dtsenable}

make -C NTS install INSTALL_ROOT=%{buildroot}

# install configuration
install -Dpm 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for NTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif

%if %{with_tests}
: Upstream test suite for NTS extension
cd NTS
cp %{SOURCE2} phpunit.xml

%{__php} \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    %{_bindir}/phpunit --verbose
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
* Fri Feb 10 2017 Remi Collet <remi@fedoraproject.org> - 0.9.0-1
- update to 0.9.0 (stable)

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 0.9.0-0.2.20161104git1857016
- rebuild with PHP 7.1.0 GA

* Tue Nov  8 2016 Remi Collet <remi@fedoraproject.org> - 0.9.0-0.1.20161104git1857016
- update to 0.9.0-dev for stream performance

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 0.8.0-2
- rebuild for PHP 7.1 new API version

* Wed Mar  2 2016 Remi Collet <remi@fedoraproject.org> - 0.8.0-1
- update to 0.8.0 (stable, no change)

* Tue Dec  8 2015 Remi Collet <remi@fedoraproject.org> - 0.8.0-0.5.RC1
- now available on PECL

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 0.8.0-0.4.rc1
- rebuild for PHP 7.0.0RC5 new API version

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 0.8.0-0.3.rc1
- F23 rebuild with rh_layout

* Wed Sep 16 2015 Remi Collet <rcollet@redhat.com> - 0.8.0-0.2.rc1
- update to 0.8.0-rc1
- rename from php-libsmbclient to php-smbclient
- https://github.com/eduardok/libsmbclient-php/pull/26 rename

* Thu Sep  3 2015 Remi Collet <rcollet@redhat.com> - 0.8.0-0.1.20150909gita65127d
- update to 0.8.0-dev
- https://github.com/eduardok/libsmbclient-php/pull/20 streams support
- https://github.com/eduardok/libsmbclient-php/pull/23 PHP 7

* Thu Sep  3 2015 Remi Collet <rcollet@redhat.com> - 0.7.0-1
- Update to 0.7.0
- drop patches merged upstream
- license is now BSD

* Wed Sep  2 2015 Remi Collet <rcollet@redhat.com> - 0.6.1-1
- Initial packaging of 0.6.1
- open https://github.com/eduardok/libsmbclient-php/pull/17
  test suite configuration
- open https://github.com/eduardok/libsmbclient-php/pull/18
  add reflection and improve phpinfo
- open https://github.com/eduardok/libsmbclient-php/issues/19
  missing license file
