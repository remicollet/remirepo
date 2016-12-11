# remirepo spec file for php-suhosin (from old fedora spec)
#
# Copyright (c) 2008-2016 Remi Collet
# Copyright (c) 2007-2009 Bart Vanbrabant
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
%endif

#global gh_commit    f0683bf1d9d77e5532e637778107e20826b8d1af
#global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     stefanesser
%global gh_project   suhosin
%{?scl:          %scl_package         php-suhosin}
%{!?php_inidir:  %global php_inidir   %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl       %{_bindir}/pecl}
%{!?__php:       %global __php        %{_bindir}/php}

%global ext_name  suhosin
%global with_zts  0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
%global ini_name  %{ext_name}.ini
%else
%global ini_name  40-%{ext_name}.ini
%endif

Name:           %{?sub_prefix}php-suhosin
Version:        0.9.38
Release:        3%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
Summary:        Suhosin is an advanced protection system for PHP installations

Group:          Development/Languages
License:        PHP
URL:            http://www.hardened-php.net/suhosin/
%if 0%{?gh_commit:1}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz
%else
Source0:        http://download.suhosin.org/suhosin-%{version}.tar.gz
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel > 5.4

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

## Compat SCL (rh-php56)
Provides:       %{?scl_prefix}php-suhosin         = %{version}-%{release}
Provides:       %{?scl_prefix}php-suhosin%{?_isa} = %{version}-%{release}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
Obsoletes:     php53-%{ext_name}  <= %{version}
Obsoletes:     php53u-%{ext_name} <= %{version}
Obsoletes:     php54-%{ext_name}  <= %{version}
Obsoletes:     php54w-%{ext_name} <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-%{ext_name} <= %{version}
Obsoletes:     php55w-%{ext_name} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-%{ext_name} <= %{version}
Obsoletes:     php56w-%{ext_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Suhosin is an advanced protection system for PHP installations. It was designed
to protect servers and users from known and unknown flaws in PHP applications
and the PHP core.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
%if 0%{?gh_commit:1}
mv %{ext_name}-%{gh_commit} NTS
%else
mv %{ext_name}-%{version} NTS
%endif

# Check extension version
ver=$(sed -n '/SUHOSIN_EXT_VERSION/{s/.* "//;s/".*$//;p}' NTS/php_suhosin.h)
if test "$ver" != "%{version}%{?gh_commit:-dev}"; then
   : Error: Upstream SUHOSIN_EXT_VERSION version is ${ver}, expecting %{version}%{?gh_commit:-dev}.
   exit 1
fi

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif


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

make -C NTS install INSTALL_ROOT=%{buildroot}

# install configuration
sed -e 's/\;\(extension=suhosin.so\)/\1/' -i NTS/%{ext_name}.ini
install -Dpm 644 NTS/%{ext_name}.ini %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
sed -e 's/\;\(extension=suhosin.so\)/\1/' -i ZTS/%{ext_name}.ini
install -Dpm 644 ZTS/%{ext_name}.ini %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif


%check
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{ext_name}.so \
    --modules | grep -i suhosin

%if %{with_zts}
: Minimal load test for NTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{ext_name}.so \
    --modules | grep -i suhosin
%endif

: Upstream test suite for NTS extension
cd NTS

# drop known to fail tests
%if "%{php_version}" < "5.5"
rm tests/executor/function_blacklist_printf.phpt
rm tests/executor/function_whitelist_call_user_func.phpt
rm tests/executor/eval_blacklist.phpt
rm tests/executor/eval_blacklist_printf.phpt
rm tests/executor/eval_whitelist_call_user_func.phpt
%endif
rm tests/filter/suhosin_upload_disallow_binary_on.phpt

TEST_PHP_EXECUTABLE=%{__php} \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__php} run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=%{ext_name}.so \


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license NTS/LICENSE
%doc NTS/{Changelog,CREDITS}

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{ext_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{ext_name}.so
%endif


%changelog
* Mon Jun 22 2015 Remi Collet <rcollet@redhat.com> - 0.9.38-3
- add virtual "rh-php56" provides

* Sat Jun 20 2015 Remi Collet <remi@fedoraproject.org> - 0.9.38-2
- allow build against rh-php56 (as more-php56)

* Fri May 22 2015 Remi Collet <remi@fedoraproject.org> - 0.9.38-1
- update to 0.9.38

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 0.9.37.1-1.1
- Fedora 21 SCL mass rebuild

* Mon Dec 15 2014 Remi Collet <remi@fedoraproject.org> - 0.9.37.1-1
- update to 0.9.37.1

* Wed Dec  3 2014 Remi Collet <remi@fedoraproject.org> - 0.9.37-1
- update to 0.9.37

* Mon Nov 24 2014 Remi Collet <remi@fedoraproject.org> - 0.9.37-0.1.0fa87e1
- update to 0.9.37RC1
- fix license handling

* Tue Aug 26 2014 Remi Collet <rcollet@redhat.com> - 0.9.36-2
- improve SCL build

* Wed Jun 11 2014 Remi Collet <remi@fedoraproject.org> - 0.9.36-1
- update to 0.9.36

* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 0.9.35-2
- add numerical prefix to extension configuration file (php 5.6)

* Mon Mar 24 2014 Remi Collet <remi@fedoraproject.org> 0.9.35-1
- update to 0.9.35 for php >= 5.4
- add ZTS build
- add missing LICENSE file
- allow SCL build
- don't ignore test results, just drop a few tests

* Tue Jul 27 2010 Remi Collet <rpms@famillecollet.com> 0.9.32.1-1
- update to 0.9.32.1

* Tue Mar  2 2010 Remi Collet <rpms@famillecollet.com> 0.9.29-3.el5.remi
- rebuild to have remi's EVR > epel's EVR

* Sat Oct 31 2009 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> - 0.9.29-1
Update to version 0.9.29
- Fixing crash bugs with PHP 5.3.0 caused by unexpected NULL in 
  EG(active_symbol_table)
- Added more compatible way to retrieve ext/session globals
- Increased default length and count limit for POST variables 
  (for people not reading docu)
- Fixed crash bug with PHP 5.2.10 caused by a change in extension 
  load order of ext/session
- Fixed harmless parameter order error in a bogus memset()
- Disable suhosin.session.cryptua by default because of 
  Internet Explorer 8 "features"
- Added suhosin.executor.include.allow_writable_files which can be 
  disabled to disallow inclusion of files writable by the webserver

* Thu Sep 18 2008 Remi Collet <rpms@famillecollet.com> 0.9.27-1.fc9.remi.1
- rebuild for php 5.3.0-dev

* Thu Sep 18 2008 Remi Collet <rpms@famillecollet.com> 0.9.27-1.###.remi
- rebuild for php 5.2.6 all FC/EL version

* Tue Aug 26 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.27-1
- Update to version 0.9.27

* Thu Aug 7 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.25-1
- Update to version 0.9.25

* Wed Jun 18 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.24-1
- Update to version 0.9.24

* Tue Apr 29 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.23-1
- Update to version 0.9.23
- Some specfile updates for review

* Fri Jan 4 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.22-2
- Use short name for license

* Wed Dec 5 2007 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.22-1
- Initial packaging of 0.9.22
